"""Custom application errors."""

from __future__ import annotations


class AppError(Exception):
    status_code = 500
    default_message = "An unexpected error occurred"

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.default_message)
        self.message = message or self.default_message


class NotFoundError(AppError):
    status_code = 404
    default_message = "Resource not found"


class AuthenticationError(AppError):
    status_code = 401
    default_message = "Authentication failed"


class AuthorizationError(AppError):
    status_code = 403
    default_message = "Not authorized"


class ValidationError(AppError):
    status_code = 422
    default_message = "Validation failed"


class RateLimitError(AppError):
    status_code = 429
    default_message = "Rate limit exceeded"


class ExternalServiceError(AppError):
    status_code = 502
    default_message = "Upstream service error"
