"""Deployment seed — runs on first boot to initialize DB with essential data."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, Base, engine
from app.models.article import Article
from app.models.source import Source
from app.models.category import Category
from app.models.admin import Admin
from app.utils.security import hash_password

def seed():
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Admin user
        if db.query(Admin).count() == 0:
            db.add(Admin(
                username="admin",
                password_hash=hash_password("admin123"),
                status="active",
                role="super_admin",
            ))
            print("[SEED] Admin user: admin / admin123")

        # Categories
        cats = {"ai-news": "AI 新闻", "models": "模型", "tools": "工具", "research": "研究"}
        for slug, name in cats.items():
            if not db.query(Category).filter(Category.slug == slug).first():
                db.add(Category(slug=slug, name=name))
        db.commit()
        print("[SEED] Categories created")

        # Minimal S-tier sources
        from app.models.source import Source as Src
        source_count = db.query(Src).count()
        print(f"[SEED] Existing sources: {source_count}")
        if source_count == 0:
            print("[SEED] No sources found. Run seed_editorial_tiers.py + add_chinese_sources.py locally then re-deploy.")

    finally:
        db.close()

if __name__ == "__main__":
    seed()
