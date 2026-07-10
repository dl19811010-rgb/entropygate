from fastapi import APIRouter

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("")
async def upload_file():
    return {"code": 200, "message": "Upload endpoint (stub)", "data": {}}
