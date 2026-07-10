from fastapi import APIRouter

router = APIRouter(prefix="/operations", tags=["Operations"])


@router.get("/health")
async def health():
    return {"code": 200, "message": "OK", "data": {"status": "healthy"}}
