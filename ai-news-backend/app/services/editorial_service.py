"""Editorial Scoring System (ESS) v1-v4
===========================================
ESS v1 – Source tier → base score
ESS v2 – Content quality signals
ESS v3 – Entity relevance & strategic event detection
ESS v4 – Narrative story generation & trend ontology
"""

import logging
import math
from datetime import datetime, timedelta
from typing import Any, Optional

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# EDITORIAL TIERS, BUCKETS, ROLES
# ═══════════════════════════════════════════════════════════════

EDITORIAL_TIERS = {
    "s_tier": {"label": "Essential", "score_range": (85, 100), "bucket": "essential", "role": "foundational / must-cover"},
    "a_tier": {"label": "Authoritative", "score_range": (70, 84), "bucket": "authoritative", "role": "primary reporting"},
    "b_tier": {"label": "Credible", "score_range": (55, 69), "bucket": "credible", "role": "context & amplification"},
    "c_tier": {"label": "Signal", "score_range": (40, 54), "bucket": "signal", "role": "early-warning / niche"},
    "d_tier": {"label": "Peripheral", "score_range": (0, 39), "bucket": "peripheral", "role": "low-priority"},
}

EDITORIAL_BUCKETS = ["essential", "authoritative", "credible", "signal", "peripheral"]

EDITORIAL_ROLES = [
    "foundational / must-cover",
    "primary reporting",
    "content & amplification",
    "early-warning / niche",
    "low-priority",
]

# ═══════════════════════════════════════════════════════════════
# ENTITY KEYWORDS MAP
# ═══════════════════════════════════════════════════════════════

ENTITY_KEYWORDS = {
    "openai": {
        "aliases": ["openai", "chatgpt", "gpt-4", "gpt-5", "o3", "o1", "sam altman", "dall-e", "sora", "codex"],
        "weight": 1.0,
        "category": "ai_lab",
        "strategic": True,
    },
    "google": {
        "aliases": ["google", "alphabet", "deepmind", "gemini", "bard", "palm", "sundar pichai", "waymo", "vertex ai"],
        "weight": 1.0,
        "category": "big_tech",
        "strategic": True,
    },
    "microsoft": {
        "aliases": ["microsoft", "msft", "azure", "copilot", "satya nadella", "bing", "github copilot"],
        "weight": 0.95,
        "category": "big_tech",
        "strategic": True,
    },
    "meta": {
        "aliases": ["meta", "facebook", "llama", "mark zuckerberg", "instagram", "whatsapp", "threads"],
        "weight": 0.9,
        "category": "big_tech",
        "strategic": True,
    },
    "anthropic": {
        "aliases": ["anthropic", "claude", "dario amodei", "constitutional ai"],
        "weight": 0.85,
        "category": "ai_lab",
        "strategic": True,
    },
    "nvidia": {
        "aliases": ["nvidia", "nvda", "jensen huang", "cuda", "h100", "b200", "rtx", "geforce", "dgx"],
        "weight": 0.95,
        "category": "hardware",
        "strategic": True,
    },
    "apple": {
        "aliases": ["apple", "tim cook", "ios", "macos", "iphone", "apple intelligence", "vision pro", "m4"],
        "weight": 0.9,
        "category": "big_tech",
        "strategic": True,
    },
    "amazon": {
        "aliases": ["amazon", "aws", "alexa", "andy jassy", "bedrock", "titan"],
        "weight": 0.85,
        "category": "big_tech",
        "strategic": True,
    },
    "tesla": {
        "aliases": ["tesla", "elon musk", "fsd", "optimus", "dojo", "cybertruck", "gigafactory"],
        "weight": 0.9,
        "category": "automotive_ai",
        "strategic": True,
    },
    "xai": {
        "aliases": ["xai", "grok", "elon musk"],
        "weight": 0.8,
        "category": "ai_lab",
        "strategic": True,
    },
    "eu": {
        "aliases": ["european union", "eu", "european commission", "gdpr", "ai act", "digital services act"],
        "weight": 0.85,
        "category": "regulation",
        "strategic": True,
    },
    "china": {
        "aliases": ["china", "chinese", "beijing", "baidu", "ernie", "alibaba", "tongyi", "bytedance", "doubao"],
        "weight": 0.85,
        "category": "geopolitical",
        "strategic": True,
    },
    "pentagon": {
        "aliases": ["pentagon", "dod", "department of defense", "darpa", "us military", "nato"],
        "weight": 0.85,
        "category": "defence",
        "strategic": True,
    },
    "huggingface": {
        "aliases": ["hugging face", "huggingface", "transformers", "diffusers"],
        "weight": 0.7,
        "category": "opensource",
        "strategic": False,
    },
    "stability": {
        "aliases": ["stability ai", "stable diffusion", "sdxl", "stable diffusion 3"],
        "weight": 0.65,
        "category": "ai_lab",
        "strategic": False,
    },
    "midjourney": {
        "aliases": ["midjourney", "midjourney v6", "david holz"],
        "weight": 0.6,
        "category": "ai_lab",
        "strategic": False,
    },
}

