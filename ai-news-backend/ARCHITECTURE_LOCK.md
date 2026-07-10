# Architecture Lock v1.0

**Version:** AI Capability Operating System v1.0  
**Date:** 2026-07-07  
**Status:** LOCKED

---

## Frozen Documents

以下文档自锁定期起 **禁止修改**，除非经过 AGR 评审和 ADR 批准：

| Document | Version | Description |
|----------|---------|-------------|
| Vision | v1.0 | 系统愿景 |
| AIS | v1.0 | AI Intelligence Specification |
| AIQL | v1.0 | AI Query Language |
| AKG | v1.0 | AI Knowledge Graph |
| ADR-0001 | v1.0 | Why Fact is Atomic |
| ADR-0002 | v1.0 | Why Capability is Projection |
| ADR-0003 | v1.0 | Why Story replaces Cluster |
| ADR-0004 | v1.0 | Why Event Sourcing |
| AGR-0001 | v2.0 | Architecture Gate Review |
| FES-0001 | v1.0 | Fact Engine Specification |
| FES-0002 | v1.0 | Fact Contract |

---

## Change Process

如需修改上述文档，必须经过以下流程：

```
Issue Discovery
    ↓
AGR Review（架构门禁评审）
    ↓
ADR Approval（架构决策批准）
    ↓
Architecture Update
```

**禁止在以下阶段新增架构概念：**
- P1-2（Fact Engine + Event Sourcing）
- P1-3（Story Engine + Capability Projection）
- P1-4（AIQL + Answer Engine）
- P2（Performance + Scalability）

**例外情况：**
只有在 AGR 发现 Critical 级架构缺陷时，才允许变更架构。

---

## Future Document Types

锁定期后，新增文档必须属于以下类型之一：

| Type | Purpose | Example |
|------|---------|---------|
| RFC | 工程实现方案 | RFC-0001: Fact Extraction Pipeline |
| DGR | 实现层门禁 | DGR-0001: Fact Engine Review |
| Test Spec | 测试规范 | Test-0001: Replay Determinism |
| CI Check | 自动化检查 | CI-0001: Fact Immutability Check |

---

## Engineering Rules

锁定期后，所有工程实现必须遵守：

1. **Rule #1:** 禁止任何 Projection 写回 Fact
2. **Rule #2:** Fact 一旦 Confirmed，不可修改
3. **Rule #3:** Replay 只能用 Rule Engine
4. **Rule #4:** Projection 必须是纯函数
5. **Rule #5:** 禁止直接读 Signal

详见: [AI-Engineering-Rules.md](file:///E:/aitoto/ai-news-backend/AI-Engineering-Rules.md)

---

## Development Mode

**当前模式:** Architecture Locked → Engineering Execution

**不允许:**
- 新增 Layer、Entity、Engine、Ontology
- 修改 Frozen Documents
- 直接写代码而不经过 RFC

**必须:**
- 每个工程任务先写 RFC
- 每个 Milestone 有 Proof（可验证）
- 每个 PR 通过 DGR
- 每次提交通过 CI Check

---

## Lock Sign-off

| Role | Name | Approval | Date |
|------|------|----------|------|
| CTO / Architecture | - | ⏳ Pending | - |
| Product Owner | - | ⏳ Pending | - |
| Engineering Lead | - | ⏳ Pending | - |

---

**Lock Version History:**

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-07-07 | Initial Architecture Lock |