# Runtime v2 Reference Validation Report

**Version:** v2
**Date:** 2026-07-08
**Era:** Validation Era — V2 Golden Dataset & Reference Validation
**Status:** RELEASED

---

## 1. Executive Summary

V2 establishes the **Golden Dataset** as the long-term reproducible validation standard for Runtime v1. It proves that the Runtime is stable not just on synthetic test cases (V1), but on 182 real-world representative signals across 8 categories.

---

## 2. Golden Dataset v1

| Metric | Value |
|--------|-------|
| Version | v1 |
| Categories | 8 (funding, release, acquisition, partnership, research, regulation, model, benchmark) |
| Total cases | 182 |
| Cases per category | 22-25 |
| Format | Structured Python module with fixed input/expected output |

Dataset source: `golden/dataset_v1.py`

---

## 3. End-to-End Golden Replay

| Layer | Result |
|-------|--------|
| Extraction (Rule) | 182/182 deterministic |
| Validation | 182/182 deterministic |
| Event Projection | 182/182 deterministic |
| Capability Projection | 182/182 deterministic |
| Full E2E | 182/182 deterministic (100%) |

Replay script: `scripts/golden_replay.py`

---

## 4. Reference Coverage

| Coverage Type | Rate |
|--------------|------|
| Predicate coverage | 11/12 (92%) |
| Event type coverage | 8/8 (100%) |
| Capability type coverage | 7/7 (100%) |
| Projection rule coverage | 8/8 (100%) |

Coverage report: `reference_coverage.md`

---

## 5. Golden Drift Detection

- Baseline saved: `golden/baseline_v1.json`
- Baseline Merkle root: `a149bb50ced15eb10c415d03728f934901cca53850fc729cd588e69f2979df7c`
- Drift check: Any Runtime change that alters the golden replay output is detected
- Script: `scripts/golden_drift_check.py`

---

## 6. CI Validation

- CI script: `scripts/ci_validate.py`
- Exit code 0 = PASS, 1 = FAIL
- Runs: Golden Replay + Drift Detection
- Any drift or non-deterministic result blocks merge

---

## 7. Summary

| Area | Result |
|------|--------|
| Golden Dataset | PASS |
| Golden Replay | PASS |
| Reference Coverage | PASS |
| Drift Detection | PASS |
| CI Validation | PASS |

**V2 Reference Validation: ALL PASS**

---

## 8. Evidence Artifacts

| Artifact | Path |
|----------|------|
| Golden Dataset | `golden/dataset_v1.py` (182 cases) |
| Golden Replay Runner | `scripts/golden_replay.py` |
| Drift Detection | `scripts/golden_drift_check.py` |
| CI Validation | `scripts/ci_validate.py` |
| Baseline | `golden/baseline_v1.json` |
| Coverage Report | `reference_coverage.md` |

---

## Signed

- Date: 2026-07-08
- Version: V2 Reference Validation
- Result: RELEASED
