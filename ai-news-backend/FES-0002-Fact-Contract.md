# FES-0002: Fact Contract

**Version:** 1.0  
**Date:** 2026-07-07  
**Status:** Active  
**Type:** Supplement to FES-0001

---

## 1. Executive Summary

FES-0002 定义 Fact Engine 的 **四项核心契约（Contract）**，确保系统满足 Event Sourcing 的基本原则。

**核心原则:**

> **Fact 是唯一 Truth。所有 Projection 都是 Fact 的派生视图。**
> **Replay 必须 100% 确定性。**
> **Fact 一旦 Confirmed，不可修改。**
> **Projection 必须是纯函数。**

---

## 2. Contract 1: Fact Immutability（不可变）

### 2.1 Rule

**Fact 一旦进入 `confirmed` 状态，不能修改。只能 superseded（被新版本替代）。**

### 2.2 Rationale

如果 Fact 可以修改，则：
- Replay 无法得到一致结果
- Projection 无法保证一致性
- 审计无法追溯变化原因

### 2.3 Implementation

**❌ 错误做法:**

```sql
-- 禁止直接修改 confirmed Fact
UPDATE facts 
SET confidence = 0.92, truth_score = 0.8
WHERE id = 'fact_001' AND status = 'confirmed';
```

**✅ 正确做法:**

```sql
-- 创建新版本，标记旧版本为 superseded
INSERT INTO facts (id, version, supersedes, ...)
VALUES ('fact_002', 2, 'fact_001', ...);

UPDATE facts 
SET status = 'superseded', superseded_at = NOW(), superseded_by = 'fact_002'
WHERE id = 'fact_001';
```

### 2.4 Version Control

```text
Fact Lifecycle with Versions:

Fact V1 (confirmed)
    │
    │  ← 新证据发现，需要更新
    │
    ▼
Fact V2 (confirmed)
    supersedes = V1
    │
    │  ← 发现错误，需要修正
    │
    ▼
Fact V3 (confirmed)
    supersedes = V2

V1 和 V2 保留为 superseded（历史记录）
V3 是当前 canonical
```

### 2.5 Query Rules

**下游模块查询时只返回当前版本:**

```sql
-- 只查询非 superseded 的 Fact
SELECT * FROM facts 
WHERE status = 'confirmed'
AND superseded_by IS NULL;
```

**历史查询可以追溯版本链:**

```sql
-- 查询 Fact 的完整版本历史
SELECT f1.*, f2.* 
FROM facts f1
LEFT JOIN facts f2 ON f1.supersedes = f2.id
WHERE f1.id = 'fact_003';
```

---

## 3. Contract 2: Fact Provenance（来源链）

### 3.1 Rule

**每个 Fact 必须能追溯完整的来源链：**

```text
Fact
    ↓
Evidence (证据)
    ↓
Signal (信号)
    ↓
Source (来源)
    ↓
Raw Document (原始文档)
```

### 3.2 Rationale

- **AI 幻觉检测:** 如果 Fact 来自 AI 提取，必须能追溯到原始内容验证
- **错误事实修正:** 发现错误时，必须能找到源头进行修正
- **审计合规:** 必须能证明每个 Fact 的来源可信

### 3.3 Implementation

**Fact → Signal → Source → Raw Document:**

```text
fact_001
    │
    signal_id = signal_123
    │
    signal_123
    │
    source_id = source_openai_blog
    raw_content = "OpenAI released GPT-5..."
    source_url = "https://openai.com/blog/gpt-5"
    │
    source_openai_blog
    │
    signal_level = S
    name = "OpenAI Blog"
```

**Evidence Chain（证据链）:**

```text
Fact: GPT-5 supports Memory
    │
    Evidence 1:
    - signal_id = signal_openai_blog
    - source_level = S
    - confidence = 0.95
    │
    Evidence 2:
    - signal_id = signal_reddit_discussion
    - source_level = B
    - confidence = 0.70
    │
    Evidence 3:
    - signal_id = signal_twitter_announcement
    - source_level = A
    - confidence = 0.85
```

### 3.4 Query: Click to Raw Document

**用户可以点击 Fact → 查看原始 HTML:**

```sql
-- API 端点: /facts/{fact_id}/provenance
SELECT 
    f.id as fact_id,
    f.subject_name,
    f.predicate,
    f.object_name,
    s.id as signal_id,
    s.title as signal_title,
    s.source_url,
    s.raw_content,
    src.name as source_name,
    src.signal_level,
    src.url as source_url
FROM facts f
JOIN signals s ON f.signal_id = s.id
JOIN sources src ON s.source_id = src.id
WHERE f.id = :fact_id;
```

