"""Role Service - stub."""
from sqlalchemy.orm import Session


class RoleService:
    def __init__(self, db: Session):
        self.db = db
