"""Feed Fetcher - RSS/Atom feed parsing and HTML scraping."""
import logging
import httpx
import feedparser
from typing import Dict, List, Optional, Any
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

HTTP_TIMEOUT = 30
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


class FeedFetcher:
    def __init__(self):
        self.client = httpx.Client(
            timeout=HTTP_TIMEOUT,
            headers={"User-Agent": USER_AGENT},
            follow_redirects=True,
        )

    def fetch_rss(self, feed_url: str) -> Optional[List[Dict[str, Any]]]:
        """Fetch and parse an RSS/Atom feed."""
        try:
            logger.debug("Fetching RSS: %s", feed_url)
            response = self.client.get(feed_url)
            response.raise_for_status()

            feed = feedparser.parse(response.text)

            if feed.bozo != 0:
                logger.warning("Feed parsing warning for %s: %s", feed_url, feed.bozo_exception)

            entries = []
            for entry in feed.entries:
                article = {
                    "title": getattr(entry, "title", ""),
                    "url": getattr(entry, "link", ""),
                    "published": getattr(entry, "published", ""),
                    "summary": getattr(entry, "summary", ""),
                    "content": self._extract_content(entry),
                    "author": getattr(entry, "author", ""),
                }
                if article["title"] and article["url"]:
                    entries.append(article)

            logger.info("Fetched %d articles from RSS: %s", len(entries), feed_url)
            return entries[:20]

        except Exception as e:
            logger.error("Failed to fetch RSS %s: %s", feed_url, e)
            return None

    def fetch_html(self, list_url: str, selectors: Dict[str, str]) -> Optional[List[Dict[str, Any]]]:
        """Fetch and parse HTML page using selectors."""
        try:
            logger.debug("Fetching HTML: %s", list_url)
            response = self.client.get(list_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")
            entries = []

            article_links = soup.select(selectors.get("article_list", "a"))
            for link in article_links[:20]:
                title_elem = link.select_one(selectors.get("title", "h2, .title"))
                summary_elem = link.select_one(selectors.get("summary", "p, .summary"))

                article = {
                    "title": title_elem.get_text(strip=True) if title_elem else link.get_text(strip=True),
                    "url": link.get("href", ""),
                    "summary": summary_elem.get_text(strip=True) if summary_elem else "",
                }

                if not article["url"].startswith("http"):
                    from urllib.parse import urljoin
                    article["url"] = urljoin(list_url, article["url"])

                if article["title"] and article["url"]:
                    entries.append(article)

            logger.info("Fetched %d articles from HTML: %s", len(entries), list_url)
            return entries

        except Exception as e:
            logger.error("Failed to fetch HTML %s: %s", list_url, e)
            return None

    def fetch_article_content(self, url: str) -> Optional[str]:
        """Fetch full article content from URL."""
        try:
            response = self.client.get(url, timeout=60)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")

            for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
                tag.decompose()

            content_selectors = [
                "article",
                ".article-content",
                ".post-content",
                ".entry-content",
                ".content-body",
                "div[class*='content']",
                "main",
                "#content",
            ]

            content_elem = None
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    break

            if content_elem:
                text = content_elem.get_text(separator="\n", strip=True)
                if len(text) > 100:
                    return text

            paragraphs = soup.find_all("p")
            if paragraphs:
                text = "\n\n".join(p.get_text(strip=True) for p in paragraphs)
                if len(text) > 100:
                    return text

            return None

        except Exception as e:
            logger.warning("Failed to fetch article content %s: %s", url, e)
            return None

    def _extract_content(self, entry) -> str:
        """Extract content from feed entry."""
        if hasattr(entry, "content") and entry.content:
            for content in entry.content:
                if content.get("type", "") in ("text/plain", "text/html"):
                    text = content.value
                    if "<" in text:
                        soup = BeautifulSoup(text, "lxml")
                        return soup.get_text(strip=True)
                    return text.strip()
        return ""

    def close(self):
        """Close HTTP client."""
        self.client.close()


feed_fetcher = FeedFetcher()