from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

from src.application.api.schemas.request_schemas.user.company_information import (
    CompanyInformationCreateRequestSchema,
)
from src.core.common.constants import Empty
from src.modules.users.common.constants import UserWebRole


class AdminCreateRequestSchema(BaseModel):
    """User create request schema."""

    name: str
    surname: str
    middle_name: str | None = Field(default=None)
    email: EmailStr
    phone: str
    password: str


class UserCreateRequestSchema(BaseModel):
    """User create request schema."""

    name: str
    surname: str
    middle_name: str | None = Field(default=None)
    email: EmailStr
    phone: str
    password: str

    role: UserWebRole
    company_information: CompanyInformationCreateRequestSchema | None = Field(
        default=None
    )


class UserLoginRequestSchema(BaseModel):
    """USet login data."""

    email: EmailStr
    password: str


class ManageUserFiltersSchema(BaseModel):
    roles: list[str | None] | None = Field(default=None)
    is_active: bool
    is_confirmed: bool
