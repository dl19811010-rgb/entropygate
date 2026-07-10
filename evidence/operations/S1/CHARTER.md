# Product Discovery Charter

> **How do we build an intelligence product people actually use?**

**Effective Date**: 2026-07-08  
**Status**: Active  
**Supersedes**: All prior product-phase governance

> **Runtime v1 is no longer under development; it is under stewardship. Product development is no longer driven by architecture, but by evidence, editorial judgment, and user value.**

---

## 运营哲学

> **Build the runtime once. Improve the product continuously. Earn user trust every day.**

* **Build the runtime once** — Runtime Charter，保证稳定可靠的基础
* **Improve the product continuously** — Product Discovery Charter，通过证据持续优化用户价值
* **Earn user trust every day** — 日常运营，用高质量 Intelligence 和稳定体验赢得用户持续回访

---

## 产品学习哲学

> **Observe carefully. Learn continuously. Improve deliberately.**

* **Observe carefully** — 连续、系统地收集证据，不急于下结论
* **Learn continuously** — 通过 Evidence 形成 Insights，建立 Editorial Standards
* **Improve deliberately** — 基于验证的模式做出决策，而不是直觉

---

## 工作准则

> **不要急着做下一个功能，而要先理解下一个用户。**

这是 Runtime 完成之后，产品团队最重要的能力转换。

---

## 治理模型

```
                   Vision
                      │
      "每天帮助用户理解 AI 世界最重要的变化"
                      │
        ┌─────────────┴─────────────┐
        │                           │
 Runtime Charter             Product Discovery Charter
   (How to build)             (How to create value)
        │                           │
        └─────────────┬─────────────┘
                      │
             Stable Product Runtime
                      │
          Daily Intelligence Operation
                      │
      Observation → Evidence → Editorial Standards → Product Decisions
```

### 四项核心产出

| 输出 | 意义 |
|------|------|
| Evidence | 我们观察到了什么 |
| Insights | 我们理解了什么 |
| Editorial Standards | 我们以后如何持续判断什么是重要的 |
| Decisions | 我们决定做什么 |

### 三个连续阶段

```
Observe → Understand → Improve
```

对应完整链路：

```
Observation → Evidence → Editorial Decision → Repeated Pattern → Hypothesis → Priority → Implementation → Measurement
```

每个改动都能回溯到某一天的 Observation。

---

## North Star Question

> **Would I open EntropyGate AI tomorrow morning? Why?**

运营人员每天回答。连续两周后，这比任何 Analytics 都真实。

---

## 五条产品原则

### P1: Every feature answers one user question

以后任何需求进入 Backlog，都先回答：

> **它回答的是哪个用户问题？**

如果回答不了，就不要做。

| Feature | 回答的问题 |
|---------|-----------|
| Homepage | 今天发生了什么？ |
| Entity | 我需要了解它。 |
| Timeline | 它如何发展到今天？ |
| Search | 我该从哪里开始？ |
| Related | 我下一步应该看什么？ |

这个原则可以有效避免产品慢慢变成"功能堆积"。

---

### P2: Intelligence over Information

不要问：

> 今天有哪些新闻？

而要问：

> 今天哪些信息真正改变了 AI 世界？

```
OpenAI 发布 GPT-5         ← News

GPT-5 发布意味着：          ← Intelligence
• Reasoning 提升
• 企业 API 能力变化
• Benchmark 格局变化
• 对 Anthropic 的竞争影响
```

---

### P3: Discovery over Navigation

搜索不是终点。Entity 也不是终点。

真正目标：

```
Homepage → Entity → Timeline → Research → Capability → Related → Another Entity
```

每一步都让用户觉得：

> 原来还有这个。

---

### P4: Evidence before Decisions

不要说：

> 我觉得首页不好。

而是：

```
Homepage Score 14天 → 3.1/5
↓
Headline 点击率最低
↓
Evidence
↓
进入 Backlog
```

以后任何产品决策，都应该有运营证据支撑。

---

### P5: Product over Infrastructure

以后如果出现选择：

```
A: Runtime 更漂亮
B: 用户体验更好
```

优先 B。

因为 Runtime 已经完成使命。

---

### P6: Small improvements. Long horizons.

> **小步改进，长期验证。**

