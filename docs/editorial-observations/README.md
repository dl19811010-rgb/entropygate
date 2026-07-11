# Editorial Observations — 运营观察日志

> **目的：** 记录每天的编辑观察，沉淀运营知识，驱动 Editorial Policy 演化。
>
> **起始日期：** 2026-07-12（EOS v1.0 上线日）
>
> **初始 Policy：** [Editorial Policy v1.0](../Editorial%20Policy%20v1.0.md)

---

## 如何使用

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

**先记录，不修改。** 等连续出现 3 天以上再考虑调整。

### 3. Repeated Patterns — 哪些现象已经连续出现？

例如：

- "Agent 连续 5 天都是 Top Topic"
- "Official Source 连续 7 天占比超过 45%"
- "GitHub Changelog 连续 10 天没有进入首页"

**连续 7 天以上 → 考虑升级为 Editorial Standard**
**连续 14 天以上 → 考虑修改 Editorial Policy**

---

## 目录结构

```
editorial-observations/
├── README.md                  ← 本文件
├── weekly-reviews/            ← 每周回顾
│   ├── week-01.md
│   └── week-02.md
├── policy-evolution.md        ← Policy 演化记录（候选→确认）
└── daily/
    ├── 2026-07-12.md
    ├── 2026-07-13.md
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

- [模式 A]：连续 X 天 — 等待确认中（需 7 天）
- [模式 B]：连续 Y 天 — 已确认（≥ 7 天），建议调整 [具体Policy]
```

---

## 从 Observation 到 Policy 的路径

```
Daily Observation
      │
      ▼
Policy Change Candidate（单次出现，仅记录）
      │
      ▼ 连续 3 天
Repeated Pattern（值得关注）
      │
      ▼ 连续 7 天
Candidate for Policy Change（进入 policy-evolution.md 候选区）
      │
      ▼ 讨论 + 验证
Policy Update（更新 Editorial Policy 版本号）
      │
      ▼
Two-week Review（两周后评估效果）
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

*运营观察从 EOS v1.0 上线开始。目标：两周后产出 Editorial Policy v1.1。*
