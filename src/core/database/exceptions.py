from dataclasses import dataclass

from src.core.common.exceptions import BaseAppError


@dataclass(eq=True)
class DatabaseError(BaseAppError):
    db_message: str

    @property
    def message(self) -> str:
        """Method for error message."""
        return f"An error occurred while processing your db request with message: {self.db_message}"
