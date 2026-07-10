"""Phase 1.3 — 修复中文源 RSS URL"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.core.database import SessionLocal
from app.models.source import Source

db = SessionLocal()

FIXES = [
    {
        "name": "阿里 AI 官方",
        "parser_type": "rss",
        "url": "https://tongyi.aliyun.com/blog",
        "config": {
            "rss_url": "https://help.aliyun.com/feed/tongyi/model-studio",
            "language": "zh",
            "max_items": 20,
        },
    },
    {
        "name": "机器之心",
        "parser_type": "rss",
        "url": "https://www.jiqizhixin.com",
        "config": {
            "rss_url": "https://www.jiqizhixin.com/rss",
            "language": "zh",
            "max_items": 15,
        },
    },
    {
        "name": "36氪 AI",
        "parser_type": "rss",
        "url": "https://36kr.com",
        "config": {
            "rss_url": "https://36kr.com/feed",
            "language": "zh",
            "max_items": 15,
        },
    },
]

for fix in FIXES:
    source = db.query(Source).filter(
        Source.name == fix["name"],
        Source.deleted_at.is_(None)
    ).first()
    if not source:
        # 创建新源
        source = Source(
            name=fix["name"],
            url=fix["url"],
            type="rss",
            parser_type=fix["parser_type"],
            config=fix["config"],
            is_active=True,
            ai_preprocess=True,
            editorial_tier="A",
            editorial_role="AI 媒体",
        )
        db.add(source)
        print(f"[NEW]  {fix['name']}")
    else:
        source.is_active = True
        source.parser_type = fix["parser_type"]
        source.url = fix["url"]
        source.config = fix["config"]
        source.last_fetch_status = "pending"
        source.editorial_tier = source.editorial_tier or "A"
        source.editorial_role = source.editorial_role or "AI 媒体"
        print(f"[FIX]  {fix['name']}")

db.commit()
print("Done")
db.close()
