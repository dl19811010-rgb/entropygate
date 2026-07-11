"""Editorial Policy — quota rules, freshness definitions, and topic taxonomy.

This is the single source of truth for editorial strategy configuration.
The scheduler, coverage reporter, and dashboard all read from here.
"""
from typing import Dict, List, Any


# ── Layer 2: Topic Taxonomy ────────────────────────────────────
TOPIC_TAXONOMY: List[Dict[str, Any]] = [
    {"slug": "reasoning", "name": "Reasoning", "priority": "high", "min_daily": 1, "color": "#6366f1"},
    {"slug": "agent", "name": "Agent", "priority": "high", "min_daily": 1, "color": "#8b5cf6"},
    {"slug": "mcp", "name": "MCP", "priority": "normal", "min_daily": 0, "color": "#a855f7"},
    {"slug": "video-generation", "name": "Video Generation", "priority": "normal", "min_daily": 0, "color": "#ec4899"},
    {"slug": "robotics", "name": "Robotics", "priority": "normal", "min_daily": 0, "color": "#f43f5e"},
    {"slug": "coding", "name": "Coding", "priority": "high", "min_daily": 1, "color": "#ef4444"},
    {"slug": "multimodal", "name": "Multimodal", "priority": "normal", "min_daily": 0, "color": "#f97316"},
    {"slug": "ai-infra", "name": "AI Infra", "priority": "normal", "min_daily": 0, "color": "#eab308"},
    {"slug": "benchmark", "name": "Benchmark", "priority": "low", "min_daily": 0, "color": "#84cc16"},
    {"slug": "open-source", "name": "Open Source", "priority": "normal", "min_daily": 0, "color": "#22c55e"},
    {"slug": "safety", "name": "Safety", "priority": "high", "min_daily": 0, "color": "#14b8a6"},
    {"slug": "policy", "name": "Policy", "priority": "normal", "min_daily": 0, "color": "#06b6d4"},
    {"slug": "funding", "name": "Funding", "priority": "normal", "min_daily": 0, "color": "#0ea5e9"},
    {"slug": "model-release", "name": "Model Release", "priority": "critical", "min_daily": 0, "color": "#3b82f6"},
    {"slug": "api", "name": "API", "priority": "normal", "min_daily": 0, "color": "#64748b"},
]


# ── Layer 6: Editorial Quota ───────────────────────────────────
# Daily distribution targets for homepage / feed composition.
# Expressed as percentage ranges of total daily articles.
EDITORIAL_QUOTA: Dict[str, Dict[str, Any]] = {
    "source_type": {
        "official":      {"min_pct": 40, "max_pct": 60, "label": "Official sources"},
        "research":      {"min_pct": 10, "max_pct": 20, "label": "Research papers"},
        "community":     {"min_pct": 5,  "max_pct": 15, "label": "Community discussion"},
        "media":         {"min_pct": 10, "max_pct": 25, "label": "Media coverage"},
        "developer":     {"min_pct": 5,  "max_pct": 15, "label": "Developer updates"},
        "social":        {"min_pct": 0,  "max_pct": 10, "label": "Social signals"},
        "documentation": {"min_pct": 0,  "max_pct": 5,  "label": "Documentation changes"},
    },
    "language": {
        "chinese":  {"min_pct": 30, "max_pct": 50, "label": "Chinese content"},
        "english":  {"min_pct": 30, "max_pct": 60, "label": "English content"},
        "other":    {"min_pct": 0,  "max_pct": 10, "label": "Other languages"},
    },
    "topic": {
        "model-release": {"min_daily": 1, "label": "At least 1 model release story"},
        "agent":         {"min_daily": 1, "label": "At least 1 agent story"},
        "reasoning":     {"min_daily": 1, "label": "At least 1 reasoning story"},
        "coding":        {"min_daily": 1, "label": "At least 1 coding story"},
    },
    "freshness": {
        "hot":    {"min_pct": 20, "max_hours": 2,   "label": "Hot (< 2h)"},
        "warm":   {"min_pct": 50, "max_hours": 24,  "label": "Warm (< 24h)"},
        "fresh":  {"min_pct": 20, "max_hours": 72,  "label": "Fresh (< 3 days)"},
        "archive":{"min_pct": 0,  "max_hours": 168, "label": "Archive (< 7 days)"},
    },
}


# ── Layer 7: Freshness Bands ───────────────────────────────────
FRESHNESS_BANDS = [
    {"slug": "hot",     "label": "Hot",     "max_hours": 2,   "color": "#ef4444"},
    {"slug": "warm",    "label": "Warm",    "max_hours": 24,  "color": "#f97316"},
    {"slug": "fresh",   "label": "Fresh",   "max_hours": 72,  "color": "#22c55e"},
    {"slug": "archive", "label": "Archive", "max_hours": 168, "color": "#64748b"},
    {"slug": "stale",   "label": "Stale",   "max_hours": None, "color": "#94a3b8"},
]


def compute_freshness(published_at, now=None) -> Dict[str, Any]:
    """Compute freshness band for an article based on published_at."""
    from datetime import datetime, timedelta
    if now is None:
        now = datetime.utcnow()
    if not published_at:
        return {"band": "stale", "hours_old": None, "label": "Stale", "color": "#94a3b8"}

    if isinstance(published_at, str):
        try:
            published_at = datetime.fromisoformat(published_at.replace("Z", ""))
        except Exception:
            return {"band": "stale", "hours_old": None, "label": "Stale", "color": "#94a3b8"}

    delta = now - published_at
    hours_old = delta.total_seconds() / 3600

    for band in FRESHNESS_BANDS:
        if band["max_hours"] is None or hours_old <= band["max_hours"]:
            return {
                "band": band["slug"],
                "hours_old": round(hours_old, 1),
                "label": band["label"],
                "color": band["color"],
            }

    return {"band": "stale", "hours_old": round(hours_old, 1), "label": "Stale", "color": "#94a3b8"}


# ── Layer 4: Priority Scheduling ───────────────────────────────
PRIORITY_SCHEDULE = {
    "critical": {"interval_minutes": 5,   "label": "Critical", "description": "Near real-time monitoring"},
    "high":     {"interval_minutes": 15,  "label": "High",     "description": "Frequent checks"},
    "normal":   {"interval_minutes": 30,  "label": "Normal",   "description": "Standard cadence"},
    "low":      {"interval_minutes": 120, "label": "Low",      "description": "Background monitoring"},
}


def get_effective_priority(source, calendar_events=None) -> str:
    """Get effective priority for a source, considering active calendar events."""
    base_priority = getattr(source, "priority", "normal") or "normal"

    if calendar_events:
        for event in calendar_events:
            boost_sources = []
            if hasattr(event, "boost_sources") and event.boost_sources:
                boost_sources = [s.strip() for s in event.boost_sources.split(",")]

            if not boost_sources or source.slug in boost_sources:
                return event.boost_priority

    return base_priority


def get_effective_interval(source, calendar_events=None) -> int:
    """Get effective crawl interval based on priority and calendar events."""
    priority = get_effective_priority(source, calendar_events)
    return PRIORITY_SCHEDULE.get(priority, PRIORITY_SCHEDULE["normal"])["interval_minutes"]