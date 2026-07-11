#!/bin/bash
# CNB部署重启脚本

echo "=== 停止旧服务 ==="
pkill -f uvicorn || echo "No uvicorn process"

echo "=== 拉取最新代码 ==="
cd /workspace
git pull

echo "=== 删除旧数据库 ==="
rm -f /workspace/ai-news-backend/ainews.db*

echo "=== 启动新服务 ==="
cd /workspace/ai-news-backend
export DATABASE_URL=sqlite:///./ainews.db
nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 7860 > /tmp/server.log 2>&1 &

echo "=== 等待服务启动 ==="
sleep 5

echo "=== 检查服务状态 ==="
curl -s http://localhost:7860/

echo ""
echo "=== 检查Categories ==="
curl -s http://localhost:7860/categories

echo ""
echo "=== 查看启动日志 ==="
cat /tmp/server.log | head -20

echo ""
echo "=== 完成 ==="