from typing import (
    Annotated,
    Union,
)

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from src.application.api.schemas.response_schemas.base_responses import (
    ErrorResponse,
    OkResponse,
)
from src.application.di.providers.auth_manager import AuthorizationManager
from src.application.di.stubs import (
    jwt_manager_stub,
    redis_client_stub,
)
from src.core.auth_core.exceptions import (
    AuthorizationFailedError,
    InvalidTokenError,
    TokenExpiredError,
)
from src.core.auth_core.jwt import JWTManager
from src.core.redis.redis_cache import RedisClient
from src.modules.users.dtos.user_dtos import BaseUserDTO

router = APIRouter()


@router.post(
    "/refresh",
    response_model=OkResponse[str],
    responses={
        status.HTTP_200_OK: {"model": OkResponse},
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse[Union[TokenExpiredError, InvalidTokenError]]
        },
    },
    status_code=status.HTTP_200_OK,
)
async def refresh_access_token(
    jwt_manager: Annotated[JWTManager, Depends(jwt_manager_stub)],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
):
    result = jwt_manager.refresh_access_token(refresh_token=credentials.credentials)

    return OkResponse(result=result)


@router.post(
    "/sign-out",
    response_model=None,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse[AuthorizationFailedError]
        },
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout_user(
    current_user: Annotated[BaseUserDTO, Depends(AuthorizationManager())],
    redis_client: Annotated[RedisClient, Depends(redis_client_stub)],
):
    await redis_client.delete_cache(keys=[str(current_user.id)])
