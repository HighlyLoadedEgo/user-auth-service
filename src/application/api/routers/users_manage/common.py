from typing import (
    Annotated,
    Union,
)

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.api.schemas.response_schemas.base_responses import (
    ErrorResponse,
    OkResponse,
)
from src.application.api.schemas.response_schemas.users.user import UserResponseSchema
from src.application.di.providers.auth_manager import AuthorizationManager
from src.application.di.stubs import async_session_stub
from src.core.auth_core.exceptions import (
    InvalidTokenError,
    TokenExpiredError,
)
from src.core.common.exceptions import NotFoundError
from src.modules.users.dtos.user_dtos import BaseUserDTO
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.use_cases.get_user_by_id import GetUserByIdUseCase

router = APIRouter()


@router.get(
    "/profile",
    response_model=OkResponse[UserResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": UserResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[NotFoundError]},
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse[Union[TokenExpiredError, InvalidTokenError]]
        },
    },
    status_code=status.HTTP_200_OK,
)
async def refresh_access_token(
    current_user: Annotated[BaseUserDTO, Depends(AuthorizationManager())],
    session: Annotated[AsyncSession, Depends(async_session_stub)],
):
    if not current_user:
        user_repo = UserRepository(session=session)
        use_case = GetUserByIdUseCase(user_repo=user_repo)
        result = await use_case(user_id=current_user.id)
    else:
        result = current_user

    return OkResponse(result=result)
