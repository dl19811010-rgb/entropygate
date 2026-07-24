#!/usr/bin/env python3
"""One-shot backfill: replace stock-photo covers with ORIGINAL article images.

Why: the P2/P3 pipeline filled covers from Unsplash keyword search, which users
report as "not close to the topic". Supabase11 priority ladder says the source
page's own hero/embedded image is the most on-topic cover. For every existing
article we:
  1. extract the first meaningful <img> from the stored body HTML (free), else
  2. fetch the original page's og:image / twitter:image (US runner can reach
     origins that are GFW-/CF-blocked from China),
  3. mirror it to R2 and PUT article.image_url.

Skips articles where no original image is found (they keep current cover).
Safe to re-run: already-correct covers resolve to the same R2 URL = no-op.

Trigger: Actions -> "Backfill original hero images (US egress)" -> Run workflow.
"""
import sys
import os
import time
import logging
import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("backfill-hero")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from image_host import upload_images, r2_enabled
from feed_fetcher import feed_fetcher, first_content_image

BASE = os.getenv("STUDIO_BASE_URL", "https://entropygate.cc.cd").rstrip("/") + "/api/v1"
ADMIN_U = "admin"
ADMIN_P = os.getenv("STUDIO_ADMIN_PASSWORD", "admin123")

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


def main():
    log.info("r2_enabled=%s", r2_enabled())
    tok = login()
    log.info("admin login OK")
    arts = fetch_all(tok)
    log.info("total articles=%d", len(arts))

    need = {}        # article-url -> original image url (to mirror)
    owner = {}       # article-url -> article row
    n_body = n_og = 0
    for a in arts:
        src_url = (a.get("url") or "").strip()
        if not src_url:
            continue
        cur = a.get("image_url") or ""
        # ① 正文内嵌图（库存 content HTML，零网络）
        img = first_content_image(a.get("content") or "", src_url)
        if img:
            n_body += 1
        # ② 原文页 og:image（美国 runner 直连；被墙/被拦返回 ""）
        if not img:
            img = feed_fetcher.fetch_og_image(src_url)
            if img:
                n_og += 1
            time.sleep(0.3)
        if not img or img == cur:
            continue
        need[src_url] = img
        owner[src_url] = a
    log.info("original images found: %d from body, %d from og:image; %d article(s) to update",
             n_body, n_og, len(need))
    if not need:
        log.info("nothing to backfill")
        return

    hosted = upload_images(need)
    r2 = sum(1 for v in hosted.values() if is_r2(v))
    log.info("uploaded to R2=%d/%d", r2, len(need))

    upd = fail = 0
    for src_url, a in owner.items():
        final = hosted.get(src_url)
        if not final or not is_r2(final) or final == (a.get("image_url") or ""):
            continue
        st, js = api("PUT", f"/articles/{a['id']}", token=tok, body={"image_url": final})
        if st == 200:
            upd += 1
        else:
            fail += 1
            log.warning("PUT /articles/%s failed %s %s", a["id"], st, str(js)[:140])
        time.sleep(0.2)
    log.info("HERO BACKFILL DONE updated=%d failed=%d", upd, fail)


if __name__ == "__main__":
    main()
