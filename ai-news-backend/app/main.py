"""FastAPI Application Entry Point."""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.database import create_all, SessionLocal
from app.core.logging import setup_logging
from app.core.middleware import RequestLoggingMiddleware
from app.core.response import success_response
from app.utils.security import hash_password

# Import all models to ensure they are registered with SQLAlchemy metadata
from app.models import admin, article, audit, category, intelligence, source, tag, tool
from app.models.admin import Admin
from app.models.category import Category

# ── Routers ─────────────────────────────────────────────────
from app.routers import admin_auth, admins, articles, audit_logs, categories
from app.routers import dashboard, homepage, intelligence, operations, roles
from app.routers import search, sources, tags, timeline, tools, upload


def _seed_initial_data():
    """Seed essential data on first boot."""
    db = SessionLocal()
    try:
        if db.query(Admin).count() == 0:
            db.add(Admin(
                username="admin",
                password_hash=hash_password("admin123"),
                status="active",
                role="super_admin",
            ))
            print("[STARTUP] Admin user created: admin / admin123")

        cats = {"ai-news": "AI 新闻", "models": "模型", "tools": "工具", "research": "研究"}
        for slug, name in cats.items():
            if not db.query(Category).filter(Category.slug == slug).first():
                db.add(Category(slug=slug, name=name))
        db.commit()
        print("[STARTUP] Categories ensured")
    except Exception as e:
        print(f"[STARTUP] Seed warning: {e}")
        db.rollback()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown events."""
    setup_logging()
    create_all()
    _seed_initial_data()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# ── CORS ────────────────────────────────────────────────────
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request logging ─────────────────────────────────────────
app.add_middleware(RequestLoggingMiddleware)

# ── Include routers ─────────────────────────────────────────
app.include_router(admin_auth.router)
app.include_router(admins.router)
app.include_router(articles.router)
app.include_router(audit_logs.router)
app.include_router(categories.router)
app.include_router(dashboard.router)
app.include_router(homepage.router)
app.include_router(intelligence.router)
app.include_router(operations.router)
app.include_router(roles.router)
app.include_router(search.router)
app.include_router(sources.router)
app.include_router(tags.router)
app.include_router(timeline.router)
app.include_router(tools.router)
app.include_router(upload.router)


# ── Root ────────────────────────────────────────────────────
@app.get("/")
async def root():
    return success_response({
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    })


# ── Frontend Static Files ────────────────────────────────────
frontends_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ai-news-frontend", "dist")
if os.path.exists(frontends_dir):
    app.mount("/", StaticFiles(directory=frontends_dir, html=True), name="frontend")

    @app.get("/{full_path:path}")
    async def catch_all(full_path: str):
        index_path = os.path.join(frontends_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
