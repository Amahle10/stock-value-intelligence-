import pandas as pd

from app.analytics.time_analysis import build_hour_day_heatmap


def test_heatmap_builds():
    df = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=100, freq="H", tz="UTC"),
        "pair": ["EUR/USD"] * 100,
        "close": [1.10 + i * 0.0001 for i in range(100)],
        "open": [1.10 + i * 0.0001 for i in range(100)],
        "high": [1.11 + i * 0.0001 for i in range(100)],
        "low": [1.09 + i * 0.0001 for i in range(100)],
        "bid": [1.10 + i * 0.0001 for i in range(100)],
        "ask": [1.11 + i * 0.0001 for i in range(100)],
    })
    heatmap = build_hour_day_heatmap(df, metric="average_return")
    assert heatmap.shape[0] > 0
    assert heatmap.shape[1] > 0
