# AGR-0001: P1 Architecture Gate Review

**Revision:** 2.0  
**Date:** 2026-07-07  
**Status:** Active  
**Review Phase:** P1-1 → P1-2  
**Reviewer:** CTO / Product Owner

---

## Executive Summary

当前系统已完成 P1-1 阶段（事件质量），具备基本的 Event Dedup、Clustering 和 Source Weighting 能力。但深入分析后发现，系统核心设计仍存在**架构偏离风险**——当前系统本质上仍是"Event 驱动"而非"Fact 驱动"，且 Knowledge 仍为 CRUD 而非 Projection。

**总体评级:** ⚠️ **Conditional Pass**（条件通过）

**评审得分:** A-（92/100）

需要在 P1-2 阶段修复 4 个 Critical 级问题后，才能进入下一阶段。

---

## 评审亮点

1. ✅ Fact 原子化分析准确，触及知识系统核心
2. ✅ Event-Driven Capability 方向正确
3. ✅ Narrative Cluster 概念有前瞻性
4. ⚠️ 遗漏了 Knowledge Projection 这一最大架构风险

---

## Review Questions & Analysis

### AGR-01: Fact 是否真正原子化？

**Status:** ❌ FAIL

**问题分析:**

当前 `IntelligencePipeline.process_signal_to_event()` 中：

```python
# 一个 Signal → 一个 Fact → 一个 Event
fact = self.fact_service.create_fact(
    claim=signal.title or signal.raw_content[:200],
    ...
)
event = self.event_service.create_event(
    title=signal.title or "New Signal",
    fact_ids=[fact.id],  # 只有一个 fact
)
```

**风险:**

如果一篇文章提到：
```
GPT-5 发布
新增 Memory
新增 MCP  
价格下降
API更新
```

当前系统会生成：**1 个 Event**

而应该生成：**4-5 个 Fact → 对应多个 Event**

**影响范围:**
- 所有 Pipeline 逻辑
- FactService 和 EventService 的交互模式
- 事件分类准确性

**建议修复:**

1. 重构 `Signal → Fact` 阶段，实现**多 Fact 提取**
2. 每个 Fact 应有独立的 subject/predicate/object
3. 一个 Signal 可以生成多个 Fact
4. 一个 Event 可以关联多个 Fact，但一个 Fact 只属于一个 Event

---

### AGR-02: Capability 是否 Event Driven？

**Status:** ❌ FAIL

**问题分析:**

当前 Capability 更新机制：

```python
# ScoringService.update_capability_scores()
# 主动查询事件 → 计算 → 更新 Capability
events = self.db.query(Event).join(...).filter(...).all()
```

**风险:**

- Capability 状态是**被动计算**的，不是由 Event 触发的
- 没有 Event → Capability 的自动更新链路
- 当大量 Event 产生时，Capabilities 可能过期

**当前数据流:**
```
查询 Capability → 统计 Event → 计算状态
```

**应该是:**
```
Event Confirmed → Capability Engine → 立即更新 Capability
```

**影响范围:**
- Capability 时效性
- 能力图谱的准确性
- 后续 AIQ 查询的可信度

**建议修复:**

1. 实现 `CapabilityEventConsumer`，监听 Event 状态变化
2. Event 状态变为 `confirmed` 时，自动触发 Capability 更新
3. 更新链路：Event → Capability Score → Truth State → Graph → Timeline

---

### AGR-03: Story 是否取代 Cluster？

**Status:** ❌ FAIL

**问题分析:**

当前 `EventClusteringService.cluster_events()`：

```python
# 基于相似度的去重
similarity = self._calculate_similarity(event, cluster.canonical_event)
if similarity >= self.DEFAULT_SIMILARITY_THRESHOLD:
    return cluster
```

**风险:**

Cluster 当前只是"去重容器"，不是"叙事单元"。**Cluster 太 NLP，应该升级为 Story。**

**例子:**

```
OpenAI 发布 GPT-5          ← 当前：可能分开成多个 Cluster
OpenAI API 更新            ← 因为相似度不够
Azure 接入 GPT-5           ← 
Cursor 支持 GPT-5          ←
社区 Benchmark 结果        ←

应该形成：GPT-5 Release Story（一个完整故事）
```

