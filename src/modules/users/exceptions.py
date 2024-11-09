from dataclasses import dataclass

from src.core.common.exceptions import BaseAppError


@dataclass(eq=True)
class UserIsAlreadyExistError(BaseAppError):
    email: str

    @property
    def message(self) -> str:
        return f"User with email: {self.email} is already exist."
