#!/usr/bin/env python3
"""Cover recipe 横评工具：同一批文章 × 多个 provider，同一 brief 出图，出 HTML 对比墙。

存在的意义（用户 2026-07-24）：封面生成是一套系统，换模型迭代 = 改配置。
但"哪个模型/哪套配方更好"必须人眼裁决——本工具把决策成本降到最低：
同批文章、同一视觉导演 brief、不同 provider 各出一张，浏览器里并排打分。

用法（本地或 Actions 手动跑，需要 STUDIO/R2/MS_IMAGE 环境变量）：
  cd crawler-worker
  set MS_IMAGE_TOKEN=...   # 或 export
  python eval_covers.py --limit 6 --providers zimage_turbo,zimage,qwen_image
  → eval_out/index.html 打开即对比墙（图片本地相对路径引用）

配额提醒：总生成数 = limit × providers 数，每提交一次烧 1 次当日额度
（50 次/key/天）。brief 每篇只取一次（各 provider 共用，不重复烧 LLM）。

不产生任何生产副作用：不传 R2、不改 DB、不动 image_map/done 文件。
"""
import argparse
import html
import json
import logging
import os
import sys
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("eval-covers")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def main():
    ap = argparse.ArgumentParser(description="AI cover provider 横评对比墙")
    ap.add_argument("--limit", type=int, default=6, help="抽样文章数（默认 6）")
    ap.add_argument("--providers", default="",
                    help="逗号分隔 provider 键名；默认注册表全部")
    ap.add_argument("--out", default=os.path.join(HERE, "eval_out"),
                    help="输出目录（默认 crawler-worker/eval_out）")
    ap.add_argument("--ids", default="",
                    help="逗号分隔文章 id 清单（指定后忽略 --limit 随机抽样）")
    args = ap.parse_args()

    import image_gen
    providers = [p.strip() for p in args.providers.split(",") if p.strip()] \
        or list(image_gen.PROVIDERS.keys())
    bad = [p for p in providers if p not in image_gen.PROVIDERS]
    if bad:
        raise SystemExit(f"unknown provider(s): {bad}; registered: {list(image_gen.PROVIDERS)}")
    # MAX_PER_RUN 是导入期读取的模块常量，remaining() 每次调用动态读模块全局，
    # 直接补丁模块属性即可放大本次横评的运行内上限
    image_gen.MAX_PER_RUN = args.limit * len(providers) + 2

    if not image_gen.enabled():
        raise SystemExit("MS_IMAGE_TOKEN / MS_TOKEN not set")

    import httpx
    base = os.getenv("STUDIO_BASE_URL", "https://entropygate.cc.cd").rstrip("/") + "/api/v1"
    admin_p = os.getenv("STUDIO_ADMIN_PASSWORD", "admin123")

    def api(method, path, token=None, body=None):
        h = {"Accept": "application/json", "Content-Type": "application/json",
             "User-Agent": "Mozilla/5.0 (compatible; EntropyGate-Eval/1.0)"}
        if token:
            h["X-Access-Token"] = token
        r = httpx.request(method, base + path, headers=h, json=body, timeout=30)
        return r.status_code, (r.json() if r.content else {})

    st, js = api("POST", "/admin/auth/login",
                 body={"username": "admin", "password": admin_p})
    tok = (js.get("data") or {}).get("token")
    if st != 200 or not tok:
        raise SystemExit(f"login failed: {st} {js}")

    # 取文章：--ids 指定 或 最近 limit 篇（取全文版以喂 brief）
    arts = []
    if args.ids:
        for aid in [i.strip() for i in args.ids.split(",") if i.strip()]:
            st, js = api("GET", f"/articles/{aid}", token=tok)
            a = (js.get("data") or {})
            if st == 200 and a.get("id"):
                arts.append(a)
    else:
        st, js = api("GET", "/articles?page=1&page_size=100", token=tok)
        items = (js.get("data") or {}).get("items") or []
        # 优先挑"无原图"长相的（素材图/无图）文章更贴近真实使用场景，
        # 但横评重点是横向对比，直接取最新 limit 篇即可
        arts = items[: args.limit]
        # 列表接口是 light 字段，逐篇补全文（brief 需要 content）
        full = []
        for a in arts:
            st2, js2 = api("GET", f"/articles/{a['id']}", token=tok)
            fa = (js2.get("data") or {})
            full.append(fa if fa.get("id") else a)
            time.sleep(0.2)
        arts = full
    if not arts:
        raise SystemExit("no articles fetched")
    log.info("eval set: %d articles × %d providers = %d generations",
             len(arts), len(providers), len(arts) * len(providers))

    os.makedirs(args.out, exist_ok=True)
    rows = []
    for idx, a in enumerate(arts):
        title = (a.get("rewritten_title") or a.get("title") or "").strip()
        body = {
            "title": title,
            "summary": (a.get("summary") or a.get("ai_summary") or "")[:500],
            "content": (a.get("content") or "")[:3000],
        }
        st, js = api("POST", "/articles/generate-cover-brief", token=tok, body=body)
        brief = (js.get("data") or {}) if st == 200 else {}
        if not (brief.get("metaphor") or "").strip():
            log.warning("brief failed for id=%s, using fallback", a.get("id"))
            brief = {"metaphor": title or "abstract AI concept",
                     "style": "abstract_light", "palette": ""}
        log.info("[%d/%d] id=%s style=%s brief=%r",
                 idx + 1, len(arts), a.get("id"), brief.get("style"),
                 (brief.get("metaphor") or "")[:70])

        cells = {}
        for p in providers:
            data = image_gen.generate_image(brief, provider=p)
            if not data:
                log.warning("  %s: FAILED", p)
                cells[p] = ""
                continue
            ext = ".jpg" if data[:3] == b"\xff\xd8\xff" else ".png"
            fn = f"{idx:02d}_{a.get('id')}_{p}{ext}"
            with open(os.path.join(args.out, fn), "wb") as f:
                f.write(data)
            log.info("  %s: %s (%dKB)", p, fn, len(data) // 1024)
            cells[p] = fn
        rows.append({"id": a.get("id"), "title": title, "brief": brief, "cells": cells})

    # ── HTML 对比墙 ──────────────────────────────────────────────────
    parts = [
        "<!doctype html><html><head><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width,initial-scale=1'>",
        "<title>EntropyGate Cover Eval</title><style>",
        "body{background:#0b0f1a;color:#e6e9f2;font:14px/1.6 system-ui,sans-serif;",
        "margin:0;padding:24px}h1{font-size:18px}h2{font-size:13px;color:#8b93a7;",
        "font-weight:500}",
        "table{border-collapse:separate;border-spacing:12px;width:100%}",
        "th{color:#8b93a7;font-weight:600;text-align:left;padding:4px}",
        "td{vertical-align:top;background:#131a2b;border-radius:10px;padding:8px;",
        "width:33%}",
        "td img{width:100%;border-radius:6px;display:block}",
        ".meta{color:#8b93a7;font-size:12px;margin:6px 2px 0;word-break:break-all}",
        ".row{background:#0f1524;border-radius:12px;padding:14px 16px;margin:18px 0}",
        ".brief{color:#aab3c8;font-size:12px;margin-top:4px}",
        ".tag{display:inline-block;background:#1d2a45;color:#7fb0ff;border-radius:4px;",
        "padding:1px 8px;font-size:11px;margin-right:6px}",
        "</style></head><body>",
        f"<h1>EntropyGate 封面横评 — {len(arts)} 篇 × {len(providers)} providers</h1>",
        f"<h2>{time.strftime('%Y-%m-%d %H:%M')} · 同一 brief 各 provider 出图 · "
        f"配额约耗 {len(arts) * len(providers)} 次</h2>",
    ]
    for r in rows:
        b = r["brief"]
        parts.append("<div class='row'>")
        parts.append(f"<div><span class='tag'>id {r['id']}</span>"
                     f"<span class='tag'>{html.escape(str(b.get('style') or ''))}</span>"
                     f"<b>{html.escape(r['title'][:90])}</b></div>")
        parts.append(f"<div class='brief'>metaphor: {html.escape(str(b.get('metaphor') or ''))}"
                     f"<br>palette: {html.escape(str(b.get('palette') or ''))}</div>")
        parts.append("<table><tr>")
        for p in providers:
            parts.append(f"<th>{html.escape(p)}</th>")
        parts.append("</tr><tr>")
        for p in providers:
            fn = r["cells"].get(p) or ""
            if fn:
                parts.append(f"<td><img src='{html.escape(fn)}' loading='lazy'>"
                             f"<div class='meta'>{html.escape(fn)}</div></td>")
            else:
                parts.append("<td><div class='meta'>FAILED</div></td>")
        parts.append("</tr></table></div>")
    parts.append("</body></html>")

    out_html = os.path.join(args.out, "index.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    log.info("DONE -> %s", out_html)


if __name__ == "__main__":
    main()
