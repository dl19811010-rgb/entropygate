# Editorial Observations — 运营观察日志

> **目的：** 记录每天的编辑观察，沉淀运营知识，驱动 Editorial Policy 演化。
>
> **起始日期：** 2026-07-12（EOS v1.0 + Editorial Policy v1.0 上线日）
>
> **初始 Policy：** [Editorial Policy v1.0](../Editorial%20Policy%20v1.0.md)
>
> **策略演化：** [PEP (Policy Evolution Proposals)](policy-evolution.md)

---

## 运营纪律

在开始记录之前，先记住这几条：

### 1. One Policy Change per Review Cycle

> 每个 Review Cycle（两周），最多发布 **1-2 个 Policy Change**。

一次改太多，就不知道是哪个变化带来了效果。保持可解释性比快速迭代更重要。

### 2. 先观察，后判断

看到一个现象，先记为 Candidate，不要马上改。

- **连续 3 天** → 值得关注
- **连续 7 天** → 可以进入 PEP 讨论
- **连续 14 天** → 值得发布 Policy Change

### 3. 记录 Rejected 同样重要

否决的提案也要记录原因。"哪些直觉是错的"和"哪些是对的"一样有价值。

### 4. Policy 比代码更常变，但变更更谨慎

> **P7: Policies evolve more often than code.**

- 觉得 Research 太多？→ 改 Quota，不改代码
- 觉得某个 Source 重要？→ 改 Tier，不改 Crawler
- 但每次改动都要走 PEP 流程，不能拍脑袋

---

## 每天做什么

每天花 10-15 分钟，回答三个问题：

### 1. Evidence — 今天发生了什么？

从 EOS 的 Coverage Report 里提取关键数据：

- 今天采了多少条？
- Top Stories 是哪几条？
- 各 Source Type 占比多少？
- 各 Topic 分布如何？
- 有哪些 Gap？
- Noise Rate 大概多少？（值得看的 / 总数）

**只记录事实，不做判断。**

### 2. Policy Change Candidates — 今天有没有发现值得调整的现象？

例如：

- "arXiv 每天都有很多，但值得看的很少，是不是应该降 Tier？"
- "Kimi 中文源质量很高，是不是应该从 B 升到 A？"
- "Research 占比只有 5%，远低于目标 15%，是不是源不够？"

**先记录，不修改。** 等连续出现 3 天以上再考虑进入 PEP。

### 3. Repeated Patterns — 哪些现象已经连续出现？

例如：

- "Agent 连续 5 天都是 Top Topic"
- "Official Source 连续 7 天占比超过 45%"
- "GitHub Changelog 连续 10 天没有进入首页"

- **连续 3 天** → 在 daily log 里标注
- **连续 7 天** → 新建 PEP Draft
- **连续 14 天** → 可以在 Review Cycle 结束时讨论是否发布

---

## 从 Observation 到 Policy 的完整路径

```
Daily Observation（每日记录）
      │
      ▼
Candidate（单次/偶尔出现，仅记录）
      │
      ▼ 连续 3 天
Notable Pattern（值得关注）
      │
      ▼ 连续 7 天
PEP Draft（进入 [policy-evolution.md](policy-evolution.md)）
      │
      ▼ Review Cycle 讨论
Accepted / Rejected（决策）
      │
      ▼ Accepted
Policy Update（更新 Editorial Policy 版本号）
      │
      ▼ 运营两周
Effect Review（效果评估 → Reviewed / 调整 / 回滚）
```

---

## 目录结构

```
editorial-observations/
├── README.md                    ← 本文件
├── policy-evolution.md          ← PEP 提案 + 决策记录
├── weekly-reviews/              ← 每周回顾
│   ├── week-01.md
│   └── week-02.md
└── daily/
    ├── 2026-07-12.md            ← Day 0（基线日）
    ├── 2026-07-13.md            ← Day 1
    └── ...
```

---

## 每日记录模板

```markdown
# YYYY-MM-DD — Day N

## 1. Evidence

### 采集概览
- 总采集数：XX 条
- 进入 Top/Major（Score ≥ 70）：XX 条
- 估算 Noise Rate：XX%

### Source Type 分布
| Type | 数量 | 占比 | 目标 | 状态 |
|------|------|------|------|------|
| Official | XX | XX% | 40% | ok/gap/over |
| Research | XX | XX% | 15% | ok/gap/over |
| Media | XX | XX% | 20% | ok/gap/over |
| Community | XX | XX% | 10% | ok/gap/over |

### Topic 热度 Top 5
1. Topic A — XX 条
2. Topic B — XX 条
3. Topic C — XX 条
4. Topic D — XX 条
5. Topic E — XX 条

### Top Stories（今天最重要的 3-5 条）
1. [标题] — [Source] — [Score]
2. ...

### Coverage Gaps
- Gap A：为什么是 Gap
- Gap B：为什么是 Gap

---

## 2. Policy Change Candidates（先记下来，不修改）

- [观察 1]：[为什么觉得可能需要调] — 第 1 天出现
- [观察 2]：[为什么觉得可能需要调] — 第 2 天出现（续）

---

## 3. Repeated Patterns（连续出现 ≥ 3 天的）

- [模式 A]：连续 X 天 — 等待确认中（需 7 天进入 PEP）
- [模式 B]：连续 Y 天 — 已达 7 天，建议创建 PEP Draft → [PEP-00X]
```

---

## 关键指标追踪表

每天更新，用于看趋势：

| 指标 | Day 0 | Day 7 | Day 14 | Day 30 |
|------|-------|-------|--------|--------|
| 总采集数 | | | | |
| Top/Major 数 | | | | |
| Noise Rate（估算） | | | | |
| Official 占比 | | | | |
| Research 占比 | | | | |
| 中文内容占比 | | | | |
| Coverage Gap 数量 | | | | |
| Source Success Rate | | | | |
| Top Topic 1 | | | | |
| Top Topic 2 | | | | |
| Top Topic 3 | | | | |

---

## Review Cycle 节奏

| Cycle | 周期 | 做什么 |
|-------|------|--------|
| Cycle 0 | 2026-07-12 ~ 2026-07-25 | 基线观察，积累数据 |
| Cycle 1 | 2026-07-26 ~ 2026-08-08 | 第一次 Policy Review，可能发布 v1.1 |
| Cycle 2 | 2026-08-09 ~ 2026-08-22 | 第二次 Review，可能发布 v1.2 |

每个 Review Cycle 的最后一天：
1. 回顾两周数据
2. 评估所有 PEP Draft
3. 选择 1-2 个发布（或都不发布）
4. 更新 Editorial Policy 版本号
5. 记录决策原因（不管是做了还是没做）

---

*运营观察从 2026-07-12 开始。目标：两周后产出第一个 PEP 决策。*
