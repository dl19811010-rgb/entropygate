# Architecture Status

## Mission Statement

> **Build capabilities. Preserve foundations. Prove correctness.**
>
> 持续构建能力，保持基础稳定，并不断证明其正确性。

| Phrase | Corresponding Era | What it means |
|--------|-------------------|---------------|
| Build capabilities | Validation Era (P3+) | Daily work — adding projections |
| Preserve foundations | Governance Freeze | Core constraint — Runtime/Platform/Governance stay stable |
| Prove correctness | Long-term success | The ultimate standard — evidence over design |

---

## 三条核心原则

> 1. **The platform evolves by adding capabilities, not by changing its foundations.**
>    — 演进方式
>
> 2. **A healthy platform is one whose capabilities continue to grow while its runtime remains unchanged.**
>    — 成功标准
>
> 3. **Change capabilities by default. Change foundations only with evidence.**
>    — 治理规则

---

## 项目阶段

| 阶段 | 核心问题 | 当前状态 |
|------|---------|----------|
| P0 | Runtime 应该长什么样？ | ✅ 完成 |
| P1 | Runtime 是否可以冻结？ | ✅ 完成（LTS） |
| P2 | Platform 如何证明 Runtime 稳定？ | ✅ 完成（Platform LTS） |
| **P3** | **Runtime 是否真的能支撑长期演进？** | **▶️ Validation Era — V1 RELEASED** |
| P4 | Ecosystem / Marketplace | 长期目标 |

---

## Platform Architecture v1.0

**Released: 2026-07-07**
**Status: LTS — Governance Freeze**

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   Platform Architecture v1.0                             │
│   ───────────────────────                                │
│                                                          │
│   ✅ Runtime Frozen                                      │
│   ✅ Platform Frozen                                     │
│   ✅ Governance Frozen                                   │
│   ✅ Validation Model Established                        │
│                                                          │
│   Current Era:  Validation Era (P3)                      │
│   Architecture Status:  LTS                              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

This is not just an architecture freeze — it is a **governance freeze**.
The entire evolution model is now stable. Only Capability changes.

The result is **Platform Governance Model v1.0** — a complete set of
rules covering every question a long-term platform needs to answer:

| Question | Mechanism |
|----------|-----------|
| Why does it exist? | Mission Statement |
| How do we think? | Three Core Principles |
| How do we decide? | Default Decision Tree |
| What can't we do? | Constitution + Governance Freeze |
| How do we approve changes? | PR Checklist |
| How do we measure? | Validation Dashboard |
| How do we record? | ADR (Design / Validation) |
| How do we plan? | V-series Milestones |
| How do we control change? | Architecture Budget |
| What do words mean? | Frozen Glossary |
| Where does code live? | Directory Contract |

The project has transitioned from an **Architecture Project**
to a **Capability Platform**.

| Asset | Status | Note |
|-------|--------|------|
| Runtime LTS | 🔒 Frozen | Core Runtime v1.0, Bug Fix / Perf / Security only |
| Platform LTS | 🔒 Frozen | State + Controllers + Policies + Views |
| Governance Model | 🔒 Frozen | ADR flow, PR checklist, Constitution |
| Validation Model | 🔒 Frozen | Dashboard, DoD, Certification flow |
| SDK Stable | ✅ GA | Backward-compatible extensions allowed |
| Platform Constitution | 📜 Fixed | Seven immutable principles (ADR-0008) |
| ADR-0001 ~ ADR-0008 | 📚 Complete | Design ADRs — Architecture Era |
| Architecture Era | 🏁 Closed | Design phase complete |

### Version Semantics

From v1.0 onward, the platform version means different things:

| Component | Version Cadence | Allowed Upgrades |
|-----------|----------------|-----------------|
| Runtime | v1.x — LTS | ❌ Prohibited by default |
| Platform | v1.x — LTS | ❌ Prohibited by default |
| Governance | v1.x — LTS | ❌ Prohibited by default |
| SDK | v1.x — Stable | ✅ Backward-compatible extensions |
| Projection Packages | Independent | ✅ Continuous releases |
| Reference Library | Growing | ✅ Continuous growth |

**Platform stays at v1.0 forever (until proven insufficient).**
What grows is Capability.

Example release pattern:
```
Platform Architecture v1.0 (Frozen, 2026-07-07)

Capability Releases
────────────────────
v1.1  + Search Projection
v1.2  + Trend Projection
v1.3  + Company Projection
v1.4  + Forecast Projection
...
```

Default answer to "Should we do Runtime v2?":
> **No. Prove v1 is insufficient first.**

