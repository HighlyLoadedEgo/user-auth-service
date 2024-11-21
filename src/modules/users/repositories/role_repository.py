from sqlalchemy import select

from src.core.database.executor import Executor
from src.core.database.models import Role
from src.modules.users.dtos.reole_dtos import RoleDTO


class RoleRepository(Executor):
    async def get_role_by_name(self, role_name: str) -> RoleDTO | None:
        """Get user by id from database."""
        stmt = select(Role).where(Role.name == role_name)
        return await self.get_record_relationship(
            stmt=stmt,
            schema=RoleDTO,
        )
