"""Import all models so SQLAlchemy can register them before create_all()."""
from app.models.admin import Admin
from app.models.article import Article
from app.models.audit import AuditLog
from app.models.category import Category
from app.models.editorial import EditorialCalendar
from app.models.intelligence import Intelligence
from app.models.source import Source
from app.models.tag import Tag, article_tags
from app.models.tool import Tool
from app.models.topic import Topic

__all__ = [
    "Admin", "Article", "AuditLog", "Category", "EditorialCalendar",
    "Intelligence", "Source", "Tag", "article_tags", "Tool", "Topic",
]