# Editorial Policy v1.0

> **版本：v1.0**
> **生效日期：2026-07-12**
> **状态：Initial Baseline**

---

## 0. 关于这个文档

### 什么是 Editorial Policy？

Editorial Policy 是 EntropyGate AI 的编辑判断标准。它定义了：

- 什么内容值得关注
- 什么内容优先展示
- 什么样的覆盖是健康的
- 什么样的信号是重要的

它不是代码。它是**判断标准**。

### 为什么版本化？

因为编辑标准会随着运营不断演化。每一次调整都应该有记录、有原因、有效果验证。

```
v1.0 → v1.1 → v1.2 → v2.0 → ...
```

每次版本升级对应：
- 明确的变更原因
- 具体的策略调整
- 预期效果
- （后续）实际效果评估

### 核心原则

> **Policies evolve more often than code.**
>
> 产品应该更多通过调整编辑策略演进，而不是修改程序逻辑。

- 觉得 Research 太多？→ 改 Quota，不改代码
- 觉得 Cursor 很重要？→ 改 Tier，不改 Pipeline
- 觉得 Agent 是热点？→ 改 Topic Weight，不改首页
- 觉得某个 Source 水了？→ 降 Priority，不改 Crawler

---

## 1. Source Tier Policy

定义：每个来源有多重要。

| Tier | 名称 | 含义 | 期望表现 |
|------|------|------|----------|
| S | Essential | 必须覆盖，漏掉就是失职 | 每日必有更新 |
| A | Authoritative | 主要信源，原创报道密度高 | 每周 3+ 条有价值 |
| B | Credible | 可信的补充来源 | 每周 1-2 条有价值 |
| C | Signal | 早期信号，不常出现在首页 | 每月有几条值得看 |
| D | Peripheral | 背景监控 | 偶尔有价值 |

### 当前配置

| Source | Tier | Priority | Type |
|--------|------|----------|------|
| OpenAI Blog | S | Critical | Official |
| Google AI Blog | S | Critical | Official |
| DeepMind Blog | S | Critical | Research |
| Anthropic Blog | A | High | Official |
| Meta AI Blog | A | High | Official |
| Hugging Face Blog | A | High | Community |
| arXiv AI | A | Normal | Research |
| TechCrunch AI | B | Normal | Media |
| AI Frontline | B | Normal | Media |
| Kimi Blog | B | Normal | Official |
| Papers with Code | C | Low | Research |
| The Batch | C | Low | Media |

### 升级/降级规则（待运营验证后细化）

- **连续 14 天** 进入 Top 10 → 考虑升一级
- **连续 14 天** 0 条值得编辑 → 考虑降一级
- **连续 30 天** 0 条值得编辑 → 考虑移出

---

## 2. Topic Taxonomy Policy

定义：我们关注哪些话题，每个话题的优先级。

### 话题列表

| Topic | 优先级 | 每日最低覆盖 | 说明 |
|-------|--------|-------------|------|
| Model Release | Critical | 1 | 新模型发布、版本更新 |
| Reasoning | High | 1 | 推理能力、o1 类进展 |
| Agent | High | 1 | Agent 框架、应用、工具使用 |
| Multimodal | High | 1 | 多模态模型、视频生成 |
| Coding | Normal | 1 | 代码生成、编程助手 |
| MCP | Normal | 0 | 模型上下文协议 |
| Robotics | Normal | 0 | 机器人、具身智能 |
| AI Infra | Normal | 0 | 算力、芯片、训练基础设施 |
| Benchmark | Normal | 0 | 评测基准、排行榜 |
| Open Source | Normal | 0 | 开源模型、开源工具 |
| Safety | Low | 0 | AI 安全、对齐 |
| Policy | Low | 0 | 监管政策、法律法规 |
| Funding | Low | 0 | 融资、商业动态 |
| Video Generation | High | 0 | 视频生成（与 Multimodal 部分重叠，更聚焦） |

### 话题归属规则（待验证）

- 每篇文章默认归属 1-3 个话题
- 主要话题（Primary Topic）只有一个
- 话题归属初期由 Source 绑定推断，后期可引入 AI 分类

---

## 3. Source Type Policy

定义：来源类型的健康比例。

| Type | 含义 | 目标占比 | 最低占比 | 最高占比 |
|------|------|----------|----------|----------|
| Official | 官方博客/公告 | 40% | 30% | 60% |
| Research | 论文/研究机构 | 15% | 10% | 25% |
| Media | 科技媒体 | 20% | 10% | 30% |
| Community | 社区/论坛 | 10% | 5% | 20% |
| Developer | GitHub/SDK/Changelog | 10% | 5% | 15% |
| Social | 社交媒体 | 3% | 0% | 10% |
| Documentation | 文档变更 | 2% | 0% | 5% |

### 判断标准

- 低于最低占比 → Coverage Gap
- 高于最高占比 → Coverage Imbalance
- 在目标范围内 → Healthy

---

## 4. Priority Scheduling Policy

定义：采集频率由什么决定。

### 基础优先级

| Priority | 采集间隔 | 适用 |
|----------|----------|------|
| Critical | 5 min | S-Tier 官方源 |
| High | 15 min | A-Tier 主要信源 |
| Normal | 30 min | B-Tier 标准节奏 |
| Low | 120 min | C/D-Tier 背景监控 |

### Calendar 事件期间调整

- 事件匹配的 Source → 提升到 Critical（5 min）
- 事件匹配的 Topic → 标记为 active，weight 临时翻倍
- 事件结束后 24 小时 → 恢复原优先级

### 健康度影响

- Source 连续 3 次失败 → 间隔翻倍（降级一档）
- Source 连续 3 次成功 → 恢复原间隔

---

## 5. Editorial Calendar Policy

定义：哪些事件需要特别关注。

### 事件类型

| 类型 | 优先级 | 提前准备 |
|------|--------|----------|
| 厂商发布会 | Critical | 提前 3 天 |
| 顶会（NeurIPS/ICML等） | High | 提前 1 周 |
| 行业大会（WAIC等） | High | 提前 3 天 |
| 定期报告（State of AI等） | Normal | 提前 1 周 |

### 当前日历

| 事件 | 类型 | 时间（示例） | 关联 Source | 关联 Topic |
|------|------|-------------|-------------|-----------|
| OpenAI DevDay | 厂商发布 | 每年约 11月 | OpenAI | Model Release, Agent |
| Google I/O | 厂商发布 | 每年约 5月 | Google | Model Release, Multimodal |
| NeurIPS | 顶会 | 每年 12月 | DeepMind, arXiv | Research, Benchmark |
| ICML | 顶会 | 每年 7月 | DeepMind, arXiv | Research |
| WAIC | 行业大会 | 每年 7月 | （中文源） | Policy, Industry |
| WWDC | 厂商发布 | 每年 6月 | （Apple相关） | Multimodal, AI Infra |

---

## 6. Freshness Policy

定义：内容的新鲜度分级。

| Band | 时间窗口 | 显示权重 | 含义 |
|------|----------|----------|------|
| Hot | < 2h | 2.0x | 突发，正在发生 |
| Warm | < 24h | 1.5x | 今天的新闻 |
| Fresh | < 3d | 1.0x | 本周值得看 |
| Archive | < 7d | 0.5x | 背景资料 |
| Stale | > 7d | 0.2x | 已过时 |

### 应用场景

- 首页排序：Freshness × Editorial Score
- Hot 标记：< 2h 的 High+ 重要性文章
- Story 持续更新：同一 Story 48 小时内持续追踪

---

## 7. Editorial Quota Policy

定义：每日报道的健康结构目标。

### 类型配额

| 维度 | 目标 | 最低 | 最高 |
|------|------|------|------|
| Official 占比 | 40% | 30% | 60% |
| Research 占比 | 15% | 10% | 25% |
| 中文内容占比 | 30% | 20% | 50% |
| 英文内容占比 | 50% | 40% | 70% |