# ═══════════════════════════════════════════════════════════════
# STRATEGIC EVENT TEMPLATES
# ═══════════════════════════════════════════════════════════════

STRATEGIC_EVENT_TEMPLATES = {
    "model_release": {
        "label": "Major Model Release",
        "signal_words": ["launch", "release", "announce", "unveil", "introduce", "shipping", "available"],
        "context_words": ["model", "llm", "language model", "multimodal", "foundation model", "gpt", "claude", "gemini"],
        "severity": 3,
        "narrative_type": "capability_leap",
    },
    "funding_round": {
        "label": "Significant Funding",
        "signal_words": ["raises", "raised", "funding", "series", "valuation", "investment", "round", "billion", "million"],
        "context_words": ["startup", "company", "ai", "venture", "capital"],
        "severity": 2,
        "narrative_type": "capital_flow",
    },
    "regulation": {
        "label": "Regulation / Policy",
        "signal_words": ["regulation", "regulate", "ban", "executive order", "law", "legislation", "compliance", "oversight"],
        "context_words": ["ai", "artificial intelligence", "government", "senate", "congress", "commission"],
        "severity": 3,
        "narrative_type": "governance_shift",
    },
    "acquisition": {
        "label": "Acquisition / M&A",
        "signal_words": ["acquire", "acquisition", "merger", "buy", "takeover", "purchase", "deal"],
        "context_words": ["company", "startup", "ai", "technology", "talent"],
        "severity": 3,
        "narrative_type": "market_consolidation",
    },
    "safety_incident": {
        "label": "AI Safety Incident",
        "signal_words": ["safety", "incident", "accident", "misuse", "hallucination", "bias", "harmful", "dangerous"],
        "context_words": ["ai", "model", "system", "chatbot", "algorithm"],
        "severity": 4,
        "narrative_type": "risk_event",
    },
    "breakthrough": {
        "label": "Research Breakthrough",
        "signal_words": ["breakthrough", "discovered", "novel", "state-of-the-art", "sota", "benchmark", "achieved"],
        "context_words": ["research", "paper", "study", "technique", "architecture", "method"],
        "severity": 2,
        "narrative_type": "knowledge_advance",
    },
    "leadership_change": {
        "label": "Leadership Change",
        "signal_words": ["ceo", "cto", "resign", "step down", "appoint", "hired", "leaves", "departure"],
        "context_words": ["openai", "google", "microsoft", "meta", "anthropic", "nvidia", "company"],
        "severity": 2,
        "narrative_type": "organisational_shift",
    },
    "product_launch": {
        "label": "Product Launch",
        "signal_words": ["launch", "shipping", "available now", "announced", "rolls out", "release"],
        "context_words": ["product", "feature", "platform", "tool", "app", "service"],
        "severity": 2,
        "narrative_type": "market_event",
    },
    "partnership": {
        "label": "Strategic Partnership",
        "signal_words": ["partnership", "partner", "collaboration", "alliance", "joint", "teaming up"],
        "context_words": ["company", "ai", "technology", "research", "development"],
        "severity": 2,
        "narrative_type": "ecosystem_shift",
    },
}

