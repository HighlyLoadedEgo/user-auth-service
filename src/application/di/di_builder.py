from fastapi import FastAPI

from src.application.di.stubs import (
    async_session_stub,
    celery_app_stub,
    jwt_manager_stub,
    redis_client_stub,
)
from src.config.settings import Settings
from src.core.auth_core.jwt import JWTManager
from src.core.celery.celery_configuration import celery_app
from src.core.database.session_context import db_provider
from src.core.redis.redis_context import redis_provider


def build_di(app: FastAPI, config: Settings) -> None:
    """Create an instance and override the depends."""

    app.dependency_overrides = {
        async_session_stub: db_provider.get_async_session,
        redis_client_stub: redis_provider.get_redis_client,
        jwt_manager_stub: lambda: JWTManager(jwt_config=config.AUTH),
        celery_app_stub: lambda: celery_app,
    }
