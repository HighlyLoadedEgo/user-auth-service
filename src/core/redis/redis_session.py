from contextlib import asynccontextmanager
from typing import AsyncIterator

from redis import asyncio

from src.config.settings import settings


def init_redis(redis_url: str) -> asyncio.Redis:
    redis_context = asyncio.from_url(
        f"{redis_url}",
        encoding="utf-8",
        decode_responses=True,
    )
    return redis_context


async def init_redis_pool() -> AsyncIterator[asyncio.Redis]:
    """Initializes redis session."""
    async with init_redis(settings.REDIS.redis_cache_url) as session:
        yield session


redis_pool_context = asynccontextmanager(init_redis_pool)
