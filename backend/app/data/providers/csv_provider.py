from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.core.config import settings
from app.data.cleaner import clean_market_data
from app.data.providers.base import ForexDataProvider


class CSVForexProvider(ForexDataProvider):
    def __init__(self, data_dir: str | None = None) -> None:
        self.data_dir = Path(data_dir or settings.csv_data_dir)

    def _file_for_pair(self, pair: str) -> Path:
        normalized = pair.replace("/", "_") + ".csv"
        return self.data_dir / normalized

    def _load_frame(self, pair: str) -> pd.DataFrame:
        file_path = self._file_for_pair(pair)
        if not file_path.exists():
            raise FileNotFoundError(f"No sample CSV found for {pair} at {file_path}")
        df = pd.read_csv(file_path)
        return clean_market_data(df, pair=pair)

    def get_latest_price(self, pair: str):
        df = self._load_frame(pair)
        row = df.iloc[-1].to_dict()
        return {
            "pair": pair,
            "timestamp": row["timestamp"].isoformat(),
            "price": float(row["close"]),
            "bid": float(row["bid"]) if pd.notna(row["bid"]) else None,
            "ask": float(row["ask"]) if pd.notna(row["ask"]) else None,
            "spread": float((row["ask"] - row["bid"])) if pd.notna(row["ask"]) and pd.notna(row["bid"]) else None,
        }

    def get_historical_prices(self, pair: str, limit: int = 5000, start=None, end=None):
        df = self._load_frame(pair)
        if limit:
            df = df.tail(limit)
        if start:
            df = df[df["timestamp"] >= pd.Timestamp(start)]
        if end:
            df = df[df["timestamp"] <= pd.Timestamp(end)]
        return df

    def get_bid_ask(self, pair: str):
        df = self._load_frame(pair)
        last = df.iloc[-1].to_dict()
        return {
            "pair": pair,
            "bid": float(last["bid"]) if pd.notna(last["bid"]) else None,
            "ask": float(last["ask"]) if pd.notna(last["ask"]) else None,
            "spread": float(last["ask"] - last["bid"]) if pd.notna(last["bid"]) and pd.notna(last["ask"]) else None,
        }
