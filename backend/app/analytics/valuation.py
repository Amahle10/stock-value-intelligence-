from __future__ import annotations

import numpy as np
import pandas as pd


def compute_valuation_metrics(df: pd.DataFrame, window: int = 48, z_threshold: float = 2.0) -> dict:
    frame = df.copy().sort_values("timestamp").reset_index(drop=True)
    close = frame["close"]
    rolling_mean = close.rolling(window=window, min_periods=10).mean()
    rolling_median = close.rolling(window=window, min_periods=10).median()
    rolling_std = close.rolling(window=window, min_periods=10).std(ddof=1)
    z_score = (close - rolling_mean) / rolling_std.replace(0, np.nan)
    percentile_rank = close.rank(pct=True)
    recent_high = close.rolling(window=window, min_periods=10).max()
    recent_low = close.rolling(window=window, min_periods=10).min()

    latest = frame.iloc[-1]
    latest_mean = float(rolling_mean.iloc[-1])
    latest_median = float(rolling_median.iloc[-1])
    latest_std = float(rolling_std.iloc[-1])
    latest_z = float(z_score.iloc[-1])
    latest_percentile = float(percentile_rank.iloc[-1])

    price_regime_score = np.clip((latest_z / z_threshold) * 100, -100, 100) if np.isfinite(latest_z) else 0.0
    if latest_z >= z_threshold:
        regime = "STATISTICALLY EXPENSIVE"
    elif latest_z <= -z_threshold:
        regime = "STATISTICALLY CHEAP"
    else:
        regime = "NEUTRAL"

    return {
        "pair": latest.get("pair", "UNKNOWN"),
        "latest_close": float(latest["close"]),
        "rolling_mean": latest_mean,
        "rolling_median": latest_median,
        "rolling_std": latest_std,
        "z_score": latest_z,
        "percentile_rank": latest_percentile,
        "distance_from_rolling_median": float(latest["close"] - latest_median),
        "distance_from_recent_high": float(latest["close"] - recent_high.iloc[-1]),
        "distance_from_recent_low": float(latest["close"] - recent_low.iloc[-1]),
        "regime_score": float(price_regime_score),
        "regime_label": regime,
        "recent_high": float(recent_high.iloc[-1]),
        "recent_low": float(recent_low.iloc[-1]),
        "threshold": z_threshold,
    }
