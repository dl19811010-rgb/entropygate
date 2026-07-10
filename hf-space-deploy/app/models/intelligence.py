from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from app.core.database import Base


class IntelligenceReport(Base):
    __tablename__ = "intelligence_reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    type = Column(String(50), default="daily_brief")  # daily_brief, trend_report, entity_analysis, strategic_alert
    summary = Column(Text, default="")
    content = Column(Text, default="")
    entities = Column(Text, default="")
    tags = Column(Text, default="")
    relevance_score = Column(Float, default=0.0)
    confidence = Column(Float, default=0.0)
    status = Column(String(20), default="draft")
    generated_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "summary": self.summary,
            "content": self.content,
            "entities": self.entities.split(",") if self.entities else [],
            "tags": self.tags.split(",") if self.tags else [],
            "relevance_score": self.relevance_score,
            "confidence": self.confidence,
            "status": self.status,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
