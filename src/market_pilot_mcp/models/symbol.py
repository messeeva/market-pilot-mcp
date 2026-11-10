import uuid
from typing import TYPE_CHECKING
from datetime import UTC, datetime
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import (
    Column,
    DateTime,
    String,
    text,
)

if TYPE_CHECKING:
    from .journal import JournalEntry


class Symbol(SQLModel, table=True):
    __tablename__ = "symbol"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )
    ticker: str = Field(
        max_length=8,
        unique=True,
        index=True,
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )
    entries: list["JournalEntry"] = Relationship(
        back_populates="symbol",
        sa_relationship_kwargs={"lazy": "raise"},
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(UTC),
        },
    )
