from collections.abc import (
    Awaitable,
    Callable,
)
from functools import partial

import structlog
from fastapi import FastAPI
from starlette import status
from starlette.requests import Request

from src.application.api.schemas.response_schemas.base_responses import (
    ErrorData,
    ErrorResponse,
)
from src.application.api.schemas.response_schemas.orjson import ORJSONResponseImpl
from src.core.common.exceptions import (
    BadRequestError,
    BaseAppError,
)
from src.modules.users.exceptions import UserIsAlreadyExistError

logger = structlog.stdlib.get_logger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        UserIsAlreadyExistError, error_handler(status_code=status.HTTP_409_CONFLICT)
    )
    app.add_exception_handler(
        BadRequestError, error_handler(status_code=status.HTTP_400_BAD_REQUEST)
    )
    app.add_exception_handler(Exception, unknown_exception_handler)


def error_handler(status_code: int) -> Callable[..., Awaitable[ORJSONResponseImpl]]:
    return partial(app_error_handler, status_code=status_code)


async def app_error_handler(
    request: Request, err: BaseAppError, status_code: int
) -> ORJSONResponseImpl:
    data = await handle_error(
        request=request,
        err=err,
        err_data=ErrorData(message=err.message, data=err),
        status_code=status_code,
    )
    return data


async def unknown_exception_handler(
    request: Request, err: Exception
) -> ORJSONResponseImpl:
    logger.error("Handle error", error=err)
    logger.exception("Unknown error occurred", error=err)
    return ORJSONResponseImpl(
        ErrorResponse(error=ErrorData(data=err)),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def handle_error(
    request: Request,
    err: Exception,
    err_data: ErrorData,
    status_code: int,
) -> ORJSONResponseImpl:
    logger.error("Handle error", error=err)

    return ORJSONResponseImpl(ErrorResponse(error=err_data), status_code=status_code)
