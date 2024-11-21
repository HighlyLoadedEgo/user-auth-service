from uuid import uuid4

from celery import Celery

from src.core.database.models import User
from src.core.redis.constants import CacheIntervals
from src.core.redis.redis_cache import RedisClient
from src.modules.users.common.constants import UserWebRole
from src.modules.users.dtos.user_dtos import WebUserCreateDTO
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.utils.password import generate_password_hash
from src.modules.users.validators.company_information_validators import (
    validate_company_info,
    validate_company_info_exists,
)
from src.modules.users.validators.user_validators import (
    validate_email_not_in_use,
    validate_full_name,
    validate_password,
)


class RegistrateUserUseCase:
    def __init__(
        self,
        celery_app: Celery,
        user_repo: UserRepository,
        cache_client: RedisClient,
    ) -> None:
        self._celery_app = celery_app
        self._user_repo = user_repo
        self._cache_client = cache_client

    async def __call__(self, registrate_user_data: WebUserCreateDTO) -> None:
        """Validate registration user data and save user in db."""
        validate_full_name(data=registrate_user_data)
        validate_password(password=registrate_user_data.password)
        if registrate_user_data.role == UserWebRole.CORPORATE:
            new_company_information = registrate_user_data.company_information
            validate_company_info_exists(company_info=new_company_information)
            validate_company_info(
                company_info=registrate_user_data.company_information  # type: ignore
            )

        user: User | None = await self._user_repo.get_user_by_email(
            email=registrate_user_data.email
        )
        validate_email_not_in_use(user=user)
        registrate_user_data.password = generate_password_hash(
            password=registrate_user_data.password
        )

        confirm_token = str(uuid4())
        await self._cache_client.add_cache(
            key=confirm_token,
            data=registrate_user_data.model_dump(mode="json"),
            expire=CacheIntervals.ONE_HOUR.value,
        )
        self._celery_app.send_task(
            "src.core.celery.tasks.mailing.send_user_confirm_mail_task",
            kwargs={
                "recipient": registrate_user_data.email,
                "token": confirm_token,
            },
        )