**产品视角:**

```
首页展示 Story
    ↓
Story 点进去 → 看到所有 Event
    ↓
Event 点进去 → 看到所有 Fact
    ↓
Fact 点进去 → 看到所有 Source

形成完整知识链
```

**影响范围:**
- 事件聚合质量
- 后续 Bloomberg 级别的叙事能力
- 用户体验（看到完整事件脉络）
- 产品层最重要的对象

**建议修复:**

1. 将 Cluster 正式升级为 **Story**（或 Narrative）
2. Story 需要理解 **Subject** 和 **Relation**
2. 引入 **Narrative Engine**：
   - 识别同一个 subject 的所有相关事件
   - 按时间顺序构建事件链
   - 生成 Narrative Summary
3. Story 应包含：主线、支线、时间线、参与者

---

### AGR-04: Knowledge 是否 Projection？

**Status:** ❌ FAIL

**问题分析:**

这是当前系统**最大的架构风险**。

当前 Capability 的更新方式：

```python
# ScoringService.update_capability_scores()
cap.maturity_score = maturity
cap.adoption_score = adoption  
cap.truth_score = truth_score
cap.status = "mature"
```

**风险:**

Knowledge（Capability 的各种属性）是**直接 CRUD 更新**的，不是 **Projection**。

**例子:**

```
Memory
- truth_score: 95       ← 直接存
- maturity: mature      ← 直接存
- supported_models: [...] ← 直接存
- timeline: [...]       ← 直接存
```

**应该是:**

```
Fact
    ↓
Event
    ↓
Projection
    ↓
Knowledge（自动推导）
```

**核心原则:**

> **Knowledge 永远不应该直接存，它永远是 Event 的投影。**

**验证方法:**

```
Drop Database（删除所有 Capability）
    ↓
Replay Event（重新回放所有 Event）
    ↓
Capability 必须完全恢复（如果不能，说明设计错误）
```

**影响范围:**
- 系统一致性
- 可恢复性
- 新增能力类型的复杂度
- 知识图谱的可信度
- 后续 Prediction 和 Forecast 的基础

**建议修复:**

1. 将 `CapabilityService` 重命名为 `CapabilityProjection`
2. Capability 的所有属性（truth_score、maturity、adoption、status、timeline）都通过 Projection 计算
3. 实现 Event Replay 机制
4. 确保：Drop → Replay → 完全恢复

---

### AGR-05: Timeline 是否 Projection？

**Status:** ⚠️ PARTIAL

**问题分析:**

当前 `CapabilityService.get_timeline()`：

```python
def get_timeline(self, capability_id: str):
    events = self.db.query(Event).join(...).filter(...).all()
    return {"capability": cap, "events": events}
```

**现状:**
- Timeline 是**查询结果**，不是**投影**
- 每次请求都重新查询数据库
- 没有缓存机制
- 没有 Timeline 状态管理

**风险:**
- 查询性能随数据量线性下降
- Timeline 一致性难以保证
- 无法做 Timeline 的增量更新

**建议修复:**

1. 实现 **Timeline Projection Engine**：
   - Event → Projection → Timeline
   - 投影结果缓存
   - 增量更新机制
2. Timeline 应作为独立实体管理

---

### AGR-06: Score 是否 Snapshot？

**Status:** ❌ FAIL

**问题分析:**

当前 `ScoringService.calculate_event_scores()`：

```python
event.confidence_score = confidence
event.impact_score = impact
event.overall_score = overall
# 直接覆盖，没有历史
```

**风险:**

新闻价值是动态变化的：
```
刚发布：      impact=55
官方确认：    impact=90  
微软宣布支持： impact=97
```

当前系统无法追踪这个变化过程。

**影响范围:**
- 事件影响力评估的准确性
- 历史回溯能力
- 趋势分析

**建议修复:**

1. 引入 `ScoreSnapshot` 模型：
   ```
   event_id, score_type, score_value, timestamp
   ```
2. 每次评分更新时创建新 Snapshot
3. 保留完整评分历史

---

### AGR-07: Graph 是否唯一事实来源？

**Status:** ⚠️ PARTIAL

**问题分析:**

