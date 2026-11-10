import logging
from ..core import settings
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.engine import URL, make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel

logger = logging.getLogger(__name__)


DEFAULT_ASYNC_DRIVERS = {
    "postgresql": "postgresql+asyncpg",
    "mysql": "mysql+asyncmy",
    "sqlite": "sqlite+aiosqlite",
}


def build_url(value: str | URL) -> URL:
    url = make_url(value)

    driver = DEFAULT_ASYNC_DRIVERS.get(url.drivername)

    if driver is not None:
        return url.set(drivername=driver)

    return url


class Database:
    def __init__(
        self,
        url: str | URL,
        *,
        connect_args: dict[str, Any] | None = None,
    ) -> None:
        logger.debug("Initializing Database")
        self.url = build_url(url)

        self.engine: AsyncEngine = create_async_engine(
            self.url,
            pool_pre_ping=True,
            connect_args=dict(connect_args or {}),
        )

        self.sessionmaker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Commit on success, roll back on failure, and close."""
        async with self.sessionmaker.begin() as session:
            yield session

    async def init(self) -> None:
        """Open a connection and create metadata"""
        async with self.engine.begin() as connection:
            await connection.run_sync(SQLModel.metadata.create_all)

        logger.debug("Database connection succesful")

    async def close(self) -> None:
        """Dispose of the connection pool during shutdown."""
        await self.engine.dispose()


database = Database(str(settings.DATABASE_URL))
