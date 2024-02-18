import contextlib
from typing import Optional, AsyncIterator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine, AsyncConnection
from sqlalchemy.orm import sessionmaker

from src.env_config import env_config

sync_engine = create_engine(
    env_config.sync_psql_url,
)

sync_session = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False
)


class DatabaseSessionManager:
    _engine: Optional[AsyncEngine]
    _session_maker: Optional[async_sessionmaker[AsyncSession]]

    def init(self) -> None:
        self._engine = create_async_engine(
            url=env_config.async_psql_url,
            pool_pre_ping=True,
        )
        self._session_maker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )

    async def create_tables(self):
        from .models import BaseModel
        async with self._engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

    async def close(self) -> None:
        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._session_maker = None

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._session_maker is None:
            raise IOError("DatabaseSessionManager is not initialized")
        async with self._session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    async def get_session(self) -> AsyncSession:
        async with self.session() as session:
            yield session

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise IOError("DatabaseSessionManager is not initialized")
        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise


db_manager = DatabaseSessionManager()
