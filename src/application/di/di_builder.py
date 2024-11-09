from fastapi import FastAPI

from src.application.di.providers.db_session import DbProvider
from src.application.di.providers.redis_client import RedisProvider
from src.application.di.stubs import (
    async_session_stub,
    redis_client_stub,
)
from src.config.settings import Settings
from src.core.database.session_management import get_engine


def build_di(app: FastAPI, config: Settings) -> None:
    """Create an instance and override the depends."""
    async_engine = get_engine(config=config.DATABASE, async_=True)
    db_provider = DbProvider(async_engine=async_engine)
    redis_provider = RedisProvider(redis_config=config.REDIS)

    app.dependency_overrides = {
        async_session_stub: db_provider.get_async_session,
        redis_client_stub: redis_provider.get_redis_client,
    }
