"""Homepage Router — public /stories endpoint."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import success_response, paginated_response
from app.models.article import Article
from app.services.editorial_service import editorial_service, build_todays_narrative

router = APIRouter(prefix="/homepage", tags=["Homepage"])


@router.get("/stories")
async def get_stories(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    bucket: str = Query(None),
    category_id: int = Query(None),
    db: Session = Depends(get_db),
):
    """Public endpoint: list approved articles ordered by editorial score."""
    q = db.query(Article).filter(Article.review_status == "approved")

    if bucket:
        q = q.filter(Article.editorial_bucket == bucket)
    if category_id:
        q = q.filter(Article.category_id == category_id)

    total = q.count()
    items = q.order_by(Article.editorial_score.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return paginated_response(
        items=[a.to_dict() for a in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/narrative")
async def get_narrative(db: Session = Depends(get_db)):
    """Public endpoint: today's editorial narrative."""
    articles = db.query(Article).filter(Article.review_status == "approved").order_by(Article.editorial_score.desc()).limit(50).all()
    narrative = build_todays_narrative(articles, db)
    return success_response(narrative)


@router.get("/featured")
async def get_featured(db: Session = Depends(get_db)):
    """Public endpoint: featured / trending articles."""
    articles = db.query(Article).filter(
        Article.review_status == "approved",
        (Article.is_featured == 1) | (Article.is_trending == 1),
    ).order_by(Article.editorial_score.desc()).limit(10).all()

    return success_response([a.to_dict() for a in articles])


@router.get("/breaking")
async def get_breaking(db: Session = Depends(get_db)):
    """Public endpoint: breaking news."""
    articles = db.query(Article).filter(
        Article.review_status == "approved",
        Article.is_breaking == 1,
    ).order_by(Article.published_at.desc()).limit(5).all()

    return success_response([a.to_dict() for a in articles])
