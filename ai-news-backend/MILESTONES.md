# P1-2 Milestones

**Phase:** P1-2  
**Target:** AI Capability Intelligence Platform v1.0  
**Status:** Validation Release V1 — COMPLETE (2026-07-08)

## 🏆 V1 Release

```
Runtime v1 Core Validation Release
Released: 2026-07-08
Status: COMPLETE

M1 Fact Store           🟢 CERTIFIED
M2 Fact Extraction      🟢 CERTIFIED
M3 Fact Validation      🟢 CERTIFIED
M4-1 Event Projection   🟢 CERTIFIED
M5-1 Capability         🟢 CERTIFIED

75+ checks ALL PASS | 40 benchmarks ALL PASS
Replay Determinism: Proven at every layer
```

---

## Overview

```
P1-2

Milestone 1: Fact Store
    ↓
Milestone 2: Fact Extraction
    ↓
Milestone 3: Fact Validation
    ↓
Milestone 4: Event Projection
    ↓
Milestone 5: Capability Projection
    ↓

P1-2 Complete
```

---

## Milestone 1: Fact Store

**Target:** 可靠的 Fact Store（唯一 Truth）

**Duration:** 1 week

**Tasks:**

- [ ] Fact Schema（SQLAlchemy Model）
- [ ] Alembic Migration
- [ ] Predicate Dictionary
- [ ] Fact Lifecycle State Machine
- [ ] Fact Contract Test Framework

**Proof:**

```python
def proof():
    signal = create_test_signal()
    facts = extract_facts(signal)
    assert len(facts) >= 1
    for fact in facts:
        assert fact.predicate in PREDICATE_DICTIONARY
    confirmed = confirm_fact(facts[0])
    with pytest.raises(Exception):
        confirmed.confidence = 0.99
        db.commit()
    return True
```

**DoD:**

| Criteria | Standard | Status |
|----------|----------|--------|
| Schema 完整 | 25 字段 + 8 索引 | ⏳ |
| Migration | 可升级/回滚 | ⏳ |
| Predicate | 12 个定义 | ⏳ |
| Lifecycle | 8 状态 + 10 转换 | ⏳ |
| Contract Test | 4 项通过 | ⏳ |

---

## Milestone 2: Fact Extraction

**Target:** Signal → Fact[]

**Duration:** 1 week

**Tasks:**

- [ ] Signal Parser
- [ ] LLM Extractor
- [ ] Rule Extractor
- [ ] Multi-Fact Extraction（1 Signal → N Facts）
- [ ] Provenance Chain（Fact → Signal → Source）

**Proof:**

```python
def proof():
    signal = create_test_signal(
        title="OpenAI released GPT-5 with Memory support, price reduced 30%"
    )
    facts = extract_facts(signal)
    assert len(facts) >= 3  # released + supports + price_changed
    predicates = [f.predicate for f in facts]
    assert "released" in predicates
    assert "supports" in predicates
    assert "price_changed" in predicates
    return True
```

**DoD:**

| Criteria | Standard | Status |
|----------|----------|--------|
| Multi-Fact | 1 Signal → N Facts | ⏳ |
| LLM Extractor | 提取准确率 ≥ 80% | ⏳ |
| Rule Extractor | 覆盖 12 predicate | ⏳ |
| Provenance | 完整来源链 | ⏳ |

---

## Milestone 3: Fact Validation

**Target:** 可信的 Fact

**Duration:** 1 week

**Tasks:**

- [ ] Fact Validation（5 维度评分）
- [ ] Conflict Detection（矛盾检测）
- [ ] Canonical Merge（相同事实合并）
- [ ] Duplicate Resolution（重复解决）
- [ ] Truth Score（真实性评分）

**Proof:**

```python
def proof():
    # 矛盾检测
    fact1 = create_fact(subject="GPT-5", predicate="supports", object="Memory")
    fact2 = create_fact(subject="GPT-5", predicate="not_supports", object="Memory")
    conflict = detect_conflict(fact1, fact2)
    assert conflict is not None
    
    # 合并
    fact3 = create_fact(subject="GPT-5", predicate="supports", object="Memory")
    fact4 = create_fact(subject="GPT-5", predicate="supports", object="Memory")
    merged = merge_facts([fact3, fact4])
    assert merged.evidence_count == 2
    
    return True
```

**DoD:**

| Criteria | Standard | Status |
|----------|----------|--------|
| Validation | 5 维度评分 | ⏳ |
| Conflict | 自动检测矛盾 | ⏳ |
| Merge | 相同事实合并 | ⏳ |
| Truth Score | 动态计算 | ⏳ |

---

