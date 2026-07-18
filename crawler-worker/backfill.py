#!/usr/bin/env python3
"""One-shot backfill: re-host all existing articles' cover images to R2.

Runs on the US GitHub runner (where origin hosts like googleapis/hf/twitter
are reachable) so original images can actually be downloaded. Mirrors every
non-R2 cover image to R2 and PATCHes Studio's article.image_url via PUT.

The crawler itself only mirrors *newly fetched* articles, so legacy articles
already in Studio keep their original (often China-blocked) image URLs. This
script fixes that gap without re-crawling sources.
"""
import sys
import os
import json
import time
import logging
import urllib.request
import urllib.error

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("backfill")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from image_host import upload_images, r2_enabled

BASE = os.getenv("STUDIO_BASE_URL", "https://entropygate.cc.cd").rstrip("/") + "/api/v1"
ADMIN_U = "admin"
ADMIN_P = os.getenv("STUDIO_ADMIN_PASSWORD", "admin123")


def api(method, path, token=None, body=None, retry=6):
    url = path if path.startswith("http") else BASE + path
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    if token:
        headers["X-Access-Token"] = token
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(retry + 1):
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retry:
                w = int(e.headers.get("Retry-After", 2 ** attempt))
                log.warning("rate-limited (429), sleep %ds", w)
                time.sleep(w)
                continue
            return e.code, (json.loads(e.read().decode()) if e.fp else {})
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


def fetch_all():
    out, page = [], 1
    while True:
        st, js = api("GET", f"/articles?page={page}&page_size=100&fields=light")
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
    arts = fetch_all()
    log.info("total articles=%d", len(arts))
    need = {}
    for a in arts:
        img = a.get("image_url")
        if img and not is_r2(img):
            need[a.get("url") or str(a["id"])] = img
    log.info("articles needing backfill=%d", len(need))
    if not need:
        log.info("nothing to backfill")
        return
    hosted = upload_images(need)
    r2 = sum(1 for v in hosted.values() if is_r2(v))
    log.info("uploaded to R2=%d/%d", r2, len(need))
    upd = fail = 0
    for a in arts:
        key = a.get("url") or str(a["id"])
        if key not in need:
            continue
        final = hosted.get(key)
        if not final or not is_r2(final) or final == a.get("image_url"):
            continue
        st, js = api("PUT", f"/articles/{a['id']}", token=tok, body={"image_url": final})
        if st == 200:
            upd += 1
        else:
            fail += 1
            log.warning("PUT /articles/%s failed %s %s", a["id"], st, str(js)[:140])
        time.sleep(0.2)
    log.info("BACKFILL DONE updated=%d failed=%d", upd, fail)


if __name__ == "__main__":
    main()
