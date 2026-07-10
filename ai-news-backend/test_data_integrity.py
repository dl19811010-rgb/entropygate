from app.core.database import SessionLocal
from app.models.article import Article
from sqlalchemy import func
from collections import Counter


def check_data_integrity():
    db = SessionLocal()
    articles = db.query(Article).filter(Article.deleted_at.is_(None)).all()

    required_empty = [a.id for a in articles if not a.title or not a.slug or not a.source_url or not a.source_name or not a.status]
    cat_null = [a.id for a in articles if not a.category_id]
    slug_counts = Counter([a.slug for a in articles if a.slug])
    dups = {k: v for k, v in slug_counts.items() if v > 1}

    status_counts = db.query(Article.status, func.count(Article.id)).filter(
        Article.deleted_at.is_(None)
    ).group_by(Article.status).all()

    print(f"总文章数: {len(articles)}")
    print(f"必填字段缺失: {len(required_empty)}")
    print(f"分类缺失: {len(cat_null)}")
    print(f"slug 重复组数: {len(dups)}")
    print(f"状态分布: {status_counts}")

    # 时间戳抽查
    print("\n时间戳抽查（最近 5 篇）:")
    recent = db.query(Article).filter(Article.deleted_at.is_(None)).order_by(Article.created_at.desc()).limit(5).all()
    for a in recent:
        print(f"  {a.title[:40]} | pub={a.published_at} | create={a.created_at}")

    db.close()
    return {
        'total': len(articles),
        'required_empty': len(required_empty),
        'cat_null': len(cat_null),
        'slug_dups': len(dups),
        'status_counts': status_counts
    }


if __name__ == '__main__':
    check_data_integrity()

