# AI Intelligence Roadmap（路线图）

> 版本：v1.0 | 创建日期：2026-07-06 | 更新频率：每 Sprint 结束后更新

> 参考：[003-AIQL.md](003-AIQL.md)

---

## 设计原则（Design Principles）

参考 [001-Vision.md](001-Vision.md) 中的设计原则章节。

---

## 核心原则

### Question Driven

路线图不是按技术阶段划分（P0/P1/P2），而是按问题划分。

每个 Sprint 的目标是：**回答 AIQL 中的 N 个问题。**

---

## 路线图总览

| Sprint | 问题范围 | 目标问题数 | 时间跨度 |
|--------|---------|-----------|---------|
| **Sprint 1** | Q001-Q020 | 20 | 2周 |
| **Sprint 2** | Q021-Q040 | 20 | 2周 |
| **Sprint 3** | Q041-Q060 | 20 | 2周 |
| **Sprint 4** | Q061-Q080 | 20 | 2周 |
| **Sprint 5** | Q081-Q100 | 20 | 2周 |

**总时间**：10周（约2个半月）

---

## Sprint 1：基础能力查询（Q001-Q020）

### 目标

建立核心数据模型，能够回答基础的能力查询和能力演进问题。

### 必须回答的问题

| ID | Question | Intent |
|----|----------|--------|
| Q001 | 哪些模型支持长期记忆（Long-term Memory）？ | Capability Lookup |
| Q002 | 哪些产品支持 MCP？ | Capability Lookup |
| Q003 | 哪些模型支持自主执行（Autonomous Execution）？ | Capability Lookup |
| Q004 | 哪些产品支持本地部署？ | Capability Lookup |
| Q005 | 哪些模型支持图像理解？ | Capability Lookup |
| Q006 | 哪些模型支持代码生成？ | Capability Lookup |
| Q007 | 哪些产品支持 Web Search？ | Capability Lookup |
| Q008 | 哪些模型支持 Streaming API？ | Capability Lookup |
| Q009 | 哪些产品支持多 Agent 协作？ | Capability Lookup |
| Q010 | 哪些模型支持 Fine-tuning？ | Capability Lookup |
| Q011 | Memory 能力最早是哪个模型推出的？什么时候？ | Evolution |
| Q012 | 过去一年，有多少模型新增了 Memory 能力？ | Evolution |
| Q013 | 哪些能力正在快速普及（过去90天新增最多）？ | Evolution |
| Q014 | 哪些能力开始衰退（过去180天没有新增支持）？ | Evolution |
| Q015 | 哪些能力是最近 30 天首次出现的？ | Evolution |
| Q016 | MCP 支持从出现到成为主流花了多长时间？ | Evolution |
| Q017 | Computer Use 的演化时间线是什么？ | Evolution |
| Q018 | 哪些能力从"仅研究"进入了"产品可用"？ | Evolution |
| Q019 | Anthropic 最近一年新增了哪些核心能力？ | Evolution |
| Q020 | 哪些能力是 OpenAI 先推出，然后其他厂商跟进的？ | Evolution |

### 需要的核心数据模型

| 实体 | 关系 |
|------|------|
| Capability | supports |
| Model | belongs_to Company |
| Product | belongs_to Company |
| Event | acts_on Model/Product |
| Event | changes Capability |
| Fact | （可选，Sprint 2 完善） |

### 里程碑

- [ ] 数据库表结构设计完成
- [ ] 核心实体（Capability/Model/Product/Company/Event）入库
- [ ] 基础查询 API 完成
- [ ] 20 个问题全部可回答

---

## Sprint 2：模型对比与活跃度（Q021-Q040）

### 目标

能够进行模型/产品对比，跟踪活跃度。

### 必须回答的问题