进入 Validation Era 后，新能力默认以 Projection 形式交付。
修改 Runtime / Platform / Governance 需要 ADR 级别的证据支持（见 ADR-0008 Exit Criteria）。

---

## 组件状态

| 组件 | 状态 | 版本 | 说明 |
|------|------|------|------|
| Core Runtime | 🔒 STABLE | 1.0 | LTS，仅修复 Bug |
| Core Contracts | 🔒 STABLE | 1.0 | Runtime Contract / Fact Contract / Replay Contract / Compatibility Contract |
| SDK | ✅ GA | 1.0 | 对外扩展接口 |
| Governance | ✅ ACTIVE | - | LTS 声明 / 版本策略 / 变更预算 / 生命周期 / 质量等级 / 能力矩阵 |
| Tooling | ✅ ACTIVE | - | Linter / Certification / Dashboard / Regression |
| Projection Library | 🔄 IN PROGRESS | - | 标准库建设 |
| Platform Audit | ✅ ACTIVE | - | Snapshot / Historical Record / Trend / Regression |

---

## 平台状态声明

### 从 "Architecture Closed" 到 "Architecture Stable"

```
┌─────────────────────────────────────────────────────────┐
│  Architecture Stable (Platform Under Validation)       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Core Runtime v1.0                                      │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 🔒 STABLE - 仅接受 Bug Fix / Performance /      │   │
│  │            Security / Internal Refactor         │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Projection SDK v1.0                                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │ ✅ OPEN - 作为扩展接口开放                        │   │
│  │   新增能力通过 Projection Package 实现           │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Platform Audit                                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │ ✅ ACTIVE - Snapshot / Trend / Regression       │   │
│  │            支持审计、趋势分析、回归追踪          │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Runtime 冻结

**Core Runtime v1.0 已稳定。**

```
🔒 STABLE

允许：
✓ Bug Fix
✓ Performance
✓ Security
✓ Internal Refactor
✓ Documentation

禁止：
✗ New Projection Type
✗ New Runtime Concept
✗ New Contract
✗ New Engine
✗ Breaking API Change
```

### Contract 冻结

**四个核心 Contract 已稳定：**

1. **Runtime Contract**: Projection Runtime / Replay / Checkpoint / Registry
2. **Projection SDK**: BaseProjectionPlugin + project() / explain() / metrics() / manifest() / fingerprint() / dependencies()
3. **Fact Contract**: Immutable / Deterministic / Provenance / Projection Purity
4. **Replay Contract**: Drop / Replay / Hash / Merkle / Checkpoint

---

## 核心工程原则

### 原则 1: Extension via Plugin

> **新增能力优先以 Projection Package 的形式实现，只有在确实无法满足需求时才讨论 Runtime 变更。**

### 原则 2: Runtime Change Budget

> **任何 Runtime API 修改必须回答三个问题：**
> 1. 为什么 Plugin 无法实现？
> 2. 为什么 SDK 无法实现？
> 3. 为什么必须修改 Runtime？
>
> 如果三个问题回答不了：**Runtime Change Rejected**

### 原则 3: Zero Runtime Changes Goal

> **P2 成功标准：在 Runtime 保持零功能修改的前提下，持续发布并认证标准库 Projection Package。**

### 原则 4: Platform Audit

> **平台行为必须可追溯、可审计、可回归。**
> - Snapshot: 每日健康快照
> - Trend: 趋势分析
> - Regression: 变化原因追踪

---

## P2 定义

**P2 = Platform Validation**

目标不是"继续开发插件"，而是：

> **验证平台是否能够支撑标准库的持续扩展。**

### P2 北极星目标

> **在 Runtime 保持零功能修改的前提下，持续发布并认证标准库 Projection Package。**

每完成一个 Projection，必须回答：

| 问题 | 通过标准 |
|------|----------|
| Runtime 有没有改？ | No |
| SDK 有没有改？ | No |
| Contract 有没有破？ | No |
| Certification 有没有通过？ | Yes |

---

## P3 — Validation Era

### Architecture Is a Constraint, Not the Main Work

The most important transition at P3:

> **Architecture is no longer the main work. It is a constraint.**

In Architecture Era (P0–P2), work was about:
> *Building the right abstractions.*

In Validation Era (P3+), work is about:
> *Proving those abstractions are right.*

Different mode. Different metrics. Different kind of value.

### Default Decision Tree (Repository-Wide)

This is the default workflow for any new issue or requirement.
It matches ADR-0008 and the PR Checklist.

```
New Requirement
      │
      ▼
