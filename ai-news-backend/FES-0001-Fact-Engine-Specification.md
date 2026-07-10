# FES-0001: Fact Engine Specification

**Version:** 1.0  
**Date:** 2026-07-07  
**Status:** Active  
**Phase:** P1-2 Sprint 1-4

---

## 1. Executive Summary

Fact Engine 是 AI Capability Intelligence Platform 的 **Truth Ingestion Layer**，是整个系统唯一的原子数据入口。

**核心原则:**

> **所有 AI、Parser、LLM 都只能产生 Fact。**
> **所有下游模块（Event、Story、Capability、Truth、Score）都只能读取 Fact。**
> **禁止任何模块直接读取 Signal。**

---

## 2. Fact Schema Definition

### 2.1 Core Fields

```sql
CREATE TABLE facts (
    id              VARCHAR(36) PRIMARY KEY,
    signal_id       VARCHAR(36) NOT NULL,          -- 来源信号
    subject_id      VARCHAR(36),                   -- 主体实体（如 GPT-5）
    subject_type    VARCHAR(50),                   -- 主体类型（model/product/company）
    subject_name    VARCHAR(200),                  -- 主体名称
    predicate       VARCHAR(100) NOT NULL,         -- 谓词（released/supports/price_changed）
    object_id       VARCHAR(36),                   -- 客体实体（如 Memory）
    object_type     VARCHAR(50),                   -- 客体类型
    object_name     VARCHAR(200),                  -- 客体名称
    object_value    VARCHAR(500),                  -- 客体值（如 -30%）
    datatype        VARCHAR(50),                   -- 数据类型（entity/number/string/boolean）
    unit            VARCHAR(50),                   -- 单位（%/USD/hours）
    time_value      DATETIME,                      -- 事实发生时间
    time_precision  VARCHAR(20),                   -- 时间精度（day/hour/minute）
    confidence      FLOAT DEFAULT 0.7,             -- 提取置信度（0.0-1.0）
    truth_score     FLOAT DEFAULT 0.0,             -- 真实性评分（-1.0-1.0）
    evidence_count  INTEGER DEFAULT 0,             -- 证据数量
    status          VARCHAR(20) DEFAULT 'extracted', -- 生命周期状态
    extractor       VARCHAR(100),                  -- 提取器标识（llm/rule/parser）
    extraction_method VARCHAR(50),                 -- 提取方法
    canonical_id    VARCHAR(36),                   -- 规范化ID（用于合并）
    version         INTEGER DEFAULT 1,             -- 版本号
    duplicate_of    VARCHAR(36),                   -- 如果是重复，指向主Fact
    merge_score     FLOAT DEFAULT 0.0,             -- 合并相似度
    extra_data      JSON,                          -- 扩展数据
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    verified_at     DATETIME,                      -- 验证时间
    confirmed_at    DATETIME,                      -- 确认时间
    rejected_at     DATETIME,                      -- 拒绝时间
    rejected_reason VARCHAR(500),                  -- 拒绝原因
    deleted_at      DATETIME                       -- 软删除
);
```

### 2.2 Indexes

```sql
CREATE INDEX idx_facts_signal_id ON facts(signal_id);
CREATE INDEX idx_facts_subject_id ON facts(subject_id);
CREATE INDEX idx_facts_predicate ON facts(predicate);
CREATE INDEX idx_facts_object_id ON facts(object_id);
CREATE INDEX idx_facts_status ON facts(status);
CREATE INDEX idx_facts_canonical_id ON facts(canonical_id);
CREATE INDEX idx_facts_time_value ON facts(time_value);
CREATE INDEX idx_facts_subject_predicate ON facts(subject_id, predicate);
CREATE INDEX idx_facts_predicate_object ON facts(predicate, object_id);
```

---

## 3. Fact Lifecycle

### 3.1 States

