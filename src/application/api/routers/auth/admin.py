from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.api.schemas.request_schemas.user.user import (
    UserCreateRequestSchema,
)
from src.application.api.schemas.response_schemas.base_responses import (
    ErrorResponse,
    OkResponse,
)
from src.application.api.schemas.response_schemas.user.user import UserResponseSchema
from src.application.di.stubs import async_session_stub
from src.core.common.exceptions import BadRequestError
from src.modules.users.dtos.user_dtos import UserCreateDTO
from src.modules.users.exceptions import UserIsAlreadyExistError
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.use_cases.auth.admin import RegistrateAdminUseCase

router = APIRouter()


@router.post(
    "/sign-up",
    response_model=OkResponse[UserResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": OkResponse[UserResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse[BadRequestError]},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[UserIsAlreadyExistError]},
    },
    status_code=status.HTTP_200_OK,
)
async def registrate_admin(
    registrate_data: UserCreateRequestSchema,
    session: AsyncSession = Depends(async_session_stub),
):
    user_repo = UserRepository(session=session)
    use_case = RegistrateAdminUseCase(user_repo=user_repo)
    result = await use_case(
        registrate_data=UserCreateDTO.model_validate(registrate_data)
    )

    return OkResponse(result=result)
