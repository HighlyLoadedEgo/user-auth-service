from pydantic import (
    BaseModel,
    Field,
)

from src.config.api import swagger_config
from src.config.auth import JWTConfig
from src.config.database import DatabaseConfig
from src.config.log import LoggerConfig
from src.config.redis import RedisConfig
from src.config.server import ServerConfig


class Settings(BaseModel):
    """Compile all settings for this application."""

    SERVER: ServerConfig = ServerConfig()
    DATABASE: DatabaseConfig = DatabaseConfig()
    JWT: JWTConfig = JWTConfig()
    REDIS: RedisConfig = RedisConfig()
    LOGGING: LoggerConfig = LoggerConfig()
    APP: dict = Field(default_factory=swagger_config)


settings = Settings()