当前系统有：
- Capability Graph（能力关系）
- Event-Fact 关系
- Source 权重

但缺少：
- 统一的 Graph Query Layer
- Graph 作为 Single Source of Truth 的架构设计
- 跨实体的图遍历能力

**风险:**
- 各模块各自维护状态，容易不一致
- 无法做复杂的图查询（如：能力依赖链、影响传播）
- 后续扩展困难

**建议修复:**

1. 建立 **Knowledge Graph Layer**：
   - 所有实体关系统一管理
   - 提供图查询接口
   - 作为唯一事实来源
2. API 层应从 Graph Layer 查询，而非直接查数据库

---

### AGR-08: 是否所有 API 都来自 Knowledge Layer？

**Status:** ❌ FAIL

**问题分析:**

当前 API 直接查询数据库：

```python
@router.get("/capabilities/{capability_id}")
def get_capability(capability_id: str, db: Session = Depends(get_db)):
    service = CapabilityService(db)
    cap = service.get_by_id(capability_id)  # 直接查 DB
```

**风险:**
- 业务逻辑分散在 Service 层
- 无法统一缓存策略
- 无法做复杂的跨实体查询
- 数据库 Schema 变更影响所有 API

**建议修复:**

1. 引入 **Knowledge Layer**：
   - 所有 API 通过 Knowledge Layer 访问数据
   - Knowledge Layer 封装所有实体关系查询
   - 提供统一的查询接口

---

### AGR-09: AIQ Query 是否完全脱离 SQL？

**Status:** ❌ FAIL

**问题分析:**

当前 `/aiq/{question_id}`：

```python
caps = cap_service.search(page=1, size=10)  # SQL 查询
events = event_service.search(page=1, size=10)  # SQL 查询
```

**风险:**
- AIQ 查询直接依赖 SQL
- 无法支持自然语言查询
- 无法做语义理解和推理
- 扩展性差

**建议修复:**

1. 实现 **AIQ Query Engine**：
   - Intent Parser（意图解析）
   - Execution Planner（执行计划）
   - Graph Query（图查询）
   - Answer Generator（答案生成）
2. AIQ 查询应基于 Knowledge Graph，而非直接 SQL

---

### AGR-10: 是否可以支持 100万 Event / 1000万 Fact / 100万 Link？

**Status:** ❌ FAIL

**问题分析:**

当前技术栈限制：
- **SQLite**：不适合大规模数据
- **无索引策略**：查询性能差
- **全表扫描**：相似度计算时全表扫描
- **无分页优化**：大数据量下内存压力

**风险:**
- 当前数据量（3 Event）下表现良好
- 数据量增长到万级时会出现明显性能问题
- 百万级数据下系统不可用

**建议修复:**

1. **数据库升级**：
   - 迁移到 PostgreSQL
   - 或引入 Neo4j 作为图数据库
2. **索引优化**：
   - 为 Event.detected_at, Event.type 创建索引
   - 为 Fact.subject, Fact.capability_id 创建索引
   - 考虑向量索引用于相似度计算
3. **缓存策略**：
   - Redis 缓存热点数据
   - 预计算 Cluster 和 Score
4. **异步处理**：
   - 相似度计算异步化
   - 评分计算异步化

---

### AGR-11: 是否任何新 Capability 都不用改代码？

**Status:** ⚠️ PARTIAL

**问题分析:**

当前新增 Capability 流程：

```python
# 需要在代码中创建
capability_service.upsert_by_slug("memory", {
    "name": "Memory",
    "type": "cognitive",
    ...
})
```

**现状:**
- Capability 可以动态创建（不需要改表结构）
- 但需要编写代码调用
- Capability Type 需要在 `CAPABILITY_TYPES` 中定义

**风险:**
- 新增能力类型需要修改代码
- 无法通过配置或 API 动态扩展

**建议修复:**

1. **Capability Type 动态化**：
   - 将类型定义从代码移到数据库
   - 支持通过 API 创建新类型
2. **自动能力发现**：
   - 通过 Fact 分析自动识别新能力
   - 无需人工干预

---

## Risk Matrix

