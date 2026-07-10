# M2 Extraction Runtime — Audit Report

**Date:** 2026-07-08
**Status:** PASS

## Fact Creation Paths (Production)

### Path 1: Primary — FactExtractionPipeline
```
Signal
  → SignalParser.parse(signal)
  → RuleExtractor.extract(parsed)  +  LLMExtractor.extract(parsed)
  → ExtractionMerger.merge(rule_facts, llm_facts)
  → FactService.create_fact(...)         ← app/services/fact_service.py:13
  → Fact (FES-0001)
```
Source: `app/services/fact_extraction.py` lines 384-423

### Path 2: Fallback — IntelligencePipeline
```
Signal (no facts extracted by Path 1)
  → FESFactService.create_fact(...)      ← app/services/fact_service.py:13
  → Fact (FES-0001)
```
Source: `app/services/intelligence_service.py` lines 438-445

### Path 3: Versioning — FactService.superseded_fact
```
Confirmed Fact (needs update)
  → FactService.superseded_fact(fact_id, **new_data)
  → Fact(...)                             ← app/services/fact_service.py:77
  → Fact V2 (FES-0001, supersedes V1)
```
Source: `app/services/fact_service.py` lines 72-89

## Verification

| Check | Status |
|-------|--------|
| All Fact() constructor calls go through FactService | ✅ PASS |
| No raw `Fact(signal_id=...)` outside service layer | ✅ PASS |
| No legacy Extractor in production code | ✅ PASS (old FactService removed in M1-0) |
| No bypass of FactExtractionPipeline for primary path | ✅ PASS |
| Only one `FactService` class in codebase | ✅ PASS (`app/services/fact_service.py`) |

## Conclusion

**Extraction Runtime: UNIFIED** — All Fact creation converges to a single `FactService` entry point, which enforces FES-0001 contract compliance.

One fallback path exists (`IntelligencePipeline`) for edge cases where extraction produces zero facts. This is acceptable as it still routes through the same FES-0001 `FactService`.
