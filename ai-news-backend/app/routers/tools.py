from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import success_response, paginated_response

router = APIRouter(prefix="/tools", tags=["Tools"])


@router.get("")
async def list_tools(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    category: str = Query(None),
    sort: str = Query(None),
    db: Session = Depends(get_db),
):
    from app.models.tool import Tool
    q = db.query(Tool)
    if category:
        q = q.filter(Tool.category == category)

    # Sort
    if sort == "-view_count" or sort == "view_count":
        q = q.order_by(Tool.sort_order.desc())
    elif sort == "-created_at":
        q = q.order_by(Tool.created_at.desc())
    else:
        q = q.order_by(Tool.is_featured.desc(), Tool.sort_order.asc())

    total = q.count()
    items = q.offset((page - 1) * size).limit(size).all()

    return paginated_response(
        items=[t.to_dict() for t in items],
        total=total,
        page=page,
        page_size=size,
    )


@router.get("/{tool_id}")
async def get_tool(tool_id: str, db: Session = Depends(get_db)):
    from app.models.tool import Tool
    # Support both numeric ID and slug
    if tool_id.isdigit():
        tool = db.query(Tool).filter(Tool.id == int(tool_id)).first()
    else:
        tool = db.query(Tool).filter(Tool.slug == tool_id).first()

    if not tool:
        return success_response(None, "Tool not found", 404)
    return success_response(tool.to_dict())
