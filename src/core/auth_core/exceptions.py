from dataclasses import dataclass

from src.core.common.exceptions import BaseAppError


@dataclass(eq=True)
class TokenExpiredError(BaseAppError):
    @property
    def message(self) -> str:
        return "Token has expired."


@dataclass(eq=True)
class InvalidTokenError(BaseAppError):
    @property
    def message(self) -> str:
        return "The token provided is invalid."


@dataclass(eq=True)
class PermissionDeniedError(BaseAppError):
    @property
    def message(self) -> str:
        return "You do not have permission to perform this action."
