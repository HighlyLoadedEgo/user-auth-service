from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)


class UserCreateDTO(BaseModel):
    """User create response schema."""

    name: str
    surname: str
    middle_name: str | None
    email: EmailStr
    phone: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserDTO(BaseModel):
    """User postgres schema."""

    id: UUID
    name: str
    surname: str
    middle_name: str | None
    email: EmailStr
    password: str
    phone: str

    is_mail: bool
    is_active: bool
    is_confirmed: bool

    role_id: UUID | None
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
