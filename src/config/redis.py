from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class RedisConfig(BaseSettings):
    REDIS_HOST: str
    REDIS_PASSWORD: str
    REDIS_PORT: str
    REDIS_DB_CACHE: int
    REDIS_DB_CELERY: str

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )

    @property
    def redis_cache_url(self) -> str:
        redis_url = f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_CACHE}"
        return redis_url

    @property
    def redis_celery_url(self) -> str:
        redis_url = f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_CELERY}"
        return redis_url
