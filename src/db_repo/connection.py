
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.env_config import env_config

async_engine = create_async_engine(
    env_config.async_psql_url,
)

async_session = sessionmaker(
    engine=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
