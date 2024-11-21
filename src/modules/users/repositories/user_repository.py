import uuid

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import (
    joinedload,
    selectinload,
)

from src.core.common.constants import SortOrder, Empty
from src.core.database.executor import Executor
from src.core.database.models import (
    Role,
    User, CompanyInformation,
)
from src.core.database.schemas import PaginationSchema
from src.modules.users.dtos.user_dtos import (
    FullUserDTO,
    UserCreateDTO,
    UserDTO, UserFiltersDTO,
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

    async def get_user_with_relations_by_email(
        self,
        email: str,
    ) -> FullUserDTO | None:
        """Get user with relations by email from database function."""
        stmt = (
            select(User)
            .options(joinedload(User.role))
            .options(selectinload(User.company_information))
            .where(User.email == email)
        )
        return await self.get_record_relationship(
            stmt=stmt,
            schema=FullUserDTO,
        )

    async def get_user_with_relations_by_id(
        self,
        user_id: uuid.UUID,
    ) -> FullUserDTO | None:
        """Get user with relations by email from database function."""
        stmt = (
            select(User)
            .options(joinedload(User.role))
            .options(selectinload(User.company_information))
            .where(User.id == user_id)
        )
        return await self.get_record_relationship(
            stmt=stmt,
            schema=FullUserDTO,
        )

    async def get_users_by_roles(self, roles_list: list[str]) -> list[FullUserDTO]:
        stmt = (
            select(User)
            .join(User.role)
            .options(joinedload(User.role))
            .options(selectinload(User.company_information))
            .where(Role.name.in_(roles_list))
        )
        return await self.get_records(stmt=stmt, schema=FullUserDTO)  # type: ignore

    async def get_users_with_relations_by_filters(
        self,
        user_filters: UserFiltersDTO,
        pagination: PaginationSchema,
    ) -> list[FullUserDTO]:
        # TODO: сделать пагинацию
        stmt = (
            select(User)
            .options(joinedload(User.role))
            .options(selectinload(User.company_information))
        )
        list_expressions = list()
        if user_filters.name:
            list_expressions.append(User.name.ilike(f"%{user_filters.name}%"))
        if user_filters.surname:
            list_expressions.append(User.surname.ilike(f"%{user_filters.surname}%"))
        if user_filters.middle_name:
            list_expressions.append(
                User.middle_name.ilike(f"%{user_filters.middle_name}%")
            )
        if user_filters.email:
            list_expressions.append(User.email.ilike(f"%{user_filters.email}%"))
        if user_filters.phone:
            list_expressions.append(User.phone.ilike(f"%{user_filters.phone}%"))
        if user_filters.roles:
            user_roles = user_filters.roles
            # TODO: понять как лучше
            if None in user_roles:
                list_expressions.append(User.role_id.is_(None))
                user_roles.remove(None)
            if user_roles:
                list_expressions.append(User.role.has(Role.name.in_(user_roles)))
        if user_filters.company_name:
            list_expressions.append(
                User.company_information.has(
                    CompanyInformation.name.ilike(f"%{user_filters.company_name}%"),
                ),
            )
        if user_filters.company_roles:
            list_expressions.append(
                User.company_information.has(CompanyInformation.role.in_(user_filters.company_roles))
            )
        if user_filters.company_tin:
            list_expressions.append(
                User.company_information.has(tin=user_filters.company_tin)
            )
        if user_filters.company_rrc:
            list_expressions.append(
                User.company_information.has(rrc=user_filters.company_rrc)
            )
        if user_filters.last_date:
            last_date = user_filters.last_date
            if pagination.order == SortOrder.ASC:
                list_expressions.append(User.created_at > last_date)
            else:
                list_expressions.append(User.created_at < last_date)
        if user_filters.is_active:
            list_expressions.append(
                User.is_active.is_(user_filters.is_active)
            )
        if user_filters.is_confirmed:
            list_expressions.append(
                User.is_active.is_(user_filters.is_confirmed)
            )
        stmt = stmt.where(*list_expressions)
        return await self.get_records_relationship(  # type: ignore
            stmt=stmt,
            schema=FullUserDTO,
        )