### 3.5 Provenance Display

```json
{
  "fact": {
    "id": "fact_001",
    "subject": "GPT-5",
    "predicate": "supports",
    "object": "Memory"
  },
  "provenance": {
    "signal": {
      "id": "signal_123",
      "title": "OpenAI released GPT-5...",
      "url": "https://openai.com/blog/gpt-5"
    },
    "source": {
      "name": "OpenAI Blog",
      "signal_level": "S",
      "credibility": 95
    },
    "raw_content": "OpenAI officially announced GPT-5 today...",
    "evidence_count": 3,
    "evidences": [
      {"source": "OpenAI Blog", "confidence": 0.95},
      {"source": "Twitter", "confidence": 0.85},
      {"source": "Reddit", "confidence": 0.70}
    ]
  }
}
```

---

## 4. Contract 3: Fact Determinism（确定性）

### 4.1 Rule

**Replay 必须是 100% 确定性：**

```text
相同输入（Fact Log）
    ↓
相同输出（Projection）
```

### 4.2 Rationale

如果 Replay 不确定：
- 第一次 Replay → 18 Events
- 第二次 Replay → 19 Events
- Projection 无法保证一致性
- 系统不可信任

### 4.3 Determinism Guarantee

**Builder 必须满足:**

```text
EventBuilder = Pure Function

Input: Fact[]
Output: Event[]

相同 Fact[] → 相同 Event[]
```

**禁止的做法:**

```python
# ❌ 错误：依赖外部状态
def build_events(facts):
    current_time = datetime.now()  # 外部状态
    random_threshold = random.random()  # 随机性
    external_config = db.query(Config).first()  # 数据库查询
```

**正确的做法:**

```python
# ✅ 正确：纯函数
def build_events(facts):
    # 所有参数来自 facts 本身
    events = []
    for fact in facts:
        event_type = PREDICATE_TO_EVENT_TYPE[fact.predicate]  # 预定义规则
        events.append(Event(
            title=f"{fact.subject_name} {fact.predicate}",
            type=event_type,
            facts=[fact.id],
            detected_at=fact.time_value or fact.created_at  # 来自 fact
        ))
    return events
```

### 4.4 AI vs Rule Engine

**分工明确:**

| Task | Who | Why |
|------|-----|-----|
| Fact Extraction | AI + LLM | 需要语义理解 |
| Fact → Event | Rule Engine | 必须 Deterministic |
| Event → Story | Rule Engine | 必须 Deterministic |
| Event → Capability | Rule Engine | 必须 Deterministic |
| Story Summary | AI + LLM | 可以有随机性（不影响 Replay） |

**关键原则:**

> **Replay 只能用 Rule Engine，不能用 AI。**
> **AI 只能参与 Fact Extraction（一次性），不能参与 Projection。**

### 4.5 Determinism Test

**测试代码:**

```python
def test_replay_determinism():
    # 第一次 Replay
    facts = get_all_facts_ordered()
    events_v1 = build_events(facts)
    
    # 第二次 Replay（相同输入）
    events_v2 = build_events(facts)
    
    # 必须完全相同
    assert len(events_v1) == len(events_v2)
    for e1, e2 in zip(events_v1, events_v2):
        assert e1.title == e2.title
        assert e1.type == e2.type
        assert e1.detected_at == e2.detected_at
        assert set(e1.facts) == set(e2.facts)
```

---

## 5. Contract 4: Projection Purity（纯函数）

### 5.1 Rule

**Projection 必须是纯函数：**

```text
Projection = f(Facts)

输入: Fact[]
输出: Capability Snapshot / Event[] / Story[]

不依赖任何外部状态
不修改任何外部状态
```

### 5.2 Rationale

如果 Projection 依赖外部状态：
- Drop → Replay 无法保证一致
- Projection 之间可能形成依赖循环
- 系统复杂度爆炸

### 5.3 Pure Function Definition

**❌ 错误：依赖数据库**

```python
# 禁止：读数据库、写数据库、再计算
def capability_projection(facts):
    # ❌ 读取外部状态
    existing_caps = db.query(Capability).all()
    
    # 计算
    for fact in facts:
        cap = find_capability(existing_caps, fact.object_name)
        cap.maturity += 1
    
    # ❌ 写数据库
    db.commit()
```

