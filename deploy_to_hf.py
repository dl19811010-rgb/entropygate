"""Deploy the AI News backend to Hugging Face Space."""
import sys, os, shutil, stat, json, tempfile

HF_USER = os.getenv("HF_USER", "dl1010")
HF_TOKEN = os.getenv("HF_TOKEN", "")
SPACE_NAME = os.getenv("SPACE_NAME", "entropygate-api")
BACKEND_DIR = r"E:\aitoto\ai-news-backend"

# ---------------------------------------------------------------------------
# 1. Create the Space
# ---------------------------------------------------------------------------
print("[1/4] Creating HF Space...")
from huggingface_hub import HfApi
api = HfApi(token=HF_TOKEN)

try:
    space = api.create_repo(
        repo_id=f"{HF_USER}/{SPACE_NAME}",
        repo_type="space",
        space_sdk="gradio",
        exist_ok=True,
    )
    print(f"  Space URL: https://huggingface.co/spaces/{HF_USER}/{SPACE_NAME}")
except Exception as e:
    print(f"  Create failed (may already exist): {e}")

# ---------------------------------------------------------------------------
# 2. Set environment variables via Space settings
# ---------------------------------------------------------------------------
print("[2/4] Setting environment variables...")
import secrets
SECRET_KEY = secrets.token_hex(32)

# Use add_space_variable for non-secret env vars
env_vars = {
    "DATABASE_URL": "sqlite:///./ainews.db",
    "SECRET_KEY": SECRET_KEY,
    "CORS_ORIGINS": "*",
    "ENVIRONMENT": "production",
    "DEBUG": "false",
    "APP_NAME": "AI News Backend",
    "APP_VERSION": "1.0.0",
    "UPLOAD_DIR": "uploads",
    "AI_API_KEY": "",
    "AI_API_URL": "https://api.openai.com/v1",
    "AI_MODEL": "gpt-4",
    "CRAWL_INTERVAL_MINUTES": "30",
    "MAX_ARTICLES_PER_SOURCE": "20",
    "EDITORIAL_DEFAULT_THRESHOLD": "0.5",
    "REDIS_URL": "redis://localhost:6379/0",
    "CELERY_BROKER_URL": "redis://localhost:6379/0",
    "CELERY_RESULT_BACKEND": "redis://localhost:6379/0",
}

for key, value in env_vars.items():
    try:
        api.add_space_variable(
            repo_id=f"{HF_USER}/{SPACE_NAME}",
            key=key,
            value=value,
        )
    except Exception as e:
        print(f"  Warning setting {key}: {e}")

print(f"  Variables set. SECRET_KEY={SECRET_KEY[:16]}...")

# ---------------------------------------------------------------------------
# 3. Prepare files for upload
# ---------------------------------------------------------------------------
print("[3/4] Preparing files...")

STAGE_DIR = os.path.join(tempfile.gettempdir(), "hf_space_stage")
if os.path.exists(STAGE_DIR):
    shutil.rmtree(STAGE_DIR)
os.makedirs(STAGE_DIR)

# --- app.py (entry point) ---
app_py = '''"""
Entry point for Hugging Face Space 鈥?runs FastAPI on port 7860.
"""
import sys, os

# Ensure app package can be imported from the Space root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.core.database import create_all

# Create tables on startup (they'll persist within the same session)
create_all()

import uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=7860,
        reload=False,
        log_level="info",
    )
'''
with open(os.path.join(STAGE_DIR, "app.py"), "w", encoding="utf-8") as f:
    f.write(app_py)

# --- requirements.txt (trimmed: no celery, no redis) ---
req_lines = [
    "fastapi==0.111.0",
    "uvicorn[standard]==0.30.0",
    "sqlalchemy==2.0.30",
    "alembic==1.13.1",
    "pydantic==2.7.4",
    "pydantic-settings==2.3.4",
    "python-multipart==0.0.9",
    "python-dotenv==1.0.1",
    "httpx==0.27.0",
    "python-slugify==8.0.4",
    "feedparser==6.0.11",
    "beautifulsoup4==4.12.3",
    "lxml==5.2.2",
    "markdown==3.6",
    "passlib[bcrypt]==1.7.4",
    "bcrypt==4.1.3",
    "python-jose[cryptography]==3.3.0",
    "pymdown-extensions==10.21.3",
    "apscheduler==3.10.4",
]
with open(os.path.join(STAGE_DIR, "requirements.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(req_lines) + "\n")

# --- Copy app/ directory ---
src_app = os.path.join(BACKEND_DIR, "app")
dst_app = os.path.join(STAGE_DIR, "app")
shutil.copytree(
    src_app, dst_app,
    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
)
print(f"  Copied: app/ ({len(os.listdir(dst_app))} top-level entries)")

# --- Copy Alembic config if present ---
alembic_src = os.path.join(BACKEND_DIR, "alembic.ini")
if os.path.exists(alembic_src):
    shutil.copy2(alembic_src, STAGE_DIR)
    print("  Copied: alembic.ini")

# --- Copy alembic/ directory if present ---
alembic_dir_src = os.path.join(BACKEND_DIR, "alembic")
alembic_dir_dst = os.path.join(STAGE_DIR, "alembic")
if os.path.exists(alembic_dir_src):
    shutil.copytree(
        alembic_dir_src, alembic_dir_dst,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    print("  Copied: alembic/")

print(f"  Staging directory: {STAGE_DIR}")

# ---------------------------------------------------------------------------
# 4. Upload to HF Space
# ---------------------------------------------------------------------------
print("[4/4] Uploading to Hugging Face Space...")
api.upload_folder(
    repo_id=f"{HF_USER}/{SPACE_NAME}",
    folder_path=STAGE_DIR,
    repo_type="space",
    commit_message="Deploy FastAPI backend v1.0.0",
)
print("  Upload complete! Space is building...")
print(f"  Check: https://huggingface.co/spaces/{HF_USER}/{SPACE_NAME}")
print(f"  API endpoint will be: https://{HF_USER}-{SPACE_NAME}.hf.space")
print("\nDone! The Space will take 1-3 minutes to build on first deploy.")
