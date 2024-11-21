from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class AuthConfig(BaseSettings):
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ACCESS_SECRET: str
    REFRESH_SECRET: str

    ADMIN_PASSWORD: str
    ADMIN_LOGIN: str

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )
