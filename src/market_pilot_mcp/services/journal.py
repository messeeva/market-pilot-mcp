from ..database import database
from ..models import JournalEntry, JournalEntryType, Symbol

import uuid
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


class JournalError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(message)


class JournalService:
    def __init__(self) -> None:
        pass

    async def create_journal_entry(
        self,
        ticker: str,
        entry_type: JournalEntryType,
    ) -> uuid.UUID:
        ticker = ticker.strip().upper()

        if not ticker or len(ticker) > 8:
            raise ValueError("Ticker must contain 1-8 characters")

        async def insert_once() -> uuid.UUID:
            async with database.get_session() as session:
                symbol = await session.scalar(
                    select(Symbol).where(Symbol.ticker == ticker)
                )

                if symbol is None:
                    symbol = Symbol(ticker=ticker)
                    session.add(symbol)
                    await session.flush()

                entry = JournalEntry(
                    symbol_id=symbol.id,
                    entry_type=entry_type,
                )
                session.add(entry)
                await session.flush()

                return entry.id

        try:
            return await insert_once()
        except IntegrityError:
            # Retry once with a fresh session and transaction.
            return await insert_once()


journal_service = JournalService()
