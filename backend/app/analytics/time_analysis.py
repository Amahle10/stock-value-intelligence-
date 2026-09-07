from __future__ import annotations

import pandas as pd


def build_hour_day_heatmap(df: pd.DataFrame, metric: str = "average_return") -> pd.DataFrame:
    frame = df.copy()
    frame["hour"] = frame["timestamp"].dt.hour
    frame["weekday"] = frame["timestamp"].dt.dayofweek
    frame["return_1"] = frame["close"].pct_change()
    frame["upward_pressure"] = (frame["close"] > frame["close"].shift(1)).astype(int)
    frame["downward_pressure"] = (frame["close"] < frame["close"].shift(1)).astype(int)

    if metric == "average_return":
        aggregated = frame.groupby(["hour", "weekday"], as_index=False)["return_1"].mean()
    elif metric == "upward_probability":
        aggregated = frame.groupby(["hour", "weekday"], as_index=False)["upward_pressure"].mean()
    elif metric == "downward_probability":
        aggregated = frame.groupby(["hour", "weekday"], as_index=False)["downward_pressure"].mean()
    else:
        aggregated = frame.groupby(["hour", "weekday"], as_index=False)["return_1"].std()

    value_column = aggregated.columns[-1]
    heatmap = aggregated.pivot(index="hour", columns="weekday", values=value_column)
    heatmap = heatmap.reindex(index=range(24), columns=range(7), fill_value=float("nan"))
    heatmap.columns = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return heatmap