Can Projection solve it?
      │
  Yes ───────────────► Build Projection
      │
     No
      ▼
Can SDK extension solve it?
      │
  Yes ───────────────► Extend SDK
      │
     No
      ▼
Can Policy solve it?
      │
  Yes ───────────────► Update Policy
      │
     No
      ▼
Collect Evidence
      │
      ▼
Write Validation ADR
      │
      ▼
Only then consider changing Runtime/Platform
```

Default answer for the first three is **Yes**.
If you can't prove "No" with evidence, use Projection / SDK / Policy.

### Architecture Budget (Annual)

Architecture changes are a scarce resource with a zero default budget.

| Type | Annual Budget | Default |
|------|-------------:|:-------:|
| Runtime Breaking Change | 0 | ❌ Prohibited |
| Platform Layer Addition | 0 | ❌ Prohibited |
| New Controller Type | 0 | ❌ Prohibited |
| New State Object | 0 | ❌ Prohibited |
| New Capability (Projection) | Unlimited | ✅ Encouraged |
| New Reference Implementation | Unlimited | ✅ Encouraged |
| New Benchmark | Unlimited | ✅ Encouraged |

**Key insight:**
Adding capabilities costs no budget.
Adding architecture consumes budget — and the budget is zero.

### Validation Milestones (V-series)

Future milestones are named by validation progress, not architecture evolution.

| Milestone | What it proves |
|-----------|---------------|
| **V1** | First 10 Certified Projections |
| **V2** | Reference Coverage ≥ 80% |
| **V3** | One Year Runtime Stability (zero breaking changes) |
| **V4** | Ecosystem Validation (≥ 5 community projections) |
| **V5** | External Adoption Validation |

Each milestone accumulates evidence that Runtime v1 was correctly designed.
The milestone name itself says what was validated.

### Validation Dashboard

This is the primary dashboard for P3.
Success is measured not by features added, but by evidence accumulated.

| Metric | Target | Trend | Current |
|--------|--------|-------|---------|
| Runtime API Changes | 0 | ↔ should stay flat | 0 |
| Platform Changes | 0 | ↔ should stay flat | 0 |
| Certified Projections | ≥ 20 | 📈 should grow | 2 |
| Reference Coverage | ≥ 80% | 📈 should grow | ~10% |
| Replay Success Rate | ≥ 95% | ↔ should stay high | 100% |
| RSI | ≥ 95 | ↔ should stay high | 100.0 |
| Architecture ADRs | Frozen (0001-0008) | 🔒 no new ADRs | 8 |

**The most important pattern:**
The first two stay flat, while the next five grow.
That is the strongest evidence that Runtime abstractions were correct.

### P3 Work Item Template

Every P3 work item follows this template.
Each capability release is itself a validation.

| Field | Value |
|-------|-------|
| Capability | What new Projection is added |
| Runtime Change | Must be **No** |
| Platform Change | Must be **No** |
| SDK Change | Yes / No |
| Policies Updated | Yes / No |
| Certification | PASS |
| Reference Coverage | before → after |
| ADR Required | Yes / No (default **No**) |

### Validation Era Commitment

> **Every new capability should strengthen confidence in the existing foundations.**
>
> 每新增一项能力，都应增强对现有基础的信心，而不是削弱它。

This is the long-term promise of the Validation Era:
- New capability → adds evidence
- New capability → introduces no new foundation abstraction
- New capability → increases trust in Runtime, Platform, and Governance

### Glossary (Frozen Vocabulary)

Vocabulary is frozen alongside Runtime and Platform.
All ADRs, docs, and issues use these terms consistently.

| Term | Definition |
|------|------------|
| **Runtime** | Executes capabilities. LTS and frozen by default. |
| **Platform** | Observes, certifies, and protects the Runtime. LTS and frozen. |
| **Governance** | The rules and processes constraining evolution. Frozen in v1.0. |
| **Capability** | A user-facing function implemented without changing Runtime. |
| **Projection** | A concrete capability package built on the Runtime. |
| **Reference** | Canonical implementation used for guidance and certification. |
| **Validation** | Evidence that existing abstractions remain sufficient. |
| **Design ADR** | ADR-0001–0008 defining how the platform was designed. |
| **Validation ADR** | ADR-0009+ recording evidence that design remains correct. |
| **RSI** | Runtime Stability Index — measure of Runtime stability. |
| **Fingerprint** | SHA256 hash of Platform Identity — unique platform identity. |
| **Identity** | Explains platform identity (Runtime Hash, SDK Hash, etc.). |
| **Descriptor** | Pure config object loaded from `platform.yaml`. |

### Directory Contract

Each top-level directory has exactly one responsibility.
New directories must answer: *which responsibility?*
If the answer is unclear, the directory probably shouldn't exist.

| Directory | Responsibility |
|-----------|---------------|
| `runtime/` | **Execute** — Core execution engines (Fact, Projection, Replay) |
| `platform/` | **Observe** — State + Controllers + Policies + Views |
| `governance/` | **Protect** — Policies, rules, release processes, standards |
| `projections/` | **Extend** — Capability packages (Core / Official / Community) |
| `sdk/` or `ai_kos/` | **Enable** — Extension interfaces and developer tools |
| `ADR/` | **Record** — Architecture decision records |
| `tests/` | **Verify** — Automated tests and golden datasets |

---

### Reference Implementation

**Timeline Projection 已成为第一个 Reference Implementation**

```yaml
projection: timeline
level: Core
stage: GA
reference: true
reference_for:
  - projection-sdk
  - contract-test
  - benchmark
  - certification
