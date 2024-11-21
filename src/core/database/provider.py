from typing import AsyncGenerator

import structlog
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
)

from src.core.database.exceptions import DatabaseError
from src.core.database.session_factory import async_session_maker

logger = structlog.stdlib.get_logger(__name__)


class DbProvider:
    def __init__(self, async_engine: AsyncEngine) -> None:
        self._async_engine = async_engine

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get async session and commit after complete."""

        try:
            session_maker = async_session_maker(async_engine=self._async_engine)
            async with session_maker.begin() as session:
                yield session
        except SQLAlchemyError as error:
            logger.error(error._message())
            raise DatabaseError(db_message=error._message())
