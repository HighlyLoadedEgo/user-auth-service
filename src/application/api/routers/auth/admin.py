from typing import Annotated

from celery import Celery
from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.api.schemas.request_schemas.user.user import (
    AdminCreateRequestSchema,
    UserLoginRequestSchema,
)
from src.application.api.schemas.response_schemas.base_responses import (
    ErrorResponse,
    OkResponse,
)
from src.application.api.schemas.response_schemas.users.user import SignInResponseSchema
from src.application.di.stubs import (
    async_session_stub,
    celery_app_stub,
    jwt_manager_stub,
    redis_client_stub,
)
from src.core.auth_core.jwt import JWTManager
from src.core.common.exceptions import (
    BadRequestError,
    NotFoundError,
)
from src.core.redis.redis_cache import RedisClient
from src.modules.users.dtos.user_dtos import (
    UserCreateDTO,
    UserLoginDTO,
)
from src.modules.users.exceptions import (
    AuthenticationError,
    EmailAlreadyInUseError,
    PermissionDeniedError,
)
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.use_cases.auth.admin.authenticate_admin import (
    AuthenticateAdminUseCase,
)
from src.modules.users.use_cases.auth.admin.confirm_admin_mail import (
    ConfirmAdminMailUseCase,
)
from src.modules.users.use_cases.auth.admin.registrate_admin import (
    RegistrateAdminUseCase,
)

router = APIRouter()


@router.post(
    "/sign-up",
    response_model=None,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse[BadRequestError]},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[EmailAlreadyInUseError]},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def registrate_admin(
    registrate_data: AdminCreateRequestSchema,
    celery_app: Annotated[Celery, Depends(celery_app_stub)],
    session: Annotated[AsyncSession, Depends(async_session_stub)],
    redis_client: Annotated[RedisClient, Depends(redis_client_stub)],
):
    user_repo = UserRepository(session=session)
    use_case = RegistrateAdminUseCase(
        user_repo=user_repo, celery_app=celery_app, cache_client=redis_client
    )
    await use_case(registrate_admin_data=UserCreateDTO.model_validate(registrate_data))


@router.post(
    "/sign-in",
    response_model=OkResponse[SignInResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": OkResponse[SignInResponseSchema]},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[AuthenticationError]},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse[PermissionDeniedError]},
    },
    status_code=status.HTTP_200_OK,
)
async def authenticate_user(
    login_data: UserLoginRequestSchema,
    session: Annotated[AsyncSession, Depends(async_session_stub)],
    jwt_manager: Annotated[JWTManager, Depends(jwt_manager_stub)],
    redis_client: Annotated[RedisClient, Depends(redis_client_stub)],
):
    user_repo = UserRepository(session=session)
    use_case = AuthenticateAdminUseCase(
        jwt_manager=jwt_manager, user_repo=user_repo, cache_client=redis_client
    )
    result = await use_case(login_data=UserLoginDTO.model_validate(login_data))

    return OkResponse(result=result)


@router.post(
    "/confirm",
    response_model=None,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[NotFoundError]},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse[PermissionDeniedError]},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[EmailAlreadyInUseError]},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def confirm_user(
    token: Annotated[str, Query()],
    session: Annotated[AsyncSession, Depends(async_session_stub)],
    celery_app: Annotated[Celery, Depends(celery_app_stub)],
    redis_client: Annotated[RedisClient, Depends(redis_client_stub)],
):
    user_repo = UserRepository(session=session)
    use_case = ConfirmAdminMailUseCase(
        user_repo=user_repo, cache_client=redis_client, celery_app=celery_app
    )
    await use_case(confirm_token=token)
