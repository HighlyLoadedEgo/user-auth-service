from pydantic import BaseModel

from src.core.common.constants import SortOrder


class PaginationSchema(BaseModel):
    offset: int = 10
    limit: int = 0
    order: SortOrder = SortOrder.ASC
