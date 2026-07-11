# Policy Evolution Proposals (PEP)

> **PEP = Policy Evolution Proposal**
>
> 记录所有编辑策略的变更候选、讨论、决策和效果评估。
>
> 初始基线：[Editorial Policy v1.0](../Editorial%20Policy%20v1.0.md)

---

## 运营纪律

### 🔒 One Policy Change per Review Cycle

> 每个 Review Cycle（两周），最多发布 **1-2 个 Policy Change**。

**原因：**

- 一次改太多，就不知道是哪个变化带来了效果
- 保持可解释性比快速迭代更重要
- Policy 的价值在于稳定，不在于频繁变化

**流程：**

```
Review Cycle 开始
    ↓
10 个 Candidates
    ↓
讨论 + 排序
    ↓
选 1 个（最多 2 个）发布
    ↓
其余继续观察
    ↓
下个 Cycle 再评估
```

---

## PEP 状态定义

| 状态 | 含义 |
|------|------|
| **Draft** | 候选中，正在收集证据 |
| **Accepted** | 已确认，将在下个 Policy 版本中发布 |
| **Implemented** | 已发布，Policy 版本已更新 |
| **Reviewed** | 运营两周后，效果已评估 |
| **Rejected** | 否决，不采纳（记录原因） |
| **Withdrawn** | 撤回，提案人主动取消 |

---

## Rejected Proposals — 为什么同样重要

> **记录哪些直觉被证明是错的，和记录哪些是对的一样有价值。**

长期下来，Rejected 列表会形成一个宝贵的知识库：

- "我们曾经以为 X 很重要，但数据证明不是"
- "我们想过要调整 Y，但证据不足"
- "Z 看起来是个问题，但其实是正常波动"

这可以避免团队反复纠结同一个问题，也让新人快速理解"为什么我们不这样做"。

---

## PEP 模板

每个新提案用这个格式：

```markdown
### PEP-00X: [简短标题]

- **提出日期：** YYYY-MM-DD
- **类别：** [Source Tier / Topic / Quota / Scoring / Scheduling / Other]
- **状态：** Draft / Accepted / Implemented / Reviewed / Rejected
- **关联 Policy 版本：** v1.X（如果已发布）

#### 问题
[描述观察到的现象或问题]

#### 证据
- [数据点 1]
- [数据点 2]
- [连续出现的天数]
- [相关 Coverage Report 链接]

#### 提案
[具体建议怎么改]

#### 预期效果
[改了之后期望看到什么变化]

#### 讨论记录
- YYYY-MM-DD: [讨论要点]
- ...

#### 决策
- **决策日期：** YYYY-MM-DD
- **结果：** Accepted / Rejected / 继续观察
- **原因：** [为什么这么决定]

#### 效果评估（运营两周后填写）
- **实际效果：** [符合预期 / 部分符合 / 不符合]
- **数据变化：** [具体指标变化]
- **经验教训：** [学到了什么]
```

---

## Active Proposals（活跃候选）

_（暂无，运营 1 周后开始填充）_

---

## Rejected Proposals（已否决）

_（暂无，运营后开始积累）_

> 每一个 Rejected 都是一次学费。记录下来，以后就不用再交了。

---

## 已发布的 Policy 版本

| 版本 | 发布日期 | 关联 PEP | 主要变更 | 效果评估 |
|------|----------|----------|----------|----------|
| v1.0 | 2026-07-12 | — | 初始基线 | 待验证 |

---

## Review Cycle 日历

| Cycle | 周期 | 状态 | 发布的 Policy |
|-------|------|------|--------------|
| Cycle 0 | 2026-07-12 ~ 2026-07-25 | 进行中 | v1.0（基线） |
| Cycle 1 | 2026-07-26 ~ 2026-08-08 | 待开始 | （待评估） |
| Cycle 2 | 2026-08-09 ~ 2026-08-22 | 待开始 | （待评估） |

每个 Review Cycle 为两周，最后一天进行：
1. 回顾两周数据
2. 评估现有 Proposals
3. 选择 1-2 个发布（或都不发布）
4. 更新 Editorial Policy 版本号

---

*PEP 体系从 2026-07-12 开始。*
*目标：每个 Cycle 都有清晰的决策记录，不管是做了还是没做。*
