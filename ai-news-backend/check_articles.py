from app.core.database import SessionLocal
from app.models.article import Article
from app.models.source import Source, CrawlLog

db = SessionLocal()

print("=== 文章统计 ===")
total = db.query(Article).filter(Article.deleted_at.is_(None)).count()
published = db.query(Article).filter(Article.deleted_at.is_(None), Article.status == "published").count()
draft = db.query(Article).filter(Article.deleted_at.is_(None), Article.status == "draft").count()
print(f"总文章数: {total}")
print(f"已发布: {published}")
print(f"草稿: {draft}")

print("\n=== 各源文章数 ===")
sources = db.query(Source).filter(Source.deleted_at.is_(None)).all()
for s in sources:
    count = db.query(Article).filter(Article.source_name == s.name, Article.deleted_at.is_(None)).count()
    print(f"{s.name:30} | {count} 篇文章")

print("\n=== 最近10篇文章 ===")
articles = db.query(Article).filter(Article.deleted_at.is_(None)).order_by(Article.created_at.desc()).limit(10).all()
for a in articles:
    ai_summary = "有" if a.ai_summary else "无"
    tags = len(a.tags) if a.tags else 0
    print(f"{a.created_at.strftime('%m-%d %H:%M')} | {a.source_name[:15]:15} | {a.title[:40]:40} | AI摘要:{ai_summary} | 标签:{tags} | {a.status}")

db.close()