```
extracted    → 初始提取状态
    ↓
parsed       → 解析完成，结构化
    ↓
normalized   → 规范化完成（实体对齐）
    ↓
verified     → 通过验证（来源可信）
    ↓
confirmed    → 确认事实（多证据支持）
    ↓
archived     → 归档（不再活跃）
    ↓
rejected     → 拒绝（不可信或无效）
```

### 3.2 State Transitions

| From | To | Condition | Action |
|------|-----|-----------|--------|
| extracted | parsed | 结构完整 | 解析完成 |
| parsed | normalized | 实体可对齐 | 实体ID映射 |
| normalized | verified | source.signal_level ∈ {S,A} | 来源可信 |
| verified | confirmed | evidence_count ≥ 2 OR source.signal_level = S | 多证据或官方 |
| any | rejected | confidence < 0.3 OR contradiction | 标记拒绝 |
| confirmed | archived | time > 90 days | 自动归档 |

### 3.3 Status Query Rules

**下游模块只能读取特定状态的 Fact:**

- Event Engine: 只读取 `confirmed` 状态的 Fact
- Story Engine: 只读取 `confirmed` 状态的 Fact
- Capability Projection: 只读取 `confirmed` 状态的 Fact
- Truth Engine: 可以读取所有状态（用于验证）
- Score Engine: 只读取 `confirmed` 状态的 Fact

---

## 4. Fact Extraction Rules

### 4.1 Predicate Dictionary

| Predicate | Description | Object Type | Example |
|-----------|-------------|-------------|---------|
| released | 产品发布 | entity | GPT-5 released |
| supports | 能力支持 | capability | GPT-5 supports Memory |
| price_changed | 价格变化 | number | price -30% |
| api_updated | API更新 | entity | API v2 released |
| deprecated | 废弃 | entity | Model deprecated |
| benchmark_result | Benchmark结果 | number | Accuracy 95% |
| integration | 集成 | product | Cursor integrates GPT-5 |
| limitation | 限制 | string | Max tokens 4096 |
| region_available | 区域可用 | region | Available in EU |
| capability_added | 能力新增 | capability | Memory added |
| capability_removed | 能力移除 | capability | Tool Use removed |

### 4.2 Extraction Process

**输入:** Signal（包含 raw_content, title, source）

**输出:** Fact[]

**流程:**

```
1. Content Analysis
   - 解析 Signal 内容
   - 识别主体、客体、谓词
   
2. Triple Construction
   - 构建(subject, predicate, object)三元组
   - 每个三元组对应一个 Fact
   
3. Entity Resolution
   - subject_id 映射到实体库
   - object_id 映射到实体库
   - 未识别实体创建临时ID
   
4. Normalization
   - predicate 规范化到字典
   - object_value 类型化
   - time_value 解析
   
5. Confidence Calculation
   - 基于 source.signal_level
   - 基于提取方法
   - 基于内容清晰度
```

### 4.3 Extraction Example

**Signal:**

```
Title: OpenAI released GPT-5 with Memory support, price reduced 30%
Content: OpenAI officially announced GPT-5 today. The new model supports Memory 
         and MCP. Pricing is reduced by 30% compared to GPT-4.
Source: OpenAI Blog (S-level)
```

**Output Facts:**

```json
[
  {
    "subject_name": "GPT-5",
    "subject_type": "model",
    "predicate": "released",
    "object_name": "Release",
    "object_type": "event",
    "confidence": 0.95,
    "extractor": "llm-v1"
  },
  {
    "subject_name": "GPT-5",
    "subject_type": "model",
    "predicate": "supports",
    "object_name": "Memory",
    "object_type": "capability",
    "confidence": 0.95,
    "extractor": "llm-v1"
  },
  {
    "subject_name": "GPT-5",
    "subject_type": "model",
    "predicate": "supports",
    "object_name": "MCP",
    "object_type": "capability",
    "confidence": 0.90,
    "extractor": "llm-v1"
  },
  {
    "subject_name": "GPT-5",
    "subject_type": "model",
    "predicate": "price_changed",
    "object_value": "-30%",
    "datatype": "number",
    "unit": "%",
    "confidence": 0.95,
    "extractor": "llm-v1"
  }
]
```

