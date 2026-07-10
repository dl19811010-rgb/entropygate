from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    action = Column(String(50), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=True)
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=True)
    admin_username = Column(String(100), default="")
    details = Column(Text, default="")
    ip_address = Column(String(50), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "action": self.action,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "admin_id": self.admin_id,
            "admin_username": self.admin_username,
            "details": self.details,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class EditorialDecision(Base):
    __tablename__ = "editorial_decisions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False, index=True)
    decision = Column(String(30), nullable=False)  # approved, rejected, needs_revision, escalated
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=True)
    admin_username = Column(String(100), default="")
    reasoning = Column(Text, default="")
    editorial_score_before = Column(Float, nullable=True)
    editorial_score_after = Column(Float, nullable=True)
    editorial_bucket_before = Column(String(30), nullable=True)
    editorial_bucket_after = Column(String(30), nullable=True)
    override_reason = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "article_id": self.article_id,
            "decision": self.decision,
            "admin_id": self.admin_id,
            "admin_username": self.admin_username,
            "reasoning": self.reasoning,
            "editorial_score_before": self.editorial_score_before,
            "editorial_score_after": self.editorial_score_after,
            "editorial_bucket_before": self.editorial_bucket_before,
            "editorial_bucket_after": self.editorial_bucket_after,
            "override_reason": self.override_reason,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
