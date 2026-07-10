"""测试全文抓取和时效性过滤 - 用TechCrunch测试"""
import sys
import asyncio
sys.path.append('.')
from app.core.database import SessionLocal
from app.models.source import Source
from app.crawler.factory import get_fetcher


async def test():
    db = SessionLocal()

    # 测试 TechCrunch AI
    source = db.query(Source).filter(Source.name == "TechCrunch AI").first()
    if not source:
        print("未找到测试源")
        return

    config = dict(source.config or {})
    config["name"] = source.name
    config["max_items"] = 3
    config["max_age_days"] = 30  # 放宽到30天测试
    config["fetch_fulltext"] = True

    fetcher = get_fetcher(source.parser_type, config)
    items = await fetcher.fetch()

    print(f"采集到 {len(items)} 条（最近30天）\n")

    for i, item in enumerate(items):
        print(f"--- {i+1}. {item.title[:70]} ---")
        print(f"  来源: {item.source_name}")
        print(f"  发布时间: {item.published_at}")
        print(f"  摘要长度: {len(item.summary or '')}")

        full_text = (item.extra or {}).get("full_text", "")
        print(f"  全文长度: {len(full_text)} 字")
        if full_text:
            print(f"  全文前300字:\n    {full_text[:300].replace(chr(10), chr(10)+'    ')}")

        print(f"  图片数: {len(item.images)}")
        for j, img in enumerate(item.images[:3]):
            print(f"    图{j+1}: {img[:90]}")
        print()

    db.close()


asyncio.run(test())

