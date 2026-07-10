"""Tag Service - stub."""
from sqlalchemy.orm import Session
from app.core.service import BaseService
from app.models.tag import Tag


class TagService(BaseService[Tag]):
    model = Tag
