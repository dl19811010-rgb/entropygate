"""Phase 3 — 修复失效中文 RSS，切换 static_html"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.core.database import SessionLocal
from app.models.source import Source

db = SessionLocal()

FIXES = [
    {
        "name": "阿里 AI 官方",
        "parser_type": "static_html",
        "url": "https://tongyi.aliyun.com/blog",
        "config": {
            "list_url": "https://tongyi.aliyun.com/blog",
            "language": "zh",
            "selectors": {
                "article_list": "a[href*='/blog/'], a[href*='/article/']",
                "title": "h2, h3, .title",
                "summary": "p",
            },
        },
    },
    {
        "name": "机器之心",
        "parser_type": "static_html",
        "url": "https://www.jiqizhixin.com",
        "config": {
            "list_url": "https://www.jiqizhixin.com/articles",
            "language": "zh",
            "selectors": {
                "article_list": "a[href*='/articles/']",
                "title": "h2, h3, .article-title",
                "summary": ".article-excerpt, p",
            },
        },
    },
    {
        "name": "36氪 AI",
        "parser_type": "static_html",
        "url": "https://36kr.com/information/ai",
        "config": {
            "list_url": "https://36kr.com/information/ai",
            "language": "zh",
            "selectors": {
                "article_list": "a[href*='/p/']",
                "title": ".article-item-title, h3, .title",
                "summary": ".article-item-description, p",
            },
        },
    },
]

for fix in FIXES:
    source = db.query(Source).filter(Source.name == fix["name"], Source.deleted_at.is_(None)).first()
    if source:
        source.parser_type = fix["parser_type"]
        source.url = fix["url"]
        source.config = fix["config"]
        source.last_fetch_status = "pending"
        print(f"[FIX] {fix['name']}: → static_html")
    else:
        print(f"[SKIP] {fix['name']}: 不存在")

db.commit()
db.close()
print("Done")
