"""FastAPI Application Entry Point."""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import create_all
from app.core.logging import setup_logging
from app.core.middleware import RequestLoggingMiddleware
from app.core.middleware import SEORenderMiddleware
from app.core.response import success_response

from app.routers import admin_auth, admins, articles, audit_logs, categories
from app.routers import dashboard, homepage, intelligence, operations, roles
from app.routers import search, sources, tags, timeline, tools, upload, crawler
from app.routers import seo


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown events."""
    setup_logging()

    import app.models
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

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)  # 压缩 >1KB 的响应
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SEORenderMiddleware)

API_PREFIX = "/api/v1"

app.include_router(admin_auth.router, prefix=API_PREFIX)
app.include_router(admin_auth.compat_router, prefix=API_PREFIX)
app.include_router(admins.router, prefix=API_PREFIX)
app.include_router(admins.compat_router, prefix=API_PREFIX)
app.include_router(articles.router, prefix=API_PREFIX)
app.include_router(audit_logs.router, prefix=API_PREFIX)
app.include_router(categories.router, prefix=API_PREFIX)
app.include_router(crawler.router, prefix=API_PREFIX)
app.include_router(dashboard.router, prefix=API_PREFIX)
app.include_router(homepage.router, prefix=API_PREFIX)
app.include_router(intelligence.router, prefix=API_PREFIX)
app.include_router(operations.router, prefix=API_PREFIX)
app.include_router(roles.router, prefix=API_PREFIX)
app.include_router(search.router, prefix=API_PREFIX)
app.include_router(sources.router, prefix=API_PREFIX)
app.include_router(tags.router, prefix=API_PREFIX)
app.include_router(timeline.router, prefix=API_PREFIX)
app.include_router(tools.router, prefix=API_PREFIX)
app.include_router(upload.router, prefix=API_PREFIX)

# SEO endpoints (sitemap.xml / robots.txt) — no API prefix, served at root
app.include_router(seo.router)


@app.get(f"{API_PREFIX}/health")
async def health():
    return success_response({"status": "ok"})


FRONTEND_DIST = "/space/static/frontend"
ADMIN_DIST = "/space/static/admin"

if os.path.isdir(os.path.join(FRONTEND_DIST, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="frontend-assets")

if os.path.isdir(os.path.join(ADMIN_DIST, "assets")):
    app.mount("/admin/assets", StaticFiles(directory=os.path.join(ADMIN_DIST, "assets")), name="admin-assets")


@app.get("/")
async def frontend_index():
    index_path = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return success_response({
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "api_docs": "/docs",
    })


@app.get("/admin/{full_path:path}")
async def admin_spa(full_path: str):
    file_path = os.path.join(ADMIN_DIST, full_path)
    if full_path and os.path.isfile(file_path):
        return FileResponse(file_path)
    index_path = os.path.join(ADMIN_DIST, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return JSONResponse({"message": "Admin not built."}, status_code=404)


@app.get("/admin")
async def admin_root():
    index_path = os.path.join(ADMIN_DIST, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return JSONResponse({"message": "Admin not built."}, status_code=404)
