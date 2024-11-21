from sqlalchemy import insert

from src.core.database.executor import Executor
from src.core.database.models import CompanyInformation
from src.modules.users.dtos.companies_dtos import (
    CompanyCreateInformationDTO,
    CompanyInformationDTO,
)


class CompanyRepository(Executor):
    async def create_company(
        self,
        data: CompanyCreateInformationDTO,
    ) -> CompanyInformationDTO | None:
        """Create company in database function."""
        stmt = (
            insert(CompanyInformation)
            .values(**data.model_dump())
            .returning(CompanyInformation)
        )
        return await self.get_record(
            stmt=stmt,
            schema=CompanyInformationDTO,
        )
