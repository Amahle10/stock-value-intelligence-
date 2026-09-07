import pandas as pd

from app.analytics.valuation import compute_valuation_metrics


def test_valuation_metrics_are_generated():
    df = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=60, freq="H", tz="UTC"),
        "pair": ["EUR/USD"] * 60,
        "close": [1.10 + i * 0.001 for i in range(60)],
        "open": [1.10 + i * 0.001 for i in range(60)],
        "high": [1.11 + i * 0.001 for i in range(60)],
        "low": [1.09 + i * 0.001 for i in range(60)],
        "bid": [1.10 + i * 0.001 for i in range(60)],
        "ask": [1.11 + i * 0.001 for i in range(60)],
    })
    metrics = compute_valuation_metrics(df, window=20)
    assert "z_score" in metrics
    assert "regime_label" in metrics
