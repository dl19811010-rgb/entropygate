from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("")
async def list_categories(db: Session = Depends(get_db)):
    from app.models.category import Category
    items = db.query(Category).filter(Category.is_active == 1).all()
    return {"code": 200, "message": "Success", "data": [c.to_dict() for c in items]}
