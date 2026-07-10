from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("")
async def list_tags(db: Session = Depends(get_db)):
    from app.models.tag import Tag
    items = db.query(Tag).order_by(Tag.usage_count.desc()).all()
    return {"code": 200, "message": "Success", "data": [t.to_dict() for t in items]}
