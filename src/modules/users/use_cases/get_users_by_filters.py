import structlog

from src.core.database.schemas import PaginationSchema
from src.modules.users.dtos.user_dtos import FullUserDTO, UserFiltersDTO, UsersDTO
from src.modules.users.repositories.user_repository import UserRepository

logger = structlog.stdlib.get_logger(__name__)


class GetUsersByFiltersUseCase:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def __call__(
        self, user_filters: UserFiltersDTO, pagination: PaginationSchema
    ) -> UsersDTO:
        """Get user info by id."""
        users: list[FullUserDTO] | None = await self._user_repo.get_users_with_relations_by_filters(
            user_filters=user_filters, pagination=pagination
        )
        # users_count = len(users)

        return UsersDTO(users=users)
