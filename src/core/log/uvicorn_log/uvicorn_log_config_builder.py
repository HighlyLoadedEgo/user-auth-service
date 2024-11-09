import logging

from src.config.log import LoggerConfig
from src.core.log.uvicorn_log.logger import (
    UvicornAccessConsoleFormatter,
    UvicornAccessJSONFormatter,
    UvicornDefaultConsoleFormatter,
    UvicornDefaultJSONFormatter,
)


def build_uvicorn_log_config(server_config: LoggerConfig):
    """Configure Uvicorn logging config."""
    level_name = logging.getLevelName(server_config.LOG_LEVEL)

    if server_config.JSON_FORMAT:
        default = UvicornDefaultJSONFormatter  # type: ignore
        access = UvicornAccessJSONFormatter  # type: ignore
    else:
        default = UvicornDefaultConsoleFormatter  # type: ignore
        access = UvicornAccessConsoleFormatter  # type: ignore

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": default,
            },
            "access": {
                "()": access,
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["default"],
                "level": level_name,
                "propagate": False,
            },
            "uvicorn.error": {
                "level": level_name,
                "handlers": ["default"],
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["access"],
                "level": level_name,
                "propagate": False,
            },
        },
    }
