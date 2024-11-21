from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from src.application.middlewares.context import set_request_id_middleware
from src.application.middlewares.structlog import structlog_bind_middleware


def init_middlewares(app: FastAPI) -> None:
    """Initialize the middlewares for the application."""

    app.add_middleware(BaseHTTPMiddleware, dispatch=structlog_bind_middleware)
    app.add_middleware(BaseHTTPMiddleware, dispatch=set_request_id_middleware)
