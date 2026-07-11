#!/usr/bin/env python3
"""
通过API直接初始化数据库数据
"""
import requests
import json

BASE_URL = "https://c3g3198mkw-7860.cnb.run"

def init_data():
    print("正在检查当前状态...")
    
    # 检查categories
    resp = requests.get(f"{BASE_URL}/categories")
    categories = resp.json()
    print(f"当前categories: {categories}")
    
    if categories.get("data"):
        print("数据已存在，无需初始化")
        return
    
    print("数据为空，需要通过WebIDE终端执行初始化")
    print("\n请在WebIDE终端中执行以下命令：")
    print("-" * 50)
    print("""
cd /workspace && git pull
cd /workspace/ai-news-backend
rm -f ainews.db*
python3 -c "
from app.core.database import SessionLocal
from app.models.admin import Admin
from app.models.category import Category
from app.utils.security import hash_password

db = SessionLocal()
try:
    if db.query(Admin).count() == 0:
        db.add(Admin(username='admin', password_hash=hash_password('admin123'), status='active', role='super_admin'))
        print('Admin created')
    cats = {'ai-news': 'AI 新闻', 'models': '模型', 'tools': '工具', 'research': '研究'}
    for slug, name in cats.items():
        if not db.query(Category).filter(Category.slug == slug).first():
            db.add(Category(slug=slug, name=name))
    db.commit()
    print('Categories created')
except Exception as e:
    print(f'Error: {e}')
    db.rollback()
finally:
    db.close()
"
DATABASE_URL=sqlite:///./ainews.db nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 7860 > /tmp/server.log 2>&1 &
""")
    print("-" * 50)

if __name__ == "__main__":
    init_data()