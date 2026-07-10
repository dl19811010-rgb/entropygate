"""修复 6 个采集失败的信息源

失败原因分析（2026-07-09）：
1. DeepSeek Blog  — RSS XML 格式错误 (not well-formed)
2. Microsoft AI    — 410 Gone（源已永久下线）
3. Qwen Blog       — 404 Not Found（URL 不是 RSS feed）
4. Cloudflare AI   — 301→404（URL 已变更）
5. Runway          — 500 Internal Server Error
6. OpenAI Blog     — 403 Forbidden（RSS 被封锁）

处理策略：
- 不可恢复的：禁用 (is_active=False)
- URL 变更的：更新 URL
- XML/RSS 不可用的：切换到 static_html 抓取
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.source import Source

db = SessionLocal()

FIXES = [
    # 1. DeepSeek — RSS XML 格式错误，改用 static_html 抓取博客列表页
    {
        "name": "DeepSeek",
        "action": "update",
        "parser_type": "static_html",
        "url": "https://www.deepseek.com/blog",
        "config": {
            "list_url": "https://www.deepseek.com/blog",
            "language": "en",
            "selectors": {
                "article_list": "a[href^='/blog/']",
                "title": "h2, h3",
                "summary": "p",
            },
        },
    },
    # 2. Microsoft AI — 410 Gone，源已永久下线
    {
        "name": "Microsoft AI",
        "action": "disable",
    },
    # 3. Qwen Blog — URL 是文档页面不是博客feed，切换为 static_html 抓取通义千问官方blog
    {
        "name": "Qwen Blog",
        "action": "update",
        "parser_type": "static_html",
        "url": "https://qwenlm.github.io/blog/",
        "config": {
            "list_url": "https://qwenlm.github.io/blog/",
            "language": "zh",
            "selectors": {
                "article_list": "a[href*='/blog/']",
                "title": "h2, h3",
                "summary": "p",
            },
        },
    },
    # 4. Cloudflare AI — URL 路径变更，但原 feed 不可用，尝试 blog.cloudflare.com/ai/
    {
        "name": "Cloudflare AI",
        "action": "disable",
    },
    # 5. Runway — RSS 服务器 500 错误，改用 static_html
    {
        "name": "Runway",
        "action": "update",
        "parser_type": "static_html",
        "url": "https://runwayml.com/news/",
        "config": {
            "list_url": "https://runwayml.com/news/",
            "language": "en",
            "selectors": {
                "article_list": "a[href*='/news/'], a[href*='/blog/']",
                "title": "h2, h3",
                "summary": "p",
            },
        },
    },
    # 6. OpenAI Blog — RSS 被 403 封锁，改用 static_html
    {
        "name": "OpenAI Blog",
        "action": "update",
        "parser_type": "static_html",
        "url": "https://openai.com/blog/",
        "config": {
            "list_url": "https://openai.com/blog/",
            "language": "en",
            "selectors": {
                "article_list": "a[href*='/blog/']",
                "title": "h2, h3",
                "summary": "p",
            },
        },
    },
]

try:
    for fix in FIXES:
        source = db.query(Source).filter(
            Source.name == fix["name"],
            Source.deleted_at.is_(None)
        ).first()

        if not source:
            print(f"[SKIP] 未找到源: {fix['name']}")
            continue

        if fix["action"] == "disable":
            source.is_active = False
            print(f"[DISABLE] {fix['name']} — 源已永久不可用，已禁用")
        elif fix["action"] == "update":
            source.parser_type = fix["parser_type"]
            source.url = fix["url"]
            source.config = fix["config"]
            source.is_active = True
            print(f"[UPDATE]  {fix['name']} — parser_type={fix['parser_type']}, url={fix['url']}")

    db.commit()
    print("\n=== 修复完成！当前活跃源 ===")
    active_sources = db.query(Source).filter(
        Source.is_active == True,
        Source.deleted_at.is_(None)
    ).all()
    for s in active_sources:
        print(f"  ✅ {s.name} ({s.parser_type}) — {s.url}")

    inactive_sources = db.query(Source).filter(
        Source.is_active == False,
        Source.deleted_at.is_(None)
    ).all()
    if inactive_sources:
        print(f"\n已禁用的源 ({len(inactive_sources)}):")
        for s in inactive_sources:
            print(f"  ❌ {s.name}")

finally:
    db.close()
