from app.core.database import SessionLocal
from app.models.source import Source
from app.models.category import Category


def seed_expanded_sources():
    db = SessionLocal()

    cat = db.query(Category).filter(Category.slug == "ai-news", Category.deleted_at.is_(None)).first()
    category_id = cat.id if cat else None

    sources = [
        {
            "name": "arXiv AI Papers",
            "url": "https://arxiv.org/list/cs.AI/recent",
            "type": "rss",
            "parser_type": "rss",
            "fetch_interval": 120,
            "dedup_strategy": "title",
            "config": {
                "rss_url": "https://arxiv.org/rss/cs.AI",
                "language": "en",
                "max_items": 15,
            },
        },
        {
            "name": "Meta AI Blog",
            "url": "https://ai.meta.com/blog/",
            "type": "rss",
            "parser_type": "rss",
            "fetch_interval": 60,
            "dedup_strategy": "title",
            "config": {
                "rss_url": "https://ai.meta.com/blog/rss/",
                "language": "en",
                "max_items": 20,
            },
        },
        {
            "name": "Hugging Face Blog",
            "url": "https://huggingface.co/blog",
            "type": "rss",
            "parser_type": "rss",
            "fetch_interval": 60,
            "dedup_strategy": "title",
            "config": {
                "rss_url": "https://huggingface.co/blog/rss",
                "language": "en",
                "max_items": 20,
            },
        },
        {
            "name": "TechCrunch AI",
            "url": "https://techcrunch.com/category/artificial-intelligence/",
            "type": "rss",
            "parser_type": "rss",
            "fetch_interval": 60,
            "dedup_strategy": "title",
            "config": {
                "rss_url": "https://techcrunch.com/category/artificial-intelligence/feed/",
                "language": "en",
                "max_items": 15,
            },
        },
        {
            "name": "DeepMind Blog",
            "url": "https://deepmind.google/discover/blog/",
            "type": "rss",
            "parser_type": "rss",
            "fetch_interval": 60,
            "dedup_strategy": "title",
            "config": {
                "rss_url": "https://deepmind.google/discover/blog/rss/",
                "language": "en",
                "max_items": 20,
            },
        },
        {
            "name": "AI 前线",
            "url": "https://www.infoq.cn/topic/AI",
            "type": "rss",
            "parser_type": "rss",
            "fetch_interval": 60,
            "dedup_strategy": "title",
            "config": {
                "rss_url": "https://www.infoq.cn/feed/tag/AI",
                "language": "zh",
                "max_items": 15,
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
    seed_expanded_sources()
