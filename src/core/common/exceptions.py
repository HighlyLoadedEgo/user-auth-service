from dataclasses import dataclass


@dataclass(eq=False)
class BaseAppError(Exception):
    @property
    def message(self) -> str:
        """Method for error message."""
        return "An error occurred while processing your request."


@dataclass(eq=True)
class BadRequestError(BaseAppError):
    info: str

    @property
    def message(self) -> str:
        return f"Bad Request: {self.info}"


@dataclass(eq=True)
class NotFoundError(BaseAppError):
    info: str

    @property
    def message(self) -> str:
        return f"Not Found: {self.info}"