---

## 5. Fact Validation Rules

### 5.1 Validation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| source_signal_level | 0.4 | S=1.0, A=0.7, B=0.3 |
| extraction_confidence | 0.2 | 提取置信度 |
| entity_recognition | 0.2 | 实体识别率 |
| time_precision | 0.1 | 时间精度 |
| predicate_match | 0.1 | predicate 是否在字典中 |

**Validation Score = Σ(criterion × weight)**

**Thresholds:**
- score ≥ 0.7 → verified
- score ∈ [0.5, 0.7) → needs_review
- score < 0.5 → rejected

### 5.2 Contradiction Detection

**规则:**

如果新 Fact 与已确认 Fact 矛盾：

```
Existing Fact: GPT-5 supports Memory (confirmed)
New Fact: GPT-5 does NOT support Memory (extracted)

→ 标记为 contradiction
→ 需要人工审核或等待更多证据
```

**矛盾类型:**
- predicate 矛盾（supports vs not_supports）
- value 矛盾（price 100 vs price 50）
- time 矛盾（同一时间不同状态）

---

## 6. Fact Merge Rules

### 6.1 Merge Conditions

**相同事实判定:**

```
Fact A 和 Fact B 可合并，当：
1. subject_id 相同（或 canonical_id 相同）
2. predicate 相同
3. object_id 相同（或 object_value 相同）
4. time_value 差异 < 24h
```

### 6.2 Merge Process

```
1. Find Candidates
   - 查询相同(subject, predicate, object)的Fact
   
2. Calculate Similarity
   - time_similarity = 1 - |time_diff| / 7days
   - source_similarity = based on signal_level
   - content_similarity = text similarity
   
3. Merge Decision
   - similarity ≥ 0.85 → merge
   - similarity < 0.85 → keep separate
   
4. Create Canonical
   - 选择置信度最高的作为 canonical
   - 其他 Fact 标记为 duplicate_of
   - 更新 evidence_count
```

### 6.3 Merge Example

**Input Facts:**

```
Fact-1: Claude supports MCP (source: Anthropic Blog, confidence: 0.95)
Fact-2: ChatGPT supports MCP (source: OpenAI Blog, confidence: 0.95)
Fact-3: Copilot supports MCP (source: GitHub Blog, confidence: 0.90)
```

**Merge Decision:**

这些 Fact **不合并**，因为 subject 不同（Claude vs ChatGPT vs Copilot）。

**但如果:**

```
Fact-1: Claude supports MCP (source: Anthropic Blog, 2026-07-01)
Fact-2: Claude supports MCP (source: Reddit, 2026-07-02)
```

**则合并:**

```
Canonical: Fact-1
Duplicate: Fact-2 (duplicate_of = Fact-1.id)
Evidence Count: 2
Truth Score: +0.3 (community confirm)
```

---

## 7. Fact Index & Query

### 7.1 Query Patterns

**Pattern 1: Subject Query**

```sql
SELECT * FROM facts 
WHERE subject_id = ? 
AND status = 'confirmed'
ORDER BY time_value DESC;
```

**Pattern 2: Predicate Query**

```sql
SELECT * FROM facts 
WHERE predicate = 'supports' 
AND object_id = ? 
AND status = 'confirmed';
```

**Pattern 3: Capability Query**

```sql
SELECT f.*, c.name as capability_name
FROM facts f
JOIN capabilities c ON f.object_id = c.id
WHERE f.predicate IN ('supports', 'capability_added')
AND f.status = 'confirmed'
ORDER BY f.time_value DESC;
```

**Pattern 4: Time Range Query**

