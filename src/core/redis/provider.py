from typing import AsyncGenerator

from src.config.redis import RedisConfig
from src.core.redis.redis_cache import RedisClient
from src.core.redis.redis_session import init_redis


class RedisProvider:
    def __init__(self, redis_config: RedisConfig):
        self._redis_config = redis_config

    async def get_redis_client(self) -> AsyncGenerator[RedisClient, None]:
        """Init RedisClient with pool context"""
        redis_context_manager = init_redis(redis_url=self._redis_config.redis_cache_url)
        async with redis_context_manager as session:
            yield RedisClient(redis_session=session)
