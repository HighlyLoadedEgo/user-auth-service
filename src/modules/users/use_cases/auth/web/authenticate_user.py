import structlog

from src.core.auth_core.jwt import JWTManager
from src.core.auth_core.schemas import (
    TokensData,
    UserSubject,
)
from src.core.redis.constants import CacheIntervals
from src.core.redis.redis_cache import RedisClient
from src.modules.users.dtos.user_dtos import (
    BaseUserDTO,
    FullUserDTO,
    UserLoginDTO,
)
from src.modules.users.exceptions import AuthenticationError
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.validators.user_validators import (
    validate_base_authentication_data,
)

logger = structlog.stdlib.get_logger(__name__)


class AuthenticateUserUseCase:
    def __init__(
        self,
        jwt_manager: JWTManager,
        user_repo: UserRepository,
        cache_client: RedisClient,
    ) -> None:
        self._user_repo = user_repo
        self._jwt_manager = jwt_manager
        self._cache_client = cache_client

    async def __call__(self, login_data: UserLoginDTO) -> TokensData:
        """Authenticate user and check permission."""
        user: FullUserDTO | None = (
            await self._user_repo.get_user_with_relations_by_email(
                email=login_data.email
            )
        )
        if not user:
            logger.warning("[Common] User doesn't have permission.")
            raise AuthenticationError()
        validate_base_authentication_data(user=user, login_data=login_data)

        caching_user = BaseUserDTO.model_validate(user)
        await self._cache_client.add_cache(
            key=str(caching_user.id),
            data=caching_user.model_dump(mode="json"),
            expire=CacheIntervals.TWO_DAY.value,
        )

        return self._jwt_manager.create_token_pair(
            subject=UserSubject.model_validate(user)
        )
