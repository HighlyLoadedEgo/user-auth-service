from fastapi import FastAPI

from src.application.api.routers.auth.admin import router as admin_auth_router
from src.application.api.routers.auth.common import router as auth_common_router
from src.application.api.routers.auth.web import router as web_auth_router
from src.application.api.routers.healthcheck import router as healthcheck_router
from src.application.api.routers.users_manage.common import router as user_common_router
from src.application.api.routers.users_manage.admin import router as admin_manage_router

def init_routers(app: FastAPI) -> None:
    """Initialize the api for the application."""
    prefix = "/api/v1"

    app.include_router(
        router=healthcheck_router,
        tags=["Check server."],
    )
    app.include_router(
        prefix=f"{prefix}/user", router=user_common_router, tags=["User common logic"]
    )
    app.include_router(
        prefix=f"{prefix}/auth", router=auth_common_router, tags=["Auth common logic."]
    )
    app.include_router(
        prefix=f"{prefix}/admin/users",
        router=admin_manage_router,
        tags=["Admin users manage."]
    )
    app.include_router(
        router=admin_auth_router,
        prefix=f"{prefix}/admin/auth",
        tags=["Admin authentication."],
    )
    app.include_router(
        router=web_auth_router,
        prefix=f"{prefix}/web/auth",
        tags=["Web authentication."],
    )
