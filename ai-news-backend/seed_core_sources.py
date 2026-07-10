"""添加 4 个核心信息源（最小补全包）"""
from app.core.database import SessionLocal
from app.models.source import Source
from app.models.category import Category
from sqlalchemy.orm.attributes import flag_modified


def seed_core_sources():
    db = SessionLocal()

    # 统一归类到 "AI新动态"
    cat = db.query(Category).filter(Category.slug == "ai-news", Category.deleted_at.is_(None)).first()
    category_id = cat.id if cat else None

    sources = [
        {
            "name": "OpenAI Blog",
            "url": "https://openai.com/blog",
            "type": "rss",
            "parser_type": "rss",
            "fetch_interval": 60,
            "dedup_strategy": "title",
            "config": {
                "rss_url": "https://openai.com/blog/rss.xml",
                "language": "en",
                "max_items": 20,
            },
        },
        {
            "name": "Google AI Blog",
            "url": "https://blog.google/technology/ai/",
            "type": "rss",
            "parser_type": "rss",
            "fetch_interval": 60,
            "dedup_strategy": "title",
            "config": {
                "rss_url": "https://blog.google/technology/ai/rss/",
                "language": "en",
                "max_items": 20,
            },
        },
        {
            "name": "Anthropic News",
            "url": "https://www.anthropic.com/news",
            "type": "static_html",
            "parser_type": "static_html",
            "fetch_interval": 60,
            "dedup_strategy": "title",
            "config": {
                "list_url": "https://www.anthropic.com/news",
                "language": "en",
                "selectors": {
                    "article_list": 'a[href^="/news/"]',
                    "title": "h2",
                    "summary": 'p[class*="body"]',
                },
            },
        },
        {
            "name": "月之暗面 Kimi Blog",
            "url": "https://www.kimi.com/blog/",
            "type": "static_html",
            "parser_type": "static_html",
            "fetch_interval": 120,
            "dedup_strategy": "title",
            "config": {
                "list_url": "https://www.kimi.com/blog/",
                "language": "zh",
                "selectors": {
                    "article_list": ".menu-card",
                    "title": ".card-title",
                    "summary": ".card-body",
                },
            },
        },
    ]

    added = 0
    skipped = 0
    for data in sources:
        exists = db.query(Source).filter(Source.name == data["name"], Source.deleted_at.is_(None)).first()
        if exists:
            print(f"已存在，跳过: {data['name']}")
            skipped += 1
            continue

        source = Source(
            name=data["name"],
            url=data["url"],
            type=data["type"],
            parser_type=data["parser_type"],
            category_id=category_id,
            fetch_interval=data["fetch_interval"],
            is_active=True,
            auto_publish=False,
            ai_preprocess=True,
            dedup_strategy=data["dedup_strategy"],
            config=data["config"],
        )
        db.add(source)
        added += 1
        print(f"添加: {data['name']}")

    db.commit()
    print(f"\n完成：新增 {added} 个，跳过 {skipped} 个")


if __name__ == "__main__":
    seed_core_sources()

