from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.historical import StockHistoricalDataClient
from .journal import journal_service
from ..core import settings


class AlpacaService:
    key: bool = False

    def __init__(self) -> None:
        if settings.ALPACA_KEY and settings.ALPACA_SECRET:
            self.key = True

    async def request(self):
        if self.key == None:
            return {"success": "false", "message": "No alpaca API key provided"}
