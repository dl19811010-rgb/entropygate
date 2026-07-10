"""Admin Service - stub."""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.admin import Admin


class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> Optional[Admin]:
        return self.db.query(Admin).filter(Admin.username == username).first()
