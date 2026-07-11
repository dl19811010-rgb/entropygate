import asyncio
from app.core.database import SessionLocal
from app.models.source import Source
from app.services.crawl_service import CrawlService
import uuid


def test_empty_rss():
    """模拟 RSS 返回 0 条，应 completed 且不报错"""
    db = SessionLocal()
    source = Source(
        id=str(uuid.uuid4()),
        name='空内容测试源',
        url='https://example.com/empty',
        type='webhook',
        parser_type='webhook',
        is_active=True,
        dedup_strategy='url',
        ai_preprocess=False,
        auto_publish=False,
        config={'payload': []}
    )
    db.add(source)
    db.commit()

    service = CrawlService(db)
    result = asyncio.run(service.fetch_source(source.id))
    log = source.logs[-1]
    print(f"空内容测试: {result} | 日志: {log.status} found={log.items_found}")

    db.delete(source)
    db.commit()
    db.close()
    return result


def test_chinese_encoding():
    """检查数据库中中文标题无乱码"""
    db = SessionLocal()
    articles = db.query(Source).filter(Source.name.in_(['量子位', '36氪 AI'])).all()
    print(f"源数量: {len(articles)}")
    for s in articles:
        print(f"  {s.name}")
    # 检查最近 5 篇文章标题
    from app.models.article import Article
    recent = db.query(Article).filter(
        Article.deleted_at.is_(None),
        Article.source_name.in_(['量子位', '36氪 AI'])
    ).order_by(Article.created_at.desc()).limit(5).all()
    print("\n最近中文文章标题:")
    for a in recent:
        print(f"  {a.title}")
    db.close()
    return recent


if __name__ == '__main__':
    print("=== 空内容测试 ===")
    test_empty_rss()
    print("\n=== 中文编码测试 ===")
    test_chinese_encoding()

