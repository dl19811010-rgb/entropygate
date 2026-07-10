#!/usr/bin/env python3
"""
Phase D — Product Discovery — Daily Observation

核心目标：找到用户每天回来打开 EntropyGate AI 的理由。

三个核心假设：
  H1: 每天至少有一条 Intelligence 值得 AI 从业者阅读
  H2: 用户会从 Feed 进入 Entity，并继续探索
  H3: 搜索不是找东西，而是发现东西

用法（必须从项目根目录运行）：
    cd e:\aitoto
    python scripts/snapshot_observation.py
"""

import os
import sys
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
BACKEND_ROOT = PROJECT_ROOT / "ai-news-backend"
S1_DIR = PROJECT_ROOT / "evidence" / "operations" / "S1"
DAILY_DIR = S1_DIR / "daily"


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


def collect_snapshot_age():
    """Collect snapshot freshness."""
    feed_path = BACKEND_ROOT / "evidence" / "feeds" / "feed_daily.json"
    alt_feed = PROJECT_ROOT / "evidence" / "feeds" / "feed_daily.json"

    snapshot_age_hours = None
    feed_exists = False

    for path in [feed_path, alt_feed]:
        if path.exists():
            mtime = datetime.fromtimestamp(os.path.getmtime(path))
            snapshot_age_hours = round((datetime.utcnow() - mtime).total_seconds() / 3600, 1)
            feed_exists = True
            break

    return {
        "feed_age_hours": snapshot_age_hours,
        "feed_exists": feed_exists,
    }


def collect_scheduler_status():
    """Collect scheduler status."""
    state_file = BACKEND_ROOT / "evidence" / "operations" / "scheduler_state.json"
    if not state_file.exists():
        return {"running": False, "last_updated": None, "jobs_count": 0}

    try:
        with open(state_file, encoding="utf-8") as f:
            state = json.load(f)
        return {
            "running": state.get("running", False),
            "last_updated": state.get("updated_at"),
            "jobs_count": len(state.get("jobs", {})),
        }
    except Exception:
        return {"running": False, "last_updated": None, "jobs_count": 0}


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


