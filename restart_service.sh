#!/bin/bash
# CNB部署重启脚本

echo "=== 停止旧服务 ==="
pkill -f uvicorn || echo "No uvicorn process"
pkill -f gunicorn || echo "No gunicorn process"

echo "=== 拉取最新代码 ==="
cd /workspace
git pull

echo "=== 启动新服务 ==="
cd /workspace/ai-news-backend
export DATABASE_URL=${DATABASE_URL:-"sqlite:///./ainews.db"}
export SECRET_KEY=${SECRET_KEY:-"f3a9c7e2-8b4d-4e1a-9f6c-2d5a8e3b7c1e-cnb"}
export CORS_ORIGINS=${CORS_ORIGINS:-"*"}
export ENVIRONMENT=${ENVIRONMENT:-"production"}
nohup gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:7860 --access-logfile - --error-logfile - > /tmp/server.log 2>&1 &

echo "=== 等待服务启动 ==="
sleep 5

echo "=== 检查服务状态 ==="
curl -s http://localhost:7860/api/v1/homepage/health

echo ""
echo "=== 检查 Categories ==="
curl -s http://localhost:7860/api/v1/categories

echo ""
echo "=== 查看启动日志 ==="
cat /tmp/server.log | head -20

echo ""
echo "=== 完成 ==="