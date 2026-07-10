# Product Evolution Roadmap

> **从架构完成 → 产品上线 → 持续创造价值**

---

## Mission Alignment

| Layer | Era | Status |
|-------|-----|--------|
| Runtime | Architecture Era | 🔒 Frozen |
| Platform | Architecture Era | 🔒 Frozen |
| Governance | Architecture Era | 🔒 Frozen |
| **Product** | **Product Evolution** | **▶️ Active** |

未来所有新价值默认落在 **Product** 层。
Runtime / Platform / Governance 仅做 LTS 级修复，不扩展新抽象。

---

## Product Principles

1. **Daily First** — 每天首页能看见新的 Intelligence。
2. **Projection Driven** — 前端只消费 Projection / Feed，不直接聚合数据库。
3. **Cache Before Render** — 首页内容走快照，不实时计算。
4. **Real Data** — Pipeline 必须每天自动产生真实数据。
5. **Trust Through Evidence** — 每个数字都对应一个具体来源。

---

## Product Roadmap

| Phase | Theme | Status |
|-------|-------|--------|
| **P1** | **Intelligence Homepage** | ▶️ Current |
| P2 | Entity Experience | Queued |
| P3 | Search & Discovery | Queued |
| P4 | AI Copilot | Queued |
| P5 | Growth & Ecosystem | Queued |

---

## P1 — Intelligence Homepage MVP

### Goal

> **让用户打开首页时，看到的是 Runtime 自动生成的 Intelligence，而不是传统新闻列表。**

### Sub-Sprints

#### Sprint 1 — Real Data Pipeline

```
Source Registry
     ↓
Scheduler (Celery Beat)
     ↓
Crawler
     ↓
Signal
     ↓
Fact Runtime
     ↓
Event / Capability
     ↓
DailyFeedProjection
     ↓
feed_daily.json (snapshot)
     ↓
Homepage API
```

#### Sprint 2 — Homepage Intelligence (Projection-Driven)

```
Today's Intelligence
    ├── Headline
    ├── Major Events
    ├── Capability Changes
    ├── Company Watch
    ├── Research
    ├── Benchmarks
    └── Trends
```

所有内容来自 `feed_daily.json`，前端不直接查询数据库。

### Definition of Done (P1 DoD)

* [x] active_sources > 0 已被修复（脚本路径问题已解决，当前 11 个活跃源）
* [ ] `DailyFeedProjection` 已实现并输出 `feed_daily.json`
* [ ] Homepage API 完全消费 `feed_daily.json`，不直接聚合数据库
* [ ] Daily Pipeline 可通过 Celery Beat 自动调度
* [ ] Product Dashboard 展示 Signals / Facts / Events / Last Refresh
* [ ] 首页所有核心内容均来自 Projection
* [ ] Runtime、Platform、Governance 保持 **0 修改**

### KPI 切换

| Old (Runtime Era) | New (Product Era) |
|-------------------|-------------------|
| Replay Success | Signals/day |
| Compatibility | Events/day |
| Coverage | Homepage Refresh |
| Golden Cases | Entity Coverage |
| | Search Success |
| | Review SLA |
| | Daily Visitors |
| | API Calls |

### Architecture Budget (Annual)

| Type | Budget | Status |
|------|-------:|:------:|
| Runtime Breaking Change | 0 | 🔒 Prohibited |
| Platform Layer Addition | 0 | 🔒 Prohibited |
| New Controller Type | 0 | 🔒 Prohibited |
| New State Object | 0 | 🔒 Prohibited |
| **New Product Feature** | **Unlimited** | **✅ Active** |
| New Projection Package | Unlimited | ✅ Active |
| New Feed Type | Unlimited | ✅ Active |

---

## Future Phases (Planned)

### P2 — Entity Experience
- Company / Model / Capability / Research / Event entity pages
- 全部由 Projection 驱动

### P3 — Search & Discovery
- 可解释搜索（Facts / Events / Capabilities / Knowledge）
- 实体关系图谱

### P4 — AI Copilot
- Explain / Summarize / Question-Answer
- 在已有 feed/knowledge 之上构建，不修改 Runtime

### P5 — Growth & Ecosystem
- API consumers
- SDK adoption
- Editorial workflow
- Feedback loop

---

## Relationship to Validation Era

P1 既是 **Product Evolution** 的起点，也是 **Validation Era** 的最佳实践：
- 新增 DailyFeedProjection → 增加 Reference Library
- 不改 Runtime / Platform → 验证 LTS 稳定性
- 持续运行 → 积累 Evidence

> **每新增一项能力，都应增强对现有基础的信心，而不是削弱它。**
