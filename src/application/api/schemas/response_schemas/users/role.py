from uuid import UUID

from pydantic import BaseModel


class RoleResponseSchema(BaseModel):
    """Role base response schema."""

    id: UUID
    name: str
