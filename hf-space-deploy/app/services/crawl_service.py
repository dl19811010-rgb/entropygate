"""Crawl Service — fetch articles from sources and compute editorial scores."""
import logging
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.source import Source
from app.services.editorial_service import editorial_service
from app.services.ai_service import ai_service

logger = logging.getLogger(__name__)


class CrawlService:
    """Orchestrates fetching articles from sources and enriching them."""

    def __init__(self, db: Session):
        self.db = db

    def crawl_source(self, source_id: int) -> int:
        """Crawl a single source. Returns number of new articles fetched."""
        source = self.db.query(Source).filter(Source.id == source_id).first()
        if not source:
            logger.warning("Source %s not found", source_id)
            return 0

        # Mark as crawled
        source.last_crawled_at = datetime.utcnow()
        self.db.commit()

        # Stub: in production, this would use feedparser / httpx to fetch RSS/Atom
        # For now, just log
        logger.info("Crawling source: %s (%s)", source.name, source.feed_url)
        return 0

    def crawl_all_active(self) -> dict:
        """Crawl all active sources. Returns summary dict."""
        sources = self.db.query(Source).filter(Source.is_active == 1, Source.status == "active").all()
        results = {"total_sources": len(sources), "new_articles": 0, "sources_crawled": 0, "errors": 0}
        for src in sources:
            try:
                count = self.crawl_source(src.id)
                results["new_articles"] += count
                results["sources_crawled"] += 1
                src.last_success_at = datetime.utcnow()
                src.health = "healthy"
                self.db.commit()
            except Exception as e:
                logger.error("Crawl error for source %s: %s", src.name, e)
                results["errors"] += 1
                src.crawl_error_count = (src.crawl_error_count or 0) + 1
                src.health = "error"
                self.db.commit()
        return results

    def ingest_article(self, source_id: int, title: str, url: str, **kwargs) -> Optional[Article]:
        """Ingest a single article and compute its editorial score."""
        # Dedup by URL
        existing = self.db.query(Article).filter(Article.url == url).first()
        if existing:
            logger.debug("Duplicate article: %s", url)
            return None

        source = self.db.query(Source).filter(Source.id == source_id).first()
        article = Article(
            title=title,
            url=url,
            source_id=source_id,
            source_name=source.name if source else "",
            source_url=source.url if source else "",
            **{k: v for k, v in kwargs.items() if hasattr(Article, k)},
        )

        # AI enrichment (stub)
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

        # Compute editorial score
        self._compute_editorial_score(article)

        return article

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
