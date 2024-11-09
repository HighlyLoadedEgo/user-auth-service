from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.dml import (
    Insert,
    Update,
)
from sqlalchemy.sql.selectable import Select


class Executor:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_record(
        self,
        stmt: Select | Insert | Update,
        schema: type[BaseModel],
    ) -> BaseModel | None:
        """Get record with from db."""
        async with self._session.begin_nested():
            results = await self._session.execute(stmt)
        data = results.scalar_one_or_none()
        return schema.model_validate(data) if data else None

    async def get_record_relationship(
        self,
        stmt: Select | Insert | Update,
        schema: type[BaseModel],
    ) -> BaseModel | None:
        """Get record with relationship from db."""
        async with self._session.begin_nested():
            results = await self._session.execute(stmt)
        data = results.unique().scalar_one_or_none()
        return schema.model_validate(data) if data else None

    async def get_records(
        self,
        stmt: Select | Insert | Update,
        schema: type[BaseModel],
    ) -> list[BaseModel]:
        """Get records with from db."""
        async with self._session.begin_nested():
            results = await self._session.execute(stmt)
        data = results.scalars()
        return [schema.model_validate(row) for row in data]

    async def get_records_relationship(
        self,
        stmt: Select | Insert | Update,
        schema: type[BaseModel],
    ) -> list[BaseModel]:
        """Get records with relationship from db."""
        async with self._session.begin_nested():
            results = await self._session.execute(stmt)
        data = results.unique().scalars().all()
        return [schema.model_validate(row) for row in data]
