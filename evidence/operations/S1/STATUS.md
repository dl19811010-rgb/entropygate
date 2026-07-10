# Runtime v1 Status

> **Build the runtime once. Improve the product continuously. Earn user trust every day.**

> **EntropyGate AI has entered the Product Learning stage. The runtime is now a stable, long-term foundation under stewardship. Future product evolution is driven by operational evidence, editorial standards, and validated user value rather than architectural change. Success is measured by the team's ability to consistently learn from real-world operation and translate those learnings into better intelligence experiences.**

**Status:** `Operational Baseline Complete — Day 0`  
**Effective Date:** 2026-07-08  
**Cycle:** S1 Stabilization  
**Phase:** D — Product Discovery  
**Mode:** Day 0 Completed → Day 1 Tomorrow

> **工作准则：不要急着做下一个功能，而要先理解下一个用户。**

---

## 🚀 项目生命周期

```
Phase A — Architecture
───────────────────────
ADR / Runtime / Specification

Phase B — Engineering
──────────────────────
Reference Impl / Validation / Conformance

Phase C — Integration
──────────────────────
Pipeline / Frontend / Operations

★★★★★ 现在 ★★★★★

Phase D — Product Discovery
────────────────────────────
真实内容 / 真实用户 / 真实反馈 / 真实数据

Phase E — Product Growth
─────────────────────────
规模化 / 生态 / 增长
```

---

## 📋 状态清单

| 维度 | 状态 | 说明 |
|------|------|------|
| Runtime Specification | 🔒 LTS | 冻结，不再修改 |
| Reference Implementation | ✅ Complete | 全部通过验证 |
| Conformance | ✅ Passing | V1-V3 全部通过 |
| Product | ✅ Running | P1-P3 + F1 完成 |
| Operations | ✅ Established | R1 全部通过 |
| Current Focus | 📊 Collect operational evidence | S1 稳定运行 |

---

## 🔒 冻结范围

以下内容在 S1 期间及后续不再修改：

- Runtime Specification
- Contracts
- Projection Interface
- Evidence Model
- Platform Core

---

## 🎯 S1 成功标准

连续 14 天满足：

- ✅ Pipeline 正常运行
- ✅ 无 Runtime Bug
- ✅ 无 Contract Drift
- ✅ 无 Replay Drift
- ✅ 首页每天更新
- ✅ Entity 持续增长
- ✅ Backlog 有价值记录
- ✅ Dashboard 数据可信

---

## 📝 S1 工作原则

### 1. Observation First
```
发现 → 记录 → 观察是否持续出现 → 进入 Backlog
```

### 2. Product over Infrastructure
> 用户会感知到吗？

### 3. Evidence before Decisions
> 先收集数据，再决定是否调整

### 4. P1: Every feature must answer one user question
> 每一个产品能力，都应该回答一个明确的问题。

| 页面 | 用户真正的问题 |
|------|--------------|
| Homepage | 今天 AI 世界发生了什么？ |
| Entity | 我想快速了解这个公司/模型现在的发展情况。 |
| Timeline | 它是怎么一步步发展到今天的？ |
| Search | 我知道一个名字，但不知道应该从哪里开始了解。 |
| Discovery | 我还能继续看什么？ |
| Dashboard | 今天这个产品运行得怎么样？ |

如果一个页面不能回答一个明确的问题，那么它大概率只是"展示数据"，而不是创造价值。

---

## 🎯 三个核心假设（Hypotheses）

### H1: Daily Intelligence 假设
> 每天至少有一条 Intelligence 值得 AI 从业者阅读。

**验证**: 每天回答"今天唯一值得推荐的一条是什么？"

---

### H2: Knowledge Exploration 假设
> 用户会从 Feed 进入 Entity，并继续探索。

**验证**: Average Exploration Depth

**典型路径**:
```
Homepage → Entity → Timeline → Research → Related → Entity
```

---

### H3: Search Discovery 假设
> 搜索不是找东西，而是发现东西。

**验证**: Search → Click → Entity → Related → Another Entity

---

## 🔍 S1 重点观察五件事

### ① 首页是否值得打开
> 如果我是 AI 从业者，今天有没有必要打开这个首页？

### ② Entity 是否越来越像 Wikipedia
> 打开以后，你会不会继续看？浏览路径是否越来越长？

### ③ Search 是否真正解决问题
> 输入关键词后，是不是立即找到，而不是搜索数据库？

### ④ Feed 是否真的有 Intelligence
> 是"News News News"还是"今天发生了什么？为什么重要？影响哪些公司？"

### ⑤ Dashboard 是否帮助运营
> 每天看的是不是"Today's Sources/Facts/Events"而不是"Replay PASS"

---

