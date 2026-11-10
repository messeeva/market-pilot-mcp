import uuid
from enum import StrEnum
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Column, String
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, SQLModel, Relationship

from .timezone import UTCDateTime, utc_now

if TYPE_CHECKING:
    from .symbol import Symbol


class JournalEntryType(StrEnum):
    ORDER = "order"
    REVIEW = "review"
    PROPOSAL = "proposal"
    DECISION = "decision"
    OBSERVATION = "observation"


class JournalEntry(SQLModel, table=True):
    __tablename__ = "journal"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )

    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            UTCDateTime(),
            default=utc_now,
            nullable=False,
        ),
    )

    entry_type: JournalEntryType = Field(
        sa_column=Column(
            SAEnum(
                JournalEntryType,
                values_callable=lambda enum: [member.value for member in enum],
                native_enum=False,
                create_constraint=True,
                validate_strings=True,
                name="journal_entry_type",
                length=16,
            ),
            nullable=False,
        ),
    )

    symbol_id: uuid.UUID = Field(
        foreign_key="symbol.id",
        nullable=False,
        index=True,
    )

    symbol: "Symbol" = Relationship(
        back_populates="entries",
        sa_relationship_kwargs={"lazy": "raise"},
    )