| Risk | Severity | Impact | Likelihood | Priority |
|------|----------|--------|------------|----------|
| AGR-01: Fact 非原子化 | Critical | 事件质量、分类准确性 | High | P0 |
| AGR-02: Capability 非 Event Driven | Critical | 能力时效性、图谱准确性 | High | P0 |
| AGR-03: Story 取代 Cluster | Critical | 叙事能力、用户体验 | Medium | P0 |
| **AGR-04: Knowledge 非 Projection** | **Critical** | **系统一致性、可恢复性** | **High** | **P0** |
| AGR-06: Score 非 Snapshot | High | 评分准确性、趋势分析 | Medium | P1 |
| AGR-10: 扩展性不足 | High | 系统可用性、性能 | High | P1 |
| AGR-07: Graph 非 SSOT | Medium | 数据一致性、扩展性 | Medium | P2 |
| AGR-08: API 未分层 | Medium | 可维护性、扩展性 | Medium | P2 |
| AGR-09: AIQ 依赖 SQL | Medium | 查询能力、扩展性 | Medium | P2 |
| AGR-05: Timeline 非 Projection | Low | 查询性能、一致性 | Low | P3 |
| AGR-11: Capability 扩展性 | Low | 运维效率 | Low | P3 |

---

## Recommendations

### P1-2 阶段必须修复（Critical）

**推荐顺序：**

1. **第一阶段：Fact Engine**
   - 实现 Signal → 多 Fact 提取
   - Fact 成为唯一原子
   - 所有下游模块只能读取 Fact

2. **第二阶段：Event Sourcing**
   - 将 `CapabilityService` 重命名为 `CapabilityProjection`
   - 实现 Event → Capability 的自动投影
   - 实现 Event Replay 机制
   - 验证：Drop → Replay → 完全恢复

3. **第三阶段：Story Engine**
   - 将 Cluster 正式升级为 Story
   - 实现基于 Subject 的事件关联
   - 构建完整知识链：Story → Event → Fact → Source

4. **第四阶段：Truth Engine**
   - 实现 `CapabilityTruthState`
   - 动态校准：official +1.0, community +0.3, contradiction -0.5, decay -0.1/day

5. **第五阶段：Score Snapshot**
   - 实现评分历史追踪
   - 记录评分随时间变化

### P1-3 阶段建议修复（High）

6. **数据库升级**：PostgreSQL + 索引优化
7. **实现 Knowledge Layer**：统一查询层

### P1-4 阶段建议修复（Medium/Low）

8. **AIQ Query Engine**：脱离 SQL，支持语义查询
9. **Timeline Projection**：缓存和增量更新
10. **Capability Type 动态化**：无需改代码扩展

---

## Architecture Improvements

### Current Architecture

```
API Layer
    ↓
Service Layer (直接查询 DB)
    ↓
Database (SQLite)
```

### Target Architecture

```
API Layer
    ↓
Knowledge Layer (统一查询、图遍历)
    ↓
┌─────────────────┬─────────────────┐
│  PostgreSQL     │   Neo4j/Graph   │
│  (结构化数据)    │   (关系/图数据)  │
└─────────────────┴─────────────────┘
    ↓
Event Bus (Kafka/Celery)
    ↓
Event Handlers (Capability Update, Score Recalc, Timeline Update)
```

---

## Conclusion

**当前系统状态:**
- ✅ 基础架构已搭建
- ✅ 核心实体模型定义完成
- ✅ P1-1 功能实现（Dedup、Clustering、Source Weighting）
- ❌ 架构偏离 Intelligence System 核心思想

**进入 P1-2 的条件:**

必须在 P1-2 开始前确认以下修复计划：

1. [ ] Fact 原子化改造方案
2. [ ] Event-Driven Capability 更新方案
3. [ ] Narrative Cluster 设计方案

**评审结论:** ⚠️ **Conditional Pass**

建议在 P1-2 阶段优先修复 Critical 级问题，否则后续开发将面临重大返工风险。

---

## Reviewer Sign-off

| Role | Name | Approval | Date |
|------|------|----------|------|
| CTO / Architecture | - | ⏳ Pending | - |
| Product Owner | - | ⏳ Pending | - |
| Engineering Lead | - | ⏳ Pending | - |

---

**Document History:**

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-07-07 | Initial Draft | System Auto-Generated |