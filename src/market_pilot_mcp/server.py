import logging
from typing import Any
from mcp.server import MCPServer
from .models import JournalEntryType
from .services import journal_service
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from .core import settings
from .database import database

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_server: MCPServer) -> AsyncGenerator[dict[str, Any]]:
    await database.init()
    try:
        yield {}
    finally:
        await database.close()


mcp = MCPServer(settings.NAME, log_level=settings.LOG_LEVEL, lifespan=lifespan)


@mcp.tool("create_entry")
async def create_journal_entry(ticker: str, entry_type: JournalEntryType):
    try:
        result = await journal_service.create_journal_entry(
            ticker=ticker, entry_type=entry_type
        )

        return {"success": "true", "symbol_id": str(result)}
    except Exception as e:
        logger.exception(e)