**✅ 正确：纯函数**

```python
# 正确：输入 Fact[]，输出 Capability Snapshot
def capability_projection(facts):
    # 输入：facts
    # 输出：capability snapshots（不写数据库）
    
    snapshots = {}
    for fact in facts:
        cap_id = fact.object_id or generate_capability_id(fact.object_name)
        
        if cap_id not in snapshots:
            snapshots[cap_id] = CapabilitySnapshot(
                id=cap_id,
                name=fact.object_name,
                maturity=0,
                adoption=set(),
                truth_score=0.0,
                events=[]
            )
        
        # 累加计算（纯函数）
        snapshots[cap_id].maturity += 1
        snapshots[cap_id].adoption.add(fact.subject_id)
        snapshots[cap_id].truth_score += get_truth_delta(fact)
        snapshots[cap_id].events.append(fact.signal_id)
    
    return snapshots  # 返回结果，不写数据库
```

### 5.4 Projection Storage

**Projection 结果可以缓存，但必须可丢弃:**

```text
Fact Store（永久）
    │
    ├─► Event Projection（可丢弃，可重建）
    │
    ├─► Story Projection（可丢弃，可重建）
    │
    ├─► Capability Projection（可丢弃，可重建）
    │
    └─► Timeline Projection（可丢弃，可重建）
```

**Drop Projections:**

```sql
-- 删除所有 Projection（Event、Story、Capability）
DELETE FROM events;
DELETE FROM stories;
DELETE FROM capabilities;
-- Fact 不动

-- Replay
-- Event、Story、Capability 自动重建
```

### 5.5 Projection Cache

**缓存策略:**

```text
第一次查询:
    Fact[] → Projection → 结果（写入缓存）

后续查询:
    直接读缓存

Drop:
    清空缓存 → 重新 Projection
```

**缓存一致性:**

```python
# 新 Fact 到达 → 更新缓存
def on_new_fact(fact):
    # 增量更新（不重新计算全部）
    update_capability_cache(fact)
    update_event_cache(fact)
    update_story_cache(fact)
```

---

## 6. Architecture: Fact Store as Single Truth

### 6.1 Database Schema

```text
┌─────────────────────────────────────────────────┐
│                  Raw Signal                      │
│                     │                            │
│                     ▼                            │
│               Fact Store                         │ ← 唯一 Truth
│                     │                            │
│    ┌────────────────┼────────────────┐          │
│    │                │                │          │
│    ▼                ▼                ▼          │
│ Event           Story          Capability       │
│ Projection      Projection     Projection       │
│    │                │                │          │
│    ▼                ▼                ▼          │
│ Timeline       Answer           Graph          │
│ Projection     Projection       View           │
└─────────────────────────────────────────────────┘

注意：
- Event 不是 Truth
- Story 不是 Truth
- Capability 不是 Truth
- 全部都是 Projection
- 真正永久保存的只有 Fact
```

### 6.2 Data Persistence

**永久存储:**

```text
Signal (可归档，不可删除)
Fact Store (唯一 Truth，永久保存)
```

**可丢弃存储:**

```text
Events (Projection，可重建)
Stories (Projection，可重建)
Capabilities (Projection，可重建)
Timelines (Projection，可重建)
```

---

## 7. Engineering Rule: No Projection → Fact

### 7.1 Highest Priority Rule

> **Rule #1：禁止任何 Projection 写回 Fact。**

### 7.2 Rationale

如果 Projection 可以写回 Fact：
- 形成循环依赖
- Replay 无法保证一致
- 系统复杂度爆炸

### 7.3 Allowed vs Forbidden

**✅ 允许的数据流:**

```text
Signal → Fact → Event
Fact → Event → Story
Event → Capability Projection
Fact → Truth Evolution
```

**❌ 禁止的数据流:**

```text
Projection → 修改 Fact
Event → 修改 Fact
Capability → 修改 Fact
Story → 修改 Fact
Score → 修改 Fact
```

### 7.4 Enforcement

**代码审查规则:**

```python
# ❌ 禁止：Projection 写回 Fact
class CapabilityProjection:
    def update_fact(self, fact_id, new_truth_score):
        # 这行代码必须被禁止
        fact = self.db.query(Fact).get(fact_id)
        fact.truth_score = new_truth_score
        self.db.commit()
```

