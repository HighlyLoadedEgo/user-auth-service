from fastapi import (
    APIRouter,
    status,
)

router = APIRouter()


@router.get(
    "/healthcheck",
    response_model=str,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": str},
    },
)
async def healthcheck():
    return "OK"
