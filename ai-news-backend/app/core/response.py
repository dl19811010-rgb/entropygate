from typing import Any, Optional


def success_response(
    data: Any = None,
    message: str = "Success",
    code: int = 200,
) -> dict:
    return {
        "code": code,
        "message": message,
        "data": data,
    }


def error_response(
    message: str = "Error",
    code: int = 400,
    data: Any = None,
) -> dict:
    return {
        "code": code,
        "message": message,
        "data": data,
    }


def paginated_response(
    items: list,
    total: int,
    page: int = 1,
    page_size: int = 20,
    message: str = "Success",
) -> dict:
    return {
        "code": 200,
        "message": message,
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, (total + page_size - 1) // page_size),
        },
    }