```sql
SELECT * FROM facts 
WHERE time_value BETWEEN ? AND ?
AND status = 'confirmed'
ORDER BY time_value;
```

### 7.2 Graph Query (Future)

```
// Neo4j-style query
MATCH (s:Subject)-[f:FACT]->(o:Object)
WHERE f.predicate = 'supports'
AND f.status = 'confirmed'
RETURN s.name, o.name, f.confidence
```

---

## 8. Fact → Event Builder

### 8.1 Event Construction Rules

**输入:** Fact[]（同一 Signal 或相关 Signal）

**输出:** Event

**规则:**

```
Event 由 Fact 聚合而成：
1. 同一 Signal 的 Fact → 同一 Event
2. 同一 Subject 的 Fact（时间相近）→ 同一 Event
3. Event.type 由 Fact.predicate 决定
```

### 8.2 Event Type Mapping

| Fact Predicate | Event Type |
|----------------|------------|
| released | MODEL_RELEASE |
| supports | FEATURE |
| api_updated | API |
| price_changed | PRICING |
| deprecated | DEPRECATION |
| benchmark_result | BENCHMARK |
| integration | ECOSYSTEM |
| limitation | LIMITATION |

### 8.3 Event Example

**Input Facts:**

```
Fact-1: GPT-5 released
Fact-2: GPT-5 supports Memory
Fact-3: GPT-5 supports MCP
Fact-4: GPT-5 price_changed -30%
```

**Output Event:**

```json
{
  "title": "GPT-5 Release",
  "type": "MODEL_RELEASE",
  "subject": "GPT-5",
  "facts": [Fact-1, Fact-2, Fact-3, Fact-4],
  "summary": "GPT-5 released with Memory and MCP support, price reduced 30%",
  "detected_at": "2026-07-07T10:00:00Z"
}
```

---

## 9. Fact → Story Builder

### 9.1 Story Construction Rules

**输入:** Fact[] + Event[]

**输出:** Story

**规则:**

```
Story 由 Event 聚合而成：
1. 同一 Subject 的 Event → 同一 Story
2. Story.timeline 按时间排序
3. Story.participants 从 Fact 提取
```

### 9.2 Story Example

**Input:**

```
Event-1: GPT-5 Release (OpenAI)
Event-2: Azure integrates GPT-5 (Microsoft)
Event-3: Cursor supports GPT-5 (Cursor)
Event-4: GPT-5 Benchmark (Community)
```

**Output Story:**

```json
{
  "title": "GPT-5 Release",
  "subject": "GPT-5",
  "timeline": [Event-1, Event-2, Event-3, Event-4],
  "participants": ["OpenAI", "Microsoft", "Cursor"],
  "facts_count": 10,
  "events_count": 4,
  "summary": "GPT-5 released by OpenAI, integrated by Azure and Cursor..."
}
```

---

## 10. Replay & Projection

### 10.1 Replay Rules

**目的:** 从 Fact Log 重新构建所有派生视图

**流程:**

```
1. Drop Projections
   - 删除所有 Event、Story、Capability
   
2. Replay Facts
   - 按时间顺序读取 Fact Log
   - 对每个 Fact 执行 Event Builder
   
3. Rebuild Projections
   - 构建 Event → Story
   - 构建 Event → Capability Projection
   - 构建 Fact → Truth Evolution
```

### 10.2 Projection Rules

**Capability Projection:**

```
Event: GPT-5 supports Memory (confirmed)
    ↓
Projection:
    Capability Memory
    - maturity += 1
    - adoption += 1 (GPT-5)
    - truth_score += 0.1 (if source = S-level)
    - timeline += [Event]
```

**Truth Evolution:**

```
Fact: GPT-5 supports Memory (confirmed)
    ↓
Truth Update:
    if source.signal_level = S: truth_score += 1.0
    if source.signal_level = A: truth_score += 0.3
    if contradiction: truth_score -= 0.5
    if no_update_days > 7: truth_score -= 0.1 * days
```

