from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class AppConfig(BaseSettings):
    DEBUG: bool = Field(default=True)

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )


CONFIG_SWAGGER_TRUE: dict = {
    "title": "Lynx",
    "docs_url": "/docs",
    "redoc_url": "/redoc",
    "swagger_ui_parameters": {"operationsSorter": "method"},
    "version": "1.0",
    "description": """
        SwaggerUI
    """,
}

CONFIG_SWAGGER_FALSE: dict = {
    "docs_url": None,
    "redoc_url": None,
}


def swagger_config() -> dict:
    """Swagger configuration."""
    return CONFIG_SWAGGER_TRUE if AppConfig().DEBUG else CONFIG_SWAGGER_FALSE
