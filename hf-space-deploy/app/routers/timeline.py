from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import success_response

router = APIRouter(prefix="/timeline", tags=["Timeline"])


@router.get("")
async def get_timeline(db: Session = Depends(get_db)):
    from app.models.article import Article
    from sqlalchemy import desc

    items = db.query(Article).filter(Article.review_status == "approved").order_by(desc(Article.published_at)).limit(50).all()
    return success_response([a.to_dict() for a in items])
