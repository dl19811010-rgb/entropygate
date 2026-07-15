#!/usr/bin/env python3
"""EntropyGate crawler-worker.

Runs on GitHub Actions (US/EU runner). Fetches AI news from overseas sources
that are blocked / IP-banned from the China-hosted Studio, then pushes the
already-fetched full-text articles to the Studio ingestion API.

Why this exists
---------------
The Studio is hosted on a China server. Overseas targets fall into two buckets:
  * GFW-blocked (Google / DeepMind / blog.google)  -> TCP never completes.
  * IP-banned cloud ranges (HuggingFace, OpenAI/Anthropic blog, The Batch)
    -> the Studio's egress IP is on their abuse lists.
A GitHub Actions runner egresses from outside the GFW on a residential/cloud
IP most targets accept, so we fetch there and ship the text to Studio.

Studio contract
---------------
POST /api/v1/articles stores the provided `content` verbatim (it does NOT
re-fetch the URL), then runs editorial scoring + LLM rewrite. So we only need
to deliver clean title / url / content / summary / source_name / language.

Dedup
-----
seen_urls.json is committed back to the repo each run so we don't re-post the
same article on every 30-minute cycle.
"""
import os
import sys
import json
import time
import logging
from datetime import datetime, timezone

import httpx
from feed_fetcher import feed_fetcher

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("crawler-worker")

HERE = os.path.dirname(os.path.abspath(__file__))
STUDIO_BASE = os.environ.get("STUDIO_BASE_URL", "").rstrip("/")
ADMIN_PASS = os.environ.get("STUDIO_ADMIN_PASSWORD", "")
SEEN_FILE = os.path.join(HERE, "seen_urls.json")
PER_SOURCE_CAP = int(os.environ.get("PER_SOURCE_CAP", "12"))
GLOBAL_CAP = int(os.environ.get("GLOBAL_CAP", "50"))


def login() -> str:
    r = httpx.post(
        f"{STUDIO_BASE}/api/v1/admin/auth/login",
        json={"username": "admin", "password": ADMIN_PASS},
        timeout=30,
    )
    r.raise_for_status()
    tok = r.json().get("data", {}).get("token")
    if not tok:
        raise RuntimeError(f"login failed: {r.text[:200]}")
    return tok


def load_seen() -> set:
    try:
        with open(SEEN_FILE, encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_seen(seen: set) -> None:
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(seen), f, ensure_ascii=False)


def iso(dt):
    if not dt:
        return None
    if isinstance(dt, datetime):
        return dt.astimezone(timezone.utc).isoformat()
    return str(dt)


def post_article(tok: str, payload: dict):
    r = httpx.post(
        f"{STUDIO_BASE}/api/v1/articles",
        json=payload,
        headers={"X-Access-Token": tok, "Content-Type": "application/json"},
        timeout=30,
    )
    if r.status_code != 200:
        return False, f"HTTP {r.status_code}: {r.text[:160]}"
    body = r.json()
    if body.get("code") not in (None, 200, "200"):
        return False, f"code={body.get('code')}: {body.get('message')}"
    return True, None


def main() -> None:
    if not STUDIO_BASE or not ADMIN_PASS:
        log.error("STUDIO_BASE_URL / STUDIO_ADMIN_PASSWORD not set")
        sys.exit(1)

    tok = login()
    log.info("Studio login OK")

    with open(os.path.join(HERE, "sources.json"), encoding="utf-8") as f:
        sources = json.load(f)

    seen = load_seen()
    total_posted = 0
    rows = []

    for src in sources:
        name = src.get("name", "?")
        ptype = src.get("parser_type", "rss")
        use_pw = ptype in ("playwright", "playwright_html")
        try:
            if ptype == "rss":
                entries = feed_fetcher.fetch_rss(src["feed_url"]) or []
            elif ptype == "html":
                entries = feed_fetcher.fetch_html(src["list_url"], src.get("selectors", {})) or []
            elif ptype == "playwright":
                entries = feed_fetcher.fetch_rss_playwright(src["feed_url"]) or []
            elif ptype == "playwright_html":
                entries = feed_fetcher.fetch_playwright_links(src["list_url"]) or []
            else:
                entries = []
        except Exception as e:
            log.warning("[%s] fetch error: %s", name, e)
            rows.append((name, 0, 0, 0, f"fetch_error: {e}"))
            continue

        posted = skipped = 0
        errs = []
        for e in entries[:PER_SOURCE_CAP]:
            url = e.get("url")
            if not url:
                continue
            if url in seen:
                skipped += 1
                continue
            content = e.get("content") or ""
            # Full-text capture when the feed only carried a summary.
            if len(content) < 300 and e.get("url"):
                try:
                    if use_pw:
                        full = feed_fetcher.fetch_article_full_playwright(e["url"])
                    else:
                        full = feed_fetcher.fetch_article_full(e["url"])
                    if full.get("content"):
                        content = full["content"]
                        imgs = full.get("images", [])
                        e["original_images"] = imgs
                        if not e.get("image_url") and imgs:
                            e["image_url"] = imgs[0]["url"]
                except Exception as ex:
                    log.warning("[%s] full fetch failed %s: %s", name, url, ex)
            payload = {
                "title": (e.get("title") or "").strip(),
                "url": url,
                "content": content,
                "summary": (e.get("summary") or "")[:500],
                "source_name": name,
                "language": src.get("language", "en"),
                "image_url": e.get("image_url") or "",
                "original_images": e.get("original_images") or [],
                "published_at": iso(e.get("published_at")),
            }
            payload = {k: v for k, v in payload.items() if v is not None}
            ok, err = post_article(tok, payload)
            if ok:
                posted += 1
                total_posted += 1
                seen.add(url)
                if total_posted >= GLOBAL_CAP:
                    break
            else:
                errs.append(f"{url}: {err}")
                log.warning("[%s] post failed: %s", name, err)
        rows.append((name, len(entries), posted, skipped, "; ".join(errs[:3])))
        if total_posted >= GLOBAL_CAP:
            break

        # be a good citizen between sources
        time.sleep(1)

    save_seen(seen)
    try:
        feed_fetcher.close()
    except Exception:
        pass
    log.info("==== RESULT SUMMARY ====")
    for name, fetched, posted, skipped, err in rows:
        log.info("RESULT source=%s fetched=%s posted=%s skipped=%s err=%s",
                 name, fetched, posted, skipped, err or "-")
    log.info("RESULT total_posted=%d seen=%d", total_posted, len(seen))
    # Stay green; failures are captured in the logs above.
    sys.exit(0)


if __name__ == "__main__":
    main()
