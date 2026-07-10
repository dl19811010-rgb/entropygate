# S1 Stabilization Cycle — Product Backlog

> 规则：只记录，不修改。
> 每周 Review 一次，统一排期。

---

## 📅 Cycle: S1
**开始日期**: 2026-07-08  
**结束日期**: 2026-07-22  
**目标**: 两周稳定运行，积累产品改进证据

---

## 🏷️ 分类标签

| 标签 | 含义 |
|------|------|
| `content` | 内容质量问题（标题、摘要、事实准确性） |
| `ui` | 界面/交互问题 |
| `performance` | 性能问题 |
| `crawler` | 数据源问题 |
| `runtime` | Runtime 输出问题 |
| `ranking` | 排序问题（搜索排序、首页排序、推荐排序） |
| `editorial` | 编辑问题（首页重点、标签、分类、优先级） |
| `idea` | 新想法/功能建议 |

---

## 📝 Backlog

### 2026-07-08

- [ ] **[idea]** 搜索排序可能需要引入时间衰减因子，旧文章不应排太高  
  Evidence: Day8 | Count: 1
- [ ] **[crawler]** 某些 Source 可能有重复抓取问题，需要观察 CrawlLog 中的 duplicate 比例  
  Evidence: Day8 | Count: 1
- [ ] **[runtime]** Events 可能有重复检测（同一事件被多次标记）  
  Evidence: Day8 | Count: 1

---

### 记录格式

```
- [ ] **[标签]** 问题描述
  Evidence: DayX, DayY, DayZ | Count: N
```

**Evidence Count**：问题被观察到的天数。计数越高，优先级越高。

---

## 📊 每日观察记录

### 2026-07-08

| 指标 | 数值 | 备注 |
|------|------|------|
| Signals Today | — | 首次运行 |
| Facts Generated | — | 首次运行 |
| Events Generated | — | 首次运行 |
| Pipeline Time | — | 首次运行 |
| Snapshot Age | — | 首次运行 |
| Success Rate | — | 首次运行 |
| Source Health | 11/11 | 全部启用 |

**首页观察**:
- Headline: —
- Events: —
- Capability: —
- Trend: —
- 垃圾信息: —

**整体评价**: —

---

## 🎯 S1 结束后的 Review Checklist

- [ ] 数据稳定性是否满足预期（Source 成功率 > 90%）
- [ ] 每日 Feed 是否具有足够的信息价值（每天 ≥ 10 条有意义的信息）
- [ ] Entity 页面是否持续更新且内容连贯
- [ ] 搜索和时间线是否随着真实数据自然增长
- [ ] Dashboard 指标是否反映真实运行状态
- [ ] 是否存在明显的重复/垃圾信息
- [ ] 内容质量的人工评分是否达到可接受水平

---

## 🚀 S1 → P4 准入标准

| 条件 | 标准 |
|------|------|
| 连续运行天数 | ≥ 10 天 |
| 每日 Signals | ≥ 50 |
| Source 成功率 | ≥ 85% |
| Snapshot 新鲜度 | ≤ 24 小时 |
| 人工评分合格率 | ≥ 70% |
| 无重大 Bug | 连续 3 天无崩溃 |

---

*此文件在 S1 期间只增不改，S1 结束后统一 Review。*