# ═══════════════════════════════════════════════════════════════
# TREND ONTOLOGY
# ═══════════════════════════════════════════════════════════════

TREND_ONTOLOGY = {
    "model_scaling": {
        "label": "Model Scaling",
        "description": "Trends in LLM size, compute, efficiency",
        "signal_keywords": ["parameters", "tokens", "compute", "flops", "training run", "scaling law"],
        "weight": 0.7,
    },
    "opensource_acceleration": {
        "label": "Open-Source Acceleration",
        "description": "Momentum in open-weight/open-source AI",
        "signal_keywords": ["open source", "open weight", "open model", "weights released", "apache", "mit license", "community"],
        "weight": 0.65,
    },
    "regulation_tightening": {
        "label": "Regulation Tightening",
        "description": "Increasing AI governance & compliance pressure",
        "signal_keywords": ["regulation", "compliance", "ai act", "executive order", "ban", "restrict", "oversight"],
        "weight": 0.7,
    },
    "agent_autonomy": {
        "label": "Agent Autonomy",
        "description": "AI agents that plan & execute independently",
        "signal_keywords": ["agent", "autonomous", "agentic", "tool use", "function calling", "planning"],
        "weight": 0.75,
    },
    "multimodal_convergence": {
        "label": "Multimodal Convergence",
        "description": "Unifying text, image, video, audio in one model",
        "signal_keywords": ["multimodal", "vision", "audio", "video", "image generation", "speech"],
        "weight": 0.7,
    },
    "hardware_race": {
        "label": "Hardware Race",
        "description": "GPU/TPU/chip competition for AI compute",
        "signal_keywords": ["gpu", "tpu", "chip", "nvidia", "h100", "b200", "semiconductor", "fab"],
        "weight": 0.7,
    },
    "safety_alignment": {
        "label": "Safety & Alignment",
        "description": "Work on making AI safe and aligned",
        "signal_keywords": ["safety", "alignment", "rlhf", "constitutional ai", "red team", "guardrails"],
        "weight": 0.65,
    },
    "enterprise_adoption": {
        "label": "Enterprise Adoption",
        "description": "AI integration into business workflows",
        "signal_keywords": ["enterprise", "business", "workflow", "copilot", "assistant", "productivity", "deploy"],
        "weight": 0.6,
    },
    "geopolitical_ai_race": {
        "label": "Geopolitical AI Race",
        "description": "US-China-EU AI competition dynamics",
        "signal_keywords": ["china", "us", "europe", "chip ban", "export control", "sanction", "sovereign ai"],
        "weight": 0.8,
    },
    "ai_economics": {
        "label": "AI Economics",
        "description": "Cost, ROI, and market dynamics",
        "signal_keywords": ["cost", "pricing", "roi", "revenue", "profit", "subscription", "api pricing"],
        "weight": 0.55,
    },
}

# ═══════════════════════════════════════════════════════════════
# INSIGHT UPGRADES — value-add layers beyond raw scoring
# ═══════════════════════════════════════════════════════════════

INSIGHT_UPGRADES = {
    "first_report": {
        "label": "First Report",
        "trigger": "article is the earliest in its entity × topic cluster within 48h",
        "bonus": 10,
    },
    "depth_supplement": {
        "label": "Depth Supplement",
        "trigger": "article adds substantial new data to an already-covered story",
        "bonus": 5,
    },
    "contrarian_view": {
        "label": "Contrarian View",
        "trigger": "article presents a significant dissenting opinion",
        "bonus": 7,
    },
    "exclusive": {
        "label": "Exclusive / Original Reporting",
        "trigger": "article contains investigation or original data",
        "bonus": 12,
    },
    "multisource_corroboration": {
        "label": "Multi-Source Corroboration",
        "trigger": "same fact reported by 3+ independent sources",
        "bonus": 6,
    },
    "expert_authored": {
        "label": "Expert Authored",
        "trigger": "author is a recognised domain expert",
        "bonus": 8,
    },
}

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════


