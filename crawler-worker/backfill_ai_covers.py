#!/usr/bin/env python3
"""Backfill AI-generated covers for articles with NO original image.

Target set per article:
  ① first_content_image(stored body HTML) — zero network
  ② og:image / twitter:image of the original page
  both empty  =>  current cover is necessarily a stock photo or the brand
  placeholder. Those get an AI-generated topical cover instead
  (user decision 2026-07-24: AI 生成 > 风景素材图).

v2 配方（2026-07-25，Supabase12 系统化）：
  视觉导演 brief（/articles/generate-cover-brief：概念→视觉隐喻）
  → provider 注册表生图（IMAGE_GEN_PROVIDER，默认 zimage_turbo）
  → 统一后处理（颗粒/暗角/冷调/JPEG）→ 确定性 key 直传 R2。
  brief 端点不可用时自动降级旧 image-query 通道。

Idempotent: article URLs already AI-covered are recorded in
ai_covers_done.json (committed back to the repo by the workflow) and
skipped on re-run — no duplicate quota burn.
AI_COVERS_FORCE=1 无视 done 文件强制重生成（配方/模型迭代后的翻新杠杆；
确定性 key 原地覆盖字节，URL 不变，DB 无需动）。
AI_COVERS_ONLY_IDS="239,244" 只处理指定 id（隐含 force，并跳过 og 慢查），
用于新配方小批量线上验证。

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


def cover_brief_for(a, tok):
    """视觉导演 brief（generate-cover-brief 端点）。返回 dict 或 str 降级 query。

    dict = 标准 v2 路径（概念→隐喻）；str = 端点不可用时的旧 query 通道
    （image_gen.build_prompt 对 str 套默认风格，仍走统一后处理）。
    """
    title = (a.get("rewritten_title") or a.get("title") or "").strip()
    if not title:
        return "artificial intelligence technology"
    body = {
        "title": title,
        "summary": (a.get("summary") or a.get("ai_summary") or "")[:500],
        "content": (a.get("content") or "")[:3000],
    }
    st, js = api("POST", "/articles/generate-cover-brief", token=tok, body=body)
    if st == 200:
        d = js.get("data") or {}
        if (d.get("metaphor") or "").strip():
            return {
                "metaphor": str(d.get("metaphor"))[:400],
                "style": str(d.get("style") or "")[:40],
                "palette": str(d.get("palette") or "")[:120],
                # 叠字层字段（v2.1）：端点未升级时为空，自动退回无字版
                "headline": str(d.get("headline") or "")[:20],
                "highlight": [str(w)[:20] for w in (d.get("highlight") or [])][:2],
            }
    # 降级：旧 image-query 端点（服务素材搜图的 query，套默认风格也能出图）
    st, js = api("POST", "/articles/generate-image-query", token=tok, body=body)
    if st == 200:
        q = ((js.get("data") or {}).get("query") or "").strip()
        if q:
            return q
    return title


def main():
    force = os.getenv("AI_COVERS_FORCE", "0") == "1"
    # 修复模式（定时任务用）：只做 done 漂移检测+重指，不生成、不做 og 慢查
    repair_only = os.getenv("AI_COVERS_REPAIR_ONLY", "0") == "1"
    only_ids = {int(x) for x in os.getenv("AI_COVERS_ONLY_IDS", "").replace("，", ",").split(",")
                if x.strip().isdigit()}
    if only_ids:
        force = True  # 定点重生成隐含 force（否则 done 集会把目标全跳过）
    log.info("r2_enabled=%s gen_enabled=%s gen_remaining=%d force=%s only_ids=%s",
             r2_enabled(), gen_enabled(), gen_remaining(), force,
             sorted(only_ids) if only_ids else "-")
    if not gen_enabled():
        raise SystemExit("MS_IMAGE_TOKEN / MS_TOKEN not set — AI gen channel disabled")

    tok = login()
    log.info("admin login OK")
    arts = fetch_all(tok)
    log.info("total articles=%d", len(arts))
    done = set() if force else load_done()
    log.info("already ai-covered=%d%s", len(done), " (FORCE: ignoring done set)" if force else "")

    need, direct, owner = {}, {}, {}
    drift = {}  # src_url -> (article, expected_r2_url)：DB 指针漂移待修复
    mp0 = load_map()  # done 漂移检测用（image_map 持有最终 R2 URL）
    n_has_original = n_done_skip = 0
    for a in arts:
        src_url = (a.get("url") or "").strip()
        if not src_url.startswith("http"):
            continue
        if only_ids and a.get("id") not in only_ids:
            continue
        if src_url in done:
            n_done_skip += 1
            # 漂移修复（2026-07-26）：Studio 重建会回滚重建前约半小时内的 DB
            # 写入（ossfs 冲刷窗口），done 文章的 image_url 被打回源站默认图/
            # 原始直链。两条图片管线（hero 原图 / AI 封面）回写的都是 R2 URL，
            # 因此「done 但现值非 R2」必为漂移 → 按 map 记录重指，零配额。
            cur = (a.get("image_url") or "")
            exp = mp0.get(src_url) or ""
            if exp and is_r2(exp) and not is_r2(cur):
                drift[src_url] = (a, exp)
            continue
        if repair_only:
            continue  # 修复模式：非 done 文章不处理（生成留给手动/定点跑）
        # 定点模式：目标已有 AI 封面（force 语义）→ 跳过 og 慢查，直接重生成
        if only_ids:
            brief = cover_brief_for(a, tok)
            g = generate_cover(brief, article_url=src_url)
            if not g:
                meta = brief.get("style") if isinstance(brief, dict) else "legacy-q"
                log.info("ai-gen miss [id=%s] %r (style=%s)",
                         a.get("id"), (a.get("title") or "")[:50], meta)
                continue
            owner[src_url] = a
            if is_r2(g):
                direct[src_url] = g
            else:
                need[src_url] = g
            meta = brief.get("style") if isinstance(brief, dict) else "legacy-q"
            log.info("ai-gen [id=%s] %r (style=%s) -> %s",
                     a.get("id"), (a.get("title") or "")[:50], meta, g[:90])
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
        # 无原图 → 现封面必为素材图/占位 → AI 生成贴题封面（v2 配方）
        brief = cover_brief_for(a, tok)
        g = generate_cover(brief, article_url=src_url)
        if not g:
            meta = brief.get("style") if isinstance(brief, dict) else "legacy-q"
            log.info("ai-gen miss [id=%s] %r (style=%s)",
                     a.get("id"), (a.get("title") or "")[:50], meta)
            continue
        owner[src_url] = a
        if is_r2(g):
            direct[src_url] = g   # 已直传 R2，无需再经 upload_images
        else:
            need[src_url] = g     # MS 临时 URL → 交 upload_images 镜像
        meta = brief.get("style") if isinstance(brief, dict) else "legacy-q"
        log.info("ai-gen [id=%s] %r (style=%s) -> %s",
                 a.get("id"), (a.get("title") or "")[:50], meta, g[:90])

    log.info("scan: %d already-original, %d done-skip; %d to ai-cover (%d direct-R2)",
             n_has_original, n_done_skip, len(need) + len(direct), len(direct))

    # 漂移修复先行：只回写指针，不经过生成/上传，any run 都执行
    if drift:
        rep = 0
        for src_url, (a, exp) in drift.items():
            st, js = api("PUT", f"/articles/{a['id']}", token=tok, body={"image_url": exp})
            if st == 200:
                rep += 1
                log.info("drift-fix [id=%s] %r -> %s",
                         a.get("id"), (a.get("title") or "")[:40], exp[:90])
            else:
                log.warning("drift-fix PUT failed [id=%s] %s %s",
                            a.get("id"), st, str(js)[:140])
            time.sleep(0.2)
        log.info("drift repair done: %d/%d re-pointed", rep, len(drift))

    if not need and not direct:
        log.info("nothing to backfill")
        return

    # 缓存破坏（同 backfill_hero v2 教训）：两条路径的键都先剔除
    mp = load_map()
    for k in list(need) + list(direct):
        mp.pop(k, None)
    save_map(mp)

    hosted = upload_images(need) if need else {}
    hosted.update(direct)
    r2 = sum(1 for v in hosted.values() if is_r2(v))
    log.info("hosted on R2=%d/%d", r2, len(hosted))

    # 直传 R2 的条目补录进 image_map（保持 dedup 缓存一致）
    if direct:
        mp = load_map()
        mp.update(direct)
        save_map(mp)

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
