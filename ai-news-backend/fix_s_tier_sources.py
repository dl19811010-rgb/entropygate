"""EOS — 修复 5 个 S 级源：从失效 RSS 切换到 static_html/web 采集

Root cause: 2026 年以后，大量 AI 公司已不再维护 RSS，内容通过 Blog/Changelog/Docs 发布。
Fix: 切换到 static_html 或已知的有效采集方式。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.core.database import SessionLocal
from app.models.source import Source

db = SessionLocal()

FIXES = [
    {
        "name": "Google DeepMind",
        "parser_type": "static_html",
        "url": "https://deepmind.google/discover/blog/",
        "config": {
            "list_url": "https://deepmind.google/discover/blog/",
            "language": "en",
            "selectors": {
                "article_list": "a[href*='/discover/blog/']",
                "title": "h2, h3, .title",
                "summary": "p",
            },
        },
        "editorial_tier": "S",
        "editorial_role": "核心 Intelligence",
    },
    {
        "name": "Meta AI",
        "parser_type": "static_html",
        "url": "https://ai.meta.com/blog/",
        "config": {
            "list_url": "https://ai.meta.com/blog/",
            "language": "en",
            "selectors": {
                "article_list": "a[href*='/blog/']",
                "title": "h2, h3, .title",
                "summary": "p",
            },
        },
        "editorial_tier": "S",
        "editorial_role": "核心 Intelligence",
    },
    {
        "name": "xAI",
        "parser_type": "static_html",
        "url": "https://x.ai/blog",
        "config": {
            "list_url": "https://x.ai/blog",
            "language": "en",
            "selectors": {
                "article_list": "a[href*='/blog']",
                "title": "h2, h3",
                "summary": "p",
            },
        },
        "editorial_tier": "S",
        "editorial_role": "核心 Intelligence",
    },
    {
        "name": "Mistral AI",
        "parser_type": "static_html",
        "url": "https://mistral.ai/news/",
        "config": {
            "list_url": "https://mistral.ai/news/",
            "language": "en",
            "selectors": {
                "article_list": "a[href*='/news/']",
                "title": "h2, h3",
                "summary": "p",
            },
        },
        "editorial_tier": "S",
        "editorial_role": "核心 Intelligence",
    },
    {
        "name": "Perplexity",
        "parser_type": "static_html",
        "url": "https://www.perplexity.ai/blog",
        "config": {
            "list_url": "https://www.perplexity.ai/blog",
            "language": "en",
            "selectors": {
                "article_list": "a[href*='/blog/']",
                "title": "h2, h3",
                "summary": "p",
            },
        },
        "editorial_tier": "A",
        "editorial_role": "AI 产品",
    },
]

try:
    updated = 0
    for fix in FIXES:
        source = db.query(Source).filter(
            Source.name == fix["name"],
            Source.deleted_at.is_(None)
        ).first()
        if not source:
            print(f"[SKIP] 未找到: {fix['name']}")
            continue
        source.parser_type = fix["parser_type"]
        source.url = fix["url"]
        source.config = fix["config"]
        source.editorial_tier = fix["editorial_tier"]
        source.editorial_role = fix["editorial_role"]
        source.is_active = True
        source.last_fetch_status = "pending"
        updated += 1
        print(f"[FIX] {fix['name']}: rss → {fix['parser_type']}")

    db.commit()
    print(f"\n已修复 {updated} 个源")

    # 验证
    active = db.query(Source).filter(Source.is_active == True, Source.deleted_at.is_(None)).all()
    print(f"\n活跃源: {len(active)}")
    for s in sorted(active, key=lambda x: (x.editorial_tier or 'Z', x.name)):
        print(f"  [{s.editorial_tier}] {s.name:<25} {s.parser_type:<15}")

finally:
    db.close()
