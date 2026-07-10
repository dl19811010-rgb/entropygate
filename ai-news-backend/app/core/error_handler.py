import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.response import error_response
from app.core.exceptions import AppException

logger = logging.getLogger(__name__)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    logger.warning("AppException: %s", exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(message=exc.message, code=exc.status_code),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content=error_response(message="Internal server error", code=500),
    )
