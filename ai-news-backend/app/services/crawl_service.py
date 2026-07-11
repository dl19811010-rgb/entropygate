"""Crawl Service — fetch articles from sources and compute editorial scores."""
import logging
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any

from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.source import Source
from app.services.editorial_service import editorial_service
from app.services.ai_service import ai_service
from app.crawler.feed_fetcher import feed_fetcher

logger = logging.getLogger(__name__)


class CrawlService:
    def __init__(self, db: Session):
        self.db = db

    def crawl_source(self, source_id: int, fetch_full_content: bool = False) -> int:
        """Crawl a single source. Returns number of new articles fetched."""
        source = self.db.query(Source).filter(Source.id == source_id).first()
        if not source:
            logger.warning("Source %s not found", source_id)
            return 0

        if source.status != "active" or source.is_active == 0:
            logger.debug("Source %s is not active, skipping", source.name)
            return 0

        if source.crawl_error_count and source.crawl_error_count >= 3:
            logger.warning("Source %s has too many errors, skipping", source.name)
            return 0

        source.last_crawled_at = datetime.utcnow()
        self.db.commit()

        logger.info("Crawling source: %s (%s)", source.name, source.feed_url)

        config = self._get_source_config(source)
        articles = self._fetch_from_source(source, config)

        if articles is None:
            source.crawl_error_count = (source.crawl_error_count or 0) + 1
            source.health = "error"
            self.db.commit()
            return 0

        new_count = 0
        for article_data in articles[:source.max_articles_per_fetch]:
            try:
                if fetch_full_content and not article_data.get("content"):
                    article_data["content"] = feed_fetcher.fetch_article_content(article_data["url"])

                article = self.ingest_article(source_id, **article_data)
                if article:
                    new_count += 1
            except Exception as e:
                logger.error("Failed to ingest article from %s: %s", source.name, e)

        source.last_success_at = datetime.utcnow()
        source.health = "healthy"
        source.crawl_error_count = 0
        self.db.commit()

        logger.info("Crawl completed for %s: %d new articles", source.name, new_count)
        return new_count

    def crawl_all_active(self, tier_filter: Optional[str] = None) -> dict:
        """Crawl all active sources. Returns summary dict."""
        query = self.db.query(Source).filter(Source.is_active == 1, Source.status == "active")

        if tier_filter:
            query = query.filter(Source.editorial_tier == tier_filter)

        sources = query.all()
        results = {"total_sources": len(sources), "new_articles": 0, "sources_crawled": 0, "errors": 0}

        for src in sources:
            try:
                if not self._should_crawl(src):
                    logger.debug("Source %s not ready for crawl yet", src.name)
                    continue

                count = self.crawl_source(src.id)
                results["new_articles"] += count
                results["sources_crawled"] += 1
            except Exception as e:
                logger.error("Crawl error for source %s: %s", src.name, e)
                results["errors"] += 1
                src.crawl_error_count = (src.crawl_error_count or 0) + 1
                src.health = "error"
                self.db.commit()

        return results

    def crawl_by_tier(self, tier: str) -> dict:
        """Crawl sources by editorial tier."""
        return self.crawl_all_active(tier_filter=tier)

    def ingest_article(self, source_id: int, title: str, url: str, **kwargs) -> Optional[Article]:
        """Ingest a single article and compute its editorial score."""
        existing = self.db.query(Article).filter(Article.url == url).first()
        if existing:
            logger.debug("Duplicate article: %s", url)
            return None

        source = self.db.query(Source).filter(Source.id == source_id).first()
        if not source:
            logger.warning("Source %s not found for article ingestion", source_id)
            return None

        article = Article(
            title=title,
            url=url,
            source_id=source_id,
            source_name=source.name,
            source_url=source.url,
            **{k: v for k, v in kwargs.items() if hasattr(Article, k)},
        )

        if article.content:
            article.ai_summary = ai_service.generate_summary(article.content)
            article.ai_keywords = ",".join(ai_service.extract_keywords(article.content))
            article.ai_entities = ",".join(ai_service.extract_entities(article.content))

        article.newsworthiness_score = ai_service.generate_newsworthiness(
            title=title, content=article.content or "", source_name=article.source_name
        )

        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)

        self._compute_editorial_score(article)

        logger.debug("Ingested new article: %s", title)
        return article

    def _should_crawl(self, source: Source) -> bool:
        """Check if source should be crawled based on interval."""
        if not source.last_crawled_at:
            return True
        interval = timedelta(minutes=source.crawl_interval_minutes or 30)
        return datetime.utcnow() - source.last_crawled_at >= interval

    def _get_source_config(self, source: Source) -> Dict[str, Any]:
        """Get source configuration."""
        if source.feed_url:
            return {"type": "rss", "url": source.feed_url}

        try:
            if hasattr(source, "config") and source.config:
                if isinstance(source.config, str):
                    return json.loads(source.config)
                return source.config
        except Exception:
            pass

        return {"type": "rss", "url": source.feed_url or source.url}

    def _fetch_from_source(self, source: Source, config: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """Fetch articles based on source type."""
        source_type = config.get("type", "rss")

        if source_type == "rss":
            feed_url = config.get("rss_url") or config.get("url") or source.feed_url
            if feed_url:
                return feed_fetcher.fetch_rss(feed_url)

        elif source_type == "static_html":
            list_url = config.get("list_url") or config.get("url") or source.url
            selectors = config.get("selectors", {})
            if list_url:
                return feed_fetcher.fetch_html(list_url, selectors)

        logger.error("No valid feed URL or list URL for source %s", source.name)
        return None

    def _compute_editorial_score(self, article: Article) -> None:
        """Compute and persist editorial score for an article."""
        try:
            result = editorial_service.compute_editorial_score(article)
            article.editorial_score = result["score"]
            article.editorial_bucket = result["bucket"]
            article.editorial_tier = result.get("tier", "c_tier")
            self.db.commit()
        except Exception as e:
            logger.warning("Editorial score computation failed for article %s: %s", article.id, e)