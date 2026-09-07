import pandas as pd

from app.analytics.price_statistics import compute_returns


def test_returns_are_computed():
    df = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=4, freq="H", tz="UTC"),
        "pair": ["EUR/USD"] * 4,
        "open": [1.0, 1.01, 1.02, 1.01],
        "high": [1.02, 1.03, 1.04, 1.03],
        "low": [0.99, 1.0, 1.01, 1.0],
        "close": [1.0, 1.01, 1.02, 1.01],
        "bid": [1.0, 1.01, 1.02, 1.01],
        "ask": [1.01, 1.02, 1.03, 1.02],
        "volume": [100, 100, 100, 100],
    })
    result = compute_returns(df)
    assert "return_1" in result.columns
    assert "log_return_1" in result.columns
    assert result["return_1"].iloc[1] > 0
