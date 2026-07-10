# AI Intelligence Question Library（AIQL）

> 版本：v1.0 | 创建日期：2026-07-06 | 更新频率：每季度 Review

> 参考：[002-AIS.md](002-AIS.md)

---

## 设计原则（Design Principles）

参考 [001-Vision.md](001-Vision.md) 中的设计原则章节。

---

## 问题格式规范

每个问题必须包含以下字段：

| 字段 | 说明 | 示例 |
|------|------|------|
| **Question ID** | 唯一标识符 | Q001 |
| **Question** | 问题原文 | 哪些模型支持长期记忆？ |
| **Intent** | 问题意图分类 | Capability Lookup |
| **Knowledge Needed** | 需要的知识类型 | Model + Capability + supports |
| **Difficulty** | 难度（1-4星） | ⭐ |
| **Priority** | 优先级（P0-P3） | P0 |
| **Visualization** | 推荐的可视化方式 | Table / Timeline / Comparison |

---

## Category 1: Capability Lookup（能力查询）

| ID | Question | Intent | Knowledge Needed | Difficulty | Priority | Visualization |
|----|----------|--------|------------------|------------|----------|---------------|
| Q001 | 哪些模型支持长期记忆（Long-term Memory）？ | Capability Lookup | Model + Capability + supports | ⭐ | P0 | Table |
| Q002 | 哪些产品支持 MCP？ | Capability Lookup | Product + Capability (tool-use.mcp.*) | ⭐ | P0 | Table |
| Q003 | 哪些模型支持自主执行（Autonomous Execution）？ | Capability Lookup | Model + Capability (agent.autonomous.execution) | ⭐ | P0 | Table |
| Q004 | 哪些产品支持本地部署？ | Capability Lookup | Product + Capability (deployment.local.*) | ⭐ | P1 | Table |
| Q005 | 哪些模型支持图像理解？ | Capability Lookup | Model + Capability (multimodal.vision.understanding) | ⭐ | P0 | Table |
| Q006 | 哪些模型支持代码生成？ | Capability Lookup | Model + Capability (reasoning.code.generation) | ⭐ | P0 | Table |
| Q007 | 哪些产品支持 Web Search？ | Capability Lookup | Product + Capability (tool-use.browser.search) | ⭐ | P1 | Table |
| Q008 | 哪些模型支持 Streaming API？ | Capability Lookup | Model + Capability (integration.api.streaming) | ⭐ | P1 | Table |
| Q009 | 哪些产品支持多 Agent 协作？ | Capability Lookup | Product + Capability (agent.multi-agent.*) | ⭐ | P1 | Table |
| Q010 | 哪些模型支持 Fine-tuning？ | Capability Lookup | Model + Capability (developer.fine-tuning.*) | ⭐ | P1 | Table |

---

## Category 2: Capability Evolution（能力演进）

| ID | Question | Intent | Knowledge Needed | Difficulty | Priority | Visualization |
|----|----------|--------|------------------|------------|----------|---------------|
| Q011 | Memory 能力最早是哪个模型推出的？什么时候？ | Evolution | Capability + first_seen + Event | ⭐ | P0 | Timeline |
| Q012 | 过去一年，有多少模型新增了 Memory 能力？ | Evolution | Capability + Event (feature-added) + 时间 | ⭐⭐ | P1 | Chart |
| Q013 | 哪些能力正在快速普及（过去90天新增最多）？ | Evolution | Capability + Event 频率统计 | ⭐⭐ | P1 | Chart |
| Q014 | 哪些能力开始衰退（过去180天没有新增支持）？ | Evolution | Capability + Event 频率趋势 | ⭐⭐ | P2 | Chart |
| Q015 | 哪些能力是最近 30 天首次出现的？ | Evolution | Capability + first_seen + 时间过滤 | ⭐ | P1 | Table |
| Q016 | MCP 支持从出现到成为主流花了多长时间？ | Evolution | Capability + 时间 + 支持数量变化 | ⭐⭐ | P2 | Timeline |
| Q017 | Computer Use 的演化时间线是什么？ | Evolution | Capability + Event 时间序列 | ⭐⭐ | P1 | Timeline |
| Q018 | 哪些能力从"仅研究"进入了"产品可用"？ | Evolution | Capability + maturity 变化 | ⭐⭐ | P2 | Table |
| Q019 | Anthropic 最近一年新增了哪些核心能力？ | Evolution | Company + Capability + Event + 时间 | ⭐⭐ | P0 | Table |
| Q020 | 哪些能力是 OpenAI 先推出，然后其他厂商跟进的？ | Evolution | Capability + first_seen + 公司对比 | ⭐⭐⭐ | P2 | Timeline |

