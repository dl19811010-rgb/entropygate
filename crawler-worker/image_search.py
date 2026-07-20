#!/usr/bin/env python3
"""Phase-2 automatic cover-image search for articles that have no image.

Pluggable providers (env-selected, see crawl.yml):
  * wikimedia  (DEFAULT, KEYLESS)  -> Wikimedia Commons API (Creative-Commons media)
  * unsplash   (needs UNSPLASH_ACCESS_KEY) -> high-quality editorial/stock photos
  * pexels     (needs PEXELS_API_KEY)      -> high-quality stock photos

The crawler runs on a US/EU GitHub runner where these hosts are reachable.
The returned URL is handed to ``image_host.upload_images()`` which mirrors it
into R2 for China reachability, so callers just get a stable image URL back.

Graceful degradation: if the provider errors, is rate-limited, or returns
nothing, callers keep the empty ``image_url`` (the frontend renders a branded
fallback). Nothing here ever raises into the main crawl loop.
"""
import os
import logging

import httpx

log = logging.getLogger("image-search")

PROVIDER = os.environ.get("IMAGE_SEARCH_PROVIDER", "wikimedia").strip().lower()
UNSPLASH_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "").strip()
PEXELS_KEY = os.environ.get("PEXELS_API_KEY", "").strip()
# Master switch. Default ON. Set AUTO_IMAGE_SEARCH=0/ false / no / off to disable.
AUTO_IMAGE_SEARCH = os.environ.get("AUTO_IMAGE_SEARCH", "1").strip().lower() not in (
    "0", "false", "no", "off"
)
SEARCH_TIMEOUT = int(os.environ.get("IMG_SEARCH_TIMEOUT", "20"))

# Wikimedia asks for a descriptive UA on API calls; we comply.
_API_UA = "EntropyGate-Crawler/1.0 (https://entropygate.cc; automated news cover search)"


def enabled() -> bool:
    """Whether auto image search should run at all."""
    return AUTO_IMAGE_SEARCH


def provider_name() -> str:
    if PROVIDER == "unsplash" and UNSPLASH_KEY:
        return "unsplash"
    if PROVIDER == "pexels" and PEXELS_KEY:
        return "pexels"
    return "wikimedia"


def _dispatch(name: str, query: str, max_results: int) -> list:
    """Call the concrete provider search. ``name`` is one of the known providers."""
    if name == "unsplash":
        return _search_unsplash(query, max_results)
    if name == "pexels":
        return _search_pexels(query, max_results)
    return _search_wikimedia(query, max_results)


def search_images(query: str, max_results: int = 4, keywords: list | None = None) -> list:
    """Return a list of ``{url, title, tags, license, source}`` dicts. Empty on failure.

    The first entry is the best match. When ``keywords`` (English relevance terms)
    are supplied, candidates are ranked by keyword overlap with their title+tags and
    only the best match above ``RANK_THRESHOLD`` is kept — fully automated relevance
    filtering, no manual curation.

    Resilience: if the configured (keyed) provider errors or returns nothing —
    e.g. Unsplash/Pexels rate-limit after their hourly quota — we transparently
    fall back to the keyless Wikimedia Commons source so an article is never
    left without a cover purely because a paid API hiccupped.
    """
    q = (query or "").strip()
    if not q:
        return []
    name = provider_name()
    try:
        hits = _dispatch(name, q, max_results)
    except Exception as e:  # never break the crawl over a cover image
        log.warning("image search (%s) failed for %r: %s", name, q, e)
        hits = []

    if not hits and name != "wikimedia":
        log.info("image search (%s) returned nothing; falling back to wikimedia", name)
        try:
            hits = _search_wikimedia(q, max_results)
        except Exception as e:
            log.warning("wikimedia fallback also failed for %r: %s", q, e)
            hits = []

    if keywords:
        hits = rank_and_filter(hits, keywords)
    return hits


# Relevance ranking threshold: a candidate must match at least this many English
# keywords (from its Unsplash description/tags) to be used. Below it, the article
# keeps the branded frontend fallback instead of an off-topic image.
RANK_THRESHOLD = 1


