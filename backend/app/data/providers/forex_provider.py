from typing import Any, Dict

import requests

from app.core.config import settings
from app.data.providers.base import ForexDataProvider


class ExternalForexProvider(ForexDataProvider):
    def __init__(self, base_url: str | None = None, api_key: str | None = None, timeout: int = 15) -> None:
        self.base_url = base_url or settings.api_url
        self.api_key = api_key or settings.api_key
        self.timeout = timeout

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def get_latest_price(self, pair: str):
        if not self.base_url:
            raise RuntimeError("External forex API is not configured.")
        response = requests.get(f"{self.base_url}/latest/{pair}", headers=self._get_headers(), timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_historical_prices(self, pair: str, limit: int = 5000, start=None, end=None):
        if not self.base_url:
            raise RuntimeError("External forex API is not configured.")
        params = {"pair": pair, "limit": limit}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        response = requests.get(f"{self.base_url}/history/{pair}", headers=self._get_headers(), params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_bid_ask(self, pair: str):
        if not self.base_url:
            raise RuntimeError("External forex API is not configured.")
        response = requests.get(f"{self.base_url}/quote/{pair}", headers=self._get_headers(), timeout=self.timeout)
        response.raise_for_status()
        return response.json()
