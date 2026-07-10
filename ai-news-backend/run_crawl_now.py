"""采集所有活跃源，填充审核数据"""
import sys, asyncio
sys.path.insert(0, '.')
from app.core.database import SessionLocal
from app.services.crawl_service import CrawlService
from app.models.source import Source

async def run():
    db = SessionLocal()
    try:
        svc = CrawlService(db)
        sources = db.query(Source).filter(
            Source.is_active == True,
            Source.deleted_at.is_(None)
        ).all()
        print(f"活跃源: {len(sources)} 个")
        tier_count = {}
        for s in sources:
            t = s.editorial_tier or 'C'
            tier_count[t] = tier_count.get(t, 0) + 1
            print(f"  [{t}级] {s.name} ({s.parser_type})")
        print(f"\nS:{tier_count.get('S',0)} A:{tier_count.get('A',0)} B:{tier_count.get('B',0)} C:{tier_count.get('C',0)}")
        print("\n开始采集...\n")

        results = await svc.fetch_all_active()
        total_new = 0
        for r in results:
            st = r['result'].get('status', '?')
            new = r['result'].get('new', 0)
            found = r['result'].get('found', 0)
            err = r['result'].get('error', '')
            if new > 0:
                print(f"[NEW] {r['name']}: +{new}/{found} 篇 (共{found}篇)")
                total_new += new
            elif st == 'completed':
                print(f"[OK]  {r['name']}: 无新 (共{found}篇)")
            else:
                print(f"[ERR] {r['name']}: {err[:80]}")
        print(f"\n采集完成，新增 {total_new} 篇文章")
    finally:
        db.close()

asyncio.run(run())
