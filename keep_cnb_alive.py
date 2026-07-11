#!/usr/bin/env python3
"""
CNB 自动续期脚本
定时推送空提交到CNB仓库，触发重新构建，避免18小时过期。

用法:
    python keep_cnb_alive.py [--interval HOURS] [--repo NAME]

默认每12小时触发一次，留有6小时余量。
"""
import os
import sys
import time
import subprocess
import argparse
from datetime import datetime, timedelta
from pathlib import Path

REPO_PATH = Path(__file__).parent.resolve()
REPO_NAME = "cnb"
DEFAULT_INTERVAL_HOURS = 12

def run_git(args, cwd=None):
    """执行git命令并返回输出"""
    cmd = ["git", "-c", "http.proxy="] + args
    result = subprocess.run(
        cmd,
        cwd=str(cwd or REPO_PATH),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode, result.stdout + result.stderr

def check_remote(repo_name):
    """检查远程仓库是否配置"""
    code, out = run_git(["remote", "-v"])
    if code != 0:
        print(f"[ERROR] 获取远程仓库失败: {out}")
        return False
    if repo_name not in out:
        print(f"[ERROR] 未找到远程仓库 '{repo_name}'，请先配置: git remote add cnb <url>")
        print(f"当前远程仓库:\n{out}")
        return False
    return True

def trigger_rebuild(repo_name, reason="scheduled keep-alive"):
    """推送空提交触发重新构建"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"chore: {reason} - {timestamp}"

    print(f"[{timestamp}] 触发CNB重新构建...")
    print(f"  提交信息: {commit_msg}")

    # 创建空提交
    code, out = run_git(["commit", "--allow-empty", "-m", commit_msg])
    if code != 0:
        print(f"[WARN] 创建提交失败: {out}")
        return False

    # 推送到CNB
    code, out = run_git(["push", repo_name, "main"])
    if code != 0:
        print(f"[ERROR] 推送失败: {out}")
        return False

    print(f"[OK] 推送成功，CNB构建已触发")
    return True

def run_once(repo_name):
    """运行一次续期"""
    if not check_remote(repo_name):
        sys.exit(1)
    success = trigger_rebuild(repo_name)
    sys.exit(0 if success else 1)

def run_daemon(interval_hours, repo_name):
    """作为守护进程持续运行"""
    if not check_remote(repo_name):
        sys.exit(1)

    print(f"CNB 自动续期守护进程启动")
    print(f"  间隔: {interval_hours} 小时")
    print(f"  仓库: {repo_name}")
    print(f"  路径: {REPO_PATH}")
    print("-" * 50)

    while True:
        try:
            trigger_rebuild(repo_name)
        except Exception as e:
            print(f"[ERROR] 异常: {e}")

        next_run = datetime.now() + timedelta(hours=interval_hours)
        print(f"\n下次运行: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)

        sleep_seconds = interval_hours * 3600
        time.sleep(sleep_seconds)

def main():
    parser = argparse.ArgumentParser(description="CNB自动续期脚本")
    parser.add_argument(
        "--once",
        action="store_true",
        help="只运行一次，触发一次构建后退出",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=DEFAULT_INTERVAL_HOURS,
        help=f"续期间隔（小时），默认{DEFAULT_INTERVAL_HOURS}",
    )
    parser.add_argument(
        "--repo",
        default=REPO_NAME,
        help=f"远程仓库名称，默认{REPO_NAME}",
    )
    args = parser.parse_args()

    repo_name = args.repo

    if args.once:
        run_once(repo_name)
    else:
        run_daemon(args.interval, repo_name)

if __name__ == "__main__":
    main()