from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter(prefix="/sources", tags=["Sources"])


@router.get("")
async def list_sources(db: Session = Depends(get_db)):
    from app.models.source import Source
    items = db.query(Source).all()
    return {"code": 200, "message": "Success", "data": [s.to_dict() for s in items]}
