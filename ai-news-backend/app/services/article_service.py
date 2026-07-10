"""Article Service — CRUD and business logic for articles."""
import logging
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_

from app.models.article import Article
from app.models.source import Source, EDITORIAL_TIERS
from app.models.audit import AuditLog, EditorialDecision
from app.services.editorial_service import editorial_service
from app.core.service import BaseService

logger = logging.getLogger(__name__)


class ArticleService(BaseService[Article]):
    model = Article

    def list_articles(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        category_id: Optional[int] = None,
        source_id: Optional[int] = None,
        search: Optional[str] = None,
        bucket: Optional[str] = None,
        sort_by: str = "created_at",
        sort_dir: str = "desc",
    ) -> tuple[list[Article], int]:
        """List articles with filtering, pagination, and sorting."""
        q = self.db.query(Article)

        if status:
            q = q.filter(Article.review_status == status)
        if category_id:
            q = q.filter(Article.category_id == category_id)
        if source_id:
            q = q.filter(Article.source_id == source_id)
        if bucket:
            q = q.filter(Article.editorial_bucket == bucket)
        if search:
            like = f"%{search}%"
            q = q.filter(
                or_(
                    Article.title.ilike(like),
                    Article.summary.ilike(like),
                    Article.content.ilike(like),
                )
            )

        # Count
        total = q.count()

        # Sort
        sort_col = getattr(Article, sort_by, Article.created_at)
        if sort_dir == "asc":
            q = q.order_by(sort_col.asc())
        else:
            q = q.order_by(desc(sort_col))

        offset = (page - 1) * page_size
        items = q.offset(offset).limit(page_size).all()
        return items, total

    def create_article(self, **kwargs) -> Article:
        """Create an article and compute its editorial score."""
        article = super().create(**kwargs)
        self._compute_and_save_editorial(article)
        return article

    def update_article(self, article_id: int, **kwargs) -> Optional[Article]:
        """Update an article."""
        article = self.get_by_id(article_id)
        if not article:
            return None
        for key, value in kwargs.items():
            if hasattr(article, key) and value is not None:
                setattr(article, key, value)
        article.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(article)
        return article

    def approve_article(self, article_id: int, admin_id: int, admin_username: str, reasoning: str = "") -> Optional[Article]:
        """Approve an article for publication."""
        article = self.get_by_id(article_id)
        if not article:
            return None

        old_score = article.editorial_score
        old_bucket = article.editorial_bucket

        article.review_status = "approved"
        article.reviewed_by = admin_id
        article.reviewed_at = datetime.utcnow()
        article.review_notes = reasoning

        # Log the editorial decision
        decision = EditorialDecision(
            article_id=article_id,
            decision="approved",
            admin_id=admin_id,
            admin_username=admin_username,
            reasoning=reasoning,
            editorial_score_before=old_score,
            editorial_score_after=old_score,
            editorial_bucket_before=old_bucket,
            editorial_bucket_after=old_bucket,
        )
        self.db.add(decision)

        # Audit
        audit = AuditLog(
            action="approve_article",
            entity_type="article",
            entity_id=article_id,
            admin_id=admin_id,
            admin_username=admin_username,
            details=reasoning,
        )
        self.db.add(audit)

        self.db.commit()
        self.db.refresh(article)
        return article

    def reject_article(self, article_id: int, admin_id: int, admin_username: str, reasoning: str = "") -> Optional[Article]:
        """Reject an article."""
        article = self.get_by_id(article_id)
        if not article:
            return None

        old_score = article.editorial_score
        old_bucket = article.editorial_bucket

        article.review_status = "rejected"
        article.reviewed_by = admin_id
        article.reviewed_at = datetime.utcnow()
        article.review_notes = reasoning

        decision = EditorialDecision(
            article_id=article_id,
            decision="rejected",
            admin_id=admin_id,
            admin_username=admin_username,
            reasoning=reasoning,
            editorial_score_before=old_score,
            editorial_score_after=old_score,
            editorial_bucket_before=old_bucket,
            editorial_bucket_after=old_bucket,
        )
        self.db.add(decision)

        audit = AuditLog(
            action="reject_article",
            entity_type="article",
            entity_id=article_id,
            admin_id=admin_id,
            admin_username=admin_username,
            details=reasoning,
        )
        self.db.add(audit)

        self.db.commit()
        self.db.refresh(article)
        return article

    def get_grouped_review(self) -> dict:
        """Return articles grouped by editorial bucket for review queue."""
        articles = self.db.query(Article).filter(Article.review_status == "pending").all()

        groups = {"essential": [], "authoritative": [], "credible": [], "signal": [], "peripheral": []}
        for a in articles:
            bucket = a.editorial_bucket or "signal"
            if bucket in groups:
                groups[bucket].append(a.to_dict())
            else:
                groups.setdefault(bucket, []).append(a.to_dict())

        return groups

    def get_brief(self, article_id: int) -> Optional[dict]:
        """Return a formatted brief for an article."""
        article = self.get_by_id(article_id)
        if not article:
            return None
        d = article.to_dict()
        d["source"] = article.source.to_dict() if article.source else None
        return d

    def _compute_and_save_editorial(self, article: Article) -> None:
        """Compute editorial score and bucket using the editorial service."""
        try:
            result = editorial_service.compute_editorial_score(article)
            article.editorial_score = result["score"]
            article.editorial_bucket = result["bucket"]
            article.editorial_tier = result.get("tier", "c_tier")
            article.newsworthiness_score = result.get("newsworthiness", 50.0)
            self.db.commit()
            self.db.refresh(article)
        except Exception as e:
            logger.warning("Editorial score computation failed: %s", e)


article_service_svc = ArticleService  # export class for DI
