from dataclasses import dataclass

from src.core.common.exceptions import BaseAppError


@dataclass(eq=True)
class EmailAlreadyInUseError(BaseAppError):
    email: str

    @property
    def message(self) -> str:
        return f"Email Already In Use: {self.email} is already exist."


@dataclass(eq=True)
class PermissionDeniedError(BaseAppError):
    info: str

    @property
    def message(self) -> str:
        return f"Permission Denied: {self.info}."


@dataclass(eq=True)
class AuthenticationError(BaseAppError):
    @property
    def message(self) -> str:
        return "Authentication Failed: Incorrect email or password"


@dataclass(eq=True)
class UserNotFoundError(BaseAppError):
    @property
    def message(self) -> str:
        return "User Not Found: User doesn't exit."
