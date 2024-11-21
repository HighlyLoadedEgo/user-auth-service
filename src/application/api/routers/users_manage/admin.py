from typing import Annotated

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.api.schemas.request_schemas.common import PaginationRequestSchema
from src.application.api.schemas.request_schemas.user.user import ManageUserFiltersSchema
from src.application.di.providers.auth_manager import AuthorizationManager
from src.application.di.stubs import async_session_stub
from src.core.database.schemas import PaginationSchema
from src.modules.users.common.constants import AdminUserRole
from src.modules.users.dtos.user_dtos import UserFiltersDTO, UsersDTO
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.use_cases.get_users_by_filters import GetUsersByFiltersUseCase

router = APIRouter()


@router.post(
    "/",
    response_model=UsersDTO,
    responses={},
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(AuthorizationManager(
            permission_list=[AdminUserRole.SUPER_ADMIN, AdminUserRole.ADMIN]
        ))
    ]
)
async def get_users_by_filters(
    session: Annotated[AsyncSession, Depends(async_session_stub)],
    user_filters: ManageUserFiltersSchema,
    pagination: PaginationRequestSchema = Depends()
):
    user_repo = UserRepository(session=session)
    use_case = GetUsersByFiltersUseCase(user_repo=user_repo)

    return await use_case(
        user_filters=UserFiltersDTO.model_validate(user_filters),
        pagination=PaginationSchema.model_validate(pagination)
    )
