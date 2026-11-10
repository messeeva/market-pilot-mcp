from market_pilot_mcp.core import settings, configure_logging
from market_pilot_mcp.server import mcp as mcp

configure_logging(settings.LOG_LEVEL)
