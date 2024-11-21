from typing import (
    ClassVar,
    Generic,
    TypeVar,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

TResult = TypeVar("TResult")
TError = TypeVar("TError")


class Response(BaseModel):
    config_model: ClassVar = ConfigDict(frozen=True, arbitrary_types_allowed=True)


class OkResponse(Response, Generic[TResult]):
    result: TResult | None = Field(default=None)
    message: str | None = Field(default=None)


class ErrorData(Response, Generic[TError]):
    message: str = "Error message"
    data: TError | None = Field(default=None)


class ErrorResponse(Response, Generic[TError]):
    error: ErrorData[TError] = Field(default_factory=ErrorData)
