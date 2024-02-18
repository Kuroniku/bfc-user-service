from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from src.env_config import env_config

async_engine = create_async_engine(
    env_config.async_psql_url,
)

sync_engine = create_engine(
    env_config.sync_psql_url,
)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False
)

sync_session = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False
)





async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
