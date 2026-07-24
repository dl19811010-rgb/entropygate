#!/usr/bin/env python3
"""Backfill original hero images + remediate tiny/off-topic covers (v2).

Per-article cover ladder (Supabase11 priority: official image > stock search):
  ① first meaningful <img> in the stored body HTML (zero network)
  ② original page og:image / twitter:image (declared-size gated: >=400x200)
  ③ Unsplash keyword-ranked search — ONLY when no original was found AND the
      current cover is tiny (<400x200) or missing. A decent current cover is
      left alone (never downgrade a good cover to stock).

Cache-busting: upload_images() dedups via image_map.json keyed by article URL —
cached entries are reused WITHOUT re-upload, which would silently keep the old
cover. Keys we intend to replace are dropped from the map before upload. The
deterministic R2 key (sha1 of article URL) means bytes are replaced in place
(same URL); the DB is only PUT when the final URL actually differs.

Trigger: Actions -> "Backfill original hero images (US egress)" -> Run workflow.
Safe to re-run: articles already showing the original image are no-ops.
"""
import sys
import os
import time
import logging
import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("backfill-hero")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from image_host import (
    upload_images, r2_enabled, sniff_dims, load_map, save_map,
    MIN_IMG_W, MIN_IMG_H,
)
from feed_fetcher import feed_fetcher, first_content_image

BASE = os.getenv("STUDIO_BASE_URL", "https://entropygate.cc.cd").rstrip("/") + "/api/v1"
ADMIN_U = "admin"
ADMIN_P = os.getenv("STUDIO_ADMIN_PASSWORD", "admin123")
PACE = int(os.getenv("IMG_SEARCH_PACE", "5"))  # 兜底搜图少量触发，短间隔即可

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


def cover_dims(url):
    """Sniff (w,h) of the current cover; (0,0) = unreachable/unknown."""
    if not url:
        return 0, 0
    try:
        r = httpx.get(url, timeout=25, follow_redirects=True,
                      headers={**UA, "Accept": "image/*,*/*;q=0.8"})
        if r.status_code != 200:
            return 0, 0
        return sniff_dims(r.content[:65536])
    except Exception:
        return 0, 0


def image_query_for(a, tok):
    """Ask the Studio (which holds the LLM key) for an English cover query + keywords."""
    title = (a.get("rewritten_title") or a.get("title") or "").strip()
    if not title:
        return "artificial intelligence technology", None
    body = {
        "title": title,
        "summary": (a.get("summary") or "")[:500],
        "content": (a.get("content") or "")[:3000],
    }
    st, js = api("POST", "/articles/generate-image-query", token=tok, body=body)
    if st == 200:
        d = js.get("data") or {}
        q = (d.get("query") or "").strip()
        kws = [str(k) for k in (d.get("keywords") or []) if k]
        if q:
            return q, (kws or None)
    return title, None


def main():
    log.info("r2_enabled=%s", r2_enabled())
    try:
        from image_search import search_images, enabled as search_enabled, provider_name
        can_search = search_enabled()
        log.info("image search enabled=%s provider=%s", can_search, provider_name())
    except Exception as ex:
        log.warning("image_search import failed: %s", ex)
        search_images, can_search = None, False

    tok = login()
    log.info("admin login OK")
    arts = fetch_all(tok)
    log.info("total articles=%d", len(arts))

    need, owner, reason = {}, {}, {}
    n_body = n_og = n_stock = 0
    for a in arts:
        src_url = (a.get("url") or "").strip()
        if not src_url.startswith("http"):
            continue
        cur = (a.get("image_url") or "").strip()
        # ① 正文内嵌图（库存 content HTML，零网络）
        img = first_content_image(a.get("content") or "", src_url)
        if img:
            n_body += 1
        # ② 原文页 og:image（声明尺寸门控；被墙/被拦返回 ""）
        if not img:
            img = feed_fetcher.fetch_og_image(src_url)
            if img:
                n_og += 1
            time.sleep(0.3)
        if img and img != cur:
            need[src_url] = img
            owner[src_url] = a
            reason[src_url] = "original"
            continue
        # ③ 无原图可用：仅当当前封面小/缺时才换素材库搜图
        w, h = cover_dims(cur) if cur else (0, 0)
        cur_ok = w >= MIN_IMG_W and h >= MIN_IMG_H
        if not cur_ok and can_search:
            q, kws = image_query_for(a, tok)
            try:
                hits = search_images(q, keywords=kws, allow_wikimedia_fallback=False) if kws \
                    else search_images(q, allow_wikimedia_fallback=False)
            except Exception as ex:
                log.warning("img-search failed [id=%s]: %s", a.get("id"), ex)
                hits = []
            if hits:
                need[src_url] = hits[0]["url"]
                owner[src_url] = a
                reason[src_url] = "stock"
                n_stock += 1
                log.info("img-stock [id=%s] %r (cur=%sx%s) -> %s",
                         a.get("id"), (a.get("title") or "")[:50], w, h, hits[0]["url"])
            else:
                log.info("img-stock [id=%s] %r no relevant hit -> keep current",
                         a.get("id"), (a.get("title") or "")[:50])
            time.sleep(PACE)

    log.info("resolve: %d body, %d og, %d stock; %d article(s) to re-host",
             n_body, n_og, n_stock, len(need))
    if not need:
        log.info("nothing to backfill")
        return

    # 缓存破坏：upload_images 命中 image_map 旧 R2 条目会直接复用不上传，
    # 必须先剔除待替换键，强制重新下载+按确定性 key 覆盖上传。
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
    log.info("HERO BACKFILL DONE db_updated=%d inplace_replaced=%d failed=%d", upd, inplace, fail)


if __name__ == "__main__":
    main()
