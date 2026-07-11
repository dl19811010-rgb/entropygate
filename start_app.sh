#!/bin/bash
set -e

echo "=== Starting AI News Application ==="
echo "Time: $(date)"
echo "Working directory: $(pwd)"

# Set environment variables if not already set
export DATABASE_URL=${DATABASE_URL:-"sqlite:////data/ainews.db"}
export SECRET_KEY=${SECRET_KEY:-"f3a9c7e2-8b4d-4e1a-9f6c-2d5a8e3b7c1e-cnb"}
export CORS_ORIGINS=${CORS_ORIGINS:-"*"}
export ENVIRONMENT=${ENVIRONMENT:-"production"}

echo "DATABASE_URL: $DATABASE_URL"
echo "ENVIRONMENT: $ENVIRONMENT"

# Ensure /data directory exists
mkdir -p /data

# Navigate to backend directory
cd /workspace/ai-news-backend

echo "Installing dependencies..."
pip install --no-cache-dir -r requirements.txt 2>&1 | tail -5
pip install --no-cache-dir apscheduler uvicorn gunicorn 2>&1 | tail -5

echo "Initializing database..."
python seed_complete.py 2>&1 || python seed_deploy.py 2>&1 || echo "Database init completed (or already initialized)"

echo "Testing application import..."
python -c "from app.main import app; print('Import successful')" 2>&1

echo "Starting application on port 7860..."
echo "Access URL will be available at the forwarded port"

# Start gunicorn in background and keep heartbeat output for CNB
nohup gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:7860 --access-logfile - --error-logfile - >/tmp/gunicorn.log 2>&1 &
GUNICORN_PID=$!
echo "Gunicorn started with PID $GUNICORN_PID"
sleep 5

while kill -0 $GUNICORN_PID 2>/dev/null; do
  sleep 30
  echo "$(date '+%Y-%m-%d %H:%M:%S') - heartbeat - gunicorn running on port 7860"
  curl -s -o /dev/null -w "%{http_code}" http://localhost:7860/api/v1/health || true
done
