"""FastAPI Application Entry Point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import create_all
from app.core.logging import setup_logging
from app.core.middleware import RequestLoggingMiddleware
from app.core.response import success_response

# ── Routers ─────────────────────────────────────────────────
from app.routers import admin_auth, admins, articles, audit_logs, categories
from app.routers import dashboard, homepage, intelligence, operations, roles
from app.routers import search, sources, tags, timeline, tools, upload, crawler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown events."""
    setup_logging()

    # Import all models so create_all() can register them
    import app.models  # noqa: F401
    create_all()

    from app.services.scheduler import scheduler_service
    from app.core.database import SessionLocal
    scheduler_service.db = SessionLocal
    scheduler_service.start()

    yield

    scheduler_service.stop()


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
app.include_router(crawler.router)


# ── Root ────────────────────────────────────────────────────
@app.get("/")
async def root():
    return success_response({
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    })
