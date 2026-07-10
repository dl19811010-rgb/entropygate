"""
数据库备份脚本
用法:
  python backup.py                    # 立即备份
  python backup.py --list             # 列出所有备份
  python backup.py --restore <文件名>  # 恢复指定备份
  python backup.py --clean            # 清理过期备份
"""
import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timedelta

BACKUP_DIR = Path("backups")
DB_FILE = Path("ainews.db")
KEEP_DAYS = 30


def create_backup():
    BACKUP_DIR.mkdir(exist_ok=True)

    if not DB_FILE.exists():
        print(f"错误: 数据库文件 {DB_FILE} 不存在")
        return False

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"ainews_{timestamp}.db"

    shutil.copy2(DB_FILE, backup_file)
    print(f"备份成功: {backup_file}")
    print(f"文件大小: {backup_file.stat().st_size / 1024:.2f} KB")
    return True


def list_backups():
    if not BACKUP_DIR.exists():
        print("暂无备份")
        return

    backups = sorted(BACKUP_DIR.glob("ainews_*.db"), reverse=True)
    if not backups:
        print("暂无备份")
        return

    print(f"共 {len(backups)} 个备份:\n")
    for i, backup in enumerate(backups, 1):
        size_kb = backup.stat().st_size / 1024
        mtime = datetime.fromtimestamp(backup.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{i:2d}. {backup.name:40s}  {size_kb:>8.2f} KB  {mtime}")


def restore_backup(filename: str):
    backup_file = BACKUP_DIR / filename
    if not backup_file.exists():
        print(f"错误: 备份文件 {backup_file} 不存在")
        return False

    if DB_FILE.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safety_backup = BACKUP_DIR / f"ainews_before_restore_{timestamp}.db"
        shutil.copy2(DB_FILE, safety_backup)
        print(f"已创建安全备份: {safety_backup}")

    shutil.copy2(backup_file, DB_FILE)
    print(f"恢复成功: {backup_file} -> {DB_FILE}")
    return True


def clean_old_backups():
    if not BACKUP_DIR.exists():
        print("备份目录不存在")
        return

    cutoff = datetime.now() - timedelta(days=KEEP_DAYS)
    deleted = 0

    for backup in BACKUP_DIR.glob("ainews_*.db"):
        if "before_restore" in backup.name:
            continue
        mtime = datetime.fromtimestamp(backup.stat().st_mtime)
        if mtime < cutoff:
            backup.unlink()
            deleted += 1
            print(f"已删除过期备份: {backup.name}")

    print(f"\n清理完成，共删除 {deleted} 个过期备份")


def main():
    parser = argparse.ArgumentParser(description="数据库备份工具")
    parser.add_argument("--list", action="store_true", help="列出所有备份")
    parser.add_argument("--restore", type=str, help="恢复指定备份文件")
    parser.add_argument("--clean", action="store_true", help="清理过期备份")
    args = parser.parse_args()

    if args.list:
        list_backups()
    elif args.restore:
        restore_backup(args.restore)
    elif args.clean:
        clean_old_backups()
    else:
        create_backup()


if __name__ == "__main__":
    os.chdir(Path(__file__).resolve().parent)
    main()

