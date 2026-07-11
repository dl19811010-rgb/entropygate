"""Editorial Calendar model — event-driven scheduling for major AI events."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from app.core.database import Base


class EditorialCalendar(Base):
    """Tracks major AI events (conferences, product launches) for boosted scheduling."""
    __tablename__ = "editorial_calendar"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False)  # e.g. "OpenAI DevDay", "Google I/O", "NeurIPS 2026"
    slug = Column(String(220), unique=True, nullable=False, index=True)
    description = Column(Text, default="")

    # ── Event timing
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    # ── Boost config: during the event window, boost crawl frequency
    boost_priority = Column(String(20), default="critical")  # priority to use during event
    boost_sources = Column(Text, default="")  # comma-separated source slugs to boost; empty = all

    # ── Topics associated with this event
    topics = Column(Text, default="")  # comma-separated topic slugs

    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "boost_priority": self.boost_priority,
            "boost_sources": [s.strip() for s in self.boost_sources.split(",")] if self.boost_sources else [],
            "topics": [t.strip() for t in self.topics.split(",")] if self.topics else [],
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }