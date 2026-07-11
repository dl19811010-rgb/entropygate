"""Homepage Router — public endpoints for the intelligence homepage."""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.response import success_response, paginated_response
from app.models.article import Article
from app.models.source import Source
from app.models.tool import Tool
from app.services.editorial_service import build_todays_narrative

router = APIRouter(prefix="/homepage", tags=["Homepage"])


@router.get("/feed")
async def get_feed(db: Session = Depends(get_db)):
    """Homepage feed — aggregated intelligence from approved articles."""
    articles = db.query(Article).filter(
        Article.review_status == "approved"
    ).order_by(Article.editorial_score.desc()).limit(20).all()

    # Build major_events from articles
    major_events = []
    for a in articles:
        event_type = "research"
        if a.strategic_event_type:
            event_type = a.strategic_event_type
        elif a.is_breaking:
            event_type = "model_release"
        elif "price" in (a.title or "").lower():
            event_type = "price_change"
        elif "funding" in (a.title or "").lower() or "融资" in (a.title or ""):
            event_type = "funding"

        major_events.append({
            "id": a.id,
            "title": a.title,
            "detected_at": a.published_at.isoformat() if a.published_at else a.created_at.isoformat() if a.created_at else None,
            "type": event_type,
            "entity_type": "article",
            "entity_slug": a.slug,
            "score": a.editorial_score or 0,
            "summary": a.summary or a.excerpt or "",
        })

    # Top sources
    top_sources = db.query(Source).filter(
        Source.is_active == 1
    ).order_by(Source.editorial_score.desc()).limit(6).all()

    return success_response({
        "major_events": major_events,
        "headline": major_events[0] if major_events else None,
        "top_sources": [s.to_dict() for s in top_sources],
        "generated_at": datetime.utcnow().isoformat(),
        "total_events": len(major_events),
    })


@router.get("/health")
async def get_health(db: Session = Depends(get_db)):
    """Homepage health — pipeline status."""
    total_articles = db.query(Article).count()
    approved = db.query(Article).filter(Article.review_status == "approved").count()
    pending = db.query(Article).filter(Article.review_status == "pending").count()
    active_sources = db.query(Source).filter(Source.is_active == 1).count()

    return success_response({
        "status": "healthy" if total_articles > 0 else "empty",
        "total_articles": total_articles,
        "approved_articles": approved,
        "pending_articles": pending,
        "active_sources": active_sources,
        "last_updated": datetime.utcnow().isoformat(),
    })


@router.get("/headline")
async def get_headline(db: Session = Depends(get_db)):
    """Homepage headline — top story."""
    article = db.query(Article).filter(
        Article.review_status == "approved",
        Article.is_featured == 1,
    ).order_by(Article.editorial_score.desc()).first()

    if not article:
        article = db.query(Article).filter(
            Article.review_status == "approved"
        ).order_by(Article.editorial_score.desc()).first()

    if not article:
        return success_response(None)

    return success_response({
        "id": article.id,
        "title": article.title,
        "summary": article.summary or article.excerpt or "",
        "detected_at": article.published_at.isoformat() if article.published_at else None,
        "score": article.editorial_score or 0,
        "entity_type": "article",
        "entity_slug": article.slug,
        "source_name": article.source_name or "",
        "is_breaking": article.is_breaking == 1,
    })


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