def rank_and_filter(hits: list, keywords: list | None, threshold: int = RANK_THRESHOLD) -> list:
    """Score each candidate by English keyword overlap with its title+tags.

    Returns ``[best]`` when the best score >= threshold, else ``[]`` (caller keeps
    the branded fallback). This is the automated relevance guard — no vision model
    needed, just metadata matching against LLM-derived keywords.
    """
    if not hits or not keywords:
        return hits
    kws = [str(k).strip().lower() for k in keywords if k]
    if not kws:
        return hits
    best, best_score = None, -1
    for h in hits:
        text = " ".join(
            [str(h.get("title") or "")] + [str(t) for t in (h.get("tags") or [])]
        ).lower()
        score = sum(1 for k in kws if k and k in text)
        if score > best_score:
            best_score, best = score, h
    if best is not None and best_score >= threshold:
        return [best]
    return []


# ── HTTP helper ─────────────────────────────────────────────────────────────
def _get(url: str, params: dict, headers: dict) -> dict:
    with httpx.Client(
        timeout=SEARCH_TIMEOUT,
        follow_redirects=True,
        headers=headers,
    ) as c:
        r = c.get(url, params=params)
    r.raise_for_status()
    return r.json()


# ── Wikimedia Commons (keyless) ──────────────────────────────────────────────
def _search_wikimedia(query: str, max_results: int) -> list:
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": "6",  # File: namespace
        "gsrlimit": str(max(8, max_results)),
        "prop": "imageinfo",
        "iiprop": "url|mime|size|extmetadata",
        "iiurlwidth": "1280",
        "formatversion": "2",
    }
    data = _get(
        "https://commons.wikimedia.org/w/api.php",
        params,
        headers={"User-Agent": _API_UA, "Accept": "application/json"},
    )
    pages = (data.get("query") or {}).get("pages") or []
    out = []
    for pg in pages:
        ii = (pg.get("imageinfo") or [{}])[0]
        mime = ii.get("mime", "")
        if not mime.startswith("image/") or mime == "image/svg+xml":
            continue
        url = ii.get("thumburl") or ii.get("url")
        if not url:
            continue
        w = ii.get("width") or 0
        h = ii.get("height") or 0
        if w and h and (w < 240 or h < 240):  # skip tiny icons / thumbnails
            continue
        em = ii.get("extmetadata") or {}
        lic = (em.get("LicenseShortName") or {}).get("value", "")
        out.append(
            {
                "url": url,
                "title": pg.get("title", ""),
                "license": lic,
                "source": "wikimedia",
            }
        )
        if len(out) >= max_results:
            break
    return out


# ── Unsplash (optional, needs key) ───────────────────────────────────────────
def _search_unsplash(query: str, max_results: int) -> list:
    params = {
        "query": query,
        "per_page": str(max_results),
        "orientation": "landscape",
        "content_filter": "high",
    }
    data = _get(
        "https://api.unsplash.com/search/photos",
        params,
        headers={
            "Authorization": f"Client-ID {UNSPLASH_KEY}",
            "Accept": "application/json",
            "User-Agent": _API_UA,
        },
    )
    out = []
    for r in data.get("results", []):
        url = (r.get("urls") or {}).get("regular")
        if url:
            tags = []
            for t in (r.get("tags") or []):
                if isinstance(t, dict):
                    tt = t.get("title")
                    if tt:
                        tags.append(str(tt))
            out.append(
                {
                    "url": url,
                    "title": r.get("description") or r.get("alt_description") or "",
                    "tags": tags,
                    "license": "Unsplash License",
                    "source": "unsplash",
                }
            )
    return out


# ── Pexels (optional, needs key) ─────────────────────────────────────────────
def _search_pexels(query: str, max_results: int) -> list:
    params = {"query": query, "per_page": str(max_results)}
    data = _get(
        "https://api.pexels.com/v1/search",
        params,
        headers={
            "Authorization": PEXELS_KEY,
            "Accept": "application/json",
            "User-Agent": _API_UA,
        },
    )
    out = []
    for p in data.get("photos", []):
        url = (p.get("src") or {}).get("large")
        if url:
            out.append(
                {
                    "url": url,
                    "title": p.get("alt") or "",
                    "tags": [],
                    "license": "Pexels License",
                    "source": "pexels",
                }
            )
    return out


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import sys

    q = sys.argv[1] if len(sys.argv) > 1 else "artificial intelligence"
    print("provider:", provider_name(), "enabled:", enabled())
    for hit in search_images(q, 3):
        print(hit)
