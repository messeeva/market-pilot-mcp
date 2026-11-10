from sqlalchemy import DateTime
from datetime import UTC, datetime
from sqlalchemy.engine import Dialect
from sqlalchemy.types import TypeDecorator


def utc_now() -> datetime:
    return datetime.now(UTC)


class UTCDateTime(TypeDecorator[datetime]):
    impl = DateTime
    cache_ok = True

    def process_bind_param(
        self,
        value: datetime | None,
        dialect: Dialect,
    ) -> datetime | None:
        if value is None:
            return None

        if value.utcoffset() is None:
            raise ValueError("A timezone-aware datetime is required")

        utc_value = value.astimezone(UTC)
        return utc_value.replace(tzinfo=None)

    def process_result_value(
        self,
        value: datetime | None,
        dialect: Dialect,
    ) -> datetime | None:
        if value is None:
            return None

        return value.replace(tzinfo=UTC)
