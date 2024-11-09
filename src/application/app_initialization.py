from typing import Any

import structlog
import uvicorn
from fastapi import FastAPI

from src.application.di.di_builder import build_di
from src.application.exception_handler import setup_exception_handlers
from src.application.middlewares.main import init_middlewares
from src.application.routers_init import init_routers
from src.config.settings import (
    Settings,
    settings,
)
from src.core.log.app_log.logger_configurator import configure_logger
from src.core.log.uvicorn_log.uvicorn_log_config_builder import build_uvicorn_log_config

logger = structlog.stdlib.get_logger(__name__)


def init_app(app_settings: Settings, lifespan: Any | None = None) -> FastAPI:
    """Initialize the FastAPI application with all dependencies."""
    app = FastAPI(
        **app_settings.APP,
        lifespan=lifespan,
    )
    init_middlewares(app=app, settings=app_settings)
    setup_exception_handlers(app=app)
    init_routers(app=app)

    return app


async def run_api(app: FastAPI, app_settings: Settings) -> None:
    """Start the FastAPI application and Uvicorn."""
    log_config = build_uvicorn_log_config(server_config=app_settings.LOGGING)
    uvicorn_config = uvicorn.Config(
        app,
        log_config=log_config,
        host=app_settings.SERVER.SERVER_HOST,
        port=app_settings.SERVER.SERVER_PORT,
    )
    server = uvicorn.Server(uvicorn_config)
    await server.serve()


async def main() -> None:
    """Main entry point."""
    configure_logger(logger_config=settings.LOGGING)
    app = init_app(app_settings=settings)
    build_di(app=app, config=settings)

    await run_api(app_settings=settings, app=app)
