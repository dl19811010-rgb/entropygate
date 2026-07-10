"""Articles Router — CRUD, review, brief, grouped-review."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import success_response, error_response, paginated_response
from app.services.article_service import ArticleService
from app.utils.dependencies import get_current_admin

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("")
async def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str = Query(None),
    category_id: int = Query(None),
    source_id: int = Query(None),
    search: str = Query(None),
    bucket: str = Query(None),
    sort_by: str = Query("created_at"),
    sort_dir: str = Query("desc"),
    db: Session = Depends(get_db),
):
    svc = ArticleService(db)
    items, total = svc.list_articles(
        page=page, page_size=page_size, status=status,
        category_id=category_id, source_id=source_id,
        search=search, bucket=bucket, sort_by=sort_by, sort_dir=sort_dir,
    )
    return paginated_response(
        items=[a.to_dict() for a in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/brief/{article_id}")
async def get_brief(article_id: int, db: Session = Depends(get_db)):
    svc = ArticleService(db)
    brief = svc.get_brief(article_id)
    if not brief:
        return error_response("Article not found", 404)
    return success_response(brief)


@router.get("/review/grouped")
async def get_grouped_review(db: Session = Depends(get_db)):
    svc = ArticleService(db)
    groups = svc.get_grouped_review()
    return success_response(groups)


@router.post("/{article_id}/approve")
async def approve_article(
    article_id: int,
    reasoning: str = Query(""),
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    svc = ArticleService(db)
    article = svc.approve_article(article_id, admin.id, admin.username, reasoning)
    if not article:
        return error_response("Article not found", 404)
    return success_response(article.to_dict(), message="Article approved")


@router.post("/{article_id}/reject")
async def reject_article(
    article_id: int,
    reasoning: str = Query(""),
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    svc = ArticleService(db)
    article = svc.reject_article(article_id, admin.id, admin.username, reasoning)
    if not article:
        return error_response("Article not found", 404)
    return success_response(article.to_dict(), message="Article rejected")


@router.get("/{article_id}")
async def get_article(article_id: int, db: Session = Depends(get_db)):
    svc = ArticleService(db)
    article = svc.get_by_id(article_id)
    if not article:
        return error_response("Article not found", 404)
    return success_response(article.to_dict())


@router.put("/{article_id}")
async def update_article(article_id: int, body: dict, admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    svc = ArticleService(db)
    article = svc.update_article(article_id, **body)
    if not article:
        return error_response("Article not found", 404)
    return success_response(article.to_dict(), message="Article updated")


@router.delete("/{article_id}")
async def delete_article(article_id: int, admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    svc = ArticleService(db)
    ok = svc.delete(article_id)
    if not ok:
        return error_response("Article not found", 404)
    return success_response(message="Article deleted")
