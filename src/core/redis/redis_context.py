from contextlib import asynccontextmanager

from src.config.settings import settings
from src.core.redis.provider import RedisProvider

redis_provider = RedisProvider(redis_config=settings.REDIS)
redis_pool_context = asynccontextmanager(redis_provider.get_redis_client)
