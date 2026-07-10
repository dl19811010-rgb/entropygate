"""Tool Service - stub."""
from sqlalchemy.orm import Session
from app.core.service import BaseService
from app.models.tool import Tool


class ToolService(BaseService[Tool]):
    model = Tool
