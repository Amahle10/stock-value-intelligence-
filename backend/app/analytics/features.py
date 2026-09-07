from __future__ import annotations

import numpy as np
import pandas as pd


def build_ml_features(df: pd.DataFrame, horizon_hours: int = 4) -> pd.DataFrame:
    frame = df.copy().sort_values("timestamp").reset_index(drop=True)
    frame["return_1"] = frame["close"].pct_change()
    frame["return_5"] = frame["close"].pct_change(5)
    frame["return_20"] = frame["close"].pct_change(20)
    frame["rolling_volatility"] = frame["return_1"].rolling(window=20, min_periods=5).std()
    frame["rolling_mean"] = frame["close"].rolling(window=20, min_periods=5).mean()
    frame["rolling_median"] = frame["close"].rolling(window=20, min_periods=5).median()
    frame["rolling_std"] = frame["close"].rolling(window=20, min_periods=5).std(ddof=1)
    frame["z_score"] = (frame["close"] - frame["rolling_mean"]) / frame["rolling_std"].replace(0, np.nan)
    frame["percentile_rank"] = frame["close"].rank(pct=True)
    frame["distance_from_rolling_median"] = (frame["close"] - frame["rolling_median"]) / frame["rolling_median"]
    frame["distance_from_recent_high"] = (frame["close"] - frame["close"].rolling(window=20, min_periods=5).max()) / frame["close"].rolling(window=20, min_periods=5).max()
    frame["distance_from_recent_low"] = (frame["close"] - frame["close"].rolling(window=20, min_periods=5).min()) / frame["close"].rolling(window=20, min_periods=5).min()
    frame["hour"] = frame["timestamp"].dt.hour
    frame["weekday"] = frame["timestamp"].dt.dayofweek
    frame["spread"] = (frame["ask"] - frame["bid"]).fillna(frame["close"] * 0.0001)
    frame["future_return"] = (frame["close"].shift(-horizon_hours) / frame["close"]) - 1
    frame["target"] = (frame["future_return"] > 0).astype(int)

    features = frame[
        [
            "return_1",
            "return_5",
            "return_20",
            "rolling_volatility",
            "z_score",
            "percentile_rank",
            "distance_from_rolling_median",
            "distance_from_recent_high",
            "distance_from_recent_low",
            "hour",
            "weekday",
            "spread",
            "target",
        ]
    ].dropna().reset_index(drop=True)
    return features
