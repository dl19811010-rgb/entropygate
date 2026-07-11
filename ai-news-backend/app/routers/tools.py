from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter(prefix="/tools", tags=["Tools"])


@router.get("")
async def list_tools(db: Session = Depends(get_db)):
    from app.models.tool import Tool
    items = db.query(Tool).all()
    return {"code": 200, "message": "Success", "data": [t.to_dict() for t in items]}