---

## Category 3: Model Comparison（模型对比）

| ID | Question | Intent | Knowledge Needed | Difficulty | Priority | Visualization |
|----|----------|--------|------------------|------------|----------|---------------|
| Q021 | GPT-4 和 Claude 3.5 在能力上有什么差异？ | Comparison | Model × Model + Capability 对比 | ⭐⭐ | P0 | Comparison Table |
| Q022 | 开源模型和闭源模型的能力差距有多大？ | Comparison | Model (开源/闭源) + Capability 对比 | ⭐⭐⭐ | P2 | Comparison Table |
| Q023 | 各模型的"首发能力"有哪些？ | Comparison | Model + Capability + first_seen | ⭐⭐ | P2 | Table |
| Q024 | 哪些模型支持完整的 Agent 能力（自主执行 + 工具调用 + 记忆）？ | Comparison | Model + 多 Capability 组合 | ⭐⭐ | P1 | Table |
| Q025 | 哪些模型在代码能力上比较突出？ | Comparison | Model + Capability + Benchmark | ⭐⭐ | P2 | Table |
| Q026 | GPT-4 API 和 Claude API 哪个更便宜？ | Comparison | Product × Product + 价格对比 | ⭐⭐ | P1 | Comparison Table |
| Q027 | 哪个模型的上下文长度最长？ | Comparison | Model + Capability (performance.scale.context) | ⭐ | P0 | Table |
| Q028 | 哪些模型支持的能力数量最多？ | Comparison | Model + Capability 计数排序 | ⭐ | P1 | Table |
| Q029 | 某模型（如 Claude）最近一年被超越的能力有哪些？ | Comparison | Model + Capability + 时间 + 对比 | ⭐⭐⭐ | P3 | Table |
| Q030 | 有没有模型在某个能力上实现了"弯道超车"？ | Comparison | Model + Capability 趋势对比 | ⭐⭐⭐ | P3 | Chart |

---

## Category 4: Model/Product Activity（模型/产品活跃度）

| ID | Question | Intent | Knowledge Needed | Difficulty | Priority | Visualization |
|----|----------|--------|------------------|------------|----------|---------------|
| Q031 | 过去 90 天，哪个模型新增能力最多？ | Activity | Model + Event (feature-added) 计数 | ⭐⭐ | P0 | Chart |
| Q032 | 过去 180 天，哪个模型更新最频繁？ | Activity | Model + Event 频率统计 | ⭐ | P1 | Chart |
| Q033 | 哪个 Agent 产品更新最频繁？ | Activity | Product + Event 频率统计 | ⭐ | P1 | Chart |
| Q034 | 哪些模型已经"停止更新"（超过6个月没有能力更新）？ | Activity | Model + Event 最后更新时间 | ⭐ | P2 | Table |
| Q035 | 最近半年，哪个模型的能力增长最快？ | Activity | Model + Capability 增长速度 | ⭐⭐ | P1 | Chart |
| Q036 | ChatGPT 最近 30 天有哪些更新？ | Activity | Product + Event + 时间过滤 | ⭐ | P0 | Timeline |
| Q037 | Claude Desktop 最近新增了哪些功能？ | Activity | Product + Event + 时间过滤 | ⭐ | P0 | Timeline |
| Q038 | 最近 7 天有哪些重要的产品更新？ | Activity | Product + Event + 时间 + high score | ⭐ | P0 | List |
| Q039 | 某个产品（如 Notion AI）的完整更新历史是什么？ | Activity | Product + Event 时间线 | ⭐⭐ | P1 | Timeline |
| Q040 | 最近半年新出现了哪些值得关注的 AI 产品？ | Activity | Product + first_seen + 时间 + score | ⭐⭐ | P1 | Table |

