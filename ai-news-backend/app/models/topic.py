"""Topic model — editorial topic taxonomy for the Observation System."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from app.core.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(120), unique=True, nullable=False, index=True)
    description = Column(Text, default="")

    # ── Editorial metadata
    priority_level = Column(String(20), default="normal")  # critical, high, normal, low
    min_daily_articles = Column(Integer, default=0)  # minimum articles per day to maintain coverage

    # ── Visual / dashboard
    icon = Column(String(50), default="")
    color = Column(String(20), default="")
    sort_order = Column(Integer, default=0)

    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "priority_level": self.priority_level,
            "min_daily_articles": self.min_daily_articles,
            "icon": self.icon,
            "color": self.color,
            "sort_order": self.sort_order,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }