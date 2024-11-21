import json
from typing import Annotated

import structlog
from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.di.stubs import (
    async_session_stub,
    jwt_manager_stub,
    redis_client_stub,
)
from src.core.auth_core.exceptions import AuthorizationFailedError
from src.core.auth_core.jwt import JWTManager
from src.core.auth_core.schemas import UserSubject
from src.core.redis.constants import CacheIntervals
from src.core.redis.redis_cache import RedisClient
from src.modules.users.dtos.user_dtos import (
    BaseUserDTO,
    FullUserDTO,
)
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.validators.user_validators import validate_user_active

logger = structlog.stdlib.get_logger(__name__)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    jwt_manager: Annotated[JWTManager, Depends(jwt_manager_stub)],
    cache_client: Annotated[RedisClient, Depends(redis_client_stub)],
    session: Annotated[AsyncSession, Depends(async_session_stub)],
) -> BaseUserDTO:
    """Retrieves the AuthUserDTO for the current user from cache or database."""
    token_payload = jwt_manager.decode_token(token=credentials.credentials)
    user_subject = UserSubject.model_validate(token_payload)

    cached_user: str | None = await cache_client.get_cache(key=str(user_subject.id))
    if not cached_user:
        user_repo = UserRepository(session=session)
        user_info: FullUserDTO | None = await user_repo.get_user_with_relations_by_id(
            user_id=user_subject.id
        )

        if not user_info:
            logger.warning("[Authorization] User doesn't exist.")
            raise AuthorizationFailedError()

        validate_user_active(user=user_info)
        await cache_client.add_cache(
            key=str(user_info.id),
            data=BaseUserDTO.model_validate(user_info).model_dump(mode="json"),
            expire=CacheIntervals.TWO_DAY.value,
        )
    else:
        user_info = json.loads(cached_user)
    auth_user_data = BaseUserDTO.model_validate(user_info)
    return auth_user_data
