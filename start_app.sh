#!/bin/bash
set -e

echo "============================================"
echo "=== AI News Platform Starting ==="
echo "============================================"
echo "Time: $(date)"
echo "Working directory: $(pwd)"

export DATABASE_URL=${DATABASE_URL:-"sqlite:////data/ainews.db"}
export SECRET_KEY=${SECRET_KEY:-"f3a9c7e2-8b4d-4e1a-9f6c-2d5a8e3b7c1e-cnb"}
export CORS_ORIGINS=${CORS_ORIGINS:-"*"}
export ENVIRONMENT=${ENVIRONMENT:-"production"}

echo "DATABASE_URL: $DATABASE_URL"
echo "ENVIRONMENT: $ENVIRONMENT"

mkdir -p /data
cd /workspace/ai-news-backend

echo ""
echo "--- Checking frontend builds ---"
if [ -f "/workspace/ai-news-frontend/dist/index.html" ]; then
  echo "[OK] Frontend dist exists"
else
  echo "[WARN] Frontend dist not found, API-only mode"
fi
if [ -f "/workspace/ai-news-admin/dist/index.html" ]; then
  echo "[OK] Admin dist exists"
else
  echo "[WARN] Admin dist not found"
fi

echo ""
echo "--- Installing Python dependencies ---"
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi
venv/bin/pip install --no-cache-dir -r requirements.txt 2>&1 | tail -3
venv/bin/pip install --no-cache-dir apscheduler uvicorn gunicorn 2>&1 | tail -3
echo "[OK] Dependencies installed"

echo ""
echo "--- Verifying application ---"
venv/bin/python -c "from app.main import app; print('[OK] Application import successful')" 2>&1

echo ""
echo "--- Starting server on port 7860 ---"
nohup venv/bin/gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app \
  --bind 0.0.0.0:7860 \
  --access-logfile - \
  --error-logfile - \
  --timeout 120 \
  >/tmp/gunicorn.log 2>&1 &
GUNICORN_PID=$!
echo "Gunicorn PID: $GUNICORN_PID"

sleep 8
if kill -0 $GUNICORN_PID 2>/dev/null; then
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:7860/ || echo "000")
  echo "[OK] Server started, health check: $STATUS"
  echo ""
  echo "============================================"
  echo "  Platform is running!"
  echo "  - Frontend: /"
  echo "  - Admin:    /admin/"
  echo "  - API:      /api/v1/"
  echo "============================================"
else
  echo "[ERROR] Server failed to start"
  cat /tmp/gunicorn.log
  exit 1
fi

while kill -0 $GUNICORN_PID 2>/dev/null; do
  sleep 60
  echo "[$(date '+%H:%M:%S')] heartbeat - OK"
done

echo "[WARN] Server process exited"
exit 1
