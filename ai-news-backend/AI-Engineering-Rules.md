# AI Engineering Rules

**Version:** 1.0  
**Date:** 2026-07-07  
**Priority:** Highest

---

## Rule #1: 禁止任何 Projection 写回 Fact

**这是整个项目的最高优先级工程规则。**

### Rule

> **禁止任何 Projection（Event、Story、Capability、Score、Timeline）写回 Fact。**

### Rationale

如果 Projection 可以写回 Fact：
- 形成循环依赖
- Replay 无法保证一致
- 系统复杂度爆炸
- Event Sourcing 架构失效

### Allowed Data Flow

```text
✅ Signal → Fact → Event
✅ Fact → Event → Story
✅ Event → Capability Projection
✅ Fact → Truth Evolution
```

### Forbidden Data Flow

```text
❌ Projection → 修改 Fact
❌ Event → 修改 Fact
❌ Capability → 修改 Fact
❌ Story → 修改 Fact
❌ Score → 修改 Fact
```

### Enforcement

**代码审查必须检查:**

```python
# ❌ 禁止代码示例
class CapabilityProjection:
    def update_fact(self, fact_id, new_truth_score):
        fact = self.db.query(Fact).get(fact_id)
        fact.truth_score = new_truth_score  # 这行代码必须被拒绝
        self.db.commit()
```

**正确做法:**

```python
# ✅ 正确代码示例
class CapabilityProjection:
    def supersede_fact(self, old_fact_id, new_fact_data):
        # 创建新版本（不修改旧版本）
        new_fact = Fact(
            version=old_fact.version + 1,
            supersedes=old_fact_id,
            **new_fact_data
        )
        self.db.add(new_fact)
        
        # 标记旧版本为 superseded（不修改内容）
        old_fact.status = 'superseded'
        old_fact.superseded_by = new_fact.id
```

---

## Rule #2: Fact 一旦 Confirmed，不可修改

### Rule

> **Fact 进入 `confirmed` 状态后，内容不可修改。只能被 `superseded`。**

### See

- FES-0002: Contract 1 - Fact Immutability

---

## Rule #3: Replay 只能用 Rule Engine

### Rule

> **Replay 必须 100% 确定性。禁止使用 AI 或随机性。**

### Allowed

```text
✅ Fact Extraction → AI + LLM（需要语义理解）
✅ Fact → Event → Rule Engine（必须 Deterministic）
✅ Event → Story → Rule Engine（必须 Deterministic）
✅ Event → Capability → Rule Engine（必须 Deterministic）
```

### Forbidden

```text
❌ Fact → Event → AI（Replay 不确定）
❌ Event → Story → AI（Replay 不确定）
❌ Event → Capability → AI（Replay 不确定）
```

### See

- FES-0002: Contract 3 - Fact Determinism

---

## Rule #4: Projection 必须是纯函数

### Rule

> **Projection = f(Facts)。不依赖外部状态，不修改外部状态。**

### See

- FES-0002: Contract 4 - Projection Purity

---

## Rule #5: 禁止直接读 Signal

### Rule

> **所有下游模块（Event、Story、Capability）只能读取 Fact，禁止直接读取 Signal。**

### Allowed

```text
✅ Fact Engine → Signal（提取 Fact）
✅ Event Builder → Fact（构建 Event）
✅ Story Engine → Fact + Event（构建 Story）
✅ Capability Projection → Fact + Event（构建 Capability）
```

### Forbidden

```text
❌ Event Builder → Signal（直接）
❌ Story Engine → Signal（直接）
❌ Capability Projection → Signal（直接）
```

### See

- ADR-0001: Why Fact is Atomic
- FES-0001: §11 Boundary Rules

---

## Enforcement Summary

| Rule | Priority | Enforcement |
|------|----------|-------------|
| Rule #1: No Projection → Fact | **P0** | Code Review + Automated Check |
| Rule #2: Fact Immutability | **P0** | Code Review + Database Constraint |
| Rule #3: Replay Determinism | **P0** | Unit Test + Automated Replay Test |
| Rule #4: Projection Purity | **P1** | Code Review + Unit Test |
| Rule #5: No Direct Signal Read | **P1** | Code Review + Architecture Check |

---

## Reference

- FES-0001: Fact Engine Specification
- FES-0002: Fact Contract
- ADR-0001: Why Fact is Atomic
- ADR-0002: Why Capability is Projection
- ADR-0004: Why Event Sourcing
- AGR-0001: Architecture Gate Review