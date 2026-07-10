from app.core.database import SessionLocal
from app.models.source import CrawlLog

db = SessionLocal()
logs = db.query(CrawlLog).order_by(CrawlLog.created_at.desc()).limit(20).all()

print(f"{'时间':<14} | {'source':<8} | {'状态':<10} | found | new | dup | 错误")
print("-" * 80)

for l in logs:
    dt = l.created_at.strftime("%m-%d %H:%M") if l.created_at else "N/A"
    err = l.error_message[:50] if l.error_message else ""
    print(f"{dt:<14} | {l.source_id[:8]:<8} | {l.status:<10} | {l.items_found:5} | {l.items_new:3} | {l.items_duplicate:3} | {err}")

db.close()

