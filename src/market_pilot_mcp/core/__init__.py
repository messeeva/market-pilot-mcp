from .config import settings
from .logging import configure_logging

configure_logging(settings.LOG_LEVEL)
