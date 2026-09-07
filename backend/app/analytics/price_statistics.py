from __future__ import annotations

import numpy as np
import pandas as pd


def compute_returns(df: pd.DataFrame) -> pd.DataFrame:
    frame = df.copy()
    frame["previous_close"] = frame["close"].shift(1)
    frame["return_1"] = frame["close"].pct_change()
    frame["log_return_1"] = np.log(frame["close"] / frame["previous_close"])
    return frame


def summarize_directional_pressure(df: pd.DataFrame) -> pd.DataFrame:
    frame = compute_returns(df)
    frame["upward_pressure"] = (frame["close"] > frame["previous_close"]).astype(int)
    frame["downward_pressure"] = (frame["close"] < frame["previous_close"]).astype(int)
    frame["hour"] = frame["timestamp"].dt.hour
    frame["weekday"] = frame["timestamp"].dt.dayofweek
    return frame.groupby(["hour", "weekday"], as_index=False).agg(
        upward_intervals=("upward_pressure", "sum"),
        downward_intervals=("downward_pressure", "sum"),
        avg_up_return=("return_1", lambda s: s[s > 0].mean() if (s > 0).any() else np.nan),
        avg_down_return=("return_1", lambda s: s[s < 0].mean() if (s < 0).any() else np.nan),
        median_return=("return_1", "median"),
        volatility=("return_1", lambda s: s.std(ddof=1) if len(s) > 1 else np.nan),
        sample_size=("return_1", "size"),
    )
