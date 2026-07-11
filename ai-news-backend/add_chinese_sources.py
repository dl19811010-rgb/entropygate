"""EOS — 添加中国 AI 产业新闻源

对标 AIBase 的内容覆盖，补充中文 AI 产业源：
- 字节跳动 AI (豆包/Seed)
- 阿里通义千问 (Qwen Blog 已有，补充阿里 AI 官方)
- 腾讯混元
- AIBase 本身作为聚合参考

这些源每天产出真正的中文 AI 产业新闻，是 Discovery 层的关键输入。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.core.database import SessionLocal
from app.models.source import Source
from app.models.category import Category

db = SessionLocal()

# 获取 AI 新闻分类
cat = db.query(Category).filter(
    Category.slug == "ai-news",
    Category.deleted_at.is_(None)
).first()
category_id = cat.id if cat else None

NEW_SOURCES = [
    {
        "name": "字节跳动 AI",
        "url": "https://www.volcengine.com/blog",
        "parser_type": "static_html",
        "editorial_tier": "S",
        "editorial_role": "核心 Intelligence",
        "config": {
            "list_url": "https://www.volcengine.com/blog",
            "language": "zh",
            "selectors": {
                "article_list": "a[href*='/blog/']",
                "title": "h2, h3, .title",
                "summary": "p",
            },
        },
    },
    {
        "name": "阿里 AI 官方",
        "url": "https://tongyi.aliyun.com/blog",
        "parser_type": "rss",
        "editorial_tier": "S",
        "editorial_role": "核心 Intelligence",
        "config": {
            "rss_url": "https://tongyi.aliyun.com/feed.xml",
            "language": "zh",
            "max_items": 20,
        },
    },
    {
        "name": "腾讯混元",
        "url": "https://hunyuan.tencent.com/blog",
        "parser_type": "static_html",
        "editorial_tier": "S",
        "editorial_role": "核心 Intelligence",
        "config": {
            "list_url": "https://hunyuan.tencent.com/blog",
            "language": "zh",
            "selectors": {
                "article_list": "a[href*='/blog/']",
                "title": "h2, h3",
                "summary": "p",
            },
        },
    },
    {
        "name": "机器之心",
        "url": "https://www.jiqizhixin.com",
        "parser_type": "rss",
        "editorial_tier": "A",
        "editorial_role": "AI 媒体",
        "config": {
            "rss_url": "https://rss.jiqizhixin.com/feed",
            "language": "zh",
            "max_items": 15,
        },
    },
    {
        "name": "量子位",
        "url": "https://www.qbitai.com",
        "parser_type": "rss",
        "editorial_tier": "A",
        "editorial_role": "AI 媒体",
        "config": {
            "rss_url": "https://www.qbitai.com/feed",
            "language": "zh",
            "max_items": 15,
        },
    },
]

try:
    added = 0
    updated = 0
    for src in NEW_SOURCES:
        existing = db.query(Source).filter(
            Source.name == src["name"],
            Source.deleted_at.is_(None)
        ).first()
        if existing:
            existing.parser_type = src["parser_type"]
            existing.url = src["url"]
            existing.config = src["config"]
            existing.editorial_tier = src["editorial_tier"]
            existing.editorial_role = src["editorial_role"]
            existing.is_active = True
            existing.last_fetch_status = "pending"
            updated += 1
            print(f"[REACTIVATE] {src['name']}")
        else:
            s = Source(
                name=src["name"],
                url=src["url"],
                type="rss",
                parser_type=src["parser_type"],
                config=src["config"],
                category_id=category_id,
                is_active=True,
                ai_preprocess=True,
                editorial_tier=src["editorial_tier"],
                editorial_role=src["editorial_role"],
            )
            db.add(s)
            added += 1
            print(f"[NEW] {src['name']}")

    db.commit()

    # 分布
    from collections import Counter
    active = db.query(Source).filter(Source.is_active == True, Source.deleted_at.is_(None)).all()
    tc = Counter(s.editorial_tier for s in active)
    print(f"\n新分布: S={tc.get('S',0)} A={tc.get('A',0)} B={tc.get('B',0)} C={tc.get('C',0)}")
    for s in sorted(active, key=lambda x: (x.editorial_tier or 'Z', x.name)):
        print(f"  [{s.editorial_tier}] {s.name:<25} {s.parser_type:<15}")

finally:
    db.close()
