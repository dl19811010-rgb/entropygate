"""Source Service - stub."""
from sqlalchemy.orm import Session
from app.core.service import BaseService
from app.models.source import Source


class SourceService(BaseService[Source]):
    model = Source
