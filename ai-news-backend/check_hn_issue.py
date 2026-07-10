from app.core.database import SessionLocal
from app.models.article import Article
from app.models.source import Source

db = SessionLocal()

hn_source = db.query(Source).filter(Source.name == "Hacker News AI").first()
print(f"Hacker News Source: {hn_source.id}")
print(f"auto_publish: {hn_source.auto_publish}")
print(f"ai_preprocess: {hn_source.ai_preprocess}")
print(f"category_id: {hn_source.category_id}")
print(f"config: {hn_source.config}")

print("\n=== 通过 source_name 查找 ===")
articles_by_name = db.query(Article).filter(Article.source_name == "Hacker News AI", Article.deleted_at.is_(None)).all()
print(f"按 source_name='Hacker News AI' 找到: {len(articles_by_name)} 篇")

print("\n=== 通过 category_id 查找 ===")
articles_by_cat = db.query(Article).filter(Article.category_id == hn_source.category_id, Article.deleted_at.is_(None)).all()
print(f"按 category_id 找到: {len(articles_by_cat)} 篇")

print("\n=== 查找包含 'Hacker' 的文章 ===")
articles_like = db.query(Article).filter(Article.source_name.like("%Hacker%"), Article.deleted_at.is_(None)).all()
for a in articles_like:
    print(f"  {a.source_name} | {a.title[:50]}")

print("\n=== 查找所有包含 'draft' 的草稿 ===")
drafts = db.query(Article).filter(Article.status == "draft", Article.deleted_at.is_(None)).order_by(Article.created_at.desc()).limit(5).all()
for a in drafts:
    print(f"  {a.created_at.strftime('%m-%d %H:%M')} | {a.source_name[:20]:20} | {a.title[:40]}")

db.close()

