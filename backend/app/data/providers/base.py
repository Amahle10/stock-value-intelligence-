from abc import ABC, abstractmethod


class ForexDataProvider(ABC):
    @abstractmethod
    def get_latest_price(self, pair: str):
        raise NotImplementedError

    @abstractmethod
    def get_historical_prices(self, pair: str, limit: int = 5000, start=None, end=None):
        raise NotImplementedError

    @abstractmethod
    def get_bid_ask(self, pair: str):
        raise NotImplementedError
