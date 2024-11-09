from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class ServerConfig(BaseSettings):
    """Model of the server configuration."""

    SERVER_HOST: str
    SERVER_PORT: int

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )
