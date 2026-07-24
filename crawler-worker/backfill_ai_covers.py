#!/usr/bin/env python3
"""Backfill AI-generated covers (Z-Image-Turbo) for articles with NO original image.

Target set per article:
  ① first_content_image(stored body HTML) — zero network
  ② og:image / twitter:image of the original page
  both empty  =>  current cover is necessarily a stock photo or the brand
  placeholder. Those get an AI-generated topical illustration instead
  (user decision 2026-07-24: AI 生成 > 风景素材图).

Idempotent: article URLs already AI-covered are recorded in
ai_covers_done.json (committed back to the repo by the workflow) and
skipped on re-run — no duplicate quota burn.

Cache-busting: same lesson as backfill_hero v2 — upload_images() reuses
cached image_map.json entries WITHOUT re-upload, so keys we replace are
dropped first. Deterministic R2 key (sha1 of article URL) overwrites the
bytes in place (URL unchanged); DB is only PUT when the final URL differs.

Run cap: IMAGE_GEN_MAX_PER_RUN (workflow sets ~25; module default 8).
Trigger: Actions -> "Backfill AI covers (Z-Image-Turbo)" -> Run workflow.
"""
import sys
import os
import json
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("backfill-ai-covers")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from image_host import upload_images, r2_enabled, load_map, save_map  # noqa: E402
from feed_fetcher import feed_fetcher, first_content_image  # noqa: E402
from image_gen import generate_cover, enabled as gen_enabled, remaining as gen_remaining  # noqa: E402

import httpx  # noqa: E402

BASE = os.getenv("STUDIO_BASE_URL", "https://entropygate.cc.cd").rstrip("/") + "/api/v1"
ADMIN_U = "admin"
ADMIN_P = os.getenv("STUDIO_ADMIN_PASSWORD", "admin123")
DONE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai_covers_done.json")

UA = {"User-Agent": "Mozilla/5.0 (compatible; EntropyGate/1.0)"}


def api(method, path, token=None, body=None, retry=6):
    url = path if path.startswith("http") else BASE + path
    headers = {"Accept": "application/json", "Content-Type": "application/json", **UA}
    if token:
        headers["X-Access-Token"] = token
    for attempt in range(retry + 1):
        try:
            r = httpx.request(method, url, headers=headers, json=body, timeout=30)
            if r.status_code == 429 and attempt < retry:
                w = int(r.headers.get("retry-after", 2 ** attempt))
                log.warning("rate-limited (429), sleep %ds", w)
                time.sleep(w)
                continue
            try:
                js = r.json()
            except Exception:
                js = {}
            return r.status_code, js
        except Exception as ex:
            if attempt < retry:
                time.sleep(2 ** attempt)
                continue
            return 0, {"error": str(ex)}


def login():
    st, js = api("POST", "/admin/auth/login", body={"username": ADMIN_U, "password": ADMIN_P})
    if st != 200 or not js.get("data", {}).get("token"):
        raise SystemExit(f"login failed: {st} {js}")
    return js["data"]["token"]


def fetch_all(token):
    out, page = [], 1
    while True:
        st, js = api("GET", f"/articles?page={page}&page_size=100", token=token)
        if st != 200:
            log.error("fetch failed %s %s", st, js)
            break
        items = js.get("data", {}).get("items") or []
        if not items:
            break
        out += items
        if len(items) < 100:
            break
        page += 1
        time.sleep(0.3)
    return out


def is_r2(u):
    return bool(u) and (".r2.dev" in u or ".r2.cloudflarestorage.com" in u)


def load_done():
    try:
        with open(DONE_PATH, encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_done(done):
    with open(DONE_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted(done), f, ensure_ascii=False, indent=0)


def image_query_for(a, tok):
    """Ask the Studio (which holds the LLM key) for an English cover query."""
    title = (a.get("rewritten_title") or a.get("title") or "").strip()
    if not title:
        return "artificial intelligence technology"
    body = {
        "title": title,
        "summary": (a.get("summary") or "")[:500],
        "content": (a.get("content") or "")[:3000],
    }
    st, js = api("POST", "/articles/generate-image-query", token=tok, body=body)
    if st == 200:
        q = ((js.get("data") or {}).get("query") or "").strip()
        if q:
            return q
    return title


def main():
    log.info("r2_enabled=%s gen_enabled=%s gen_remaining=%d", r2_enabled(), gen_enabled(), gen_remaining())
    if not gen_enabled():
        raise SystemExit("MS_IMAGE_TOKEN / MS_TOKEN not set — AI gen channel disabled")

    tok = login()
    log.info("admin login OK")
    arts = fetch_all(tok)
    log.info("total articles=%d", len(arts))
    done = load_done()
    log.info("already ai-covered=%d", len(done))

    need, owner = {}, {}
    n_has_original = n_done_skip = 0
    for a in arts:
        src_url = (a.get("url") or "").strip()
        if not src_url.startswith("http"):
            continue
        if src_url in done:
            n_done_skip += 1
            continue
        if gen_remaining() <= 0:
            log.info("gen quota for this run exhausted, stop scanning")
            break
        # 有原图通道命中的不归本回填管（backfill_hero 的职责）
        if first_content_image(a.get("content") or "", src_url):
            n_has_original += 1
            continue
        og = ""
        try:
            og = feed_fetcher.fetch_og_image(src_url)
        except Exception as ex:
            log.warning("og check failed %s: %s", src_url, ex)
        time.sleep(0.3)
        if og:
            n_has_original += 1
            continue
        # 无原图 → 现封面必为素材图/占位 → AI 生成贴题插画
        q = image_query_for(a, tok)
        g = generate_cover(q)
        if not g:
            log.info("ai-gen miss [id=%s] %r (q=%r)",
                     a.get("id"), (a.get("title") or "")[:50], q[:50])
            continue
        need[src_url] = g
        owner[src_url] = a
        log.info("ai-gen [id=%s] %r (q=%r) -> %s",
                 a.get("id"), (a.get("title") or "")[:50], q[:50], g[:90])

    log.info("scan: %d already-original, %d done-skip; %d to ai-cover",
             n_has_original, n_done_skip, len(need))
    if not need:
        log.info("nothing to backfill")
        return

    # 缓存破坏（同 backfill_hero v2 教训）
    mp = load_map()
    for k in need:
        mp.pop(k, None)
    save_map(mp)

    hosted = upload_images(need)
    r2 = sum(1 for v in hosted.values() if is_r2(v))
    log.info("uploaded to R2=%d/%d", r2, len(need))

    upd = inplace = fail = 0
    for src_url, a in owner.items():
        final = hosted.get(src_url)
        if not final or not is_r2(final):
            continue
        done.add(src_url)
        if final == (a.get("image_url") or ""):
            inplace += 1  # 同 key 覆盖：URL 未变但字节已替换
            continue
        st, js = api("PUT", f"/articles/{a['id']}", token=tok, body={"image_url": final})
        if st == 200:
            upd += 1
        else:
            fail += 1
            log.warning("PUT /articles/%s failed %s %s", a["id"], st, str(js)[:140])
        time.sleep(0.2)
    save_done(done)
    log.info("AI COVER BACKFILL DONE db_updated=%d inplace_replaced=%d failed=%d done_total=%d",
             upd, inplace, fail, len(done))


if __name__ == "__main__":
    main()