---

## 11. Boundary Rules

### 11.1 Module Boundaries

| Module | Can Read | Can Write | Cannot |
|--------|----------|-----------|--------|
| Fact Engine | Signal | Fact | 直接写 Event |
| Event Builder | Fact | Event | 直接读 Signal |
| Story Engine | Fact, Event | Story | 直接读 Signal |
| Capability Projection | Fact, Event | (Projection) | 直接修改 Capability |
| Truth Engine | Fact | truth_score | 直接读 Signal |
| Score Engine | Fact | Score | 直接读 Signal |

### 11.2 Data Flow Rules

**禁止的路径:**

```
❌ Signal → Event（直接）
❌ Signal → Capability（直接）
❌ Signal → Story（直接）
❌ 直接修改 Capability 状态
```

**允许的路径:**

```
✅ Signal → Fact → Event
✅ Fact → Event → Story
✅ Event → Capability Projection
✅ Fact → Truth Evolution
```

---

## 12. DoD (Definition of Done)

### Sprint 1: Fact Extraction

| 验收项 | 标准 | 状态 |
|--------|------|------|
| Signal 能拆分为多个 Fact | ✅ 同一 Signal 至少支持 N 个 Fact | ⏳ |
| Fact Schema 完整 | ✅ 所有字段定义完成 | ⏳ |
| Predicate Dictionary | ✅ 至少 12 个 predicate | ⏳ |
| Extraction Confidence | ✅ 置信度计算正确 | ⏳ |

### Sprint 2: Fact Validation

| 验收项 | 标准 | 状态 |
|--------|------|------|
| Fact 生命周期完整 | ✅ Extracted → Confirmed → Rejected | ⏳ |
| Validation Score | ✅ 多维度评分计算 | ⏳ |
| Contradiction Detection | ✅ 自动检测矛盾 | ⏳ |

### Sprint 3: Fact Merge

| 验收项 | 标准 | 状态 |
|--------|------|------|
| Canonical Merge | ✅ 相同事实不会无限增长 | ⏳ |
| Evidence Count | ✅ 合并后更新证据数 | ⏳ |
| Truth Score Update | ✅ 合并影响真实性评分 | ⏳ |

### Sprint 4: Fact Index

| 验收项 | 标准 | 状态 |
|--------|------|------|
| Subject Query | ✅ 按 subject_id 查询 | ⏳ |
| Predicate Query | ✅ 按 predicate 查询 | ⏳ |
| Fact → Event Builder | ✅ Event 只能由 Fact 构建 | ⏳ |
| Fact → Story Builder | ✅ Story 基于 Fact/Event | ⏳ |

### P1-2 Final DoD

| 验收项 | 标准 | 状态 |
|--------|------|------|
| Signal 能拆分为多个 Fact | ✅ 同一 Signal 至少支持 N 个 Fact | ⏳ |
| Fact 生命周期完整 | ✅ Extracted → Confirmed → Rejected | ⏳ |
| Fact 支持 Canonical Merge | ✅ 相同事实不会无限增长 | ⏳ |
| Fact 支持 Replay | ✅ 删除 Event 后可重新构建 | ⏳ |
| Event 只能由 Fact 构建 | ✅ 禁止 Signal → Event 直连 | ⏳ |
| Capability 只能由 Event Projection 更新 | ✅ 禁止直接修改 Capability 状态 | ⏳ |
| Story 基于 Fact/Event 聚合 | ✅ 不再依赖文本相似度 Cluster | ⏳ |

---

## 13. Reference

- ADR-0001: Why Fact is Atomic
- ADR-0002: Why Capability is Projection
- ADR-0003: Why Story replaces Cluster
- ADR-0004: Why Event Sourcing
- AGR-0001: Architecture Gate Review

---

## 14. Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-07-07 | Initial Specification | System |