from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

from .company_information import UserCompanyInformationResponseSchema
from .role import RoleResponseSchema


class UserResponseSchema(BaseModel):
    """User base response schema."""

    id: UUID
    name: str
    surname: str
    middle_name: str | None = Field(default=None)
    email: EmailStr
    phone: str

    is_mail: bool
    is_active: bool
    is_confirmed: bool

    role: RoleResponseSchema | None = Field(default=None)
    company_information: UserCompanyInformationResponseSchema | None = Field(
        default=None
    )

    created_at: datetime
    updated_at: datetime | None = Field(default=None)


class SignInResponseSchema(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: str
