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


def search_images(query: str, max_results: int = 4) -> list:
    """Return a list of ``{url, title, license, source}`` dicts. Empty on failure.

    The first entry is the best match and is what the caller should use.
    """
    q = (query or "").strip()
    if not q:
        return []
    try:
        name = provider_name()
        if name == "unsplash":
            return _search_unsplash(q, max_results)
        if name == "pexels":
            return _search_pexels(q, max_results)
        return _search_wikimedia(q, max_results)
    except Exception as e:  # never break the crawl over a cover image
        log.warning("image search (%s) failed for %r: %s", provider_name(), q, e)
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
            out.append(
                {
                    "url": url,
                    "title": r.get("description") or r.get("alt_description") or "",
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