---

## Category 5: Trend Analysis（趋势分析）

| ID | Question | Intent | Knowledge Needed | Difficulty | Priority | Visualization |
|----|----------|--------|------------------|------------|----------|---------------|
| Q041 | 最近 90 天最热门的 AI 能力是什么？ | Trend | Capability + Event 频率 + 趋势 | ⭐⭐ | P0 | Chart |
| Q042 | 过去一年，AI 能力发展的主要方向是什么？ | Trend | Capability + Event 年度统计 + 分类 | ⭐⭐ | P1 | Chart |
| Q043 | 哪类能力增长最快（推理/多模态/Agent/工具调用）？ | Trend | Capability Domain + 增长速度对比 | ⭐⭐ | P1 | Chart |
| Q044 | 开源和闭源的发展速度对比如何？ | Trend | Model (开源/闭源) + Event 频率对比 | ⭐⭐ | P2 | Chart |
| Q045 | 最近半年，哪些公司最活跃（发布更新最多）？ | Trend | Company + Event 计数排序 | ⭐ | P1 | Chart |
| Q046 | 能力更新有季节性规律吗？ | Trend | Event + 时间序列分析 | ⭐⭐⭐ | P3 | Chart |
| Q047 | 某一年（如2025年）AI 领域的里程碑事件有哪些？ | Trend | Event + 年度 + high score | ⭐⭐ | P1 | Timeline |
| Q048 | 哪些能力从"前沿"变成了"标配"？ | Trend | Capability + 支持数量阈值 + 时间 | ⭐⭐⭐ | P2 | Table |
| Q049 | 行业平均的"能力扩散速度"在变快还是变慢？ | Trend | Capability + 扩散速度 + 年度对比 | ⭐⭐⭐ | P3 | Chart |
| Q050 | 未来 6 个月，最有可能出现的新能力方向是什么？ | Trend | Trend prediction | ⭐⭐⭐⭐ | P3 | Text |

---

## Category 6: Developer Ecosystem（开发者生态）

| ID | Question | Intent | Knowledge Needed | Difficulty | Priority | Visualization |
|----|----------|--------|------------------|------------|----------|---------------|
| Q051 | 哪些 API 最近 30 天有重大更新？ | Developer | Product + Event (api-added/api-changed) + 时间 | ⭐ | P0 | List |
| Q052 | 哪些 SDK 新增了 Structured Output 支持？ | Developer | Product + Capability (interaction.output.structured) | ⭐ | P1 | Table |
| Q053 | 哪些模型有官方 Python SDK？ | Developer | Model + Product (SDK) + supports | ⭐ | P1 | Table |
| Q054 | 哪个模型的 API 降价幅度最大？ | Developer | Model + Event (pricing-changed) + 幅度 | ⭐⭐ | P1 | Table |
| Q055 | 哪些 API 端点被废弃了？什么时候下线？ | Developer | Product + Event (api-deprecated) + 时间 | ⭐ | P1 | Table |
| Q056 | Embedding 模型有哪些？哪个性能最好？ | Developer | Model + Capability + Benchmark | ⭐⭐ | P2 | Table |
| Q057 | 最近新增了哪些 AI 开发框架？ | Developer | Entity (framework) + first_seen + 时间 | ⭐ | P2 | Table |
| Q058 | 最近半年，开发者工具增长最快的方向是什么？ | Developer | Capability (developer.*) + 增长趋势 | ⭐⭐ | P2 | Chart |
| Q059 | 哪些平台提供了 AI 能力的 API 接入？ | Developer | Product + Capability (integration.api.rest) | ⭐ | P1 | Table |
| Q060 | 支持 Fine-tuning 的模型有哪些？最近有新增吗？ | Developer | Model + Capability + Event + 时间 | ⭐⭐ | P2 | Table |

---

## Category 7: Pricing & Availability（价格与可用性）

| ID | Question | Intent | Knowledge Needed | Difficulty | Priority | Visualization |
|----|----------|--------|------------------|------------|----------|---------------|
| Q061 | 过去 90 天，哪些 API 降价了？幅度多大？ | Pricing | Product + Event (pricing-changed) + 降价 + 时间 | ⭐⭐ | P0 | Table |
| Q062 | 最近有哪些模型/产品调整了使用限额？ | Pricing | Product + Event (limitation-changed) + 时间 | ⭐ | P1 | Table |
| Q063 | 哪些模型/产品在中国大陆可以直接使用？ | Availability | Model/Product + Region | ⭐⭐ | P1 | Table |
| Q064 | 最近有哪些地区新开放了 AI 服务？ | Availability | Event (availability-expanded) + region + 时间 | ⭐ | P1 | Map |
| Q065 | 免费用户可以用的最强模型是什么？ | Availability | Model + affected_users (free) + capability 排序 | ⭐⭐ | P1 | Table |
| Q066 | 某产品（如 ChatGPT）历次价格调整的时间线是什么？ | Pricing | Product + Event (pricing-changed) 时间线 | ⭐ | P2 | Timeline |
| Q067 | 哪些产品推出了新的定价套餐？ | Pricing | Product + Event (pricing-changed) + new plan | ⭐ | P2 | Table |
| Q068 | API 价格整体下降了多少（同比）？ | Pricing | Event (pricing-changed) + 年度统计 | ⭐⭐⭐ | P3 | Chart |
| Q069 | 有哪些服务暂停或限制了特定地区的访问？ | Availability | Event (availability-restricted) + region | ⭐ | P1 | Table |
| Q070 | 哪些产品支持免费使用？ | Availability | Product + Pricing (free tier) | ⭐ | P1 | Table |

---

## Category 8: Safety & Incidents（安全与故障）

| ID | Question | Intent | Knowledge Needed | Difficulty | Priority | Visualization |
|----|----------|--------|------------------|------------|----------|---------------|
| Q071 | 最近 30 天有哪些 AI 服务故障？ | Safety | Product + Event (incident) + 时间 | ⭐ | P1 | List |
| Q072 | OpenAI 最近半年有过几次重大故障？ | Safety | Company + Event (incident) 计数 | ⭐ | P2 | Chart |
| Q073 | 哪些模型/产品更新了安全策略？ | Safety | Product + Event (security-update) + 时间 | ⭐ | P1 | Table |
| Q074 | 最近有哪些安全漏洞被修复？ | Safety | Event (security-update) + 漏洞描述 | ⭐⭐ | P2 | List |
| Q075 | 哪些产品增加了内容审核或安全护栏？ | Safety | Product + Event + safety.guardrails | ⭐ | P2 | Table |
| Q076 | 过去一年，AI 服务的稳定性是变好还是变差？ | Safety | Event (incident) 频率趋势 | ⭐⭐ | P3 | Chart |
| Q077 | 重大故障的平均恢复时间是多少？ | Safety | Event (incident) + 恢复时间统计 | ⭐⭐ | P3 | Chart |
| Q078 | 最近有哪些监管政策直接影响了 AI 产品可用性？ | Safety | Event (availability-changed) + policy 标签 | ⭐⭐ | P2 | List |
| Q079 | 某模型（如 GPT-4）的越狱抵抗能力如何？ | Safety | Model + safety.resistance.jailbreak + Benchmark | ⭐⭐⭐ | P3 | Table |
| Q080 | 有没有模型被发现有严重的幻觉问题？ | Safety | Model + safety.resistance.hallucination + Benchmark | ⭐⭐⭐ | P3 | Table |

---

## Category 9: Company Analysis（公司分析）

