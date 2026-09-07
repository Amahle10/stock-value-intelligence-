from typing import Optional

from pydantic import BaseModel


class MarketRecord(BaseModel):
    timestamp: str
    pair: str
    open: float
    high: float
    low: float
    close: float
    bid: Optional[float] = None
    ask: Optional[float] = None
    volume: Optional[float] = None


class LatestPrice(BaseModel):
    pair: str
    timestamp: str
    price: float
    bid: Optional[float] = None
    ask: Optional[float] = None
    spread: Optional[float] = None