def generate_daily_observation():
    """Generate today's observation report."""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    DAILY_DIR.mkdir(parents=True, exist_ok=True)

    source_health = collect_source_health()
    snapshot = collect_snapshot_age()
    scheduler = collect_scheduler_status()
    daily_reports = count_daily_reports()
    entity_snapshots = count_entity_snapshots()

    md = f"""# Daily Observation — {today}

> **核心目标**: 找到用户每天回来打开 EntropyGate AI 的理由。

---

## ⭐ North Star Question

> **Would I open EntropyGate AI tomorrow morning? Why?**

Answer：_

---

## 📊 Daily Editorial Score

| 维度 | 1–5 分 |
|------|-------|
| 今日内容是否重要 | ___ |
| 是否有新的洞察 | ___ |
| 首页是否值得浏览 | ___ |
| 是否愿意分享给同行 | ___ |
| 是否愿意明天再回来 | ___ |

**Total**: ___ / 25

---

## 🎯 Today's Intelligence Confidence

> **今天首页是否足够代表 AI 世界？**

[ ] High    — 覆盖了主要事件和趋势
[ ] Medium  — 有价值内容，但不够全面
[ ] Low     — 内容太少或质量太低

---

## 📰 Today's Editorial Decision

### Q1: 今天唯一值得推荐的一条是什么？

Answer：_

Why：_

────────────────────────────

### Q2: 如果用户今天只有 3 分钟，他离开前应该知道什么？

Answer：_

Why：_

---

## 🎯 三个核心假设（Hypotheses）

### H1: Daily Intelligence 假设
> 每天至少有一条 Intelligence 值得 AI 从业者阅读。

**验证**: 今天唯一值得推荐的一条是什么？
**可测指标**: 每天至少 1 条被编辑标记为"值得推荐"的内容
**状态**: {'✅ 验证通过' if False else '⬜ 待验证'}

---

### H2: Knowledge Exploration 假设
> 用户会从 Feed 进入 Entity，并继续探索。

**验证**: Average Exploration Depth
**典型路径**:
```
Homepage → Entity → Timeline → Research → Related → Entity
```
**可测指标**: 平均探索深度、Entity 点击率、Timeline 打开率
**状态**: {'✅ 验证通过' if False else '⬜ 待验证'}

---

### H3: Search Discovery 假设
> 搜索不是找东西，而是发现东西。

**验证**: Search → Click → Entity → Related → Another Entity
**可测指标**: 搜索成功率、搜索后继续浏览比例
**状态**: {'✅ 验证通过' if False else '⬜ 待验证'}

---

## 📊 Product KPI

| KPI | Value | 意义 |
|-----|-------|------|
| Daily Active Sources | {source_health['enabled']} | 数据是否持续流入 |
| Feed Freshness | {'✅' if snapshot['feed_exists'] else '❌'} ({snapshot['feed_age_hours'] or 'N/A'}h) | 首页是否保持新鲜 |
| Entity Coverage | {entity_snapshots} | 实体知识是否持续增长 |
| **Intelligence Yield** | _ | 真正有价值的信息占多少（推荐/事件） |
| **Homepage Click Depth** | _ | 用户从首页开始的平均浏览深度 |
| **Entity Completion** | _ | 实体资料完整度（Overview/Timeline/Knowledge/Capabilities/Relations/Research） |
| **Search Success** | _ | 第一次搜索就找到目标的比例 |
| **Editorial Acceptance** | _ | 自动生成内容无需人工修改的比例 |
| **Average Exploration Depth** | _ | 用户平均浏览路径长度 |

---

## 🏠 ① 首页是否值得打开

> 如果我是 AI 从业者，今天有没有必要打开这个首页？

**首页评分**: ★★★★★ / 5

| Section | Score | Notes |
|---------|-------|-------|
| Headline | ★★★★★ | _ |
| Today's Feed | ★★★★☆ | _ |
| Events | ★★★☆☆ | _ |
| Capability | ★★★★☆ | _ |
| Trend | ★★★☆☆ | _ |
| Research | ★★★★★ | _ |

**整体评价**: _

---

## 📚 ② Entity 是否越来越像 Wikipedia

> 打开以后，你会不会继续看？浏览路径是否越来越长？

| Entity | Coverage | Notes |
|--------|----------|-------|
| Overview | ⬜ | _ |
| Recent Events | ⬜ | _ |
| Timeline | ⬜ | _ |
| Capabilities | ⬜ | _ |
| Relations | ⬜ | _ |
| Research | ⬜ | _ |

**最佳 Entity**: _
**浏览深度**: _ (浅/中/深)
**Average Entity Completeness**: _/6

---

## 🔍 ③ Search 是否真正解决问题

> 输入关键词后，是不是立即找到，而不是搜索数据库？

| Query | Result | Notes |
|-------|--------|-------|
| Example: GPT-5 | _ | _ |
| Example: OpenAI | _ | _ |

**Search Success Rate**: _/10
**问题**: _

---

## 💡 ④ Feed 是否真的有 Intelligence

> 是"News News News"还是"今天发生了什么？为什么重要？影响哪些公司？"

**Intelligence Score**: ★★★★★ / 5

| Aspect | Rating | Notes |
|--------|--------|-------|
| 今天发生了什么？ | ★★★★★ | _ |
| 为什么重要？ | ★★★★☆ | _ |
| 影响哪些公司？ | ★★★☆☆ | _ |
| 影响哪些能力？ | ★★★☆☆ | _ |
| 接下来可能发生什么？ | ★★☆☆☆ | _ |

**Intelligence Yield**: _ / _ (推荐数 / 事件数)

---

## 📈 ⑤ Product Command Center

> 今天发生了什么？哪些内容值得推荐？哪些数据源异常？哪些实体增长最快？

| Metric | Tracked | Useful |
|--------|---------|--------|
| Today's Sources | ⬜ | ⬜ |
| Today's Facts | ⬜ | ⬜ |
| Today's Events | ⬜ | ⬜ |
| Today's Headline | ⬜ | ⬜ |
| Duplicate % | ⬜ | ⬜ |
| Source Failure % | ⬜ | ⬜ |
| Top Entity | ⬜ | ⬜ |
| Top Capability | ⬜ | ⬜ |
| Search Queries | ⬜ | ⬜ |
| Entity Views | ⬜ | ⬜ |

**Command Center Value**: ★★★★★ / 5

---

## 📡 Source Health

| Metric | Value |
|--------|-------|
| Total Sources | {source_health['total']} |
| Enabled | {source_health['enabled']} |

## 📦 Snapshots

| Metric | Value |
|--------|-------|
| Feed Exists | {'✅' if snapshot['feed_exists'] else '❌'} |
| Feed Age (hours) | {snapshot['feed_age_hours'] or 'N/A'} |
| Entity Snapshots | {entity_snapshots} |
| Daily Reports | {daily_reports} |

## ⏰ Scheduler

| Metric | Value |
|--------|-------|
| Running | {'✅' if scheduler['running'] else '❌'} |
| Jobs Count | {scheduler['jobs_count']} |
| Last Updated | {scheduler['last_updated'] or 'N/A'} |

---

## 📚 Today We Learned

> **今天我们学到了什么？**

Answer：_

---

## 📝 Notes

*（当天发现的问题或想法，不要立即修改，只记录）*

---

*Auto-generated at {datetime.utcnow().isoformat()}*
"""

    output_path = DAILY_DIR / f"{today}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"✅ Observation saved: {output_path}")
    print(f"   Sources: {source_health['enabled']}/{source_health['total']}")
    print(f"   Feed age: {snapshot['feed_age_hours'] or 'N/A'} hours")
    print(f"   Entity snapshots: {entity_snapshots}")
    print(f"   Scheduler: {'running' if scheduler['running'] else 'stopped'}")

    return output_path


if __name__ == "__main__":
    generate_daily_observation()
