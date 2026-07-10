"""Admin Auth Router — login endpoint."""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import success_response, error_response
from app.utils.security import verify_password
from app.utils.jwt import create_access_token
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin Auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    admin: dict


@router.post("/login")
async def login_admin(req: LoginRequest, db: Session = Depends(get_db)):
    svc = AdminService(db)
    admin = svc.get_by_username(req.username)
    if not admin or not verify_password(req.password, admin.password_hash):
        return error_response("Invalid username or password", code=401)

    if not admin.is_active:
        return error_response("Admin account is disabled", code=403)

    # Update last login
    admin.last_login_at = datetime.utcnow()
    db.commit()

    token = create_access_token(data={"sub": str(admin.id), "role": admin.role, "username": admin.username})
    return success_response({
        "token": token,
        "admin": admin.to_dict(),
    }, message="Login successful")
