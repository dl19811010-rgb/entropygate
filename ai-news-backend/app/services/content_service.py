"""Content Service - stub."""
from sqlalchemy.orm import Session


class ContentService:
    def __init__(self, db: Session):
        self.db = db
