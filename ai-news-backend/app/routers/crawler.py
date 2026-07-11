"""Crawler & Editorial Observation System API."""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.crawl_service import CrawlService
from app.services.scheduler import scheduler_service
from app.services.editorial_service import generate_coverage_report
from app.models.source import Source, SOURCE_TYPES, PRIORITY_LEVELS
from app.models.topic import Topic
from app.models.editorial import EditorialCalendar
from app.core.editorial_policy import (
    TOPIC_TAXONOMY, EDITORIAL_QUOTA, FRESHNESS_BANDS,
    PRIORITY_SCHEDULE, compute_freshness,
)

router = APIRouter(prefix="/crawler", tags=["Crawler & EOS"])


# ── Scheduler control ──────────────────────────────────────────

@router.get("/status")
async def get_status():
    """Get scheduler status and priority schedule."""
    return scheduler_service.get_job_status()


@router.post("/start")
async def start_scheduler():
    """Start the crawl scheduler."""
    try:
        scheduler_service.start()
        return {"code": 200, "message": "Scheduler started", "data": scheduler_service.get_job_status()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop")
async def stop_scheduler():
    """Stop the crawl scheduler."""
    try:
        scheduler_service.stop()
        return {"code": 200, "message": "Scheduler stopped", "data": scheduler_service.get_job_status()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/trigger")
async def trigger_crawl(priority: str = Query(None, description="Priority level: critical, high, normal, low")):
    """Trigger a crawl manually by priority level."""
    if priority:
        success = scheduler_service.trigger_crawl(priority)
        if success:
            return {"code": 200, "message": f"Triggered crawl for {priority} priority"}
        raise HTTPException(status_code=400, detail=f"Unknown priority: {priority}")

    scheduler_service.trigger_all()
    return {"code": 200, "message": "Triggered crawl for all priority levels"}


# ── Crawl operations ───────────────────────────────────────────

@router.post("/crawl/{source_id}")
async def crawl_source(source_id: int, db: Session = Depends(get_db)):
    """Crawl a specific source."""
    try:
        crawl_service = CrawlService(db)
        count = crawl_service.crawl_source(source_id)
        return {"code": 200, "message": "Crawl completed", "data": {"new_articles": count}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crawl/all")
async def crawl_all(db: Session = Depends(get_db)):
    """Crawl all active sources."""
    try:
        crawl_service = CrawlService(db)
        results = crawl_service.crawl_all_active()
        return {"code": 200, "message": "Crawl completed", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Source management with EOS dimensions ──────────────────────

@router.get("/sources")
async def get_sources(
    source_type: str = Query(None, description="Filter by source type"),
    priority: str = Query(None, description="Filter by priority"),
    topic: str = Query(None, description="Filter by topic slug"),
    db: Session = Depends(get_db),
):
    """Get all sources with EOS metadata, with optional filters."""
    query = db.query(Source).filter(Source.is_active == 1, Source.status == "active")

    if source_type:
        query = query.filter(Source.source_type == source_type)
    if priority:
        query = query.filter(Source.priority == priority)
    if topic:
        query = query.filter(Source.topics.contains(topic))

    sources = query.all()
    return {"code": 200, "data": [src.to_dict() for src in sources]}


@router.get("/sources/{source_id}")
async def get_source(source_id: int, db: Session = Depends(get_db)):
    """Get a specific source with full EOS metadata."""
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return {"code": 200, "data": source.to_dict()}


@router.post("/sources/{source_id}/activate")
async def activate_source(source_id: int, db: Session = Depends(get_db)):
    """Activate a source."""
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    source.is_active = 1
    source.status = "active"
    source.health = "healthy"
    source.crawl_error_count = 0
    db.commit()
    return {"code": 200, "message": "Source activated", "data": source.to_dict()}


@router.post("/sources/{source_id}/deactivate")
async def deactivate_source(source_id: int, db: Session = Depends(get_db)):
    """Deactivate a source."""
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    source.is_active = 0
    source.status = "paused"
    db.commit()
    return {"code": 200, "message": "Source deactivated", "data": source.to_dict()}


# ── EOS: Topic management (Layer 2) ────────────────────────────

@router.get("/topics")
async def get_topics(db: Session = Depends(get_db)):
    """Get all topics with coverage stats."""
    topics = db.query(Topic).filter(Topic.is_active == 1).order_by(Topic.sort_order).all()

    # Count articles per topic in last 24h
    from app.models.article import Article
    now = datetime.utcnow()
    day_ago = now - timedelta(hours=24)

    result = []
    for topic in topics:
        # Count sources covering this topic
        sources = db.query(Source).filter(
            Source.is_active == 1,
            Source.topics.contains(topic.slug),
        ).count()

        result.append({
            **topic.to_dict(),
            "source_count": sources,
        })

    return {"code": 200, "data": result}


# ── EOS: Source Type distribution (Layer 3) ────────────────────

@router.get("/distribution/source-type")
async def get_source_type_distribution(db: Session = Depends(get_db)):
    """Get source distribution by source_type."""
    from sqlalchemy import func
    from collections import Counter

    sources = db.query(Source).filter(Source.is_active == 1, Source.status == "active").all()
    counts = Counter([s.source_type or "unknown" for s in sources])

    return {
        "code": 200,
        "data": {
            "types": SOURCE_TYPES,
            "distribution": dict(counts),
            "total": len(sources),
        },
    }


@router.get("/distribution/priority")
async def get_priority_distribution(db: Session = Depends(get_db)):
    """Get source distribution by priority."""
    from collections import Counter

    sources = db.query(Source).filter(Source.is_active == 1, Source.status == "active").all()
    counts = Counter([s.priority or "normal" for s in sources])

    return {
        "code": 200,
        "data": {
            "priorities": PRIORITY_SCHEDULE,
            "distribution": dict(counts),
            "total": len(sources),
        },
    }


# ── EOS: Editorial Calendar (Layer 5) ──────────────────────────

@router.get("/calendar")
async def get_calendar_events(
    active_only: bool = Query(False, description="Only return currently active events"),
    db: Session = Depends(get_db),
):
    """Get editorial calendar events."""
    query = db.query(EditorialCalendar).filter(EditorialCalendar.is_active == 1)

    if active_only:
        now = datetime.utcnow()
        query = query.filter(
            EditorialCalendar.start_date <= now,
            EditorialCalendar.end_date >= now,
        )

    events = query.order_by(EditorialCalendar.start_date).all()
    return {"code": 200, "data": [e.to_dict() for e in events]}


@router.post("/calendar")
async def create_calendar_event(event_data: dict, db: Session = Depends(get_db)):
    """Create a new editorial calendar event."""
    from slugify import slugify

    required = ["name", "start_date", "end_date"]
    for field in required:
        if field not in event_data:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")

    slug = event_data.get("slug") or slugify(event_data["name"])

    # Parse dates
    try:
        start = datetime.fromisoformat(event_data["start_date"]) if isinstance(event_data["start_date"], str) else event_data["start_date"]
        end = datetime.fromisoformat(event_data["end_date"]) if isinstance(event_data["end_date"], str) else event_data["end_date"]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format.")

    event = EditorialCalendar(
        name=event_data["name"],
        slug=slug,
        description=event_data.get("description", ""),
        start_date=start,
        end_date=end,
        boost_priority=event_data.get("boost_priority", "critical"),
        boost_sources=",".join(event_data.get("boost_sources", [])) if isinstance(event_data.get("boost_sources"), list) else event_data.get("boost_sources", ""),
        topics=",".join(event_data.get("topics", [])) if isinstance(event_data.get("topics"), list) else event_data.get("topics", ""),
        is_active=1,
    )
    db.add(event)
    db.commit()

    return {"code": 200, "message": "Calendar event created", "data": event.to_dict()}


# ── EOS: Editorial Coverage Report (Layer 8) ───────────────────

@router.get("/coverage")
async def get_coverage_report(db: Session = Depends(get_db)):
    """Generate editorial coverage report for the last 24 hours.

    Answers: 'Today did we miss anything?'
    """
    report = generate_coverage_report(db)
    return {"code": 200, "data": report}


# ── EOS: Editorial Policy & Quota (Layer 6) ────────────────────

@router.get("/policy")
async def get_editorial_policy():
    """Get the current editorial policy configuration."""
    return {
        "code": 200,
        "data": {
            "topic_taxonomy": TOPIC_TAXONOMY,
            "editorial_quota": EDITORIAL_QUOTA,
            "freshness_bands": FRESHNESS_BANDS,
            "priority_schedule": PRIORITY_SCHEDULE,
            "source_types": SOURCE_TYPES,
        },
    }


# ── EOS: Freshness check ───────────────────────────────────────

@router.get("/freshness/{article_id}")
async def get_article_freshness(article_id: int, db: Session = Depends(get_db)):
    """Get freshness band for a specific article."""
    from app.models.article import Article

    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    freshness = compute_freshness(article.published_at)
    return {"code": 200, "data": freshness}