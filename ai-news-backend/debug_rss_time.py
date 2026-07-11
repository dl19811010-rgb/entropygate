"""调试 rss2json 返回的时间格式"""
import asyncio
import httpx
from email.utils import parsedate_to_datetime
import json

async def test():
    # 直接用 rss2json 拉 TechCrunch AI
    rss_url = "https://techcrunch.com/category/artificial-intelligence/feed/"
    proxy_url = f"https://api.rss2json.com/v1/api.json?rss_url={rss_url}"

    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient(timeout=15, follow_redirects=True, headers=headers) as c:
        r = await c.get(proxy_url)
        data = r.json()
        print(f"状态: {data.get('status')}")
        items = data.get("items", [])
        print(f"条目数: {len(items)}")

        for i, item in enumerate(items[:5]):
            pub_str = item.get("pubDate", "")
            print(f"\n{i+1}. {item.get('title','')[:60]}")
            print(f"   pubDate: {pub_str}")
            try:
                dt = parsedate_to_datetime(pub_str)
                print(f"   解析为: {dt}")
                print(f"   timetuple: {dt.timetuple()[:6]}")
            except Exception as e:
                print(f"   解析失败: {e}")

asyncio.run(test())

