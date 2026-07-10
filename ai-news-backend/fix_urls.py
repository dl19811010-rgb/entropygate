"""Fix remaining bad URLs"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.core.database import SessionLocal
from app.models.source import Source

db = SessionLocal()

FIXES = [
    {
        "name": "36氪 AI",
        "url": "https://36kr.com/information/ai",
        "config": {
            "list_url": "https://36kr.com/information/ai",
            "language": "zh",
        },
    },
    {
        "name": "阿里 AI 官方",
        "url": "https://tongyi.aliyun.com/blog",
        "config": {
            "list_url": "https://tongyi.aliyun.com/blog",
            "language": "zh",
        },
    },
]

for f in FIXES:
    s = db.query(Source).filter(Source.name == f["name"], Source.deleted_at.is_(None)).first()
    if s:
        s.url = f["url"]
        cfg = dict(s.config or {})
        cfg.update(f["config"])
        s.config = cfg
        s.last_fetch_status = "pending"
        print(f"[FIX] {f['name']}: {f['url']}")

db.commit()
db.close()
print("Done")
