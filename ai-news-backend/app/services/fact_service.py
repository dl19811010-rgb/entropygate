"""Fact Service - stub."""
from sqlalchemy.orm import Session


class FactService:
    def __init__(self, db: Session):
        self.db = db