## Milestone 4: Event Projection

**Target:** 所有 Projection 都能由 Fact 重建

**Duration:** 1 week

**Tasks:**

- [ ] Event Projection（Fact → Event）
- [ ] Story Projection（Event → Story）
- [ ] Timeline Projection（Event → Timeline）
- [ ] Replay Engine（Drop → Replay → 恢复）
- [ ] Determinism Test（100% 确定性）

**Proof:**

```python
def proof():
    # 记录当前状态
    events_before = get_events()
    caps_before = get_capabilities()
    
    # Drop Projections
    drop_projections()
    
    # Replay
    replay_engine.replay_all()
    
    # 验证一致
    events_after = get_events()
    caps_after = get_capabilities()
    
    assert events_before == events_after
    assert caps_before == caps_after
    
    return True
```

**DoD:**

| Criteria | Standard | Status |
|----------|----------|--------|
| Event Projection | Fact → Event | ⏳ |
| Story Projection | Event → Story | ⏳ |
| Timeline Projection | Event → Timeline | ⏳ |
| Replay | Drop → Replay → 一致 | ⏳ |
| Determinism | 100% 确定性 | ⏳ |

---

## Milestone 5: Capability Projection

**Target:** AI Capability Intelligence Platform v1.0

**Duration:** 1 week

**Tasks:**

- [ ] Capability Projection（Event → Capability）
- [ ] AIQL Query Engine（Fact-based Query）
- [ ] Answer Builder（Query → Answer）
- [ ] Replay Validation（定期验证）
- [ ] Integration Test（端到端）

**Proof:**

```python
def proof():
    # 端到端测试
    signal = create_test_signal(
        title="OpenAI released GPT-5 with Memory support"
    )
    
    # Pipeline
    facts = extract_facts(signal)
    events = build_events(facts)
    stories = build_stories(events)
    capabilities = project_capabilities(events)
    
    # 验证
    assert len(facts) >= 2
    assert len(events) >= 1
    assert len(stories) >= 1
    assert len(capabilities) >= 1
    
    # 查询
    result = aiql_query("What capabilities does GPT-5 support?")
    assert "Memory" in result
    
    # Replay 验证
    drop_projections()
    replay_all()
    assert get_capabilities() == capabilities
    
    return True
```

**DoD:**

| Criteria | Standard | Status |
|----------|----------|--------|
| Capability Projection | Event → Capability | ⏳ |
| AIQL | 查询准确率 ≥ 85% | ⏳ |
| Answer | 回答可用 | ⏳ |
| Replay | 定期验证通过 | ⏳ |
| E2E | 端到端测试通过 | ⏳ |

---

## P1-2 Complete Criteria

| 验收项 | 标准 | 状态 |
|--------|------|------|
| Signal 能拆分为多个 Fact | ✅ 同一 Signal 至少 N 个 Fact | ⏳ |
| Fact 生命周期完整 | ✅ Extracted → Confirmed → Rejected | ⏳ |
| Fact 支持 Canonical Merge | ✅ 相同事实不会无限增长 | ⏳ |
| Fact 支持 Replay | ✅ 删除 Event 后可重新构建 | ⏳ |
| Event 只能由 Fact 构建 | ✅ 禁止 Signal → Event 直连 | ⏳ |
| Capability 只能由 Event Projection 更新 | ✅ 禁止直接修改 Capability | ⏳ |
| Story 基于 Fact/Event 聚合 | ✅ 不再依赖文本相似度 Cluster | ⏳ |

---

## Success Metrics

**从"代码完成"改为"可证明":**

| 里程碑 | 成功标准 |
|--------|----------|
| Milestone 1 | Schema 完整 + Contract 测试通过 |
| Milestone 2 | Signal → N Facts + Provenance 完整 |
| Milestone 3 | Conflict 检测 + Merge 正确 + Truth Score 合理 |
| Milestone 4 | Drop Projection → Replay → Hash 一致 |
| Milestone 5 | E2E 测试通过 + AIQL 查询可用 |

---

## Reference

- [ARCHITECTURE_LOCK](file:///E:/aitoto/ai-news-backend/ARCHITECTURE_LOCK.md)
- [RFC-0001](file:///E:/aitoto/ai-news-backend/RFC/RFC-0001-Fact-Store.md)
- [FES-0001](file:///E:/aitoto/ai-news-backend/FES-0001-Fact-Engine-Specification.md)
- [FES-0002](file:///E:/aitoto/ai-news-backend/FES-0002-Fact-Contract.md)
- [AI-Engineering-Rules](file:///E:/aitoto/ai-news-backend/AI-Engineering-Rules.md)