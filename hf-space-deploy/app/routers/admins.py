from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.utils.dependencies import get_current_admin

router = APIRouter(prefix="/admins", tags=["Admins"])


@router.get("")
async def list_admins(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    from app.models.admin import Admin
    items = db.query(Admin).all()
    return {"code": 200, "message": "Success", "data": [a.to_dict() for a in items]}


@router.get("/me")
async def get_me(admin=Depends(get_current_admin)):
    return {"code": 200, "message": "Success", "data": admin.to_dict()}
