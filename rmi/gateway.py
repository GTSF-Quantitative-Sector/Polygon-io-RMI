import aiohttp
import asyncio
from datetime import date
from typing import Optional


class Connection:
    session: Optional[aiohttp.ClientSession]

    def __init__(self, api_key: str, timeout: Optional[float] = 10):
        """Initialize Connection Object

        Args:
            api_key (str): Polygon.io API key
            timeout (Optional[float]): time in seconds to wait before timing out

        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = None

    async def get_close(self, ticker: str, query_date: date) -> float:
        """Get close price for a ticker on a specific query date

        Args:
            ticker (str): the ticker to retreive the close price for
            query_date (date): date from which to get the close price
        Returns:
            float: close price for that date

        """
        if not self.active:
            raise RuntimeError("Must use async context manager to initialize client")

        date_string = query_date.strftime("%Y-%m-%d")
        url = f"/v1/open-close/{ticker}/{date_string}?apiKey={self.api_key}"

        assert self.session is not None
        try:
            async with self.session.get(url, timeout=self.timeout) as resp:
                response = await resp.json()
        except asyncio.TimeoutError:
            raise TimeoutError(
                f"Timed out while retreiving price for {ticker} on {date_string}"
            )

        if response["status"] == "NOT_FOUND":
            raise LookupError(
                f"could not find close price for {ticker} on {query_date}"
            )
        return response["close"]

    async def __aenter__(self):
        self.session = aiohttp.ClientSession("https://api.polygon.io")
        self.active = True
        return self

    async def __aexit__(self, *args):
        await self.session.close()
        self.active = False
