from uuid import UUID

import structlog

from src.core.common.exceptions import NotFoundError
from src.modules.users.dtos.user_dtos import FullUserDTO
from src.modules.users.repositories.user_repository import UserRepository

logger = structlog.stdlib.get_logger(__name__)


class GetUserByIdUseCase:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def __call__(self, user_id: UUID) -> FullUserDTO:
        """Get user info by id."""
        user: FullUserDTO | None = await self._user_repo.get_user_with_relations_by_id(
            user_id=user_id
        )
        if not user:
            logger.warning("[Common] User doesn't exist.")
            raise NotFoundError(info="User not found.")

        return user
