#!/usr/bin/env python3
"""One-off / dispatched cover-image backfill for existing articles.

Reuses the Phase-2 auto image-search machinery (LLM query + keyword-ranked
search + R2 mirror) to give a cover image to EVERY existing article that still
lacks one, AND to REPLACE covers that were assigned by the old keyless
Wikimedia provider (which could not rank by relevance and often produced
off-topic images).

Idempotent + incremental:
  * The article id is the key, so re-running never double-counts.
  * ``image_map.json`` records the provider used for each cover. Articles whose
    cover is already from ``unsplash`` (the relevant provider) are skipped, so
    weekly self-healing runs only touch new / cover-less articles.

Provider policy:
  * Uses the SAME provider as the live crawl (Unsplash by default, env-selected).
  * ``allow_wikimedia_fallback=False`` is passed so that if Unsplash is empty or
    rate-limited we leave the article cover-less (branded frontend fallback)
    rather than assigning an off-topic Wikimedia image.

Run via the `cover_backfill.yml` workflow (manual dispatch or weekly Sunday
schedule). Paced by ``IMG_SEARCH_PACE`` seconds between searches to stay under
the Unsplash 50 req/hour free-tier cap.
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
# Seconds to wait between Unsplash searches (stay under 50 req/hour).
PACE = int(os.environ.get("IMG_SEARCH_PACE", "75"))
IMAGE_MAP_PATH = os.path.join(HERE, "image_map.json")

log = logging.getLogger("cover_backfill")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def load_image_map() -> dict:
    try:
        with open(IMAGE_MAP_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_image_map(mp: dict) -> None:
    try:
        with open(IMAGE_MAP_PATH, "w", encoding="utf-8") as f:
            json.dump(mp, f, ensure_ascii=False, indent=2)
    except Exception as e:  # noqa: BLE001
        log.warning("could not persist image_map.json: %s", e)


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


def fetch_all(tok: str):
    """Return every article (admin list, paginated)."""
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
        items = d.get("items", [])
        out.extend(items)
        tot = d.get("total", 0)
        if len(out) >= tot or not items:
            break
        page += 1
    return out


def _already_unsplash(mp: dict, aid) -> bool:
    entry = mp.get(str(aid))
    if isinstance(entry, dict):
        return entry.get("provider") == "unsplash"
    return False


def main() -> None:
    if not STUDIO_BASE or not ADMIN_PASS:
        log.error("STUDIO_BASE_URL / STUDIO_ADMIN_PASSWORD not set")
        sys.exit(1)

    tok = login()
    log.info("Studio login OK")

    from image_search import search_images, enabled as search_enabled, provider_name

    auto_search = search_enabled()
    prov = provider_name()
    log.info("image search enabled=%s provider=%s pace=%ss", auto_search, prov, PACE)

    if not auto_search:
        log.error("image search disabled; nothing to backfill")
        sys.exit(1)

    mp = load_image_map()
    articles = fetch_all(tok)
    log.info("cover_backfill: %d article(s) total in Studio", len(articles))

    need = {}
    skipped_unsplash = 0
    for a in articles:
        aid = a["id"]
        title = (a.get("title") or "").strip()
        if not title:
            continue
        # Already has a relevant (Unsplash) cover -> skip for incremental runs.
        if (a.get("image_url") or "").strip() and _already_unsplash(mp, aid):
            skipped_unsplash += 1
            continue
        q, kws = image_query_for(title, a.get("summary"), a.get("content"), tok)
        try:
            # Do NOT fall back to off-topic Wikimedia when Unsplash is empty/limited.
            hits = search_images(q, keywords=kws, allow_wikimedia_fallback=False) if kws \
                else search_images(q, allow_wikimedia_fallback=False)
        except Exception as ex:  # noqa: BLE001
            log.warning("img-search failed [id=%s]: %s", aid, ex)
            hits = []
        if hits:
            need[str(aid)] = hits[0]["url"]
            log.info(
                "img-search [id=%s] %r (q=%r) -> %s (%s)",
                aid, title[:50], q[:50], hits[0]["url"], hits[0].get("source"),
            )
        else:
            log.info("img-search [id=%s] %r (q=%r) no relevant hit -> keep current", aid, title[:50], q[:50])
        time.sleep(PACE)  # pace Unsplash to respect 50 req/hour

    log.info("cover_backfill: %d to upload, %d already-unsplash skipped", len(need), skipped_unsplash)

    if need:
        from image_host import upload_images
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
                mp[str(aid)] = {"url": url, "provider": "unsplash"}
                log.info("updated [id=%s] -> %s", aid, url)
            else:
                log.warning("update failed [id=%s]: %s", aid, r.text[:160])
        log.info("cover_backfill: updated %d / %d, R2=%d", updated, len(hosted), r2)
    else:
        log.info("cover_backfill: nothing to upload")

    save_image_map(mp)
    # Stay green; all failure modes are already logged above.
    sys.exit(0)


if __name__ == "__main__":
    main()
