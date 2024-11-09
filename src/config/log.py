from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class LoggerConfig(BaseSettings):
    """
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0
    """

    LOG_LEVEL: str | int
    JSON_FORMAT: bool

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )
