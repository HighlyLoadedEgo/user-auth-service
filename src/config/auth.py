from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class JWTConfig(BaseSettings):
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ACCESS_SECRET: str
    REFRESH_SECRET: str

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )
