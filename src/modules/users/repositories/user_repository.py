import uuid

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from src.core.database.executor import Executor
from src.core.database.models import User
from src.modules.users.dtos.user_dtos import (
    UserCreateDTO,
    UserDTO,
)


class UserRepository(Executor):
    async def create_user(
        self,
        data: UserCreateDTO,
    ) -> UserDTO | None:
        """Create user in database function."""
        stmt = insert(User).values(**data.model_dump()).returning(User)
        return await self.get_record(
            stmt=stmt,
            schema=UserDTO,
        )

    async def get_user_by_id(self, user_id: uuid.UUID) -> UserDTO | None:
        """Get user by id from database."""
        stmt = select(User).where(User.id == user_id)
        return await self.get_record_relationship(
            stmt=stmt,
            schema=UserDTO,
        )

    async def get_user_by_email(self, email: str) -> UserDTO | None:
        """Get user by email from database."""
        stmt = select(User).where(User.email == email)
        return await self.get_record_relationship(
            stmt=stmt,
            schema=UserDTO,
        )
