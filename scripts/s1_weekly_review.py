#!/usr/bin/env python3
"""
S1 Stabilization — Weekly Review

生成每周总结：S1-W1.md, S1-W2.md

用法：
    python scripts/s1_weekly_review.py
"""

import os
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
BACKEND_ROOT = PROJECT_ROOT / "ai-news-backend"
S1_DIR = PROJECT_ROOT / "evidence" / "operations" / "S1"
DAILY_DIR = S1_DIR / "daily"


def get_week_number():
    """Get current week number (W1, W2)."""
    start_date = datetime(2026, 7, 8)
    today = datetime.utcnow()
    days_diff = (today - start_date).days
    week = (days_diff // 7) + 1
    return f"W{week}"


def collect_daily_observations():
    """Collect all daily observations for this week."""
    if not DAILY_DIR.exists():
        return []

    observations = []
    for f in sorted(DAILY_DIR.glob("*.md")):
        with open(f, encoding="utf-8") as fp:
            content = fp.read()
            observations.append({
                "date": f.stem,
                "content": content,
            })
    return observations


def collect_backlog_items():
    """Collect backlog items from product_backlog.md."""
    backlog = []
    backlog_path = S1_DIR / "product_backlog.md"
    if backlog_path.exists():
        with open(backlog_path, encoding="utf-8") as f:
            for line in f:
                if "- [ ]" in line:
                    backlog.append(line.strip())
    return backlog


def collect_source_health():
    """Collect source health from registry."""
    registry = BACKEND_ROOT / "evidence" / "operations" / "source_registry.yaml"
    if not registry.exists():
        return {"total": 0, "enabled": 0}

    with open(registry, encoding="utf-8") as f:
        reg = yaml.safe_load(f)

    sources = reg.get("sources", [])
    return {
        "total": len(sources),
        "enabled": sum(1 for s in sources if s.get("enabled")),
    }


def collect_scheduler_status():
    """Collect scheduler status."""
    state_file = BACKEND_ROOT / "evidence" / "operations" / "scheduler_state.json"
    if not state_file.exists():
        return {"running": False, "jobs_count": 0}

    try:
        with open(state_file, encoding="utf-8") as f:
            state = json.load(f)
        return {
            "running": state.get("running", False),
            "jobs_count": len(state.get("jobs", {})),
        }
    except Exception:
        return {"running": False, "jobs_count": 0}


def count_daily_reports():
    """Count daily reports."""
    report_dir = BACKEND_ROOT / "evidence" / "operations" / "daily"
    if not report_dir.exists():
        return 0
    return len([f for f in os.listdir(report_dir) if f.endswith(".json")])


def count_entity_snapshots():
    """Count entity snapshots."""
    snapshot_dir = BACKEND_ROOT / "evidence" / "snapshots"
    if not snapshot_dir.exists():
        return 0
    return len([f for f in os.listdir(snapshot_dir) if f.endswith(".json")])


def generate_weekly_review():
    """Generate weekly review."""
    week = get_week_number()
    today = datetime.utcnow().strftime("%Y-%m-%d")

    observations = collect_daily_observations()
    backlog_items = collect_backlog_items()
    source_health = collect_source_health()
    scheduler = collect_scheduler_status()
    daily_reports = count_daily_reports()
    entity_snapshots = count_entity_snapshots()

    # Categorize backlog
    categories = {
        "content": [],
        "ui": [],
        "performance": [],
        "crawler": [],
        "runtime": [],
        "ranking": [],
        "editorial": [],
        "idea": [],
    }
    for item in backlog_items:
        for cat in categories.keys():
            if f"[{cat}]" in item.lower():
                categories[cat].append(item)
                break

    # Top 5 issues by count
    cat_counts = [(k, len(v)) for k, v in categories.items() if v]
    cat_counts.sort(key=lambda x: x[1], reverse=True)
    top_5 = cat_counts[:5]

    # Generate Markdown
    md = f"""# S1 Weekly Review — {week}

**生成日期**: {today}

---

## 📊 本周概览

| Metric | Value |
|--------|-------|
| Days Observed | {len(observations)} |
| Sources | {source_health['enabled']}/{source_health['total']} |
| Scheduler | {'✅ Running' if scheduler['running'] else '❌ Stopped'} |
| Entity Snapshots | {entity_snapshots} |
| Daily Reports | {daily_reports} |

---

## 📝 本周发现

### Content
*（手动填写）*

- _

### Crawler
*（手动填写）*

- _

### Search
*（手动填写）*

- _

### Homepage
*（手动填写）*

- _

---

## 📋 Backlog 新增

### content
{chr(10).join(categories['content']) if categories['content'] else '- 无'}

### ui
{chr(10).join(categories['ui']) if categories['ui'] else '- 无'}

### performance
{chr(10).join(categories['performance']) if categories['performance'] else '- 无'}

### crawler
{chr(10).join(categories['crawler']) if categories['crawler'] else '- 无'}

### runtime
{chr(10).join(categories['runtime']) if categories['runtime'] else '- 无'}

### ranking
{chr(10).join(categories['ranking']) if categories['ranking'] else '- 无'}

### editorial
{chr(10).join(categories['editorial']) if categories['editorial'] else '- 无'}

### idea
{chr(10).join(categories['idea']) if categories['idea'] else '- 无'}

---

## 🔝 Top 5 Issues

{chr(10).join([f"{i+1}. {cat}: {count} items" for i, (cat, count) in enumerate(top_5)]) if top_5 else "- 暂无"}

---

## ✨ Top 5 Improvements

*（手动填写）*

- _

---

## 🎯 Decisions

*（本周重要决策，全部进入 Backlog）*

- _

---

## 🔧 Runtime 修改

0

## 🔧 Platform 修改

0

---

*Auto-generated at {datetime.utcnow().isoformat()}*
"""

    output_path = S1_DIR / f"S1-{week}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"✅ Weekly Review saved: {output_path}")
    print(f"   Week: {week}")
    print(f"   Daily observations: {len(observations)}")
    print(f"   Backlog items: {len(backlog_items)}")
    print(f"   Scheduler: {'running' if scheduler['running'] else 'stopped'}")

    return output_path


if __name__ == "__main__":
    generate_weekly_review()