**必须改为:**

```python
# ✅ 正确：创建新 Fact Version
class CapabilityProjection:
    def supersede_fact(self, old_fact_id, new_fact_data):
        # 创建新版本
        new_fact = Fact(
            version=old_fact.version + 1,
            supersedes=old_fact_id,
            **new_fact_data
        )
        self.db.add(new_fact)
        
        # 标记旧版本
        old_fact = self.db.query(Fact).get(old_fact_id)
        old_fact.status = 'superseded'
        old_fact.superseded_by = new_fact.id
```

---

## 8. P1-2 PR Split

### 8.1 Five PRs

| PR | 内容 | 允许合并条件 |
|----|------|-------------|
| **PR-1** | Fact Schema + Migration | ✅ 可独立合并 |
| **PR-2** | Fact Extractor (Signal → Fact[]) | ✅ 可独立合并 |
| **PR-3** | Fact Validator + Merge | ✅ 可独立合并 |
| **PR-4** | Event Builder (Fact → Event) | ✅ 可独立合并（验证 Determinism） |
| **PR-5** | Capability Projection + Replay | ✅ 最后合并（验证 Replay） |

### 8.2 PR Validation

**PR-1 Validation:**

```bash
# 验证 Schema
python -c "from app.models.intelligence import Fact; print(Fact.__table__.columns.keys())"

# 验证 Migration
alembic upgrade head
alembic downgrade head
alembic upgrade head
```

**PR-2 Validation:**

```python
# 验证 Signal → 多 Fact
signal = create_test_signal()
facts = extract_facts(signal)
assert len(facts) >= 1  # 至少一个 Fact
```

**PR-3 Validation:**

```python
# 验证 Merge
fact1 = create_fact(subject="GPT-5", predicate="supports", object="Memory")
fact2 = create_fact(subject="GPT-5", predicate="supports", object="Memory")
merged = merge_facts([fact1, fact2])
assert merged.canonical_id == fact1.id
assert fact2.duplicate_of == fact1.id
```

**PR-4 Validation:**

```python
# 验证 Determinism
facts = get_test_facts()
events_v1 = build_events(facts)
events_v2 = build_events(facts)
assert events_v1 == events_v2  # 必须完全相同
```

**PR-5 Validation:**

```python
# 验证 Replay
drop_projections()
replay_facts()
events = get_events()
capabilities = get_capabilities()
assert len(events) > 0
assert len(capabilities) > 0
```

---

## 9. Contract Violation Detection

### 9.1 Automated Checks

**Rule Engine 检查:**

```python
def check_fact_immutability():
    # 检查是否有 confirmed Fact 被修改
    modified_facts = db.query(Fact).filter(
        Fact.status == 'confirmed',
        Fact.updated_at > Fact.confirmed_at
    ).all()
    return len(modified_facts) == 0

def check_projection_purity():
    # 检查 Projection 是否依赖外部状态
    # (通过代码分析或单元测试)
    pass

def check_no_projection_writeback():
    # 检查是否有 Projection 写回 Fact
    # (通过代码审查规则)
    pass
```

### 9.2 Runtime Monitoring

**Replay 定期验证:**

```python
# 每周自动 Replay 验证
@scheduled_task(cron="0 3 * * 0")
def weekly_replay_verification():
    # 记录当前状态
    current_events = get_events()
    current_caps = get_capabilities()
    
    # Replay
    drop_projections()
    replay_facts()
    
    # 验证一致
    replay_events = get_events()
    replay_caps = get_capabilities()
    
    if current_events != replay_events:
        alert("Replay inconsistency detected!")
```

---

## 10. Summary

**四项核心契约:**

| Contract | Rule | Enforcement |
|----------|------|-------------|
| **Immutability** | Fact confirmed 后不可修改 | 只能 superseded |
| **Provenance** | Fact → Signal → Source → Raw | 来源链完整 |
| **Determinism** | Replay 100% 确定性 | Rule Engine only |
| **Projection Purity** | Projection = f(Facts) | 纯函数，不依赖外部 |

**最高优先级工程规则:**

> **Rule #1：禁止任何 Projection 写回 Fact。**

---

## 11. Reference

- FES-0001: Fact Engine Specification
- ADR-0001: Why Fact is Atomic
- ADR-0002: Why Capability is Projection
- ADR-0004: Why Event Sourcing

---

## 12. Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-07-07 | Initial Contract Definition | System |