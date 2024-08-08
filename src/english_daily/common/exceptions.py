from http import HTTPStatus


class APIErrorMixin:
    """REST API error mixin."""

    message: str
    code: str
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message: str | None = None, code: str | None = None) -> None:
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __str__(self) -> str:
        return self.message

    def to_dict(self) -> dict:
        return {
            "error": {
                "code": self.code,
                "message": self.message,
            },
        }


class BaseEnglishDailyError(Exception):
    """Base service error."""


class EnglishDailyError(APIErrorMixin, BaseEnglishDailyError):
    """English Daily service error."""


class NotFoundError(EnglishDailyError):
    """Resource not found."""

    message = "Resource not found"
    code = "not_found"
    status_code: int = HTTPStatus.NOT_FOUND


class ConflictError(EnglishDailyError):
    """Resource conflict."""

    message = "Resource cannot be processed"
    code = "resource_conflict"
    status_code: int = HTTPStatus.CONFLICT


class ImproperlyConfiguredError(EnglishDailyError):
    """Improperly configured service."""

    message = "Improperly configured service"
    code = "improperly_configured"
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR


class AuthorizationError(EnglishDailyError):
    """Authorization error."""

    message = "Authorization error"
    code = "authorization_error"
    status_code = HTTPStatus.UNAUTHORIZED


class RequiredHeaderMissingError(EnglishDailyError):
    """Required header is missing in Headers."""

    message = "Required header is missing"
    code = "missing_header"
    status_code: int = HTTPStatus.BAD_REQUEST
