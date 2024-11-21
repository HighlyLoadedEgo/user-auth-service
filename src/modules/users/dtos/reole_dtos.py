import uuid
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class RoleDTO(BaseModel):
    """Role postgres schema."""

    id: uuid.UUID
    name: str
    created_at: datetime
    updated_at: datetime | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True)
