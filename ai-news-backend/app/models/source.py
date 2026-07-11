from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean
from app.core.database import Base

# ── Editorial Tiers ──────────────────────────────────────────────
EDITORIAL_TIERS = {
    "s_tier": {
        "label": "Essential",
        "score_range": (85, 100),
        "bucket": "essential",
        "role": "foundational / must-cover",
        "description": "Undisputed sources of record; missing them is an editorial gap",
    },
    "a_tier": {
        "label": "Authoritative",
        "score_range": (70, 84),
        "bucket": "authoritative",
        "role": "primary reporting",
        "description": "Original reporting, high fact-density, trusted brand",
    },
    "b_tier": {
        "label": "Credible",
        "score_range": (55, 69),
        "bucket": "credible",
        "role": "context & amplification",
        "description": "Reputable but often secondary; good for diversity of coverage",
    },
    "c_tier": {
        "label": "Signal",
        "score_range": (40, 54),
        "bucket": "signal",
        "role": "early-warning / niche",
        "description": "Niche blogs, research labs, indie analysts — useful as early signal",
    },
    "d_tier": {
        "label": "Peripheral",
        "score_range": (0, 39),
        "bucket": "peripheral",
        "role": "low-priority monitoring",
        "description": "Low editorial value; rarely surfaced unless scarcity demands it",
    },
}

# ── Source Types ────────────────────────────────────────────────
SOURCE_TYPES = {
    "official": {"label": "Official", "description": "Official company/lab blogs and announcements"},
    "research": {"label": "Research", "description": "Academic papers, preprint servers, research labs"},
    "community": {"label": "Community", "description": "Forums, discussion platforms, community curation"},
    "media": {"label": "Media", "description": "Tech journalism, news outlets, industry press"},
    "social": {"label": "Social", "description": "Social media accounts of key figures and orgs"},
    "developer": {"label": "Developer", "description": "GitHub releases, changelogs, SDK updates"},
    "documentation": {"label": "Documentation", "description": "API docs, product docs, technical references"},
}

# ── Priority Levels ─────────────────────────────────────────────
PRIORITY_LEVELS = {
    "critical": {"label": "Critical", "crawl_interval": 5, "description": "Breaking news, major releases — near real-time"},
    "high": {"label": "High", "crawl_interval": 15, "description": "Important sources, frequent updates"},
    "normal": {"label": "Normal", "crawl_interval": 30, "description": "Standard editorial cadence"},
    "low": {"label": "Low", "crawl_interval": 120, "description": "Background monitoring, low urgency"},
}


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(220), unique=True, nullable=False, index=True)
    url = Column(String(500), nullable=False)
    feed_url = Column(String(500), default="")
    feed_type = Column(String(20), default="rss")  # rss, atom, web

    description = Column(Text, default="")
    language = Column(String(10), default="en")
    country = Column(String(10), default="global")
    category = Column(String(100), default="")
    topic_focus = Column(String(200), default="")

    # ── Editorial tiering (Layer 1: Source Tier)
    editorial_tier = Column(String(20), default="b_tier")
    editorial_role = Column(String(50), default="context & amplification")
    editorial_score = Column(Float, default=60.0)
    editorial_bucket = Column(String(30), default="credible")

    # ── Source Type (Layer 3: Source Type)
    source_type = Column(String(30), default="media")  # official, research, community, media, social, developer, documentation

    # ── Event Priority (Layer 4: Event Priority)
    priority = Column(String(20), default="normal")  # critical, high, normal, low

    # ── Topics (Layer 2: Topic Strategy) — comma-separated topic slugs
    topics = Column(Text, default="")  # e.g. "reasoning,agent,api"

    # Meta
    credibility_score = Column(Float, default=50.0)
    bias_rating = Column(String(20), default="center")
    fact_check_rating = Column(String(20), default="mixed")

    # Crawl control
    is_active = Column(Integer, default=1)
    crawl_interval_minutes = Column(Integer, default=30)
    max_articles_per_fetch = Column(Integer, default=20)
    last_crawled_at = Column(DateTime, nullable=True)
    last_success_at = Column(DateTime, nullable=True)
    crawl_error_count = Column(Integer, default=0)

    # Status
    status = Column(String(20), default="active")  # active, paused, error, archived
    health = Column(String(20), default="healthy")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "url": self.url,
            "feed_url": self.feed_url,
            "feed_type": self.feed_type,
            "description": self.description,
            "language": self.language,
            "country": self.country,
            "category": self.category,
            "topic_focus": self.topic_focus,
            "editorial_tier": self.editorial_tier,
            "editorial_role": self.editorial_role,
            "editorial_score": self.editorial_score,
            "editorial_bucket": self.editorial_bucket,
            "source_type": self.source_type,
            "priority": self.priority,
            "topics": [t.strip() for t in self.topics.split(",")] if self.topics else [],
            "credibility_score": self.credibility_score,
            "bias_rating": self.bias_rating,
            "fact_check_rating": self.fact_check_rating,
            "is_active": self.is_active,
            "crawl_interval_minutes": self.crawl_interval_minutes,
            "max_articles_per_fetch": self.max_articles_per_fetch,
            "last_crawled_at": self.last_crawled_at.isoformat() if self.last_crawled_at else None,
            "last_success_at": self.last_success_at.isoformat() if self.last_success_at else None,
            "crawl_error_count": self.crawl_error_count,
            "status": self.status,
            "health": self.health,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }