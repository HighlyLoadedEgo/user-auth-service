from pydantic import BaseModel

from src.modules.users.common.constants import CompanyRole


class CompanyInformationCreateRequestSchema(BaseModel):
    """CompanyInformation base schema."""

    name: str
    role: CompanyRole
    tin: str
    rrc: str