def _score_to_bucket(score: float) -> str:
    """Map a numeric editorial score to its bucket label."""
    if score >= 85:
        return "essential"
    elif score >= 70:
        return "authoritative"
    elif score >= 55:
        return "credible"
    elif score >= 40:
        return "signal"
    return "peripheral"


def _score_to_tier(score: float) -> str:
    """Map a numeric editorial score to its tier key."""
    if score >= 85:
        return "s_tier"
    elif score >= 70:
        return "a_tier"
    elif score >= 55:
        return "b_tier"
    elif score >= 40:
        return "c_tier"
    return "d_tier"


def identify_entity(text: str) -> list[dict]:
    """Identify known entities in text using ENTITY_KEYWORDS.

    Returns list of dicts: {entity_key, entity_name, category, weight, matched_alias}
    """
    text_lower = text.lower() if text else ""
    found = []
    for entity_key, data in ENTITY_KEYWORDS.items():
        for alias in data["aliases"]:
            if alias in text_lower:
                found.append({
                    "entity_key": entity_key,
                    "entity_name": alias,
                    "category": data["category"],
                    "weight": data["weight"],
                    "strategic": data["strategic"],
                })
                break  # one match per entity
    # Sort by weight descending
    found.sort(key=lambda e: e["weight"], reverse=True)
    return found


def detect_strategic_event(title: str, content: str) -> Optional[dict]:
    """Detect if an article matches a strategic event template.

    Returns dict with event_type, label, severity, confidence, or None.
    """
    text = f"{title} {content}" if title and content else (title or content)
    if not text:
        return None
    text_lower = text.lower()

    best_match = None
    best_score = 0

    for event_key, template in STRATEGIC_EVENT_TEMPLATES.items():
        signal_hits = sum(1 for w in template["signal_words"] if w in text_lower)
        context_hits = sum(1 for w in template["context_words"] if w in text_lower)
        if signal_hits >= 1 and context_hits >= 1:
            score = signal_hits + context_hits + (template["severity"] * 0.5)
            if score > best_score:
                best_score = score
                confidence = min(1.0, signal_hits / max(1, len(template["signal_words"])) * 0.7 + 0.3)
                best_match = {
                    "event_type": event_key,
                    "label": template["label"],
                    "severity": template["severity"],
                    "confidence": round(confidence, 2),
                    "narrative_type": template["narrative_type"],
                }

    return best_match


def build_strategic_events(articles: list) -> list[dict]:
    """Build strategic event clusters from a list of articles."""
    events = {}
    for article in articles:
        title = getattr(article, "title", "") or article.get("title", "") if isinstance(article, dict) else ""
        content = getattr(article, "content", "") or article.get("content", "") if isinstance(article, dict) else ""
        event = detect_strategic_event(title, content)
        if event:
            key = event["event_type"]
            if key not in events:
                events[key] = {
                    "event_type": key,
                    "label": event["label"],
                    "severity": event["severity"],
                    "count": 0,
                    "articles": [],
                    "max_confidence": 0,
                }
            events[key]["count"] += 1
            events[key]["max_confidence"] = max(events[key]["max_confidence"], event["confidence"])
            aid = getattr(article, "id", None) or article.get("id") if isinstance(article, dict) else None
            events[key]["articles"].append(aid)

    return sorted(events.values(), key=lambda e: (e["severity"], e["count"]), reverse=True)


# ═══════════════════════════════════════════════════════════════
# STORY / NARRATIVE GENERATION (ESS v4)
# ═══════════════════════════════════════════════════════════════


