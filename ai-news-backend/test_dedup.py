from difflib import SequenceMatcher
from app.core.database import SessionLocal
from app.models.article import Article


def check_cross_source_dedup():
    db = SessionLocal()
    articles = db.query(Article).filter(
        Article.deleted_at.is_(None),
        Article.source_name.in_(['量子位', '36氪 AI', '机器之能'])
    ).all()

    print(f"检查 {len(articles)} 篇文章的跨源重复情况")
    pairs = []
    for i, a1 in enumerate(articles):
        for a2 in articles[i+1:]:
            if a1.source_name == a2.source_name:
                continue
            if not a1.title or not a2.title:
                continue
            ratio = SequenceMatcher(None, a1.title.lower(), a2.title.lower()).ratio()
            if ratio >= 0.85:
                pairs.append((ratio, a1.title, a1.source_name, a2.title, a2.source_name))

    pairs.sort(reverse=True)
    print(f"发现 {len(pairs)} 组跨源高相似标题 (>=0.85):")
    for ratio, t1, s1, t2, s2 in pairs[:10]:
        print(f"  相似度 {ratio:.2f}")
        print(f"    [{s1}] {t1[:60]}")
        print(f"    [{s2}] {t2[:60]}")

    db.close()


if __name__ == '__main__':
    check_cross_source_dedup()

