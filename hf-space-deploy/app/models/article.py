from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.tag import article_tags


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Core content
    title = Column(String(500), nullable=False)
    slug = Column(String(520), index=True)
    summary = Column(Text, default="")
    content = Column(Text, default="")
    excerpt = Column(Text, default="")

    # Source
    url = Column(String(1000), default="")
    source_url = Column(String(1000), default="")
    source_name = Column(String(300), default="")
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)

    # Meta
    author = Column(String(200), default="")
    language = Column(String(10), default="en")
    published_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)

    # Classification
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    tags = relationship("Tag", secondary=article_tags, lazy="selectin")

    # Scoring
    relevance_score = Column(Float, default=0.0)
    quality_score = Column(Float, default=0.0)
    credibility_score = Column(Float, default=0.0)
    newsworthiness_score = Column(Float, default=0.0)

    # Editorial
    editorial_score = Column(Float, default=0.0)
    editorial_bucket = Column(String(30), default="signal")
    editorial_tier = Column(String(20), default="c_tier")

    # Review
    review_status = Column(String(30), default="pending")  # pending, approved, rejected, needs_revision
    review_notes = Column(Text, default="")
    reviewed_by = Column(Integer, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)

    # AI enrichment
    ai_summary = Column(Text, default="")
    ai_tags = Column(Text, default="")
    ai_sentiment = Column(String(20), default="neutral")
    ai_keywords = Column(Text, default="")
    ai_entities = Column(Text, default="")

    # Fact layer
    fact_score = Column(Float, default=0.0)
    fact_count = Column(Integer, default=0)

    # Strategic / ESS
    strategic_event_id = Column(String(100), nullable=True)
    strategic_event_type = Column(String(50), nullable=True)
    narrative_thread = Column(String(200), nullable=True)

    # Image
    image_url = Column(String(1000), default="")
    thumbnail_url = Column(String(1000), default="")

    # Flags
    is_featured = Column(Integer, default=0)
    is_trending = Column(Integer, default=0)
    is_breaking = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    source = relationship("Source", lazy="selectin")
    category = relationship("Category", lazy="selectin")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "summary": self.summary,
            "content": self.content,
            "excerpt": self.excerpt,
            "url": self.url,
            "source_url": self.source_url,
            "source_name": self.source_name,
            "source_id": self.source_id,
            "author": self.author,
            "language": self.language,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "fetched_at": self.fetched_at.isoformat() if self.fetched_at else None,
            "category_id": self.category_id,
            "category": self.category.to_dict() if self.category else None,
            "tags": [t.to_dict() for t in self.tags] if self.tags else [],
            "relevance_score": self.relevance_score,
            "quality_score": self.quality_score,
            "credibility_score": self.credibility_score,
            "newsworthiness_score": self.newsworthiness_score,
            "editorial_score": self.editorial_score,
            "editorial_bucket": self.editorial_bucket,
            "editorial_tier": self.editorial_tier,
            "review_status": self.review_status,
            "review_notes": self.review_notes,
            "reviewed_by": self.reviewed_by,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "ai_summary": self.ai_summary,
            "ai_tags": self.ai_tags.split(",") if self.ai_tags else [],
            "ai_sentiment": self.ai_sentiment,
            "ai_keywords": self.ai_keywords.split(",") if self.ai_keywords else [],
            "ai_entities": self.ai_entities.split(",") if self.ai_entities else [],
            "fact_score": self.fact_score,
            "fact_count": self.fact_count,
            "strategic_event_id": self.strategic_event_id,
            "strategic_event_type": self.strategic_event_type,
            "narrative_thread": self.narrative_thread,
            "image_url": self.image_url,
            "thumbnail_url": self.thumbnail_url,
            "is_featured": self.is_featured,
            "is_trending": self.is_trending,
            "is_breaking": self.is_breaking,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
