import uuid
from enum import StrEnum
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Column, String
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, SQLModel, Relationship

from .timezone import UTCDateTime, utc_now


class ProposalActions(StrEnum):
    RESEARCH = "research"
    WATCH = "watch"
    BUY = "buy"
    REDUCE = "reduce"
    EXIT = "exit"


class ProposalStatus(StrEnum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Proposal(SQLModel, table=True):
    __tablename__ = "journal"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )

    title: str = Field(nullable=False)
    thesis: str = Field(nullable=False)
    counter_argument: str = Field(nullable=False)

    proposed_action: ProposalActions = Field(
        sa_column=Column(
            SAEnum(
                ProposalActions,
                values_callable=lambda enum: [member.value for member in enum],
                native_enum=False,
                create_constraint=True,
                validate_strings=True,
                name="proposed_action",
                length=16,
            ),
            nullable=False,
        ),
    )