```

以后新的 Projection 都应该回答：
> 为什么不能像 Timeline 一样实现？

---

## Runtime Core Validation

**Status: Released**  
**Version: v1**  
**Date: 2026-07-08**  
**Evidence: Complete**

The Runtime v1 core chain has been fully validated:

```
Signal → Fact → Canonical → Event → Capability
  ✅      ✅       ✅         ✅       ✅
  M1      M2       M3        M4-1    M5-1
```

- 75 certification checks — ALL PASS
- 40 benchmark cases — ALL PASS
- Replay determinism proven at every projection layer
- No Runtime modifications required

See:
- [Runtime v1 Validation Report](runtime_v1_validation_report.md)
- [Runtime Guarantees](runtime_guarantees.md)
- [ADR-0009](ADR/ADR-0009-Runtime-Core-Validation-Completed.md)
- [Evidence Index](evidence/README.md)

---

## 当前 RSI

**Runtime Stability Index: 100.0/100** (🟢 EXCELLENT)

- Runtime API Changes: 0
- Contract Modifications: 0
- Frozen Concept Changes: 0
- Compatibility Score: 100%
- Replay Success Rate: 100%
- Golden Dataset: PASS

### RSI Release Gate

```
RSI >= 90       → PASS (Release OK)
80 <= RSI < 90  → WARNING (Release with caution)
RSI < 80        → BLOCKED (Fix before release)
```

---

## 架构状态声明

**Architecture is STABLE, not CLOSED.**

平台未来的创新发生在：
- Projection Package 层
- Tooling 层
- Platform Audit 层
- Marketplace 层

而不是 Runtime 层。

---

## 自动化治理

### Architecture Linter

```bash
python -m ai_kos.tools.linter
```

自动检查：
- Runtime Public API 修改
- Frozen Contract 修改
- Projection 规则违反
- Compatibility 破坏

### Projection Certification

```bash
python -m ai_kos.tools.certification my_projection.MyProjection
```

自动运行：
- Contract Test
- Golden Replay
- Benchmark
- Compatibility
- Explain / Metrics / Fingerprint / Manifest / Dependencies

输出 Certification Report。

### Runtime Health Dashboard

```bash
python -m ai_kos.tools.dashboard
```

输出：
- Runtime 状态
- Projection 统计
- RSI (Runtime Stability Index)
- 违规记录

---

## 文档索引

| 文档 | 路径 |
|------|------|
| LTS 声明 | governance/LTS-Declaration.md |
| 版本策略 | governance/Version-Strategy.md |
| Runtime 变更预算 | governance/Runtime-Change-Budget.md |
| Projection 生命周期 | governance/Projection-Lifecycle.md |
| Projection 质量等级 | governance/Projection-Quality-Levels.md |
| Projection 能力矩阵 | governance/Projection-Capability-Matrix.md |
| Package 路线图 | governance/Package-Roadmap.md |
| Package 评审 | governance/Package-Review.md |
| 发布策略 | governance/Release-Policy.md |
| 废弃策略 | governance/Deprecation-Policy.md |
| 安全策略 | governance/Security-Policy.md |
| 架构状态 | ARCHITECTURE-STATUS.md (本文件) |

---

## 更新记录

| 日期 | 事件 | RSI |
|------|------|-----|
| 2026-07-07 | Architecture Freeze → Platform Validation | 100.0 |

---

## 联系

- Runtime Maintainer: Core Team
- Architecture Board: arch@ai-kos.dev
- Security: security@ai-kos.dev