#!/usr/bin/env python3
"""One-off / dispatched cover-image backfill for existing articles.

Reuses the Phase-2 auto image-search machinery (LLM query + keyword-ranked
search + R2 mirror) to give a cover image to EVERY existing article that still
lacks one. This closes the gap for pre-P3 backlog articles (mostly English RSS
sources that embed no image of their own).

Idempotent: only articles with an empty image_url are processed, and each is
keyed by its Studio id, so re-running never double-counts or clobbers covers.

Run via the `cover_backfill.yml` workflow (manual dispatch). Uses the
keyless Wikimedia provider by default to avoid Unsplash's 50 req/hour cap when
backfilling dozens of articles at once.
"""
import os
import sys
import time
import json
import logging
import httpx

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

STUDIO_BASE = os.environ.get("STUDIO_BASE_URL", "").rstrip("/")
ADMIN_PASS = os.environ.get("STUDIO_ADMIN_PASSWORD", "")

log = logging.getLogger("cover_backfill")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def login() -> str:
    last = None
    for attempt in range(6):
        try:
            r = httpx.post(
                f"{STUDIO_BASE}/api/v1/admin/auth/login",
                json={"username": "admin", "password": ADMIN_PASS},
                timeout=30,
            )
            if r.status_code == 200:
                tok = (r.json() or {}).get("data", {}).get("token")
                if tok:
                    return tok
            last = f"HTTP {r.status_code}: {r.text[:120]}"
        except Exception as e:  # noqa: BLE001
            last = str(e)
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"login failed: {last}")


def image_query_for(title: str, summary: str, content: str, tok: str):
    """Ask the Studio (which holds the LLM key) for an English cover-image
    search query + relevance keywords. Falls back to the bare title."""
    if not title:
        return "artificial intelligence technology", None
    body = {
        "title": title,
        "summary": (summary or "")[:500],
        "content": (content or "")[:3000],
    }
    try:
        r = httpx.post(
            f"{STUDIO_BASE}/api/v1/articles/generate-image-query",
            json=body,
            headers={"X-Access-Token": tok, "Content-Type": "application/json"},
            timeout=30,
        )
        if r.status_code == 200:
            d = (r.json() or {}).get("data") or {}
            q = (d.get("query") or "").strip()
            kws = [str(k) for k in (d.get("keywords") or []) if k]
            if q:
                return q, (kws or None)
    except Exception as ex:  # noqa: BLE001
        log.warning("generate-image-query failed for %r: %s", title[:60], ex)
    return title, None


def fetch_no_cover(tok: str):
    """Return all articles whose image_url is empty (admin list, paginated)."""
    out = []
    page = 1
    h = {"X-Access-Token": tok}
    while True:
        r = httpx.get(
            f"{STUDIO_BASE}/api/v1/articles",
            params={"page": page, "page_size": 100},
            headers=h,
            timeout=60,
        )
        d = r.json().get("data", {})
        for a in d.get("items", []):
            if not (a.get("image_url") or "").strip():
                out.append(a)
        tot = d.get("total", 0)
        if len(out) >= tot or not d.get("items"):
            break
        page += 1
    return out


def main() -> None:
    if not STUDIO_BASE or not ADMIN_PASS:
        log.error("STUDIO_BASE_URL / STUDIO_ADMIN_PASSWORD not set")
        sys.exit(1)

    tok = login()
    log.info("Studio login OK")

    from image_search import search_images, enabled as search_enabled, provider_name
    from image_host import upload_images

    auto_search = search_enabled()
    prov = provider_name()
    log.info("image search enabled=%s provider=%s", auto_search, prov)

    articles = fetch_no_cover(tok)
    log.info("cover_backfill: %d article(s) currently have no cover", len(articles))

    need = {}
    for a in articles:
        aid = a["id"]
        title = (a.get("title") or "").strip()
        if not title:
            continue
        # Skip transient shells (no structured flash_meta yet): they will get a
        # cover on the next regular crawl once their flash_meta is generated.
        fm = a.get("flash_meta") or ""
        if "info_card" not in fm:
            log.info("skip [id=%s] %r (no flash_meta yet -> wait for crawl)", aid, title[:50])
            continue
        q, kws = image_query_for(title, a.get("summary"), a.get("content"), tok)
        time.sleep(0.4)
        if not auto_search:
            log.warning("image search disabled; cannot backfill [id=%s]", aid)
            continue
        try:
            hits = search_images(q, keywords=kws) if kws else search_images(q)
        except Exception as ex:  # noqa: BLE001
            log.warning("img-search failed [id=%s]: %s", aid, ex)
            hits = []
        if hits:
            need[str(aid)] = hits[0]["url"]
            log.info(
                "img-search [id=%s] %r (q=%r) -> %s (%s, %s)",
                aid, title[:50], q[:50], hits[0]["url"],
                hits[0].get("source"), hits[0].get("license"),
            )
        else:
            log.info(
                "img-search [id=%s] %r (q=%r) no relevant hit -> branded fallback",
                aid, title[:50], q[:50],
            )
        time.sleep(0.5)  # polite consumer of the search API

    if need:
        hosted = upload_images(need)  # {str(aid): final_url}
        updated = 0
        r2 = 0
        for aid_s, url in hosted.items():
            if not url:
                continue
            aid = int(aid_s)
            r = httpx.put(
                f"{STUDIO_BASE}/api/v1/articles/{aid}",
                json={"image_url": url},
                headers={"X-Access-Token": tok, "Content-Type": "application/json"},
                timeout=30,
            )
            if r.status_code == 200 and (r.json().get("code") in (None, 200, "200")):
                updated += 1
                if ".r2.dev" in url or ".r2.cloudflarestorage.com" in url:
                    r2 += 1
                log.info("updated [id=%s] -> %s", aid, url)
            else:
                log.warning("update failed [id=%s]: %s", aid, r.text[:160])
        log.info("cover_backfill: updated %d / %d, R2=%d", updated, len(hosted), r2)
    else:
        log.info("cover_backfill: nothing to do")

    # Stay green; all failure modes are already logged above.
    sys.exit(0)


if __name__ == "__main__":
    main()
