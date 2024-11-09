import json
from typing import Any

import structlog
from redis import asyncio
from redis.exceptions import ConnectionError

logger = structlog.stdlib.get_logger(__name__)


class RedisClient:
    def __init__(self, redis_session: asyncio.Redis):
        self._redis_session = redis_session

    async def delete_cache(self, keys: list[str]) -> None:
        """Delete a cache by list of keys."""
        try:
            async with self._redis_session as redis:
                logger.info(f"Deleting cache by keys {keys}")
                await redis.delete(*keys)
                return None
        except ConnectionError as e:
            logger.error(f"[Redis] Error!!!! Redis service unavailable: {e}.")
            return None

    async def get_cache(self, key: str) -> str | None:
        """Get a cache by a key."""
        logger.info(f"Try to get cache by key: {key}")
        try:
            async with self._redis_session as redis:
                get_key = await redis.get(key)
                if get_key:
                    return get_key
                return None
        except ConnectionError as e:
            logger.error(f"[Redis] Error!!!! Redis service unavailable: {e}.")
            return None

    async def add_cache(self, key: str, data: Any, expire: int) -> None:
        """Add data to cache."""
        try:
            async with self._redis_session as redis:
                await redis.set(key, json.dumps(data), ex=expire)
                return None
        except ConnectionError as e:
            logger.error(f"[Redis] Error!!!! Redis service unavailable: {e}.")
            return None
