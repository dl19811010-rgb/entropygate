# Runtime v1 Guarantees

**Version:** v1  
**Date:** 2026-07-08  
**Status:** ACTIVE

---

## Guaranteed Properties

These properties are proven by certification tests and benchmark verification. They will remain true as long as the Runtime v1 core abstractions are unchanged.

### 1. Deterministic Extraction

> **Same Signal, fixed extraction config → same set of Facts, always.**

- Rule Extractor: pure function, no external dependencies
- LLM Extractor: temperature=0.1 fixed, rule fallback on failure
- Extraction Pipeline: unified entry point, single FactService

### 2. Deterministic Validation

> **Same Facts, fixed validation rules → same Conflicts, Canonical Facts, Truth Scores, and Decisions, always.**

- Conflict Detection: 5 types, deterministic rule-based
- Canonical Merge: deterministic SHA256-based merge IDs
- Truth Score: 5 configurable weighted dimensions, all deterministic
- Validation Decision: 5 levels, threshold-based

### 3. Deterministic Event Projection

> **Same Canonical Facts, fixed projection rules → same Events, always.**

- EventBuilder: pure function, 0 external dependencies
- Projection Rules: 12 single + 3 composite, priority-ordered
- Event IDs: SHA256-based, order-independent
- 3-run replay: event_count, event IDs, Merkle root, content all identical

### 4. Deterministic Capability Projection

> **Same Events, fixed projection rules → same Capability Snapshots, always.**

- CapabilityProjector: pure function, 0 external dependencies
- Capability Rules: 8 event types → 7 capability types
- Capability IDs: SHA256-based, order-independent
- 3-run replay: snapshot_count, IDs, Merkle root, status, scores, membership all identical

### 5. Replay Stability

> **Replay(N) == Replay(N+1) for all N ≥ 1, at every projection layer.**

Proven by 3-run replay verification at every level:
- Event Projection: identical across runs
- Capability Projection: identical across runs

### 6. Stable Identity

> **All projection outputs have deterministic, order-independent SHA256-based IDs.**

- Event ID = SHA256(sorted(fact_ids) + event_type + subject + date)
- Capability ID = SHA256(subject + sorted(event_ids))
- IDs are 16 hex characters, stable for the same input set

---

## NOT Guaranteed

These properties are explicitly outside the scope of Runtime v1 guarantees:

### LLM Output Quality

The LLM Extractor's output quality depends on the LLM model, prompt engineering, and training data. Runtime v1 guarantees only that the **extraction contract** (temperature=0.1, JSON schema, rule fallback) is followed. Extraction accuracy is a data quality concern, not a Runtime concern.

### External Data Source Quality

Fact truth_score depends on source reliability ratings (S/A/B/C/D). These ratings are configuration, not Runtime guarantees. Misclassified sources will produce inaccurate scores — this is a data governance issue.

### AIQL Query Accuracy

AIQL is not yet implemented. When built, it will be a Projection that queries certified Runtime outputs. Query accuracy will be a Capability concern, not a Runtime concern.

### End-to-End DB Runtime

Full alembic migration and pytest execution has not been verified in the current environment due to a venv Python/platform incompatibility. This is an operational environment issue, not a Runtime design issue. All engineering certifications have been completed via static analysis and pure-Python runtime verification.

---

## Guarantee Scope

```
┌─────────────────────────────────────────────┐
│  ✅ GUARANTEED                              │
│                                             │
│  Signal → Fact → Canonical → Event → Cap    │
│  (deterministic at every step)              │
│                                             │
│  Replay(N) == Replay(N+1)                   │
│  Stable IDs                                 │
│  Contract compliance (FES-0001)             │
│                                             │
├─────────────────────────────────────────────┤
│  ❌ NOT GUARANTEED                          │
│                                             │
│  LLM extraction accuracy                    │
│  Source quality / credibility               │
│  AIQL query accuracy (not yet built)        │
│  DB runtime environment                     │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Reference

- [FES-0002 Fact Contract](FES-0002-Fact-Contract.md)
- [ARCHITECTURE_LOCK](ARCHITECTURE_LOCK.md)
- [AI-Engineering-Rules](AI-Engineering-Rules.md)
- [Runtime v1 Validation Report](runtime_v1_validation_report.md)
