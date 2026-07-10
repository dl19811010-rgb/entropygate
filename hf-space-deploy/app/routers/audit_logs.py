from fastapi import APIRouter

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])


@router.get("")
async def list_audit_logs():
    return {"code": 200, "message": "Success", "data": []}
