"""Feed Fetcher - RSS/Atom feed parsing and HTML scraping."""
import logging
import datetime
import httpx
import feedparser
from email.utils import parsedate_to_datetime
from typing import Dict, List, Optional, Any
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

HTTP_TIMEOUT = 30
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


class FeedFetcher:
    def __init__(self):
        self.client = httpx.Client(
            timeout=HTTP_TIMEOUT,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": (
                    "text/html,application/xhtml+xml,application/xml;q=0.9,"
                    "image/avif,image/webp,image/apng,*/*;q=0.8"
                ),
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            },
            follow_redirects=True,
        )
        # Cache of proxy-aware clients keyed by proxy URL. China sources fetch
        # directly (no proxy); overseas sources reuse a per-proxy client.
        self._proxy_clients: Dict[str, httpx.Client] = {}

    def _client(self, proxy: Optional[str] = None) -> httpx.Client:
        """Return the client to use for a fetch. With no proxy, the shared
        direct client; otherwise a cached proxy-aware client."""
        if not proxy:
            return self.client
        cached = self._proxy_clients.get(proxy)
        if cached is None:
            cached = httpx.Client(
                timeout=HTTP_TIMEOUT,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": (
                        "text/html,application/xhtml+xml,application/xml;q=0.9,"
                        "image/avif,image/webp,image/apng,*/*;q=0.8"
                    ),
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                },
                follow_redirects=True,
                proxy=proxy,
                # Proxied egress: the Ghelper node and some overseas targets
                # present certs the runtime CA store doesn't trust. We only
                # fetch public content, so disable verification for the proxy
                # hop (and target) to avoid spurious SSL failures.
                verify=False,
            )
            self._proxy_clients[proxy] = cached
        return cached

    def fetch_rss(self, feed_url: str, proxy: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """Fetch and parse an RSS/Atom feed."""
        try:
            logger.debug("Fetching RSS: %s (proxy=%s)", feed_url, proxy)
            response = self._client(proxy).get(feed_url)
            response.raise_for_status()

            feed = feedparser.parse(response.text)

            if feed.bozo != 0:
                logger.warning("Feed parsing warning for %s: %s", feed_url, feed.bozo_exception)

            entries = []
            for entry in feed.entries:
                summary = getattr(entry, "summary", "")
                content = self._extract_content(entry)
                # Fallback: if the feed has no summary but has inline content,
                # derive a short summary so the homepage card is never empty.
                if not summary and content:
                    summary = content[:280]

                article = {
                    "title": getattr(entry, "title", ""),
                    "url": getattr(entry, "link", ""),
                    "published_at": self._parse_date(entry),
                    "summary": summary,
                    "content": content,
                    "image_url": self._extract_image(entry),
                    "author": getattr(entry, "author", ""),
                }
                if article["title"] and article["url"]:
                    entries.append(article)

            logger.info("Fetched %d articles from RSS: %s", len(entries), feed_url)
            return entries[:20]

        except Exception as e:
            logger.error("Failed to fetch RSS %s: %s", feed_url, e)
            return None

    def fetch_html(self, list_url: str, selectors: Dict[str, str], proxy: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """Fetch and parse HTML page using selectors."""
        try:
            logger.debug("Fetching HTML: %s (proxy=%s)", list_url, proxy)
            response = self._client(proxy).get(list_url)
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

    def fetch_article_full(self, url: str, timeout: int = 35, proxy: Optional[str] = None) -> Dict[str, Any]:
        """Fetch the full article body + embedded images from the article URL.

        Returns a dict ``{"content": str|None, "images": [{"url", "alt"}, ...]}``.
        The full body is what downstream AI rewriting consumes, so a news item
        keeps its original facts/meaning instead of being distilled from a short
        RSS summary. Images are collected for archival/editorial reference only —
        they are NOT meant to be republished (copyright); callers must not surface
        them on the public site.
        """
        result: Dict[str, Any] = {"content": None, "images": []}
        try:
            from urllib.parse import urljoin

            response = self._client(proxy).get(url, timeout=timeout)
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

            # ── Body text ───────────────────────────────────────────────
            if content_elem:
                text = content_elem.get_text(separator="\n", strip=True)
                if len(text) > 100:
                    result["content"] = text

            if not result["content"]:
                paragraphs = soup.find_all("p")
                if paragraphs:
                    text = "\n\n".join(p.get_text(strip=True) for p in paragraphs)
                    if len(text) > 100:
                        result["content"] = text

            # ── Image collection (archival only) ────────────────────────
            img_root = content_elem or soup
            seen = set()
            images = []
            for img in img_root.find_all("img"):
                src = (
                    img.get("src")
                    or img.get("data-src")
                    or img.get("data-lazy-src")
                    or img.get("data-original")
                )
                if not src or src.startswith("data:"):
                    continue
                if src.startswith("//"):
                    src = "https:" + src
                abs_src = urljoin(url, src)
                # Skip tiny icons / tracking pixels / spacers.
                w = img.get("width")
                h = img.get("height")
                try:
                    if (w and int(w) <= 1) or (h and int(h) <= 1):
                        continue
                except (TypeError, ValueError):
                    pass
                low = abs_src.lower()
                if any(t in low for t in ("pixel", "tracking", "beacon", "1x1", "spacer.gif")):
                    continue
                if abs_src in seen:
                    continue
                seen.add(abs_src)
                alt = (img.get("alt") or "").strip()
                images.append({"url": abs_src, "alt": alt})
                if len(images) >= 12:
                    break
            # Fallback: og:image as the lead image if nothing in-body.
            if not images:
                og = soup.find("meta", attrs={"property": "og:image"})
                if og and og.get("content"):
                    images.append({"url": urljoin(url, og["content"]), "alt": ""})
            result["images"] = images

            return result

        except Exception as e:
            logger.warning("Failed to fetch full article %s: %s", url, e)
            return result

    def _parse_date(self, entry) -> Optional[datetime.datetime]:
        """Parse the article publish date from a feed entry into a UTC datetime.

        Tries the structured ``*_parsed`` fields first (most reliable), then
        falls back to parsing the raw RFC-2822 date strings. Returns None when
        no usable date is present — this lets the ingest layer decide whether
        to fall back to fetched_at.
        """
        for key in ("published_parsed", "updated_parsed", "created_parsed"):
            val = getattr(entry, key, None)
            if val:
                try:
                    return datetime.datetime(*val[:6], tzinfo=datetime.timezone.utc)
                except (TypeError, ValueError):
                    pass

        for key in ("published", "updated", "created"):
            raw = getattr(entry, key, "")
            if raw:
                try:
                    dt = parsedate_to_datetime(raw)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=datetime.timezone.utc)
                    return dt.astimezone(datetime.timezone.utc)
                except (TypeError, ValueError):
                    pass
        return None

    def _extract_image(self, entry) -> str:
        """Best-effort image extraction from a feed entry."""
        media_thumb = getattr(entry, "media_thumbnail", None)
        if isinstance(media_thumb, list) and media_thumb and media_thumb[0].get("url"):
            return media_thumb[0]["url"]

        media_content = getattr(entry, "media_content", None)
        if isinstance(media_content, list):
            for item in media_content:
                if item.get("medium") == "image" and item.get("url"):
                    return item["url"]

        enclosures = getattr(entry, "enclosures", None)
        if isinstance(enclosures, list):
            for enc in enclosures:
                if (enc.get("type") or "").startswith("image") and enc.get("url"):
                    return enc["url"]

        # Fallback: og:image inside the entry's inline HTML content.
        content = self._extract_content(entry)
        if content and "<" in content:
            soup = BeautifulSoup(content, "lxml")
            og = soup.find("meta", attrs={"property": "og:image"})
            if og and og.get("content"):
                return og["content"]
        return ""

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