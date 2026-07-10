from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import success_response

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    from app.models.article import Article
    from app.models.source import Source
    from app.models.category import Category

    total_articles = db.query(Article).count()
    approved = db.query(Article).filter(Article.review_status == "approved").count()
    pending = db.query(Article).filter(Article.review_status == "pending").count()
    total_sources = db.query(Source).count()
    active_sources = db.query(Source).filter(Source.is_active == 1).count()

    return success_response({
        "total_articles": total_articles,
        "approved": approved,
        "pending": pending,
        "total_sources": total_sources,
        "active_sources": active_sources,
    })


@router.get("/editorial-distribution")
async def editorial_distribution(db: Session = Depends(get_db)):
    from app.models.article import Article
    from sqlalchemy import func

    rows = db.query(Article.editorial_bucket, func.count(Article.id)).group_by(Article.editorial_bucket).all()
    return success_response({row[0] or "unknown": row[1] for row in rows})
