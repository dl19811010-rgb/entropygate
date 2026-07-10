#!/usr/bin/env python3
"""
S1 Stabilization — Baseline Generator

生成 BASELINE-2026-Q3.md，记录产品第一次稳定运行时的真实状态。

用法：
    python scripts/s1_baseline.py
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


def collect_content_metrics():
    """Collect content metrics."""
    return {
        "daily_signals": 0,
        "daily_facts": 0,
        "daily_events": 0,
        "headline_count": 0,
        "entity_count": count_entity_snapshots(),
    }


def collect_quality_metrics():
    """Collect quality metrics."""
    return {
        "fact_precision": 0,
        "review_queue": 0,
        "duplicate_rate": 0,
        "source_success_rate": 0,
    }


def collect_runtime_metrics():
    """Collect runtime metrics."""
    return {
        "replay_status": "N/A",
        "conformance": "N/A",
        "compatibility": "N/A",
        "spec_age": "N/A",
    }


def collect_operations_metrics():
    """Collect operations metrics."""
    return {
        "pipeline_time": 0,
        "snapshot_age_hours": 0,
        "crawler_success": 0,
        "failure_count": 0,
    }


def collect_product_metrics():
    """Collect product metrics."""
    return {
        "search_queries": 0,
        "entity_views": 0,
        "feed_refreshes": 0,
    }


def count_entity_snapshots():
    """Count entity snapshots."""
    snapshot_dir = BACKEND_ROOT / "evidence" / "snapshots"
    if not snapshot_dir.exists():
        return 0
    return len([f for f in os.listdir(snapshot_dir) if f.endswith(".json")])


def collect_daily_summary():
    """Collect summary from daily observations."""
    summary = {
        "days_counted": 0,
        "avg_feed_age_hours": 0,
        "max_feed_age_hours": 0,
        "min_feed_age_hours": float("inf"),
    }

    if not DAILY_DIR.exists():
        return summary

    feed_ages = []
    for f in sorted(DAILY_DIR.glob("*.md")):
        with open(f, encoding="utf-8") as fp:
            content = fp.read()
            if "Feed Age" in content:
                lines = content.split("\n")
                for line in lines:
                    if "Feed Age" in line:
                        parts = line.split("|")
                        if len(parts) >= 3:
                            age_str = parts[2].strip()
                            if age_str != "N/A":
                                try:
                                    feed_ages.append(float(age_str))
                                except ValueError:
                                    pass

    if feed_ages:
        summary["days_counted"] = len(feed_ages)
        summary["avg_feed_age_hours"] = round(sum(feed_ages) / len(feed_ages), 1)
        summary["max_feed_age_hours"] = max(feed_ages)
        summary["min_feed_age_hours"] = min(feed_ages)

    return summary


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


def generate_baseline():
    """Generate the baseline report."""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    quarter = "Q3"
    year = "2026"

    content = collect_content_metrics()
    quality = collect_quality_metrics()
    runtime = collect_runtime_metrics()
    operations = collect_operations_metrics()
    product = collect_product_metrics()
    daily_summary = collect_daily_summary()
    source_health = collect_source_health()

    md = f"""# BASELINE-{year}-{quarter}

> 产品第一次稳定运行时的真实状态。
> 所有未来改进都与此基线对比。

**生成日期**: {today}  
**周期**: S1 Stabilization  
**天数**: {daily_summary['days_counted']}

---

## 📊 内容指标（Content）

| Metric | Value |
|--------|-------|
| Daily Signals | {content['daily_signals']} |
| Daily Facts | {content['daily_facts']} |
| Daily Events | {content['daily_events']} |
| Headline Count | {content['headline_count']} |
| Entity Count | {content['entity_count']} |

---

## ✅ 质量指标（Quality）

| Metric | Value |
|--------|-------|
| Fact Precision | {quality['fact_precision']}% |
| Review Queue | {quality['review_queue']} |
| Duplicate Rate | {quality['duplicate_rate']}% |
| Source Success Rate | {quality['source_success_rate']}% |

---

## 🔧 Runtime 指标

| Metric | Value |
|--------|-------|
| Replay | {runtime['replay_status']} |
| Conformance | {runtime['conformance']} |
| Compatibility | {runtime['compatibility']} |
| Spec Age | {runtime['spec_age']} |

---

## ⚙️ 运营指标（Operations）

| Metric | Value |
|--------|-------|
| Average Pipeline Time | {operations['pipeline_time']}s |
| Average Snapshot Age | {daily_summary['avg_feed_age_hours'] or 'N/A'} hours |
| Max Snapshot Age | {daily_summary['max_feed_age_hours'] if daily_summary['max_feed_age_hours'] != float('inf') else 'N/A'} hours |
| Min Snapshot Age | {daily_summary['min_feed_age_hours'] if daily_summary['min_feed_age_hours'] != float('inf') else 'N/A'} hours |
| Crawler Success Rate | {operations['crawler_success']}% |
| Failure Count | {operations['failure_count']} |

---

## 📦 产品指标（Product）

| Metric | Value |
|--------|-------|
| Search Queries | {product['search_queries']} |
| Entity Views | {product['entity_views']} |
| Feed Refreshes | {product['feed_refreshes']} |

---

## 📡 数据源状态

| Metric | Value |
|--------|-------|
| Total Sources | {source_health['total']} |
| Enabled Sources | {source_health['enabled']} |

---

## 🎯 S1 成功标准

| 标准 | 状态 |
|------|------|
| Pipeline 正常运行 | ⬜ |
| 无 Runtime Bug | ⬜ |
| 无 Contract Drift | ⬜ |
| 无 Replay Drift | ⬜ |
| 首页每天更新 | ⬜ |
| Entity 持续增长 | ⬜ |
| Backlog 有价值记录 | ⬜ |
| Dashboard 数据可信 | ⬜ |

---

## 🏷️ 里程碑

```
Runtime v1

Architecture      ✅

Validation        ✅

Product           ✅

Operations        ✅

────────────────────────

Operational Proof

S1 Baseline       {today}

S2 90 Days

S3 1 Year

ASR-{year}
```

---

## 📝 备注

*（手动填写：S1 期间的重要发现和总结）*

---

*Auto-generated at {datetime.utcnow().isoformat()}*
"""

    output_path = PROJECT_ROOT / "evidence" / "operations" / f"BASELINE-{year}-{quarter}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"✅ Baseline saved: {output_path}")
    print(f"   Period: S1 ({daily_summary['days_counted']} days)")
    print(f"   Entities: {content['entity_count']}")
    print(f"   Sources: {source_health['enabled']}/{source_health['total']}")

    return output_path


if __name__ == "__main__":
    generate_baseline()
