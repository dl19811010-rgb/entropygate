class AppException(Exception):
    """Base application exception with an HTTP status code."""

    def __init__(self, message: str = "An error occurred", status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403)


class ValidationException(AppException):
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=422)


class ConflictException(AppException):
    def __init__(self, message: str = "Conflict"):
        super().__init__(message, status_code=409)