| ID | Question | Intent | Knowledge Needed | Difficulty | Priority | Visualization |
|----|----------|--------|------------------|------------|----------|---------------|
| Q081 | OpenAI 的模型产品线有哪些？ | Company | Company + Model 列表 + 关系 | ⭐ | P0 | Tree |
| Q082 | Anthropic 在 Agent 领域的布局是什么？ | Company | Company + Product + Capability (agent.*) | ⭐⭐ | P1 | Graph |
| Q083 | 某公司（如 Google）的开发者工具有哪些？ | Company | Company + Product (developer tools) | ⭐ | P2 | Table |
| Q084 | 哪些公司同时拥有模型和产品？ | Company | Company + Model + Product | ⭐ | P1 | Table |
| Q085 | 某公司最近半年重点投入什么能力方向？ | Company | Company + Event + Capability Domain 统计 | ⭐⭐ | P1 | Chart |
| Q086 | 哪些公司在多模态领域投入最多？ | Company | Company + Capability (multimodal.*) + Event | ⭐⭐ | P2 | Chart |
| Q087 | 某公司（如 Microsoft）的 AI 产品有哪些？ | Company | Company + Product 列表 | ⭐ | P1 | Table |
| Q088 | 哪些公司推出了开源模型？ | Company | Company + Model (开源) | ⭐ | P1 | Table |
| Q089 | 某公司的 AI 能力演进路线是什么？ | Company | Company + Event 时间线 | ⭐⭐ | P2 | Timeline |
| Q090 | 哪些公司在 AI 安全领域投入最多？ | Company | Company + Capability (safety.*) + Event | ⭐⭐ | P2 | Chart |

---

## Category 10: Evolution Summary（演化总结）

| ID | Question | Intent | Knowledge Needed | Difficulty | Priority | Visualization |
|----|----------|--------|------------------|------------|----------|---------------|
| Q091 | 过去一年，AI 能力最重要的变化是什么？ | Summary | Event + score + 年度统计 | ⭐⭐ | P1 | Text |
| Q092 | AI 能力发展的十大里程碑是什么？ | Summary | Event + high score + 时间线 | ⭐⭐⭐ | P2 | Timeline |
| Q093 | 哪些能力正在成为 AI 的"标配"？ | Summary | Capability + 支持数量 + 时间 | ⭐⭐ | P2 | Table |
| Q094 | AI 能力的扩散速度在变快还是变慢？ | Summary | Capability + 扩散速度趋势 | ⭐⭐⭐ | P3 | Chart |
| Q095 | 最近一年，Agent 能力的发展趋势是什么？ | Summary | Capability (agent.*) + Event 趋势 | ⭐⭐ | P1 | Chart |
| Q096 | 哪些能力从"热门"变成了"常规"？ | Summary | Capability + 热度趋势 | ⭐⭐ | P2 | Table |
| Q097 | AI 行业的能力演进有什么规律？ | Summary | Evolution + 模式识别 | ⭐⭐⭐⭐ | P3 | Text |
| Q098 | 未来 AI 能力发展的三个方向是什么？ | Summary | Trend prediction | ⭐⭐⭐⭐ | P3 | Text |
| Q099 | AI 能力的"生命周期"是什么样的？ | Summary | Capability + Evolution 阶段 | ⭐⭐⭐ | P3 | Text |
| Q100 | 能力从首次出现到被主流采纳需要多长时间？ | Summary | Capability + 扩散时间统计 | ⭐⭐⭐ | P2 | Chart |

---

## 附录：按优先级统计

| Priority | 数量 | 占比 |
|----------|------|------|
| P0 | 20 | 20% |
| P1 | 38 | 38% |
| P2 | 30 | 30% |
| P3 | 12 | 12% |

## 附录：按难度统计

| Difficulty | 数量 | 占比 |
|------------|------|------|
| ⭐ | 28 | 28% |
| ⭐⭐ | 42 | 42% |
| ⭐⭐⭐ | 20 | 20% |
| ⭐⭐⭐⭐ | 10 | 10% |

---

*文档版本：v1.0*
*创建日期：2026-07-06*
*下次 Review：2026-10-06*
