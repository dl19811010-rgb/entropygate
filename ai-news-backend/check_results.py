"""检查采集结果质量"""
import sys
sys.path.append('.')
from app.core.database import SessionLocal
from app.models.article import Article
from app.models.tag import Tag
from collections import Counter

db = SessionLocal()

# 基本统计
total = db.query(Article).count()
published = db.query(Article).filter(Article.status == "published").count()
draft = db.query(Article).filter(Article.status == "draft").count()
featured = db.query(Article).filter(Article.is_featured == True).count()
has_ai_summary = db.query(Article).filter(Article.ai_summary.isnot(None)).count()
has_quality = db.query(Article).filter(Article.quality_score > 0).count()

print("=== 采集结果统计 ===")
print(f"  总文章数: {total}")
print(f"  已发布: {published}")
print(f"  草稿: {draft}")
print(f"  精选: {featured}")
print(f"  有AI摘要: {has_ai_summary}")
print(f"  有质量分: {has_quality}")

# 按源统计
print("\n=== 按源统计 ===")
arts = db.query(Article).all()
src_count = Counter(a.source_name for a in arts)
for src, cnt in sorted(src_count.items(), key=lambda x: -x[1]):
    print(f"  {src:30s} {cnt:3d} 篇")

# 质量分分布
print("\n=== 质量分分布 ===")
score_ranges = [(90, 100, "优秀"), (75, 89, "良好"), (60, 74, "一般"), (40, 59, "较差"), (0, 39, "很低")]
for lo, hi, label in score_ranges:
    cnt = db.query(Article).filter(Article.quality_score >= lo, Article.quality_score <= hi).count()
    bar = "#" * (cnt // 2)
    print(f"  {label}({lo}-{hi}): {cnt:3d} {bar}")

# 相关性分布
print("\n=== 相关性分布 ===")
for lo, hi, label in score_ranges:
    cnt = db.query(Article).filter(Article.relevance_score >= lo, Article.relevance_score <= hi).count()
    bar = "#" * (cnt // 2)
    print(f"  {label}({lo}-{hi}): {cnt:3d} {bar}")

# 标签统计
print("\n=== 热门标签 Top 15 ===")
tags = db.query(Tag).all()
tag_counts = []
for tag in tags:
    cnt = len(tag.articles)
    tag_counts.append((tag.name, cnt))
tag_counts.sort(key=lambda x: -x[1])
for name, cnt in tag_counts[:15]:
    print(f"  {name:20s} {cnt:3d} 次")

# 抽样检查高分文章
print("\n=== 高质量文章 Top 5 ===")
top = db.query(Article).order_by(Article.quality_score.desc()).limit(5).all()
for a in top:
    print(f"  [{a.source_name}] 质量:{a.quality_score} 相关:{a.relevance_score} 精选:{a.is_featured}")
    print(f"    标题: {a.title[:70]}")
    ai_sum = (a.ai_summary or "无")[:60]
    print(f"    AI摘要: {ai_sum}")
    tag_names = [t.name for t in a.tags]
    print(f"    标签: {tag_names}")
    print()

# 抽样检查低质量文章
print("=== 低质量文章 Bottom 5 ===")
low = db.query(Article).filter(Article.quality_score > 0).order_by(Article.quality_score.asc()).limit(5).all()
for a in low:
    print(f"  [{a.source_name}] 质量:{a.quality_score} 相关:{a.relevance_score}")
    print(f"    标题: {a.title[:70]}")
    print()

# 检查无AI摘要的文章
no_summary = db.query(Article).filter(Article.ai_summary.is_(None)).count()
no_content = db.query(Article).filter(Article.content.is_(None)).count()
print(f"=== 数据完整性 ===")
print(f"  无AI摘要: {no_summary} 篇")
print(f"  无正文内容: {no_content} 篇")

db.close()

