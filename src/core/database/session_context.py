from contextlib import asynccontextmanager

from src.config.settings import settings
from src.core.database.provider import DbProvider
from src.core.database.session_factory import get_engine

async_engine = get_engine(config=settings.DATABASE, async_=True)
db_provider = DbProvider(async_engine=async_engine)
async_session_context = asynccontextmanager(db_provider.get_async_session)
