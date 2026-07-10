import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.source import Source
from app.models.category import Category
from datetime import datetime

db = SessionLocal()

try:
    ai_category = db.query(Category).filter(Category.name == "AI新动态").first()
    if not ai_category:
        ai_category = Category(name="AI新动态", slug="ai-news", description="AI模型、能力、Agent相关更新")
        db.add(ai_category)
        db.commit()
        db.refresh(ai_category)

    sources_to_disable = [
        "机器之能",
        "量子位",
        "36氪 AI",
        "AI 前线",
        "机器之心",
        "Synced",
    ]

    for name in sources_to_disable:
        source = db.query(Source).filter(Source.name == name).first()
        if source:
            source.is_active = False
            print(f"禁用: {name}")

    new_sources = [
        {
            "name": "OpenAI Blog",
            "url": "https://openai.com/blog",
            "parser_type": "rss",
            "config": {
                "rss_url": "https://openai.com/blog/rss",
                "language": "en",
                "max_age_days": 7,
                "fetch_fulltext": True,
                "priority": "high",
            },
        },
        {
            "name": "Anthropic News",
            "url": "https://www.anthropic.com/news",
            "parser_type": "rss",
            "config": {
                "rss_url": "https://www.anthropic.com/news/rss",
                "language": "en",
                "max_age_days": 7,
                "fetch_fulltext": True,
                "priority": "high",
            },
        },
        {
            "name": "Google AI Blog",
            "url": "https://ai.googleblog.com",
            "parser_type": "rss",
            "config": {
                "rss_url": "https://ai.googleblog.com/feeds/posts/default",
                "language": "en",
                "max_age_days": 7,
                "fetch_fulltext": True,
                "priority": "high",
            },
        },
        {
            "name": "Google DeepMind",
            "url": "https://deepmind.google/discover/blog",
            "parser_type": "rss",
            "config": {
                "rss_url": "https://deepmind.google/discover/blog/rss",
                "language": "en",
                "max_age_days": 7,
                "fetch_fulltext": True,
                "priority": "high",
            },
        },
        {
            "name": "Microsoft AI",
            "url": "https://blogs.microsoft.com/ai",
            "parser_type": "rss",
            "config": {
                "rss_url": "https://blogs.microsoft.com/ai/feed/",
                "language": "en",
                "max_age_days": 7,
                "fetch_fulltext": True,
                "priority": "high",
            },
        },
        {
            "name": "Meta AI",
            "url": "https://ai.meta.com/blog",
            "parser_type": "rss",
            "config": {
                "rss_url": "https://ai.meta.com/blog/rss/",
                "language": "en",
                "max_age_days": 7,
                "fetch_fulltext": True,
                "priority": "high",
            },
        },
        {
            "name": "xAI",
            "url": "https://x.ai",
            "parser_type": "rss",
            "config": {
                "rss_url": "https://x.ai/feed.xml",
                "language": "en",
                "max_age_days": 7,
                "fetch_fulltext": True,
                "priority": "high",
            },
        },
        {
            "name": "Qwen Blog",
            "url": "https://qwen.readthedocs.io",
            "parser_type": "rss",
            "config": {
                "rss_url": "https://qwen.readthedocs.io/zh/latest/news/index.html",
                "language": "zh",
                "max_age_days": 7,
                "fetch_fulltext": True,
                "priority": "medium",
            },
        },
        {
            "name": "DeepSeek",
            "url": "https://www.deepseek.com/blog",
            "parser_type": "rss",
            "config": {
                "rss_url": "https://www.deepseek.com/blog/rss",
                "language": "en",
                "max_age_days": 7,
                "fetch_fulltext": True,
                "priority": "high",
            },
        },
        {
            "name": "Mistral AI",
            "url": "https://mistral.ai/news",
            "parser_type": "rss",
            "config": {
                "rss_url": "https://mistral.ai/news/feed/",
                "language": "en",
                "max_age_days": 7,
                "fetch_fulltext": True,
                "priority": "high",
            },
        },
        {
            "name": "Perplexity",
            "url": "https://www.perplexity.ai/blog",
            "parser_type": "rss",
            "config": {
                "rss_url": "https://www.perplexity.ai/blog/rss",
                "language": "en",
                "max_age_days": 7,
                "fetch_fulltext": True,
                "priority": "medium",
            },
        },
        {
            "name": "Runway",
            "url": "https://runwayml.com/blog",
            "parser_type": "rss",
            "config": {
                "rss_url": "https://runwayml.com/blog/feed",
                "language": "en",
                "max_age_days": 7,
                "fetch_fulltext": True,
                "priority": "medium",
            },
        },
        {
            "name": "Cursor",
            "url": "https://cursor.sh",
            "parser_type": "rss",
            "config": {
                "rss_url": "https://cursor.sh/changelog.xml",
                "language": "en",
                "max_age_days": 7,
                "fetch_fulltext": True,
                "priority": "high",
            },
        },
        {
            "name": "Cloudflare AI",
            "url": "https://blog.cloudflare.com/ai",
            "parser_type": "rss",
            "config": {
                "rss_url": "https://blog.cloudflare.com/ai/feed",
                "language": "en",
                "max_age_days": 7,
                "fetch_fulltext": True,
                "priority": "medium",
            },
        },
        {
            "name": "Hugging Face",
            "url": "https://huggingface.co/blog",
            "parser_type": "rss",
            "config": {
                "rss_url": "https://huggingface.co/blog/feed.xml",
                "language": "en",
                "max_age_days": 7,
                "fetch_fulltext": True,
                "priority": "high",
            },
        },
        {
            "name": "GitHub Changelog",
            "url": "https://github.blog/changelog",
            "parser_type": "rss",
            "config": {
                "rss_url": "https://github.blog/changelog/feed",
                "language": "en",
                "max_age_days": 7,
                "fetch_fulltext": True,
                "priority": "medium",
            },
        },
    ]

    for src in new_sources:
        existing = db.query(Source).filter(Source.name == src["name"]).first()
        if existing:
            print(f"已存在: {src['name']}")
            existing.is_active = True
            existing.config = src["config"]
            existing.category_id = ai_category.id
        else:
            source = Source(
                name=src["name"],
                url=src["url"],
                type="rss",
                parser_type=src["parser_type"],
                config=src["config"],
                category_id=ai_category.id,
                is_active=True,
            )
            db.add(source)
            print(f"新增: {src['name']}")

    db.commit()
    print("\n源配置更新完成")

    sources = db.query(Source).filter(Source.is_active == True, Source.deleted_at.is_(None)).all()
    print(f"\n活跃源数量: {len(sources)}")
    for s in sources:
        print(f"  - {s.name} ({s.parser_type})")

finally:
    db.close()

