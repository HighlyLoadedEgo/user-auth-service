from contextlib import asynccontextmanager
from typing import AsyncIterator

from redis import asyncio

from src.config.settings import settings
from src.core.redis.main import init_redis


async def init_redis_pool() -> AsyncIterator[asyncio.Redis]:
    """Initializes redis session."""
    async with init_redis(settings.REDIS.redis_cache_url) as session:
        yield session


redis_pool_context = asynccontextmanager(init_redis_pool)
