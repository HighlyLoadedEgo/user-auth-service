import uuid
from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
)

from src.modules.users.common.constants import CompanyRole


class UserCompanyInformationResponseSchema(BaseModel):
    """Response schema for company information"""

    id: uuid.UUID
    name: str
    role: CompanyRole
    tin: str
    rrc: str

    created_at: datetime
    updated_at: datetime | None = Field(default=None)
