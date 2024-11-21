import uuid
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from src.modules.users.common.constants import CompanyRole


class CompanyCreateInformationDTO(BaseModel):
    """Schema to create company information."""

    name: str
    role: CompanyRole
    tin: str
    rrc: str

    user_id: uuid.UUID | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True)


class CompanyInformationDTO(BaseModel):
    """Postgres data schema."""

    id: uuid.UUID
    name: str
    role: CompanyRole
    tin: str
    rrc: str
    user_id: uuid.UUID

    created_at: datetime
    updated_at: datetime | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True)
