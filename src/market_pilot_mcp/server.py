import logging
from .core import settings
from mcp.server import MCPServer
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

mcp = MCPServer(
    settings.NAME,
    log_level=settings.log_level,
)
