from dataclasses import dataclass

from src.core.common.exceptions import BaseAppError


@dataclass(eq=True)
class TokenExpiredError(BaseAppError):
    @property
    def message(self) -> str:
        return "Token Expired: Token has expired."


@dataclass(eq=True)
class InvalidTokenError(BaseAppError):
    @property
    def message(self) -> str:
        return "Invalid Token: The token provided is invalid."


@dataclass(eq=True)
class AuthorizationFailedError(BaseAppError):
    @property
    def message(self) -> str:
        return "Authorization Failed: Access denied."
