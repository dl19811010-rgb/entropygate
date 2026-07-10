# M5-1 Capability Projection — Runtime Certification Report

**Version:** 1.0
**Date:** 2026-07-08
**Phase:** P3 Validation Era — M5-1 Capability Projection Runtime
**Status:** PASS

---

## 1. Capability Projection Engine

Pure-function CapabilityProjector: `ProjectionEvents → CapabilitySnapshots`

| Check | Result |
|-------|--------|
| Pure function (0 external deps) | PASS |
| Single event → single capability | PASS |
| Multi-event per subject → 1 aggregated snapshot | PASS |
| Multi-subject → separate snapshots | PASS |
| Deterministic output + sort order | PASS |
| Frozen dataclass (immutable snapshots) | PASS |
| Empty input → empty output | PASS |

**Projection Engine: PASS**

---

## 2. Capability Rules

8 event types → 7 capability types, deterministic mapping:

| Event Type | Capability Type | Status |
|-----------|----------------|--------|
| product_release | PRODUCT | PASS |
| funding_event | INVESTMENT | PASS |
| acquisition_event | MARKET | PASS |
| capability_update | TECHNICAL | PASS |
| partnership_event | PARTNERSHIP | PASS |
| benchmark_event | PERFORMANCE | PASS |
| deprecation_event | GENERAL | PASS |
| general_update | GENERAL | PASS |

4 status levels, date-driven thresholds:

| Status | Rule | Status |
|--------|------|--------|
| EMERGING | ≤30 days since first detection | PASS |
| ACTIVE | 1+ events, ≤90 days since last | PASS |
| MATURE | 5+ events, ≤180 days since last | PASS |
| DECLINING | >90 days since last event | PASS |

**Capability Rules: PASS**

---

## 3. Stable Capability ID

SHA256(subject_name + sorted(event_ids)) → 16 hex chars

| Check | Result |
|-------|--------|
| Same input → same ID | PASS |
| Order-independent | PASS |
| Fixed length (16) | PASS |
| Different event set → different ID | PASS |

**Stable Capability ID: PASS**

---

## 4. Capability Replay + Determinism

| Check | Result |
|-------|--------|
| 3-run Replay: snapshot_count identical | PASS |
| 3-run Replay: all capability IDs identical | PASS |
| 3-run Replay: Merkle root identical | PASS |
| 3-run Replay: status identical per snapshot | PASS |
| 3-run Replay: maturity_score, adoption_score, truth_score identical | PASS |
| 3-run Replay: event membership (source_event_ids) identical | PASS |
| 3-run Replay: tracked_capabilities identical | PASS |
| Empty input → deterministic empty | PASS |

**Capability Replay: PASS**

---

## 5. Projection Benchmark

10 scenarios, all deterministic:

| Scenario | Events | Snapshots | Determinism |
|----------|--------|-----------|-------------|
| Product Release | 1 | 1 | PASS |
| Funding | 1 | 1 | PASS |
| Multi-event aggregation | 2 | 1 | PASS |
| Mixed event types (5 subjects) | 5 | 5 | PASS |
| Event update (cap additions) | 3 | 1 | PASS |
| Event removal / declining | 1 | 1 | PASS |
| Duplicate replay | 2 | 1 | PASS |
| Empty input | 0 | 0 | PASS |
| Mixed events (1 subject) | 5 | 1 | PASS |
| Large set (30 events) | 30 | 10 | PASS |

**Benchmark: 10/10 PASS**

---

## 6. Summary

| Area | Result |
|------|--------|
| Capability Projection Engine | PASS |
| Capability Rules | PASS |
| Stable Capability ID | PASS |
| Capability Replay | PASS |
| Replay Determinism | PASS |
| Projection Benchmark (10 scenes) | PASS |
| Runtime Contract | PASS |

**M5-1 Capability Projection: ALL PASS (17/17 checks)**

---

## The Core Question Answered

> **对于任意一组 Event，在固定 Runtime 和固定 Projection Rules 下，Replay 任意次数，是否始终生成完全一致的 Capability Snapshot？**

**答案：YES.**

Evidence:
- 3-run Replay on 5 events (3 subjects): snapshot_count=3, all capability IDs identical, Merkle root identical
- All snapshot fields identical across runs: status, maturity_score, adoption_score, truth_score, event_count, source_event_ids, tracked_capabilities
- 10 benchmark scenarios, all pass 3-run determinism verification

---

## Runtime v1 链路闭环

```
Signal          ✅ M1 Fact Store
    ↓
Fact            ✅ M2 Extraction (deterministic)
    ↓
Canonical Fact  ✅ M3 Validation (conflict + merge + truth)
    ↓
Event           ✅ M4-1 Projection (deterministic replay)
    ↓
Capability      ✅ M5-1 Projection (deterministic replay)
```

---

## Evidence Artifacts

| Artifact | Path |
|----------|------|
| Capability Projection Engine | `app/services/capability_projection.py` (410+ lines) |
| Runtime Verification | `scripts/verify_m5.py` (17/17 PASS) |

---

## Signed

- Date: 2026-07-08
- Phase: M5-1 Capability Projection Runtime
- Result: ALL PASS (Engineering)
- Runtime v1 Core Chain: COMPLETE
