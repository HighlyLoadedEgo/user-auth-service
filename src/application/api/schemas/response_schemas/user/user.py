from uuid import UUID

from pydantic import (
    BaseModel,
    EmailStr,
)


class UserResponseSchema(BaseModel):
    """User create response schema."""

    id: UUID
    name: str
    surname: str
    middle_name: str | None
    email: EmailStr
    phone: str
