from __future__ import annotations

import numpy as np
import pandas as pd


def normalize_pair(pair: str) -> str:
    if not pair:
        return pair
    return pair.upper().replace(" ", "").replace("_", "/")


def clean_market_data(df: pd.DataFrame, pair: str | None = None) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    frame = df.copy()
    frame["pair"] = normalize_pair(pair or frame.get("pair", "").iloc[0] if "pair" in frame.columns else "")
    frame = frame.drop_duplicates(subset=["timestamp", "pair"], keep="last")
    frame["timestamp"] = pd.to_datetime(frame.get("timestamp", pd.Series(dtype="datetime64[ns]")), errors="coerce", utc=True)
    frame = frame.dropna(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)

    numeric_columns = ["open", "high", "low", "close", "bid", "ask", "volume"]
    for col in numeric_columns:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce")

    frame["missing_rows"] = frame.isna().any(axis=1)
    frame["invalid_ohlc"] = ~((frame["high"] >= frame["low"]) & (frame["high"] >= frame["open"]) & (frame["high"] >= frame["close"]) & (frame["low"] <= frame["open"]) & (frame["low"] <= frame["close"]))
    frame["impossible_price"] = (frame[["open", "high", "low", "close"]] <= 0).any(axis=1)
    frame["bid_ask_sanity"] = False
    if {"bid", "ask"}.issubset(frame.columns):
        frame["bid_ask_sanity"] = ((frame["ask"] >= frame["bid"]) & (frame["bid"] > 0) & (frame["ask"] > 0)).fillna(False)
    frame["outlier_flag"] = False
    if "close" in frame.columns:
        median_price = frame["close"].median()
        mad = (frame["close"] - median_price).abs().median()
        threshold = 12 * mad if mad else np.nan
        frame["outlier_flag"] = (frame["close"] - median_price).abs() > threshold

    frame = frame[~frame["impossible_price"]].copy()
    frame = frame[~frame["invalid_ohlc"]].copy()

    return frame.reset_index(drop=True)


def summarize_data_quality(df: pd.DataFrame) -> dict:
    total_rows = int(len(df))
    missing_rows = int(df.isna().sum().sum())
    duplicates = int(df.duplicated(subset=["timestamp", "pair"]).sum())
    outliers_flagged = int(df.get("outlier_flag", pd.Series([False] * len(df))).sum())
    return {"rows": total_rows, "missing_rows": missing_rows, "duplicates": duplicates, "outliers_flagged": outliers_flagged}
