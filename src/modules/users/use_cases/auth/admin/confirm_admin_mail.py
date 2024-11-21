import json

from celery import Celery

from src.core.common.exceptions import NotFoundError
from src.core.database.models import User
from src.core.redis.redis_cache import RedisClient
from src.modules.users.dtos.user_dtos import UserCreateDTO
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.validators.user_validators import validate_email_not_in_use


class ConfirmAdminMailUseCase:
    def __init__(
        self,
        celery_app: Celery,
        user_repo: UserRepository,
        cache_client: RedisClient,
    ) -> None:
        self._celery_app = celery_app
        self._user_repo = user_repo
        self._cache_client = cache_client

    async def __call__(self, confirm_token: str) -> None:
        """Confirm admin mail after registration."""
        cached_data: None | str = await self._cache_client.get_cache(key=confirm_token)
        if not cached_data:
            raise NotFoundError(info="Confirm token not found.")
        create_admin_data: UserCreateDTO = UserCreateDTO.model_validate(
            json.loads(cached_data)
        )

        user: User | None = await self._user_repo.get_user_by_email(
            email=create_admin_data.email
        )
        validate_email_not_in_use(user=user)

        create_admin_data.is_active = True
        await self._user_repo.create_user(data=create_admin_data)

        self._celery_app.send_task(
            "src.core.celery.tasks.mailing.send_notify_new_admin_signup_mail_task",
        )
