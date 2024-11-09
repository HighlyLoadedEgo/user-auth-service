from src.config.log import LoggerConfig
from src.core.log.app_log.logger import StructLogger


def configure_logger(logger_config: LoggerConfig) -> None:
    """Configure the logger for the application."""
    struct_logger = StructLogger(
        level=logger_config.LOG_LEVEL, json_format=logger_config.JSON_FORMAT
    )
    struct_logger.configure()