### Topic 最低保障

- Model Release: ≥ 1 条/天
- Agent: ≥ 1 条/天
- Reasoning: ≥ 1 条/天
- Coding: ≥ 1 条/天

### 首页结构（目标，非硬性）

```
Top Story:    1 条  (Hot + Critical Importance)
Major Stories: 3-5 条 (Warm + High Importance)
Regular:      8-12 条 (Fresh + Normal Importance)
Background:   3-5 条  (Archive + Low Importance)
```

---

## 8. Coverage Policy

定义：什么算 "覆盖到了"，什么算 "漏掉了"。

### Coverage 指标

| 指标 | 计算方式 | 健康阈值 |
|------|----------|----------|
| Source Coverage | 有更新的 S+A Tier Source / 总数 | ≥ 80% |
| Topic Coverage | 达到最低保障的 Topic / 总数 | ≥ 70% |
| Type Balance | 类型占比在目标范围内的项数 | ≥ 80% |
| Language Balance | 中英文都达到最低占比 | Yes/No |

### Gap 分级

| 级别 | 含义 | 响应 |
|------|------|------|
| Critical | S-Tier Source 全天无更新 | 人工检查是否源挂了 |
| High | Critical Topic 全天 0 条 | 第二天重点关注 |
| Normal | Type 比例偏离目标 | 观察是否连续出现 |
| Low | C/D-Tier Source 无更新 | 不处理 |

---

## 9. Editorial Scoring Policy（初始基线）

定义：一篇文章的编辑价值如何评分。

### 评分维度（v1.0 简化版）

| 维度 | 权重 | 说明 |
|------|------|------|
| Source Tier | 30% | S=100, A=80, B=60, C=40, D=20 |
| Source Type | 15% | Official=100, Research=80, Media=60, Developer=60, Community=40 |
| Topic Priority | 25% | Critical=100, High=80, Normal=60, Low=30 |
| Freshness | 20% | Hot=100, Warm=80, Fresh=60, Archive=30, Stale=10 |
| Novelty（待实现） | 10% | 是否是新故事/新进展 |

### Bucket 划分

| Score | Bucket | 展示位置 |
|-------|--------|----------|
| 85+ | Top | 首页顶部/推荐 |
| 70-84 | Major | 首页主要区域 |
| 55-69 | Regular | 首页常规列表 |
| 40-54 | Minor | 折叠/次级页面 |
| < 40 | Noise | 不展示 |

---

## 10. Version History

### v1.0 (2026-07-12) — Initial Baseline

**状态：** 初始版本，未经运营验证

**包含：**
- Source Tier Policy (S/A/B/C/D)
- Topic Taxonomy (13 个话题)
- Source Type Policy (7 种类型 + 目标比例)
- Priority Scheduling (Critical/High/Normal/Low)
- Editorial Calendar (6 个预置事件)
- Freshness Bands (Hot/Warm/Fresh/Archive/Stale)
- Editorial Quota (类型/语言/Topic 配额)
- Coverage Policy (Gap 分级)
- Editorial Scoring (5 维度)

**待验证：**
- 所有比例目标是否合理
- Topic 分类是否需要调整
- Source Tier 是否准确
- Scoring 权重是否符合编辑直觉

---

## 11. Change Log Template

未来版本更新按此格式记录：

```
### vX.Y (YYYY-MM-DD) — [简短描述]

**状态：** [Active / Draft / Deprecated]

**变更原因：**
- [为什么改]

**具体调整：**
- [Source Tier] xxx 从 A 降为 B
- [Topic] 新增 xxx Topic，优先级 Normal
- [Quota] Research 最高占比从 25% 降为 20%
- [Scoring] Source Type 权重从 15% 调整为 20%

**预期效果：**
- [期望看到什么变化]

**实际效果（运营后填写）：**
- [两周后评估结果]
```

---

*文档版本：v1.0 | 生效日期：2026-07-12 | 下次评估：2026-07-26（两周后）*
