from fastapi import APIRouter

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("")
async def list_roles():
    from app.models.source import EDITORIAL_TIERS
    roles = [{"key": k, **v} for k, v in EDITORIAL_TIERS.items()]
    return {"code": 200, "message": "Success", "data": roles}
