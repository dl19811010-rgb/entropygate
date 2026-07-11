# Editorial Observation System (EOS)

> **EOS 不是一个爬虫。它是编辑部的观察系统。**

---

## 1. Why — 为什么存在

传统的新闻聚合平台的思路是：

```
尽可能多的源 → 尽可能多的文章 → 用户自己看
```

这个思路的问题是：**它回答的是"有什么"，而不是"缺什么"。**

编辑部每天真正关心的问题是：

> 今天有没有漏掉什么重要的事？

EOS 的存在就是为了回答这个问题。它从"采了多少"转向"覆盖得怎么样"，从"爬虫能力"转向"编辑观察能力"。

EOS 的核心使命：

> **Build the observation layer for an AI newsroom.**

---

## 2. Questions — 它回答哪些问题

EOS 设计为回答以下编辑日常问题：

| 问题 | 对应能力 |
|------|----------|
| 今天有哪些重要消息？ | Editorial Scoring + Freshness |
| 今天漏掉了什么？ | Coverage Report + Gaps |
| 各个公司/实验室今天有动静吗？ | Source Registry + Competitive Coverage |
| 这个消息有多新鲜？ | Freshness Bands |
| 今天的报道结构健康吗？ | Editorial Quota |
| 接下来什么事件值得关注？ | Editorial Calendar |
| 今天对报道有信心吗？ | Editorial Confidence |
| 哪些是噪音，哪些值得看？ | Editorial Noise Rate |

如果一个问题无法用上面任何一个回答，那它可能不属于 EOS 的范畴。

---

## 3. Architecture — 八层模型

```
Layer 8   Coverage Report     ← 今天有没有漏掉什么？
Layer 7   Freshness Bands     ← 这条消息有多新鲜？
Layer 6   Editorial Quota     ← 今天的报道结构合理吗？
Layer 5   Editorial Calendar  ← 有什么事件需要特别关注？
Layer 4   Priority Scheduler  ← 什么时候去采？
Layer 3   Source Type         ← 这是什么类型的来源？
Layer 2   Topic Taxonomy      ← 这属于什么话题？
Layer 1   Source Tier         ← 这个来源有多重要？
```

**从下往上读：** 越底层越偏向"技术配置"，越上层越偏向"编辑判断"。

**数据流方向：** 自下而上 — Source → Scheduler → Crawl → Score → Coverage → Observation。

---

## 4. Responsibilities — 每层职责

### Layer 1: Source Tier

**回答：** 这个来源有多重要？

| Tier | 名称 | 含义 |
|------|------|------|
| S | Essential | 必须覆盖，漏掉就是失职 |
| A | Authoritative | 主要信源，原创报道密度高 |
| B | Credible | 可信的补充来源 |
| C | Signal | 早期信号，不常出现在首页 |
| D | Peripheral | 背景监控 |

**输入：** 人工编辑评级
**输出：** source.editorial_tier

---

### Layer 2: Topic Taxonomy

**回答：** 这条新闻属于什么话题？

固定话题分类（编辑视角，不是技术分类）：

- Model Release, Reasoning, Agent, MCP
- Video Generation, Robotics, Coding
- Multimodal, AI Infra, Benchmark
- Open Source, Safety, Policy, Funding

每个 Topic 有：
- 优先级（critical / high / normal / low）
- 每日最低覆盖数（min_daily_articles）

**输入：** Source.topics 字段（每个来源绑定 3-8 个话题）
**输出：** by_topic 覆盖统计

---

### Layer 3: Source Type

**回答：** 这是什么类型的来源？

| Type | 含义 | 首页占比参考 |
|------|------|-------------|
| Official | 官方博客/公告 | ≥ 40% |
| Research | 论文/研究机构 | 10-20% |
| Media | 科技媒体 | 10-25% |
| Community | 社区/论坛 | 5-15% |
| Developer | GitHub/SDK/Changelog | 5-15% |
| Social | 社交媒体 | ≤ 10% |
| Documentation | 文档变更 | ≤ 5% |

**为什么重要：** 防止首页变成"全是论文"或"全是媒体报道"，保证报道结构稳定。

---

### Layer 4: Priority Scheduler

**回答：** 什么时候去采？

不是按 Tier 固定时间，而是按 Priority 动态调度：

| Priority | 间隔 | 适用场景 |
|----------|------|----------|
| Critical | 5 min | 重要事件期间、官方发布 |
| High | 15 min | 主要信源日常监控 |
| Normal | 30 min | 标准节奏 |
| Low | 120 min | 背景监控 |

Priority 不是固定值。Editorial Calendar 事件期间，相关 Source 的 Priority 会自动提升。

**未来方向：** Webhook / RSS 更新检测 → 立即触发，不等 Scheduler。

---

### Layer 5: Editorial Calendar

**回答：** 有什么事件需要特别关注？

重大会议、发布会期间，自动提升采集频率：

```
NeurIPS 期间
  → arXiv: normal → critical (30min → 5min)
  → DeepMind: critical → critical (保持)
  → 相关 Topic 全部标记为 active
```

已预置的事件类型：
- 学术会议：NeurIPS, ICML, CVPR, ICLR
- 厂商大会：Google I/O, OpenAI DevDay, WWDC
- 行业活动：WAIC, SIGGRAPH

---

### Layer 6: Editorial Quota

**回答：** 今天的报道结构合理吗？

每天的报道应该有稳定的结构，不是碰运气：

```
Source Type 比例：
  Official     ≥ 40%
  Research     10-20%
  Media        10-25%
  Community    5-15%

语言分布：
  中文         ≥ 30%
  英文         ≥ 30%

Topic 最低保障：
  Model Release  ≥ 1 条/天
  Agent          ≥ 1 条/天
  Reasoning      ≥ 1 条/天
  Coding         ≥ 1 条/天
```

Quota 是目标，不是硬性限制。它的作用是让 Coverage Report 有判断标准。

---

### Layer 7: Freshness Bands

**回答：** 这条消息有多新鲜？

| Band | 时间窗口 | 颜色 | 含义 |
|------|----------|------|------|
| Hot | < 2h | 🔴 Red | 突发，正在发生 |
| Warm | < 24h | 🟠 Orange | 今天的新闻 |
| Fresh | < 3d | 🟢 Green | 本周值得看 |
| Archive | < 7d | ⚪ Gray | 背景资料 |
| Stale | > 7d | ⚫ Dark | 已过时 |

**为什么用 5 档：** 编辑做版时会天然按"热/温/凉/旧"来排优先级，这是编辑的思维模型。

---

### Layer 8: Coverage Report

**回答：** 今天有没有漏掉什么？

这是 EOS 最顶层的输出。每天自动生成，核心是 **Gap List**：

```
今天的 Gap：
  ⚠️  Meta 今天没有更新
  ⚠️  Robotics 话题 0 条
  ⚠️  Research 类型只有 7%（目标 ≥ 10%）
  ⚠️  中文内容 22%（目标 ≥ 30%）
```

Coverage Report 不告诉你"采到了多少"，它告诉你"还差什么"。

---

## 5. Input / Output

### 输入

| 输入 | 来源 | 形式 |
|------|------|------|
| Source 配置 | 人工 + 种子数据 | DB: sources 表 |
| Topic 分类 | 编辑策略配置 | editorial_policy.py |
| Quota 规则 | 编辑策略配置 | editorial_policy.py |
| 日历事件 | 人工录入 | DB: editorial_calendar |
| 文章数据 | Crawler 抓取 | DB: articles 表 |

### 输出

| 输出 | 形式 | 消费者 |
|------|------|--------|
| 每日 Coverage Report | JSON API | Dashboard, 编辑晨会 |
| Topic 热度分布 | JSON API | 首页推荐, Trend Dashboard |
| Freshness 标签 | 每篇文章属性 | Story Builder, 排序 |
| Gap List | JSON + 日志 | 编辑手动补漏 |
| Scheduler 状态 | JSON API | 运维, 调试 |

---

## 6. Boundaries — 与其他模块的边界

### EOS vs Runtime

```
Runtime = 执行（Execute）
EOS     = 观察（Observe）
```

EOS 不负责：
- 文章的存储和检索（Runtime）
- 用户认证和权限（Runtime）
- API 接口框架（Runtime）

EOS 负责：
- 观察采集是否充分
- 观察覆盖是否均衡
- 观察健康度和信心

### EOS vs Editorial Service

Editorial Service 是**单篇文章的评分**：
- 这篇文章值多少分？
- 应该分到哪个 bucket？

EOS 是**整体覆盖的观察**：
- 今天的报道结构怎么样？
- 有没有漏掉什么？

关系：Editorial Service 是 EOS 的输入之一。

### EOS vs Editorial Policy

EOS 是**测量仪器**：
- 今天发生了什么？
- 覆盖得怎么样？
- 有哪些 Gap？

Editorial Policy 是**判断标准**：
- 什么算重要？
- 什么比例算健康？
- 什么频率合适？

关系：EOS 产出数据，Policy 定义标准。两者一起驱动编辑运营。

> **P7: Policies evolve more often than code.**
>
> 产品应该更多通过调整编辑策略演进，而不是修改程序逻辑。

- 觉得 Research 太多？→ 改 Quota，不改代码
- 觉得某个 Source 很重要？→ 改 Tier，不改 Crawler
- 觉得某个 Topic 热了？→ 改 Topic Weight，不改首页排序逻辑

---

### EOS vs Narrative Engine（未来）

Narrative Engine 是**把多条信号组织成观点**：
- "今天 AI 世界最重要的变化：Agent 正在成为默认的软件交互方式"
- 把 OpenAI、Anthropic、Cursor 的三条新闻，变成一个 Narrative

EOS 是**观察和测量**：
- 今天有多少条 Agent 相关的信号？
- Agent 连续多少天是 Top Topic？
- 支撑这个 Narrative 的证据够不够？

关系：Narrative Engine 建立在 EOS 之上。没有稳定的观察，就没有可信的叙事。

---

## 7. The Evolution Path — 从观察到标准

EOS 不是终点。它是整个编辑体系的起点。

```
Phase 1: Observation（观察）
    EOS v1.0 上线
    每天记录 Coverage / Gaps / Noise Rate
    ↓ 2 周

Phase 2: Evidence（证据）
    积累足够多的日常观察
    识别 Repeated Patterns
    ↓ 连续出现 7 天

Phase 3: Policy Evolution（策略演化）
    把 Repeated Pattern 升级为 Editorial Standard
    发布 Editorial Policy v1.1 / v1.2
    ↓ 持续迭代

Phase 4: Editorial Confidence（编辑信心）
    编辑标准稳定下来
    可以回答"为什么今天首页是这样的"
    ↓ 标准足够稳定后

Phase 5: Narrative（叙事）
    基于稳定的编辑标准
    构建 Editorial Narrative Engine
    从"今天发生了什么"到"今天为什么重要"
```

**核心判断：EOS v1.0 不是 Discovery 的结束，而是 Discovery 的测量仪器。**

---

## 8. North Star

EOS 的北极星指标不是"采集了多少篇"。

而是：

> **编辑打开 Coverage Report 后，能不能马上知道今天该关注什么。**

如果编辑每天看一眼 Coverage Report，就知道：
- 今天哪些公司有动作
- 哪些话题没覆盖到
- 报道结构健不健康
- 对今天的报道有没有信心

那 EOS 就成功了。

**更大的北极星：**

> 连续运营两周后，我们能不能说清楚：为什么今天首页是这样的？
>
> （答案应该指向 Editorial Policy，而不是"改了代码"。）

---

## 9. Roadmap

### 当前阶段：Observation Era（观察期）

**目标：** 让 EOS 连续运行，积累运营数据，验证 Editorial Policy v1.0。

**时长：** 至少 2 周（Day 0: 2026-07-12）

**不做什么：**
- 不新增 Layer
- 不加新数据源
- 不改架构

**做什么：**
- 每天记录运营观察
- 跟踪关键指标趋势
- 识别 Repeated Patterns
- 积累 Policy Change Candidates

---

### 下一阶段：Policy Evolution Era

**触发条件：** 连续运营 2 周，积累了足够的 Pattern

**产出：**
- Editorial Policy v1.1（第一次基于数据的策略调整）
- 确认哪些 Tier/Topic/Quota 是对的，哪些需要调
- 建立 "Observation → Evidence → Pattern → Policy" 的迭代节奏

---

### 远期：Narrative Era

**触发条件：** Editorial Policy 稳定（至少迭代 3 个版本）

**方向：**
- Editorial Narrative Engine
- 从"今天发生了什么"到"今天为什么重要"
- 这时候做 ENE 才有意义，因为它建立在经过验证的编辑标准之上

---

*文档版本：v1.1 | 最后更新：2026-07-12*
*更新内容：加入 P7 原则、演进路径、重新定义 Roadmap（观察期优先）*
