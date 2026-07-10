from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import success_response

router = APIRouter(prefix="/intelligence", tags=["Intelligence"])


@router.get("/reports")
async def list_reports(db: Session = Depends(get_db)):
    from app.models.intelligence import IntelligenceReport
    items = db.query(IntelligenceReport).order_by(IntelligenceReport.created_at.desc()).limit(20).all()
    return success_response([r.to_dict() for r in items])


@router.get("/daily-brief")
async def daily_brief(db: Session = Depends(get_db)):
    from app.services.intelligence_service import IntelligenceService
    svc = IntelligenceService(db)
    reports, _ = svc.list_reports(page=1, page_size=1)
    return success_response(reports)
