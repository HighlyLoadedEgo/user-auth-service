from typing import AsyncGenerator

from sqlalchemy import (
    Engine,
    create_engine,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config.database import DatabaseConfig


def get_engine(config: DatabaseConfig, async_: bool = True) -> AsyncEngine | Engine:
    """Create an engine for the storages."""
    if async_:
        return create_async_engine(config.db_url(async_=async_))
    else:
        return create_engine(config.db_url(async_=async_))


def async_session_maker(async_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create an async session for the storages."""
    return async_sessionmaker(async_engine, expire_on_commit=False)


async def create_async_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """Create async session for db"""
    async with session_factory() as session:
        yield session