def generate_entity_story(entity_key: str, articles: list) -> dict:
    """Generate a narrative story for an entity from recent articles.

    Args:
        entity_key: e.g. 'openai', 'google'
        articles: list of Article dicts or objects

    Returns:
        dict with narrative summary, key developments, trend direction
    """
    data = ENTITY_KEYWORDS.get(entity_key, {})
    articles_texts = []
    for a in articles:
        if isinstance(a, dict):
            articles_texts.append(f"{a.get('title', '')} {a.get('summary', '')}")
        else:
            articles_texts.append(f"{getattr(a, 'title', '')} {getattr(a, 'summary', '')}")

    combined = " ".join(articles_texts)

    # Extract themes
    themes = []
    for trend_key, trend in TREND_ONTOLOGY.items():
        hits = sum(1 for kw in trend["signal_keywords"] if kw in combined.lower())
        if hits > 0:
            themes.append({"key": trend_key, "label": trend["label"], "relevance": min(1.0, hits * 0.3)})
    themes.sort(key=lambda t: t["relevance"], reverse=True)

    return {
        "entity_key": entity_key,
        "entity_name": data.get("aliases", [entity_key])[0] if data else entity_key,
        "category": data.get("category", "unknown"),
        "article_count": len(articles),
        "themes": themes[:5],
        "summary": f"{len(articles)} articles covering {entity_key} in the last period.",
        "trend_direction": "rising" if len(articles) >= 3 else "stable",
    }


def build_todays_narrative(articles: list, db=None) -> dict:
    """Build the daily narrative: entity stories + strategic events + trends.

    Returns a structured narrative dict.
    """
    # Group articles by entity
    entity_groups: dict[str, list] = {}
    for article in articles:
        if isinstance(article, dict):
            title = article.get("title", "")
            content = article.get("content", "")
        else:
            title = getattr(article, "title", "")
            content = getattr(article, "content", "")

        entities = identify_entity(f"{title} {content}")
        if not entities:
            # no entity matched, put in general
            entity_groups.setdefault("_general", []).append(article)
            continue
        for ent in entities:
            entity_groups.setdefault(ent["entity_key"], []).append(article)

    # Generate entity stories
    entity_stories = []
    for ekey, earticles in entity_groups.items():
        if ekey == "_general":
            continue
        story = generate_entity_story(ekey, earticles)
        entity_stories.append(story)

    entity_stories.sort(key=lambda s: s.get("article_count", 0), reverse=True)

    # Strategic events
    strategic_events = build_strategic_events(articles)

    # Trends
    active_trends = _detect_active_trends(articles)

    return {
        "date": datetime.utcnow().isoformat(),
        "total_articles": len(articles),
        "entity_count": len(entity_stories),
        "entities": entity_stories,
        "strategic_events": strategic_events,
        "active_trends": active_trends,
    }


def _detect_active_trends(articles: list) -> list[dict]:
    """Detect which trends in TREND_ONTOLOGY are active."""
    combined_text = ""
    for a in articles:
        if isinstance(a, dict):
            combined_text += f" {a.get('title', '')} {a.get('summary', '')}"
        else:
            combined_text += f" {getattr(a, 'title', '')} {getattr(a, 'summary', '')}"

    active = []
    for tkey, tdata in TREND_ONTOLOGY.items():
        hits = sum(1 for kw in tdata["signal_keywords"] if kw in combined_text.lower())
        if hits > 0:
            active.append({
                "key": tkey,
                "label": tdata["label"],
                "signals": min(hits, 10),
                "intensity": round(min(1.0, hits * 0.15), 2),
            })
    active.sort(key=lambda t: t["intensity"], reverse=True)
    return active[:8]


# ═══════════════════════════════════════════════════════════════
# EDITORIAL SERVICE
# ═══════════════════════════════════════════════════════════════


