from uuid import uuid4

from celery import Celery

from src.core.database.models import User
from src.core.redis.constants import CacheIntervals
from src.core.redis.redis_cache import RedisClient
from src.modules.users.dtos.user_dtos import UserCreateDTO
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.utils.password import generate_password_hash
from src.modules.users.validators.user_validators import (
    validate_email_not_in_use,
    validate_full_name,
    validate_password,
)


class RegistrateAdminUseCase:
    def __init__(
        self,
        celery_app: Celery,
        user_repo: UserRepository,
        cache_client: RedisClient,
    ) -> None:
        self._celery_app = celery_app
        self._user_repo = user_repo
        self._cache_client = cache_client

    async def __call__(self, registrate_admin_data: UserCreateDTO) -> None:
        """Validate registration admin data and save user in db."""
        validate_full_name(data=registrate_admin_data)
        validate_password(password=registrate_admin_data.password)

        user: User | None = await self._user_repo.get_user_by_email(
            email=registrate_admin_data.email
        )
        validate_email_not_in_use(user=user)
        registrate_admin_data.password = generate_password_hash(
            password=registrate_admin_data.password
        )

        confirm_token = str(uuid4())
        await self._cache_client.add_cache(
            key=confirm_token,
            data=registrate_admin_data.model_dump(mode="json"),
            expire=CacheIntervals.ONE_HOUR.value,
        )
        self._celery_app.send_task(
            "src.core.celery.tasks.mailing.send_admin_confirm_mail_task",
            kwargs={
                "recipient": registrate_admin_data.email,
                "token": confirm_token,
            },
        )
