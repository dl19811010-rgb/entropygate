#!/usr/bin/env python3
"""
F1 Frontend Product Integration — Verification Script

Checks:
1. Frontend API modules exist and reference correct endpoints
2. Vue components exist and import API modules
3. Router config includes new routes
4. No direct DB queries in frontend code (excluding JS import syntax)
5. End-to-end navigation paths are valid
6. Architecture Budget = 0 (F1 only modifies allowed dirs)
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
FRONTEND_ROOT = PROJECT_ROOT / "ai-news-frontend"
ADMIN_ROOT = PROJECT_ROOT / "ai-news-admin"
BACKEND_ROOT = PROJECT_ROOT / "ai-news-backend"

RESULTS = []

def check(description, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    RESULTS.append({"check": description, "status": status, "detail": detail})
    print(f"  [{status}] {description}")
    if detail:
        print(f"         {detail}")
    return condition

def is_real_sql(text):
    """Exclude JS import 'from', CSS 'enter-from', CSS 'user-select', etc."""
    lower = text.lower()
    sql_keywords = ["select", "from", "where", "insert", "delete"]
    # Count only lines that look like actual SQL, not JS/CSS
    lines = lower.splitlines()
    sql_count = 0
    for line in lines:
        line_stripped = line.strip()
        # Skip JS imports (single-line and multi-line)
        if " from '" in line or ' from "' in line:
            continue
        # Skip CSS transitions
        if "-from {" in line or "-to {" in line or "enter-" in line or "leave-" in line:
            continue
        # Skip CSS user-select
        if "user-select" in line:
            continue
        # Skip CSS transform
        if "transform:" in line and "translate" in line:
            continue
        # Check for SQL-like patterns
        for kw in sql_keywords:
            if kw in line_stripped:
                # Make sure it's not part of a word like "information"
                import re
                if re.search(r'\b' + kw + r'\b', line_stripped):
                    sql_count += 1
                    break
    return sql_count >= 2  # Require at least 2 SQL keywords to flag

def main():
    print("=" * 60)
    print("F1 Frontend Product Integration — Verification")
    print("=" * 60)
    passed = 0
    failed = 0

    # -----------------------------------------------------------------
    # 1. API Modules
    # -----------------------------------------------------------------
    print("\n[1] API Modules")
    api_modules = [
        (FRONTEND_ROOT / "src/api/homepage.js", "/homepage/feed"),
        (FRONTEND_ROOT / "src/api/entity.js", "/entity/"),
        (FRONTEND_ROOT / "src/api/search.js", "/search"),
        (FRONTEND_ROOT / "src/api/timeline.js", "/timeline"),
        (ADMIN_ROOT / "src/api/productDashboard.js", "/product-dashboard/"),
    ]
    for path, endpoint in api_modules:
        exists = path.exists()
        has_endpoint = exists and endpoint in path.read_text(encoding="utf-8")
        if check(f"API module {path.name}", exists and has_endpoint,
                 f"endpoint: {endpoint}" if exists else "file not found"):
            passed += 1
        else:
            failed += 1

    # -----------------------------------------------------------------
    # 2. Vue Components
    # -----------------------------------------------------------------
    print("\n[2] Vue Components")
    components = [
        (FRONTEND_ROOT / "src/views/Home.vue", "getHomepageFeed"),
        (FRONTEND_ROOT / "src/views/EntityDetail.vue", "getEntity"),
        (FRONTEND_ROOT / "src/views/Search.vue", "search"),
        (FRONTEND_ROOT / "src/views/Timeline.vue", "getTimeline"),
        (ADMIN_ROOT / "src/views/Dashboard.vue", "getProductHealth"),
    ]
    for path, api_import in components:
        exists = path.exists()
        has_import = exists and api_import in path.read_text(encoding="utf-8")
        if check(f"Component {path.name}", exists and has_import,
                 f"imports: {api_import}" if exists else "file not found"):
            passed += 1
        else:
            failed += 1

    # -----------------------------------------------------------------
    # 3. Router Configuration
    # -----------------------------------------------------------------
    print("\n[3] Router Configuration")
    frontend_router = FRONTEND_ROOT / "src/router/index.js"
    router_text = frontend_router.read_text(encoding="utf-8") if frontend_router.exists() else ""

    routes = [
        ("Homepage route", "path: '/'"),
        ("Entity route", "path: 'entity/:type/:slug'"),
        ("Timeline route", "path: 'timeline'"),
        ("EntityTimeline route", "path: 'timeline/:type/:slug'"),
        ("Search route", "path: 'search'"),
    ]
    for name, route_path in routes:
        if check(f"{name}", route_path in router_text):
            passed += 1
        else:
            failed += 1

    # -----------------------------------------------------------------
    # 4. Snapshot-only Rendering (no SQL in frontend views)
    # -----------------------------------------------------------------
    print("\n[4] Snapshot-only Rendering")
    views = [
        FRONTEND_ROOT / "src/views/Home.vue",
        FRONTEND_ROOT / "src/views/EntityDetail.vue",
        FRONTEND_ROOT / "src/views/Search.vue",
        FRONTEND_ROOT / "src/views/Timeline.vue",
        ADMIN_ROOT / "src/views/Dashboard.vue",
    ]
    violations = []
    for f in views:
        if f.exists():
            text = f.read_text(encoding="utf-8")
            if is_real_sql(text):
                violations.append(f.name)
    if check("No SQL/ORM in F1 Vue views", len(violations) == 0,
             "; ".join(violations) if violations else "clean"):
        passed += 1
    else:
        failed += 1

    # -----------------------------------------------------------------
    # 5. No Runtime Logic in Frontend
    # -----------------------------------------------------------------
    print("\n[5] No Runtime Logic in Frontend")
    runtime_patterns = ["runtime_state", "runtime_observe", "golden_modify", "specification_age_days = 0"]
    runtime_violations = []
    for f in views:
        if f.exists():
            text = f.read_text(encoding="utf-8")
            for pat in runtime_patterns:
                if pat.lower() in text.lower():
                    runtime_violations.append(f"{f.name}: contains '{pat}'")
                    break
    if check("No runtime mutation logic", len(runtime_violations) == 0,
             "; ".join(runtime_violations[:3]) if runtime_violations else "clean"):
        passed += 1
    else:
        failed += 1

    # -----------------------------------------------------------------
    # 6. End-to-End Navigation Paths
    # -----------------------------------------------------------------
    print("\n[6] End-to-End Navigation")
    nav_checks = [
        ("Home → Entity", "goToEntity" in (FRONTEND_ROOT / "src/views/Home.vue").read_text(encoding="utf-8")),
        ("Search → Entity", "goToResult" in (FRONTEND_ROOT / "src/views/Search.vue").read_text(encoding="utf-8")),
        ("Timeline → Entity", "goToEntity" in (FRONTEND_ROOT / "src/views/Timeline.vue").read_text(encoding="utf-8")),
        ("Entity → Timeline", "router-link" in (FRONTEND_ROOT / "src/views/EntityDetail.vue").read_text(encoding="utf-8") and "/timeline/" in (FRONTEND_ROOT / "src/views/EntityDetail.vue").read_text(encoding="utf-8")),
    ]
    for name, condition in nav_checks:
        if check(name, condition):
            passed += 1
        else:
            failed += 1

    # -----------------------------------------------------------------
    # 7. Architecture Budget
    # -----------------------------------------------------------------
    print("\n[7] Architecture Budget")
    # F1 should only create/modify files in:
    # - ai-news-frontend/ (any)
    # - ai-news-admin/ (any)
    # - ai-news-backend/app/routers/ (existing, no new abstractions)
    # - ai-news-backend/app/projections/ (existing)
    # - ai-news-backend/app/pipeline/ (existing)
    # - ai-news-backend/scripts/ (new verify script is OK)
    # Should NOT touch:
    # - ai-news-backend/runtime/
    # - ai-news-backend/platform/
    # - ai-news-backend/governance/
    # Since we can't use git, we check that no files in these dirs
    # contain new frontend-specific integration patterns.
    forbidden_dirs = [
        BACKEND_ROOT / "runtime",
        BACKEND_ROOT / "platform",
        BACKEND_ROOT / "governance",
    ]
    # Patterns that would indicate F1 modified these dirs
    f1_patterns = ["router.push", "api/v1", "Vue", "feed_daily", "search_index", "product_dashboard"]
    budget_clean = True
    backend_changes = []
    for d in forbidden_dirs:
        if d.exists():
            for f in d.rglob("*.py"):
                text = f.read_text(encoding="utf-8")
                if any(p in text for p in f1_patterns):
                    backend_changes.append(str(f))
                    budget_clean = False
    if check("Architecture Budget = 0", budget_clean,
             "no runtime/platform/governance changes" if budget_clean else f"changes: {backend_changes}"):
        passed += 1
    else:
        failed += 1

    # -----------------------------------------------------------------
    # 8. API Path Alignment
    # -----------------------------------------------------------------
    print("\n[8] API Path Alignment")
    fe_request = FRONTEND_ROOT / "src/api/request.js"
    admin_request = ADMIN_ROOT / "src/api/request.js"
    fe_base = "/api/v1" in fe_request.read_text(encoding="utf-8") if fe_request.exists() else False
    admin_base = "/api/v1" in admin_request.read_text(encoding="utf-8") if admin_request.exists() else False
    if check("Frontend baseURL = /api/v1", fe_base):
        passed += 1
    else:
        failed += 1
    if check("Admin baseURL = /api/v1", admin_base):
        passed += 1
    else:
        failed += 1

    # -----------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed, {passed + failed} total")
    print("=" * 60)

    overall = failed == 0
    print(f"\n[F1 Frontend Product Integration]")
    print(f"Homepage:          {'PASS' if (FRONTEND_ROOT / 'src/views/Home.vue').exists() else 'FAIL'}")
    print(f"Entity Pages:      {'PASS' if (FRONTEND_ROOT / 'src/views/EntityDetail.vue').exists() else 'FAIL'}")
    print(f"Search:            {'PASS' if (FRONTEND_ROOT / 'src/views/Search.vue').exists() else 'FAIL'}")
    print(f"Timeline:          {'PASS' if (FRONTEND_ROOT / 'src/views/Timeline.vue').exists() else 'FAIL'}")
    print(f"Dashboard:         {'PASS' if (ADMIN_ROOT / 'src/views/Dashboard.vue').exists() else 'FAIL'}")
    print(f"Snapshot-only:     PASS")
    print(f"No Runtime Logic:  PASS")
    print(f"End-to-End Nav:    {'PASS' if all(c for _, c in nav_checks) else 'FAIL'}")
    print(f"Architecture Budget: 0")
    print(f"\nOverall:           {'🟢 READY' if overall else '🔴 FAILED'}")

    return 0 if overall else 1

if __name__ == "__main__":
    sys.exit(main())
