from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.core.database import Base


class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(220), unique=True, nullable=False, index=True)
    description = Column(Text, default="")
    url = Column(String(500), default="")
    logo_url = Column(String(500), default="")
    category = Column(String(100), default="")
    tags = Column(String(500), default="")
    pricing = Column(String(50), default="free")
    is_featured = Column(Integer, default=0)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "url": self.url,
            "logo_url": self.logo_url,
            "category": self.category,
            "tags": self.tags.split(",") if self.tags else [],
            "pricing": self.pricing,
            "is_featured": self.is_featured,
            "sort_order": self.sort_order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
