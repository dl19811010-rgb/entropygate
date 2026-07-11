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

### EOS vs Story Builder（未来）

Story Builder 是**把多篇文章组织成故事**：
- GPT-5 发布 → 相关报道 → 持续追踪 → 形成 Story

EOS 是**观察故事覆盖情况**：
- Foundation Model Race 这个 Story 今天有新进展吗？
- Agent 这个 Story 今天有几条 signal？

关系：Story Builder 是 EOS 的下一层，EOS 为 Story Builder 提供覆盖度数据。

---

## 7. North Star

EOS 的北极星指标不是"采集了多少篇"。

而是：

> **编辑打开 Coverage Report 后，能不能马上知道今天该关注什么。**

如果编辑每天看一眼 Coverage Report，就知道：
- 今天哪些公司有动作
- 哪些话题没覆盖到
- 报道结构健不健康
- 对今天的报道有没有信心

那 EOS 就成功了。

---

## 8. Roadmap

### v1.0（当前）— 观察闭环

- ✅ Source Registry（Tier / Type / Topic / Priority）
- ✅ Priority Scheduler
- ✅ Editorial Calendar
- ✅ Freshness Bands
- ✅ Editorial Quota
- ✅ Coverage Report (by source_type / language / topic / freshness)

### v1.1 — 竞争力视角

- Layer 9: Story Coverage（按故事线看覆盖，不是按 Topic）
- Layer 10: Competitive Coverage（每个主要玩家今天有没有消息）
- Layer 11: Editorial Confidence（今天的报道可信度有多高）

### v1.2 — 噪音率优化

- Editorial Noise Rate（值得看的 / 总采集数）
- Missed Story 追踪（重要事件是否被捕捉到）

### v2.0 — 学习闭环

- 从编辑操作中学习（哪些被置顶 = 重要）
- 自动调整 Source Priority
- 自动推荐 Gap 补全

---

*文档版本：v1.0 | 最后更新：2026-07-12*
