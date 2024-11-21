import json

from celery import Celery

from src.core.common.exceptions import NotFoundError
from src.core.database.models import User
from src.core.redis.redis_cache import RedisClient
from src.modules.users.common.constants import UserWebRole
from src.modules.users.dtos.user_dtos import (
    UserCreateDTO,
    WebUserCreateDTO,
)
from src.modules.users.repositories.company_repository import CompanyRepository
from src.modules.users.repositories.role_repository import RoleRepository
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.validators.role_validators import validate_role_exists
from src.modules.users.validators.user_validators import validate_email_not_in_use


class ConfirmUserMailUseCase:
    def __init__(
        self,
        celery_app: Celery,
        user_repo: UserRepository,
        role_repo: RoleRepository,
        company_repo: CompanyRepository,
        cache_client: RedisClient,
    ) -> None:
        self._celery_app = celery_app
        self._user_repo = user_repo
        self._role_repo = role_repo
        self._company_repo = company_repo
        self._cache_client = cache_client

    async def __call__(self, confirm_token: str) -> None:
        """Confirm user mail after registration."""
        cached_data: None | str = await self._cache_client.get_cache(key=confirm_token)
        if not cached_data:
            raise NotFoundError(info="Confirm token not found.")
        create_full_user_data: WebUserCreateDTO = WebUserCreateDTO.model_validate(
            json.loads(cached_data)
        )

        user: User | None = await self._user_repo.get_user_by_email(
            email=create_full_user_data.email
        )
        validate_email_not_in_use(user=user)

        role = await self._role_repo.get_role_by_name(
            role_name=create_full_user_data.role.value
        )

        new_user_data = UserCreateDTO.model_validate(create_full_user_data)
        validate_role_exists(role=role)
        new_user_data.role_id = role.id  # type: ignore
        if not create_full_user_data.company_information:
            new_user_data.is_confirmed = True
        new_user_data.is_active = True

        await self._user_repo.create_user(data=new_user_data)

        if create_full_user_data.role == UserWebRole.CORPORATE:
            new_company_data = create_full_user_data.company_information
            new_company_data.user_id = new_user_data.id  # type: ignore

            await self._company_repo.create_company(data=new_company_data)  # type: ignore

            self._celery_app.send_task(
                "core.celery.tasks.tasks.send_notify_new_company_signup_mail_task"
            )
