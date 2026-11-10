from .core import settings
from .core import configure_logging


def main() -> None:
    configure_logging(settings.LOG_LEVEL)

    from .server import mcp

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
