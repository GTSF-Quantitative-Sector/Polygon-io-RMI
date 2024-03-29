""" Main client code """

import asyncio
import os
from datetime import date, timedelta
from typing import Any, List, Optional

import numpy as np
import numpy.typing as npt

from . import gateway


class Client:

    """RMI Client class. Calculates RMI and RSI from Polygon.io"""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

        if os.name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    async def get_rsi(self, ticker: str, query_date: str = None, period: int = 14) -> float:
        """Get current Relative Strength Index for a specified ticker

        Args:
            ticker (str): ticker for which to calculate RSI
            query_date (Optional[str]): date to start looking back from in YYYY-MM-DD format. Defaults to None, which uses today's date.
            period (Optional[int]): RSI calculation lookback period. Defaults to 14
        Returns:
            float: calculated RSI

        """
        return await self.get_rmi(ticker, query_date, period, 1)

    async def get_rmi(self, ticker: str, query_date: str = None, period: int = 20, momentum: int = 5) -> float:
        """Get current Relative Momentum Index for a specified ticker

        Args:
            ticker (str): ticker for which to calculate RMI
            query_date (Optional[str]): date to start looking back from in YYYY-MM-DD format. Defaults to None, which uses today's date.
            period (Optional[int]): RMI calculation lookback period. Defaults to 20
            momentum (Optional[int]): Stock chart bar lookback period. Defaults to 5
        Returns:
            float: calculated RMI

        """

        previous_close_prices = await self._get_previous_close_prices(ticker, period + 1, query_date)

        # subtract difference of momentum days
        momentum_changes = (
            self._shift(previous_close_prices, -momentum) - previous_close_prices
        )

        # drop nan values caused by shift
        momentum_changes = momentum_changes[~np.isnan(momentum_changes)]

        positive_changes = np.copy(momentum_changes)
        positive_changes[positive_changes < 0] = 0

        negative_changes = momentum_changes
        negative_changes[negative_changes > 0] = 0

        average_positive_gain = np.mean(positive_changes)
        average_negative_gain = np.abs(np.mean(negative_changes)) + 1e-7

        rs = average_positive_gain / average_negative_gain

        return 100 - 100 / (1 + rs)

    async def _get_previous_close_prices(
        self, ticker: str, days: int, query_date: str = None
    ) -> npt.NDArray[np.float64]:
        """Get close prices from previous days

        Args:
            ticker (str): Ticker to retreive close prices for
            days (int): number of previous close prices to retreive
            query_date (Optional[str]): date to start looking back from in YYYY-MM-DD format. Defaults to None, which uses today's date.

        Returns:
            np.ndarray: numpy array with close prices
        """
        days_to_lookback = int(days * 1.5)
        curr_date = date.today() if query_date is None else date.fromisoformat(query_date)

        async with gateway.Connection(self.api_key) as conn:
            close_tasks: List[asyncio.Task[float]] = []
            for _ in range(days_to_lookback):
                close_tasks.append(
                    asyncio.create_task(conn.get_close(ticker, curr_date))
                )
                curr_date -= timedelta(days=1)

            results = await asyncio.gather(*close_tasks, return_exceptions=True)
            prices: List[float] = []
            for result in results:
                if isinstance(result, ValueError):
                    raise result
                if not isinstance(result, LookupError):
                    prices.append(result)

        prices.reverse()
        return np.array(prices[-days:])

    def _shift(
        self, arr: npt.ArrayLike, num: int, fill_value: Optional[Any] = np.nan
    ) -> npt.NDArray[Any]:
        """Shift numpy array elements forwards or backwards

        Args:
            arr (npt.ArrayLike): array to shift
            num (int): number of places to shift the array
            fill_value (Optional[Any]): value for which to fill leftover indices
        Returns:
            np.ndarray: Shifted numpy array

        """

        arr = np.roll(arr, num)
        if num < 0:
            arr[num:] = fill_value
        elif num > 0:
            arr[:num] = fill_value
        return arr
