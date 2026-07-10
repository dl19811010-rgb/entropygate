"""Category Service - stub."""
from sqlalchemy.orm import Session
from app.core.service import BaseService
from app.models.category import Category


class CategoryService(BaseService[Category]):
    model = Category
