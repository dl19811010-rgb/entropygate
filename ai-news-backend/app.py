"""
Entry point for CNB deployment — runs FastAPI with frontend static files.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DATABASE_URL", "sqlite:////data/ainews.db")
os.environ.setdefault("SECRET_KEY", "f3a9c7e2-8b4d-4e1a-9f6c-2d5a8e3b7c1e-cnb")
os.environ.setdefault("CORS_ORIGINS", "*")
os.environ.setdefault("ENVIRONMENT", "production")

from app.core.config import settings
from app.core.database import create_all

create_all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=7860,
        reload=False,
        log_level="info",
    )