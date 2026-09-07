from __future__ import annotations

import numpy as np
import pandas as pd


def historical_analogue_outcomes(df: pd.DataFrame, horizon_hours: int = 4, lookback_window: int = 200) -> dict:
    frame = df.copy().sort_values("timestamp").reset_index(drop=True)
    frame["return_1"] = frame["close"].pct_change()
    frame["rolling_mean"] = frame["close"].rolling(window=48, min_periods=10).mean()
    frame["rolling_std"] = frame["close"].rolling(window=48, min_periods=10).std(ddof=1)
    frame["z_score"] = (frame["close"] - frame["rolling_mean"]) / frame["rolling_std"].replace(0, np.nan)
    frame["percentile_rank"] = frame["close"].rank(pct=True)
    frame["volatility_percentile"] = frame["return_1"].rolling(window=48, min_periods=10).std().rank(pct=True)

    current = frame.iloc[-1]
    future_returns = frame["close"].shift(-horizon_hours) / frame["close"] - 1
    frame["future_return"] = future_returns

    conditions = [
        (abs(frame["z_score"] - current["z_score"]) < 0.7),
        (abs(frame["percentile_rank"] - current["percentile_rank"]) < 0.08),
        (abs(frame["volatility_percentile"] - current["volatility_percentile"]) < 0.2),
    ]
    mask = np.logical_and.reduce(conditions)
    comparable = frame[mask].tail(lookback_window).dropna(subset=["future_return"])

    sample_size = int(len(comparable))
    if sample_size == 0:
        return {
            "pair": frame.iloc[-1].get("pair", "UNKNOWN"),
            "horizon": f"{horizon_hours}h",
            "similar_observations": 0,
            "price_higher_probability": np.nan,
            "price_lower_probability": np.nan,
            "average_future_return": np.nan,
            "median_future_return": np.nan,
            "reversion_probability": np.nan,
        }

    price_higher_probability = float((comparable["future_return"] > 0).mean())
    price_lower_probability = float((comparable["future_return"] < 0).mean())
    average_future_return = float(comparable["future_return"].mean())
    median_future_return = float(comparable["future_return"].median())
    reversion_probability = float((comparable["future_return"].abs() < 0.01).mean())

    return {
        "pair": frame.iloc[-1].get("pair", "UNKNOWN"),
        "horizon": f"{horizon_hours}h",
        "similar_observations": sample_size,
        "price_higher_probability": price_higher_probability,
        "price_lower_probability": price_lower_probability,
        "average_future_return": average_future_return,
        "median_future_return": median_future_return,
        "reversion_probability": reversion_probability,
    }