class EditorialService:
    """Orchestrates ESS v1-v4 scoring pipeline."""

    # Source tier base scores (v1)
    SOURCE_TIER_BASE = {
        "s_tier": 90,
        "a_tier": 75,
        "b_tier": 58,
        "c_tier": 42,
        "d_tier": 25,
    }

    # Weights for each signal dimension (v2)
    WEIGHTS = {
        "source_reputation": 0.30,
        "content_quality": 0.25,
        "entity_relevance": 0.20,
        "timeliness": 0.10,
        "diversity": 0.05,
        "strategic_signal": 0.10,
    }

    def compute_editorial_score(self, article: Any) -> dict:
        """Master pipeline: compute the final editorial score for one article.

        Args:
            article: An Article ORM object or dict with keys:
                - source: Source ORM object or dict with editorial_tier, editorial_score
                - title, content, summary
                - published_at
                - newsworthiness_score

        Returns:
            dict with keys: score, bucket, tier, newsworthiness, components
        """
        # ---- v1: Source tier base score ----
        source = None
        if hasattr(article, "source"):
            source = article.source
        elif isinstance(article, dict):
            source = article.get("source")

        source_tier = None
        source_score = None
        if source:
            if hasattr(source, "editorial_tier"):
                source_tier = source.editorial_tier
                source_score = source.editorial_score
            elif isinstance(source, dict):
                source_tier = source.get("editorial_tier")
                source_score = source.get("editorial_score")

        v1_base = self.SOURCE_TIER_BASE.get(source_tier, 42) if source_tier else 42

        # ---- v2: Content quality ----
        title = getattr(article, "title", "") or article.get("title", "")
        content = getattr(article, "content", "") or article.get("content", "")
        summary = getattr(article, "summary", "") or article.get("summary", "")

        content_len_score = _clamp(0, 100, min(len(content) / 5, 100) if content else 30)
        title_len_score = _clamp(0, 100, 80 if 5 <= len(title.split()) <= 20 else 50)
        has_summary_score = 80 if summary and len(summary) > 20 else 30

        content_quality = (content_len_score * 0.4 + title_len_score * 0.3 + has_summary_score * 0.3)

        # ---- v3: Entity relevance ----
        full_text = f"{title} {content} {summary}"
        entities = identify_entity(full_text)
        entity_weight_sum = sum(e["weight"] for e in entities)
        strategic_count = sum(1 for e in entities if e["strategic"])
        entity_score = _clamp(0, 100, entity_weight_sum * 60 + strategic_count * 15)

        # Strategic event detection
        event = detect_strategic_event(title, content)
        event_bonus = event["severity"] * 8 if event else 0

        # ---- Timeliness ----
        published_at = None
        if hasattr(article, "published_at"):
            published_at = article.published_at
        elif isinstance(article, dict):
            published_at = article.get("published_at")

        timeliness_score = 50
        if published_at:
            if isinstance(published_at, str):
                try:
                    published_at = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
                except (ValueError, TypeError):
                    published_at = None
            if published_at and isinstance(published_at, datetime):
                age_hours = (datetime.utcnow() - published_at.replace(tzinfo=None)).total_seconds() / 3600
                if age_hours < 1:
                    timeliness_score = 100
                elif age_hours < 4:
                    timeliness_score = 90
                elif age_hours < 12:
                    timeliness_score = 75
                elif age_hours < 24:
                    timeliness_score = 60
                elif age_hours < 48:
                    timeliness_score = 40
                elif age_hours < 168:
                    timeliness_score = 20
                else:
                    timeliness_score = 10

        # ---- Newsworthiness ----
        nw_score = getattr(article, "newsworthiness_score", None)
        if nw_score is None and isinstance(article, dict):
            nw_score = article.get("newsworthiness_score", 50)
        if nw_score is None:
            nw_score = 50

        # ---- Combine (weighted) ----
        raw_score = (
            self.WEIGHTS["source_reputation"] * v1_base
            + self.WEIGHTS["content_quality"] * content_quality
            + self.WEIGHTS["entity_relevance"] * entity_score
            + self.WEIGHTS["timeliness"] * timeliness_score
            + self.WEIGHTS["diversity"] * 50
            + self.WEIGHTS["strategic_signal"] * (event_bonus)
        )

        final_score = round(_clamp(0, 100, raw_score), 1)

        return {
            "score": final_score,
            "bucket": _score_to_bucket(final_score),
            "tier": _score_to_tier(final_score),
            "newsworthiness": nw_score,
            "components": {
                "source_base": round(v1_base, 1),
                "content_quality": round(content_quality, 1),
                "entity_relevance": round(entity_score, 1),
                "timeliness": round(timeliness_score, 1),
                "strategic_event": round(event_bonus, 1),
                "entities": [e["entity_key"] for e in entities[:5]],
                "event": event,
            },
        }


def _clamp(lo: float, hi: float, val: float) -> float:
    return max(lo, min(hi, val))


editorial_service = EditorialService()
