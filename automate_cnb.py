#!/usr/bin/env python3
"""
使用Playwright自动化操作CNB WebIDE终端
"""
import time
import subprocess
import sys

def check_playwright():
    try:
        from playwright.sync_api import sync_playwright
        return True
    except ImportError:
        return False

def install_playwright():
    print("正在安装Playwright...")
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)

def automate_cnb_terminal():
    from playwright.sync_api import sync_playwright
    
    commands = [
        "pkill -f uvicorn || true",
        "cd /workspace && git pull",
        "rm -f /workspace/ai-news-backend/ainews.db*",
        "cd /workspace/ai-news-backend && DATABASE_URL=sqlite:///./ainews.db nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 7860 > /tmp/server.log 2>&1 &",
        "sleep 3 && curl -s http://localhost:7860/categories"
    ]
    
    print("正在启动浏览器...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        print("正在访问WebIDE...")
        page.goto("https://cnb-gcf-1jt888jcc-001.cnb.space/?folder=%2Fworkspace")
        
        print("等待页面加载...")
        time.sleep(10)
        
        # 尝试找到终端或创建新终端
        try:
            terminal = page.query_selector(".terminal.xterm")
            if not terminal:
                print("点击New Terminal按钮...")
                new_term_btn = page.query_selector("button:has-text('New Terminal')")
                if new_term_btn:
                    new_term_btn.click()
                    time.sleep(5)
        except Exception as e:
            print(f"查找终端时出错: {e}")
        
        # 发送命令到终端
        for cmd in commands:
            print(f"执行: {cmd}")
            page.keyboard.type(cmd)
            page.keyboard.press("Enter")
            time.sleep(3)
        
        print("\n命令执行完成！")
        print("请检查浏览器窗口查看结果...")
        input("按Enter键关闭浏览器...")
        
        browser.close()

if __name__ == "__main__":
    if not check_playwright():
        install_playwright()
    
    automate_cnb_terminal()