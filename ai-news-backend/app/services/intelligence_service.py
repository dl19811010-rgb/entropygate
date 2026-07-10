"""Intelligence Service - stub."""
from sqlalchemy.orm import Session
from app.models.intelligence import IntelligenceReport


class IntelligenceService:
    def __init__(self, db: Session):
        self.db = db

    def generate_daily_brief(self):
        pass

    def list_reports(self, page=1, page_size=20):
        q = self.db.query(IntelligenceReport)
        total = q.count()
        items = q.order_by(IntelligenceReport.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
        return [r.to_dict() for r in items], total
