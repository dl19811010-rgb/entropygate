# Reference Coverage Report

**Golden Dataset v1**
**Date: 2026-07-08**

---

## Dataset Summary

| Metric | Value |
|--------|-------|
| Version | v1 |
| Categories | 8 |
| Total cases | 182 |
| Replay deterministic | 100% (182/182) |
| Baseline Merkle root | a149bb50ced15eb10c415d03728f934901cca53850fc729cd588e69f2979df7c |

---

## Category Distribution

| Category | Cases | Focus |
|----------|-------|-------|
| funding | 25 | Investment rounds, valuation events |
| release | 25 | Product launches, model releases |
| acquisition | 22 | Company acquisitions, team acquisitions |
| partnership | 22 | Strategic partnerships, integrations |
| research | 22 | Papers, findings, academic releases |
| regulation | 22 | Laws, executive orders, governance |
| model | 22 | Model updates, deprecations, capability changes |
| benchmark | 22 | Benchmark results, performance evaluations |

---

## Predicate Coverage

| Predicate | Categories Covered | Cases |
|-----------|-------------------|-------|
| released | 7/8 (all except regulation) | ~80 |
| supports | release, research, model | ~30 |
| benchmark_result | research, model, benchmark | ~25 |
| integration | partnership, acquisition, regulation | ~20 |
| capability_updated | model, release | ~8 |
| capability_added | model | ~6 |
| depreciation / capability_removed | model | ~6 |
| api_updated | release, partnership, model | ~8 |
| price_changed | release, model | ~4 |
| limitation | regulation | ~4 |
| region_available | model | ~4 |

**Predicate Coverage: 11/12 (92%)** — remaining: `not_supports` (only used in conflict detection)

---

## Event Type Coverage

| Event Type | Cases | % |
|-----------|-------|---|
| PRODUCT_RELEASE | ~55 | 30% |
| CAPABILITY_UPDATE | ~30 | 16% |
| PARTNERSHIP_EVENT | ~25 | 14% |
| BENCHMARK_EVENT | ~27 | 15% |
| FUNDING_EVENT | ~20 | 11% |
| GENERAL_UPDATE | ~18 | 10% |
| DEPRECATION_EVENT | ~4 | 2% |
| ACQUISITION_EVENT | ~3 | 2% |

**Event Type Coverage: 8/8 (100%)**

---

## Capability Type Coverage

| Capability Type | Dominant in | Coverage |
|----------------|------------|----------|
| PRODUCT | release, research | ✅ |
| TECHNICAL | model, release | ✅ |
| INVESTMENT | funding | ✅ |
| MARKET | acquisition | ✅ |
| PARTNERSHIP | partnership | ✅ |
| PERFORMANCE | benchmark | ✅ |
| GENERAL | regulation, model | ✅ |

**Capability Type Coverage: 7/7 (100%)**

---

## Replay Stability

| Layer | Result |
|-------|--------|
| Extraction (Rule) | 100% deterministic |
| Validation | 100% deterministic |
| Event Projection | 100% deterministic |
| Capability Projection | 100% deterministic |
| Full E2E chain | 100% deterministic |

**Replay Stability: 4/4 layers, all 100%**

---

## Next Steps

- Expand to 300+ cases (target: V2)
- Add `not_supports` cases for full predicate coverage
- Add multi-subject scenarios per category
- Integrate with CI pipeline (script: `scripts/ci_validate.py`)
