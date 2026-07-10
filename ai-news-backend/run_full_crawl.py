"""按优先级逐个触发所有活跃源采集 - 每个源独立 session"""
import sys
import asyncio
import time
sys.path.append('.')
from app.core.database import SessionLocal
from app.models.source import Source
from app.services.crawl_service import CrawlService


async def crawl_one(source_id):
    """每个源用独立 session，失败不影响其他源"""
    db = SessionLocal()
    try:
        service = CrawlService(db)
        result = await service.fetch_source(source_id)
        return result
    except Exception as e:
        db.rollback()
        return {"status": "failed", "error": str(e)[:100]}
    finally:
        db.close()


async def main():
    # 先获取所有活跃源 ID 和名称
    db = SessionLocal()
    sources = db.query(Source).filter(Source.is_active == True).order_by(Source.name).all()
    source_list = [(str(s.id), s.name) for s in sources]
    db.close()

    print(f"共 {len(source_list)} 个活跃源，开始采集...\n")

    results = []
    for i, (source_id, name) in enumerate(source_list, 1):
        print(f"[{i}/{len(source_list)}] 采集: {name:30s} ...", end="", flush=True)
        start = time.time()

        result = await crawl_one(source_id)

        elapsed = time.time() - start
        status = result.get("status", "unknown") if isinstance(result, dict) else "unknown"
        found = result.get("found", 0) if isinstance(result, dict) else 0
        new = result.get("new", 0) if isinstance(result, dict) else 0
        error = result.get("error", "")[:60] if isinstance(result, dict) else ""

        if status == "completed":
            print(f" OK  {elapsed:.1f}s  found:{found} new:{new}")
        else:
            print(f" ERR {elapsed:.1f}s  {status} {error}")

        results.append({"name": name, "status": status, "found": found, "new": new, "error": error})

    # 汇总
    print("\n" + "=" * 60)
    print("采集汇总")
    print("=" * 60)
    success = sum(1 for r in results if r["status"] == "completed")
    failed = sum(1 for r in results if r["status"] != "completed")
    total_found = sum(r["found"] for r in results)
    total_new = sum(r["new"] for r in results)

    print(f"  成功: {success} / {len(results)} 个源")
    print(f"  失败: {failed} 个源")
    print(f"  总发现: {total_found} 条")
    print(f"  总入库: {total_new} 条")

    if failed:
        print(f"\n失败源:")
        for r in results:
            if r["status"] != "completed":
                print(f"  - {r['name']}: {r['error']}")

    print(f"\n成功源明细:")
    for r in results:
        if r["status"] == "completed":
            print(f"  - {r['name']:30s} found:{r['found']:2d} new:{r['new']:2d}")


asyncio.run(main())