| ID | Question | Intent |
|----|----------|--------|
| Q021 | GPT-4 和 Claude 3.5 在能力上有什么差异？ | Comparison |
| Q022 | 开源模型和闭源模型的能力差距有多大？ | Comparison |
| Q023 | 各模型的"首发能力"有哪些？ | Comparison |
| Q024 | 哪些模型支持完整的 Agent 能力？ | Comparison |
| Q025 | 哪些模型在代码能力上比较突出？ | Comparison |
| Q026 | GPT-4 API 和 Claude API 哪个更便宜？ | Comparison |
| Q027 | 哪个模型的上下文长度最长？ | Comparison |
| Q028 | 哪些模型支持的能力数量最多？ | Comparison |
| Q029 | 某模型最近一年被超越的能力有哪些？ | Comparison |
| Q030 | 有没有模型在某个能力上实现了"弯道超车"？ | Comparison |
| Q031 | 过去 90 天，哪个模型新增能力最多？ | Activity |
| Q032 | 过去 180 天，哪个模型更新最频繁？ | Activity |
| Q033 | 哪个 Agent 产品更新最频繁？ | Activity |
| Q034 | 哪些模型已经"停止更新"？ | Activity |
| Q035 | 最近半年，哪个模型的能力增长最快？ | Activity |
| Q036 | ChatGPT 最近 30 天有哪些更新？ | Activity |
| Q037 | Claude Desktop 最近新增了哪些功能？ | Activity |
| Q038 | 最近 7 天有哪些重要的产品更新？ | Activity |
| Q039 | 某个产品的完整更新历史是什么？ | Activity |
| Q040 | 最近半年新出现了哪些值得关注的 AI 产品？ | Activity |

### 需要的新增数据模型

| 实体 | 关系 |
|------|------|
| Fact | 完善 Fact 层，支持多 Fact 组成 Event |
| Event | score（事件评分） |
| Capability | support_count（支持数量） |

### 里程碑

- [ ] Fact 层完整实现
- [ ] 模型/产品对比 API 完成
- [ ] 活跃度统计 API 完成
- [ ] 20 个问题全部可回答

---

## Sprint 3：趋势分析与开发者生态（Q041-Q060）

### 目标

能够分析趋势，覆盖开发者生态问题。

### 必须回答的问题

| ID | Question | Intent |
|----|----------|--------|
| Q041 | 最近 90 天最热门的 AI 能力是什么？ | Trend |
| Q042 | 过去一年，AI 能力发展的主要方向是什么？ | Trend |
| Q043 | 哪类能力增长最快？ | Trend |
| Q044 | 开源和闭源的发展速度对比如何？ | Trend |
| Q045 | 最近半年，哪些公司最活跃？ | Trend |
| Q046 | 能力更新有季节性规律吗？ | Trend |
| Q047 | 某一年 AI 领域的里程碑事件有哪些？ | Trend |
| Q048 | 哪些能力从"前沿"变成了"标配"？ | Trend |
| Q049 | 行业平均的"能力扩散速度"在变快还是变慢？ | Trend |
| Q050 | 未来 6 个月，最有可能出现的新能力方向是什么？ | Trend |
| Q051 | 哪些 API 最近 30 天有重大更新？ | Developer |
| Q052 | 哪些 SDK 新增了 Structured Output 支持？ | Developer |
| Q053 | 哪些模型有官方 Python SDK？ | Developer |
| Q054 | 哪个模型的 API 降价幅度最大？ | Developer |
| Q055 | 哪些 API 端点被废弃了？什么时候下线？ | Developer |
| Q056 | Embedding 模型有哪些？哪个性能最好？ | Developer |
| Q057 | 最近新增了哪些 AI 开发框架？ | Developer |
| Q058 | 最近半年，开发者工具增长最快的方向是什么？ | Developer |
| Q059 | 哪些平台提供了 AI 能力的 API 接入？ | Developer |
| Q060 | 支持 Fine-tuning 的模型有哪些？最近有新增吗？ | Developer |

### 需要的新增数据模型

| 实体 | 关系 |
|------|------|
| Evolution | 能力演化历史 |
| Benchmark | 评测基准 |
| Pricing | 价格信息 |

### 里程碑

- [ ] Evolution 层完整实现
- [ ] 趋势分析 API 完成
- [ ] 开发者生态数据入库
- [ ] 20 个问题全部可回答

---

## Sprint 4：价格与安全（Q061-Q080）

### 目标

覆盖价格、可用性、安全、故障等问题。

### 必须回答的问题

