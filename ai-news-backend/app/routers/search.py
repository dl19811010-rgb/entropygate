from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import success_response, paginated_response
from app.models.article import Article

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("")
async def search(
    q: str = Query(""),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    from sqlalchemy import or_

    query = db.query(Article).filter(Article.review_status == "approved")
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(Article.title.ilike(like), Article.summary.ilike(like), Article.content.ilike(like))
        )

    total = query.count()
    items = query.order_by(Article.editorial_score.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return paginated_response(
        items=[a.to_dict() for a in items],
        total=total,
        page=page,
        page_size=page_size,
    )
