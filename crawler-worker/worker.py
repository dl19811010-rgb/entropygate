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
same article on every 30-minute cycle. It is a *local speed* cache only.

When several crawl jobs run in parallel (multi-worker), that file is no longer
authoritative — each runner starts from its own snapshot. True dedup is handled
by the Studio backend: we pre-filter candidates via ``POST /api/v1/crawler/check-urls``
(see dedup.py) and the backend's idempotent-by-URL ingest guarantees at most one
article per source URL even if two workers race to POST the same link.
"""
import os
import sys
import json
import time
import logging
from datetime import datetime, timezone

import httpx
from feed_fetcher import feed_fetcher
from dedup import filter_new, check_existing_urls

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("crawler-worker")

HERE = os.path.dirname(os.path.abspath(__file__))
STUDIO_BASE = os.environ.get("STUDIO_BASE_URL", "").rstrip("/")
ADMIN_PASS = os.environ.get("STUDIO_ADMIN_PASSWORD", "")
SEEN_FILE = os.path.join(HERE, "seen_urls.json")
PER_SOURCE_CAP = int(os.environ.get("PER_SOURCE_CAP", "12"))
GLOBAL_CAP = int(os.environ.get("GLOBAL_CAP", "50"))
# Optional multi-worker sharding: when several crawl jobs run in parallel they
# can split the source list via SOURCES_FILTER (comma-separated names). Empty
# (default) means "process every source" — backward compatible with the single
# runner. Dedup across workers is handled by the backend (see dedup.py).
WORKER_ID = os.environ.get("WORKER_ID", "default")
SOURCES_FILTER = [s.strip() for s in os.environ.get("SOURCES_FILTER", "").split(",") if s.strip()]
CHECK_URLS = os.environ.get("CHECK_URLS", "1") != "0"  # disable backend pre-filter if needed


def login() -> str:
    # Retry with backoff: the Studio can return transient 503 while it is
    # mid-rebuild (we trigger deploys independently of the crawl schedule),
    # and a single 5xx must not fail an entire crawl run.
    last_err = None
    for attempt in range(6):
        try:
            r = httpx.post(
                f"{STUDIO_BASE}/api/v1/admin/auth/login",
                json={"username": "admin", "password": ADMIN_PASS},
                timeout=30,
            )
            if r.status_code >= 500:
                last_err = f"HTTP {r.status_code}"
                log.warning("login got %s (attempt %d/6), retrying...",
                            r.status_code, attempt + 1)
                time.sleep(10 * (attempt + 1))
                continue
            r.raise_for_status()
            tok = r.json().get("data", {}).get("token")
            if not tok:
                raise RuntimeError(f"login failed: {r.text[:200]}")
            return tok
        except (httpx.HTTPError, httpx.TimeoutException) as ex:
            last_err = str(ex)
            log.warning("login error (attempt %d/6): %s", attempt + 1, ex)
            time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"login failed after retries: {last_err}")


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


def report_run(tok: str, report: dict) -> None:
    """Tell the Studio about this run so its observation endpoints reflect
    real collection health (see POST /api/v1/crawler/report).

    Non-fatal: a failure here must never break an otherwise-successful crawl.
    """
    try:
        r = httpx.post(
            f"{STUDIO_BASE}/api/v1/crawler/report",
            json=report,
            headers={"X-Access-Token": tok, "Content-Type": "application/json"},
            timeout=30,
        )
        if r.status_code == 200:
            log.info("crawler report accepted: %s", (r.json().get("data") or {}))
        else:
            log.warning("crawler report rejected HTTP %s: %s", r.status_code, r.text[:160])
    except Exception as ex:
        log.warning("crawler report failed (non-fatal): %s", ex)


def image_query_for(p: dict, tok: str) -> tuple:
    """Ask the Studio (which holds the LLM key) for an English cover-image
    search query + relevance keywords for this article. Returns (query, keywords).

    Fully automated — the crawler worker has no LLM key of its own, so it
    delegates cover-image relevance generation to the Studio's GLM endpoint.
    On any failure we fall back to the bare article title (no keywords), so the
    crawler still runs a plain title search instead of crashing the crawl loop.
    """
    title = (p.get("title") or "").strip()
    if not title:
        return "artificial intelligence technology", None
    body = {
        "title": title,
        "summary": (p.get("summary") or "")[:500],
        "content": (p.get("content") or "")[:3000],
    }
    try:
        r = httpx.post(
            f"{STUDIO_BASE}/api/v1/articles/generate-image-query",
            json=body,
            headers={"X-Access-Token": tok, "Content-Type": "application/json"},
            timeout=30,
        )
        if r.status_code == 200:
            data = (r.json() or {}).get("data") or {}
            q = (data.get("query") or "").strip()
            kws = [str(k) for k in (data.get("keywords") or []) if k]
            if q:
                return q, (kws or None)
    except Exception as ex:
        log.warning("generate-image-query failed for %r: %s", title[:60], ex)
    # Graceful fallback: bare title, no relevance keywords.
    return title, None


def main() -> None:
    if not STUDIO_BASE or not ADMIN_PASS:
        log.error("STUDIO_BASE_URL / STUDIO_ADMIN_PASSWORD not set")
        sys.exit(1)

    tok = login()
    log.info("Studio login OK (worker_id=%s sources_filter=%s)",
             WORKER_ID, SOURCES_FILTER or "ALL")
    t0 = time.time()

    with open(os.path.join(HERE, "sources.json"), encoding="utf-8") as f:
        sources = json.load(f)

    # Multi-worker sharding: if SOURCES_FILTER is set, only process the named
    # sources. Empty filter => every source (single-runner default).
    if SOURCES_FILTER:
        sources = [s for s in sources if s.get("name") in SOURCES_FILTER]
        if not sources:
            log.error("SOURCES_FILTER=%s matched no sources; aborting", SOURCES_FILTER)
            sys.exit(1)
        log.info("sharding: %d source(s) selected by SOURCES_FILTER", len(sources))

    seen = load_seen()
    planned = []          # articles to POST this run
    stats = {}            # source_name -> counters

    # ── Pass 1: fetch feeds + full text, decide what's new ────────────
    for src in sources:
        name = src.get("name", "?")
        stats[name] = {"fetched": 0, "posted": 0, "skipped": 0, "err": ""}
        ptype = src.get("parser_type", "rss")
        use_pw = ptype in ("playwright", "playwright_html")
        try:
            if ptype == "rss":
                entries = feed_fetcher.fetch_rss(src["feed_url"]) or []
            elif ptype == "rsshub":
                entries = feed_fetcher.fetch_rsshub(src["rsshub_route"]) or []
            elif ptype == "html":
                entries = feed_fetcher.fetch_html(src["list_url"], src.get("selectors", {})) or []
            elif ptype == "playwright":
                entries = feed_fetcher.fetch_rss_playwright(src["feed_url"]) or []
            elif ptype == "playwright_html":
                entries = feed_fetcher.fetch_playwright_links(src["list_url"]) or []
            else:
                entries = []
            # Fallback: a Cloudflare-blocked Playwright RSS feed yields nothing;
            # retry via the source's listing page if one is configured.
            if not entries and src.get("list_url"):
                log.info("[%s] feed empty, falling back to listing page", name)
                entries = feed_fetcher.fetch_playwright_links(src["list_url"]) or []
        except Exception as e:
            log.warning("[%s] fetch error: %s", name, e)
            stats[name]["err"] = f"fetch_error: {e}"
            continue

        stats[name]["fetched"] = len(entries)
        for e in entries[:PER_SOURCE_CAP]:
            url = e.get("url")
            if not url:
                continue
            if url in seen:
                stats[name]["skipped"] += 1
                continue
            content = e.get("content") or ""
            # RSSHub feeds already carry the full body; the origin is
            # Cloudflare-hard-blocked, so never re-fetch it.
            if e.get("from_rsshub"):
                pass
            # Full-text capture when the feed only carried a summary.
            elif len(content) < 300 and e.get("url"):
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
            planned.append({
                "name": name,
                "url": url,
                "title": (e.get("title") or "").strip(),
                "content": content,
                "summary": (e.get("summary") or "")[:500],
                "source_name": name,
                "language": src.get("language", "en"),
                "image_url": e.get("image_url") or "",
                "original_images": e.get("original_images") or [],
                "published_at": iso(e.get("published_at")),
            })
            if len(planned) >= GLOBAL_CAP:
                break
        if len(planned) >= GLOBAL_CAP:
            break
        # be a good citizen between sources
        time.sleep(1)

    # ── Distributed dedup (cross-worker) ──────────────────────────────
    # Local ``seen`` already prevents re-fetching within this run. But when
    # multiple crawl jobs run in parallel, another worker may have just POSTed
    # a URL this worker hasn't recorded yet. Ask the backend which candidate
    # URLs already exist and drop them BEFORE we spend bandwidth on full-text
    # re-fetch / cover-image search. On any failure check_existing_urls returns
    # an empty set, so we simply proceed (the backend still dedups on ingest).
    if CHECK_URLS and planned:
        candidate_urls = [p["url"] for p in planned if p.get("url")]
        existing = check_existing_urls(STUDIO_BASE, tok, candidate_urls)
        if existing:
            before = len(planned)
            planned, dropped = filter_new(planned, existing)
            dedup_dropped = before - len(planned)
            log.info("dedup: backend reports %d existing URL(s); dropped %d (kept %d)",
                     len(existing), dedup_dropped, len(planned))
        else:
            dedup_dropped = 0
    else:
        dedup_dropped = 0

    # ── Pass 2: resolve cover images ──────────────────────────────────
    # Phase 2 (auto image search): for articles that STILL have no cover after
    # Pass 1, try an automatic image search (Wikimedia by default, keyless) and
    # use the best hit as the "original" so image_host mirrors it into R2 like
    # any other picture. Articles that remain empty keep the branded frontend
    # fallback. If R2 creds / R2_PUBLIC_BASE are not set, upload_images degrades
    # to keeping the searched URL as-is.
    from image_host import upload_images

    auto_search = False
    prov = "?"
    try:
        from image_search import search_images, enabled as search_enabled, provider_name
        auto_search = search_enabled()
        prov = provider_name()
    except Exception as ex:
        log.warning("image_search import failed (disabled): %s", ex)

    need = {}
    searched = 0
    for p in planned:
        if p.get("image_url"):
            need[p["url"]] = p["image_url"]
        elif auto_search:
            title = (p.get("title") or "").strip()
            if title:
                try:
                    q, kws = image_query_for(p, tok)
                    hits = search_images(q, keywords=kws) if kws else search_images(q)
                    if hits:
                        need[p["url"]] = hits[0]["url"]
                        searched += 1
                        log.info("img-search [%s] %r (q=%r) -> %s (%s, %s)",
                                 p["source_name"], title[:60], q[:50], hits[0]["url"],
                                 hits[0].get("source"), hits[0].get("license"))
                    else:
                        log.info("img-search [%s] %r (q=%r) no relevant hit -> branded fallback",
                                 p["source_name"], title[:60], q[:50])
                except Exception as ex:
                    log.warning("img-search failed for %s: %s", p["url"], ex)
                time.sleep(0.5)  # be a polite consumer of the search API

    if auto_search:
        log.info("img-search: %d article(s) got a searched cover (provider=%s)",
                 searched, prov)

    if need:
        try:
            hosted = upload_images(need)
            for p in planned:
                p["image_url"] = hosted.get(p["url"]) or p["image_url"]
            r2 = sum(1 for v in hosted.values()
                     if v and (".r2.dev" in v or ".r2.cloudflarestorage.com" in v))
            log.info("images: %d on R2 / %d total resolved", r2, len(hosted))
            for v in hosted.values():
                if v and (".r2.dev" in v or ".r2.cloudflarestorage.com" in v):
                    log.info("R2_SAMPLE_URL %s", v)   # verification aid (force run)
                    break
        except Exception as ex:
            log.warning("image step failed (keeping original urls): %s", ex)

    # ── Pass 3: POST to Studio ───────────────────────────────────────
    total_posted = 0
    for p in planned:
        payload = {
            "title": p["title"],
            "url": p["url"],
            "content": p["content"],
            "summary": p["summary"],
            "source_name": p["source_name"],
            "language": p["language"],
            "image_url": p["image_url"],
            "original_images": p["original_images"],
            "published_at": p["published_at"],
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        ok, err = post_article(tok, payload)
        rec = stats[p["name"]]
        if ok:
            total_posted += 1
            seen.add(p["url"])
            rec["posted"] += 1
        else:
            rec["err"] = (rec["err"] + f"; post_fail: {err}").strip("; ")
            log.warning("[%s] post failed: %s", p["name"], err)

    save_seen(seen)
    try:
        feed_fetcher.close()
    except Exception:
        pass

    # ── Aggregate run stats for the Studio observation endpoints ──
    fetched = sum(s["fetched"] for s in stats.values())
    skipped_local = sum(s["skipped"] for s in stats.values())
    post_errors = sum(1 for s in stats.values() if "post_fail" in s["err"])
    error_notes = "; ".join(
        f"{n}:{s['err']}" for n, s in stats.items() if s["err"]
    )[:1000]
    report_run(tok, {
        "worker_id": WORKER_ID,
        "status": "completed",
        "sources_total": len(sources),
        "discovered": fetched,
        "planned": len(planned),
        "new": total_posted,
        "duplicate": skipped_local + dedup_dropped,
        "errors": post_errors,
        "duration_seconds": round(time.time() - t0, 1),
        "notes": error_notes or None,
    })

    log.info("==== RESULT SUMMARY ====")
    for name, s in stats.items():
        log.info("RESULT source=%s fetched=%s posted=%s skipped=%s err=%s",
                 name, s["fetched"], s["posted"], s["skipped"], s["err"] or "-")
    log.info("RESULT total_posted=%d planned=%d seen=%d dedup_dropped=%d",
             total_posted, len(planned), len(seen), dedup_dropped)
    # Stay green; failures are captured in the logs above.
    sys.exit(0)


if __name__ == "__main__":
    main()
