#!/bin/bash
set -e

echo "=== Starting AI News Application ==="
echo "Time: $(date)"

cd ai-news-backend

echo "Installing dependencies..."
pip install --no-cache-dir -r requirements.txt
pip install --no-cache-dir apscheduler uvicorn gunicorn

echo "Initializing database..."
python seed_deploy.py || echo "Database initialization completed or skipped"

echo "Starting application on port 7860..."
exec gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:7860
