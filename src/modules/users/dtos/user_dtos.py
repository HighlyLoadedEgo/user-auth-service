from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)

from src.core.common.constants import Empty
from src.modules.users.common.constants import UserWebRole
from src.modules.users.dtos.companies_dtos import (
    CompanyCreateInformationDTO,
    CompanyInformationDTO,
)
from src.modules.users.dtos.reole_dtos import RoleDTO


class UserLoginDTO(BaseModel):
    """User login schema."""

    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserCreateDTO(BaseModel):
    """User create response schema."""

    name: str
    surname: str
    middle_name: str | None = Field(default=None)
    email: EmailStr
    phone: str
    password: str

    is_active: bool = Field(default=False)
    is_confirmed: bool = Field(default=False)
    is_mail: bool = Field(default=False)

    role_id: UUID | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True)


class WebUserCreateDTO(BaseModel):
    """Schema for web user."""

    name: str
    surname: str
    middle_name: str | None = Field(default=None)
    email: EmailStr
    phone: str
    password: str

    is_active: bool = Field(default=False)
    is_confirmed: bool = Field(default=False)
    is_mail: bool = Field(default=False)

    role: UserWebRole
    company_information: CompanyCreateInformationDTO | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True)


class UserDTO(BaseModel):
    """User postgres schema."""

    id: UUID
    name: str
    surname: str
    middle_name: str | None = Field(default=None)
    email: EmailStr
    password: str
    phone: str

    is_mail: bool
    is_active: bool
    is_confirmed: bool

    role_id: UUID | None = Field(default=None)
    created_at: datetime
    updated_at: datetime | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True)


class FullUserDTO(UserDTO):
    """Full information about user."""

    role: RoleDTO | None = Field(default=None)
    company_information: CompanyInformationDTO | None = Field(default=None)


class BaseUserDTO(BaseModel):
    """Cached user model."""

    id: UUID
    name: str
    surname: str
    middle_name: str | None = Field(default=None)
    email: EmailStr
    phone: str

    is_mail: bool
    is_active: bool
    is_confirmed: bool

    created_at: datetime
    updated_at: datetime | None = Field(default=None)

    role: RoleDTO | None = Field(default=None)
    company_information: CompanyInformationDTO | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True)


class UserFiltersDTO(BaseModel):
    name: str | None = Field(default=None)
    surname: str | None = Field(default=None)
    middle_name: str | None = Field(default=None)
    email: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    roles: list[str | None] | None = Field(default=None)
    company_name: str | None = Field(default=None)
    company_roles: list[str] | None = Field(default=None)
    company_tin: int | None = Field(default=None)
    company_rrc: int | None = Field(default=None)
    last_date: datetime | None = Field(default=None)
    is_confirmed: bool | None = Field(default=None)
    is_active: bool | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True)


class UsersDTO(BaseModel):
    users: list[FullUserDTO]
    count: int