未来竞争力来自：
* 每天提高一点首页质量
* 每周完善一点知识网络
* 每月优化一点编辑标准

而不是一次大的重构。

---

## 两种工作模式

### Mode 1：Operate（默认状态，90% 时间）

每天只有四类事：
* 运行系统
* 观察用户价值
* 收集证据
* 更新 Backlog

目标不是"让产品变大"，而是回答：

> **今天我们学到了什么？**

### Mode 2：Improve（触发状态，10% 时间）

只有满足完整链路，才进入开发：

```
Observation
    ↓
Evidence
    ↓
Repeated Pattern（重复出现）
    ↓
Hypothesis
    ↓
Prioritized Backlog
    ↓
Implementation
```

**Repeated Pattern**：很多产品问题都是偶然。只有连续出现，才值得开发。

例如：
```
Day 3  搜索不好用
Day 5  搜索不好用
Day 8  搜索不好用
    ↓
Repeated Pattern
    ↓
P3 Search Ranking 改进
```

而不是 Day 1 就开始写代码。

---

## 改进检查清单（四问）

未来所有产品改进，都必须回答下面四个问题：

| 问题 | 来源 |
|------|------|
| 我们观察到了什么？ | Observation |
| 我们有什么证据？ | Evidence |
| 它是不是重复出现？ | Repeated Pattern |
| 如果解决，它改善哪个用户问题？ | P1 |

如果这四个问题回答不完整，就先继续观察。

避免因为短期噪声而打乱产品节奏。

---

## Product Review Checklist

以后每一个产品功能都经过一次 Charter 检查：

```text
Product Checklist

□ Answer one user question
□ Increase intelligence value
□ Improve discovery
□ Evidence attached
□ No unnecessary infrastructure impact
```

五个都过不了，不用讨论实现，直接 Reject。

---

## S1 Product Review 结构

S1 结束时，不写技术报告，而是写真正的 Product Review：

```text
S1 Product Review

Executive Summary

Hypothesis Validation
    H1: Daily Intelligence
    H2: Knowledge Exploration
    H3: Search Discovery

Homepage Review

Entity Review

Search Review

Discovery Review

Top Insights

Top Problems

Top Opportunities

Next Quarter Priorities
```

这份文档回答的是"产品是否正在创造价值"。

---

## S1 Exit Checklist

两周结束时，不仅要生成 Baseline，还要回答：

```text
□ Would we keep operating this product?

□ Would we recommend it to an AI practitioner?

□ Is the homepage already useful every day?

□ Do we know what to improve next?

□ Are improvements backed by evidence?

□ Can we consistently explain why today's homepage looks the way it does?
```

如果六个答案都是 Yes，进入 Phase E。如果不是，继续 Discovery。不要急。

### 能力标准

> **The team can consistently explain why today's homepage looks the way it does.**

这是一个很强的成熟度指标。因为首页不是随机排列、不是新闻聚合、不是模型排序，而是每天都有明确理由：
* 为什么是这一条头条？
* 为什么它比另外一条重要？
* 为什么今天推荐 Capability，而不是融资？

如果团队能够持续回答这些问题，说明 Editorial Intelligence 已经形成。

---

## 核心资产：Editorial Intelligence

未来最大的资产不是代码、不是 Runtime、甚至不是 API。而是：

```
Editorial Knowledge
    ↓
Editorial Standards
    ↓
Editorial Consistency
```

如果一年以后换了一批工程师，Runtime 不变。
如果换了一批编辑，首页依然保持同样的 Intelligence 水平。

这说明产品真正成熟了。

这是 AI Intelligence 产品最难建立、也最难复制的能力。

---

## Phase E 准入条件

- H1/H2/H3 全部成立
- S1 Baseline 完成
- 连续两周稳定运营
- Product Review 通过
- 至少有一个 Validated Pattern 可转化为 Growth Initiative

### Growth 的输入

Growth 不应该从"开发"开始，而是从验证的模式开始：

```
Evidence → Validated Pattern → Growth Initiative
```

例如：
* 连续十四天发现 Timeline 点击率最高 → Growth Initiative: Timeline 首页入口提前
* 不是"我想到一个 Timeline 新功能"

两种思维差别非常大。

---

*Charter established at 2026-07-08*