## 📊 Product KPI

| KPI | 意义 |
|-----|------|
| Daily Active Sources | 数据是否持续流入 |
| Feed Freshness | 首页是否保持新鲜 |
| Entity Coverage | 实体知识是否持续增长 |
| **Intelligence Yield** | 真正有价值的信息占多少（推荐/事件） |
| **Homepage Click Depth** | 用户从首页开始的平均浏览深度 |
| **Entity Completion** | 实体资料完整度（Overview/Timeline/Knowledge/Capabilities/Relations/Research） |
| **Search Success** | 第一次搜索就找到目标的比例 |
| **Editorial Acceptance** | 自动生成内容无需人工修改的比例 |
| **Average Exploration Depth** | 用户平均浏览路径长度 |

---

## 📋 S1 产出

| 产出 | 路径 | 用途 |
|------|------|------|
| Daily Observation | `daily/YYYY-MM-DD.md` | 每日运营记录（包含五件观察+KPI） |
| Weekly Review | `S1-W1.md`, `S1-W2.md` | 每周总结 |
| Product Backlog | `product_backlog.md` | 只记录不修改 |
| Baseline Report | `BASELINE-2026-Q3.md` | 第一份产品基线 |

---

## 🏷️ 里程碑

```
Runtime v1

Architecture      ✅
Validation        ✅
Capability        ✅
Operations        ✅
Stewardship       ✅
Integration       ✅
Product MVP       ✅
────────────────────────
Product Learning  ▶️（当前）
Product Growth    ⏳（等待证据）
```

---

## 🔄 两种工作模式

### Mode 1：Operate（默认，90% 时间）
每天：运行系统 → 观察用户价值 → 收集证据 → 更新 Backlog
> 目标：今天我们学到了什么？

### Mode 2：Improve（触发，10% 时间）
仅当完整链路满足时才开发：
```
Observation → Evidence → Editorial Decision → Repeated Pattern → Hypothesis → Priority → Implementation → Measurement
```
**Repeated Pattern**：问题连续出现才值得开发，避免为偶然现象修改产品节奏。

---

## 🎯 四项核心产出

| 输出 | 意义 |
|------|------|
| Evidence | 我们观察到了什么 |
| Insights | 我们理解了什么 |
| Editorial Standards | 我们以后如何持续判断什么是重要的 |
| Decisions | 我们决定做什么 |

---

## 🔄 完整演进闭环

```
Vision
    ↓
Stable Runtime
    ↓
Reliable Intelligence
    ↓
Useful Product
    ↓
Daily Observation
    ↓
Evidence
    ↓
Editorial Standards
    ↓
Product Decisions
    ↓
Better Product
```

这是一个不依赖"持续重构基础设施"的演进模型，而是依赖持续学习和运营积累。

---

## 🚪 S1 Exit Checklist

```
□ Would we keep operating this product?
□ Would we recommend it to an AI practitioner?
□ Is the homepage already useful every day?
□ Do we know what to improve next?
□ Are improvements backed by evidence?
```
五个全部 Yes → 进入 Phase E。否则继续 Discovery。

---

## 📅 Timeline

| 日期 | 事件 |
|------|------|
| 2026-07-08 | S1 启动 |
| 2026-07-14 | S1-W1 Review |
| 2026-07-21 | S1-W2 Review |
| 2026-07-22 | S1 结束 / 生成 BASELINE |
| 2026-07-22 | S1 Product Review |

---

## 🔄 S1 结束后的流程

### Discovery 成功标准（5 个问题）

S1 结束时，不问"有没有 Bug"，而是回答：

1. **H1 是否成立？** 用户每天都能看到至少一条值得关注的 Intelligence 吗？
2. **H2 是否成立？** 用户是否愿意从首页继续探索 Entity、Timeline 和 Knowledge？
3. **H3 是否成立？** 搜索是否帮助用户发现更多内容，而不仅仅是定位内容？
4. **哪三类内容最能吸引用户？**
5. **Backlog 中哪些问题真正影响用户价值，哪些只是工程层面的优化？**

### 流程

1. 生成 `BASELINE-2026-Q3.md`
2. 召开 Product Review（回答以上 5 个问题）
3. 基于证据决定 P4 优先级
4. 进入下一阶段

---

## 🔮 Phase E — Product Growth（预览，暂不开发）

**Objective**: 让更多用户持续使用 EntropyGate AI。

**Success Metrics**:
- DAU / WAU / Returning Users
- Search Usage
- Entity Exploration
- API Consumers
- Editorial Acceptance
- Intelligence Yield

**Entry Criteria**:
- H1/H2/H3 全部成立
- S1 Baseline 完成
- 连续两周稳定运营

---

*Created at 2026-07-08*
