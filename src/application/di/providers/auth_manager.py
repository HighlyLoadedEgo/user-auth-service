from typing import Annotated

import structlog
from fastapi import Depends

from src.application.di.providers.current_user import get_current_user
from src.modules.users.dtos.user_dtos import BaseUserDTO
from src.modules.users.validators.user_validators import check_permission

logger = structlog.stdlib.get_logger(__name__)


class AuthorizationManager:
    """
    Handles the authorization process
    by validating the JWT token and user permissions.
    """

    def __init__(
        self,
        permission_list: list[str] | None = None,
    ) -> None:
        self._permission_list = permission_list

    async def __call__(
        self, auth_user_data: Annotated[BaseUserDTO, Depends(get_current_user)]
    ) -> BaseUserDTO:
        """Validates the JWT token and initializes the user's authorization context."""

        if self._permission_list:
            check_permission(user=auth_user_data, permission_list=self._permission_list)

        return auth_user_data
