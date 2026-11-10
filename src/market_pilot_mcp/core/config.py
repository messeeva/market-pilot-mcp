from typing import Annotated, Literal

from pydantic import BeforeValidator, Field, MySQLDsn, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty="true",
        extra="ignore",
    )

    # === App Config === #
    NAME: str = "Market Pilot MCP"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO"
    )

    DATABASE_ENGINE: Literal["postgres", "sqlite"] = Field(default="postgres")
    DATABASE_URL: Annotated[PostgresDsn | MySQLDsn, BeforeValidator(lambda x: str(x))]

    ALPACA_KEY: str | None = None
    ALPACA_SECRET: str | None = None


settings = Settings()