| ID | Question | Intent |
|----|----------|--------|
| Q061 | 过去 90 天，哪些 API 降价了？幅度多大？ | Pricing |
| Q062 | 最近有哪些模型/产品调整了使用限额？ | Pricing |
| Q063 | 哪些模型/产品在中国大陆可以直接使用？ | Availability |
| Q064 | 最近有哪些地区新开放了 AI 服务？ | Availability |
| Q065 | 免费用户可以用的最强模型是什么？ | Availability |
| Q066 | 某产品历次价格调整的时间线是什么？ | Pricing |
| Q067 | 哪些产品推出了新的定价套餐？ | Pricing |
| Q068 | API 价格整体下降了多少（同比）？ | Pricing |
| Q069 | 有哪些服务暂停或限制了特定地区的访问？ | Availability |
| Q070 | 哪些产品支持免费使用？ | Availability |
| Q071 | 最近 30 天有哪些 AI 服务故障？ | Safety |
| Q072 | OpenAI 最近半年有过几次重大故障？ | Safety |
| Q073 | 哪些模型/产品更新了安全策略？ | Safety |
| Q074 | 最近有哪些安全漏洞被修复？ | Safety |
| Q075 | 哪些产品增加了内容审核或安全护栏？ | Safety |
| Q076 | 过去一年，AI 服务的稳定性是变好还是变差？ | Safety |
| Q077 | 重大故障的平均恢复时间是多少？ | Safety |
| Q078 | 最近有哪些监管政策直接影响了 AI 产品可用性？ | Safety |
| Q079 | 某模型的越狱抵抗能力如何？ | Safety |
| Q080 | 有没有模型被发现有严重的幻觉问题？ | Safety |

### 需要的新增数据模型

| 实体 | 关系 |
|------|------|
| Region | 地区信息 |
| Incident | 故障事件 |
| Security | 安全信息 |

### 里程碑

- [ ] 价格/可用性数据入库
- [ ] 安全/故障数据入库
- [ ] 相关查询 API 完成
- [ ] 20 个问题全部可回答

---

## Sprint 5：公司分析与演化总结（Q081-Q100）

### 目标

完成所有 100 个问题，具备完整的分析能力。

### 必须回答的问题

| ID | Question | Intent |
|----|----------|--------|
| Q081 | OpenAI 的模型产品线有哪些？ | Company |
| Q082 | Anthropic 在 Agent 领域的布局是什么？ | Company |
| Q083 | 某公司的开发者工具有哪些？ | Company |
| Q084 | 哪些公司同时拥有模型和产品？ | Company |
| Q085 | 某公司最近半年重点投入什么能力方向？ | Company |
| Q086 | 哪些公司在多模态领域投入最多？ | Company |
| Q087 | 某公司的 AI 产品有哪些？ | Company |
| Q088 | 哪些公司推出了开源模型？ | Company |
| Q089 | 某公司的 AI 能力演进路线是什么？ | Company |
| Q090 | 哪些公司在 AI 安全领域投入最多？ | Company |
| Q091 | 过去一年，AI 能力最重要的变化是什么？ | Summary |
| Q092 | AI 能力发展的十大里程碑是什么？ | Summary |
| Q093 | 哪些能力正在成为 AI 的"标配"？ | Summary |
| Q094 | AI 能力的扩散速度在变快还是变慢？ | Summary |
| Q095 | 最近一年，Agent 能力的发展趋势是什么？ | Summary |
| Q096 | 哪些能力从"热门"变成了"常规"？ | Summary |
| Q097 | AI 行业的能力演进有什么规律？ | Summary |
| Q098 | 未来 AI 能力发展的三个方向是什么？ | Summary |
| Q099 | AI 能力的"生命周期"是什么样的？ | Summary |
| Q100 | 能力从首次出现到被主流采纳需要多长时间？ | Summary |

### 需要的新增数据模型

| 实体 | 关系 |
|------|------|
| Company | 完善公司分析数据 |
| Knowledge | 从事件归纳的高层知识 |

### 里程碑

- [ ] 公司分析数据完善
- [ ] 演化总结能力完成
- [ ] 100 个问题全部可回答
- [ ] 知识图谱完整建立

---

## 验收标准

每个 Sprint 结束时必须满足：

| 标准 | 说明 |
|------|------|
| **问题回答率** | 本 Sprint 的 20 个问题全部可回答 |
| **数据完整性** | 支撑问题的核心数据已入库 |
| **API 可用性** | 相关查询 API 已完成并可用 |
| **可视化** | 每个问题都有推荐的可视化方式 |
| **可追溯性** | 所有回答都有证据来源 |

---

*文档版本：v1.0*
*创建日期：2026-07-06*
*下次 Review：Sprint 1 结束后（2026-07-20）*
