from fastapi import FastAPI

from src.application.api.routers.auth.admin import router as admin_auth_router
from src.application.api.routers.healthcheck import router as healthcheck_router


def init_routers(app: FastAPI) -> None:
    """Initialize the api for the application."""
    prefix = "/api/v1"

    app.include_router(
        router=healthcheck_router,
        tags=["Check server."],
    )
    app.include_router(
        router=admin_auth_router,
        prefix=f"{prefix}/admin/auth",
        tags=["Admin service authentication."],
    )
