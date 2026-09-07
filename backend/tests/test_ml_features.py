import pandas as pd

from app.analytics.features import build_ml_features


def test_ml_features_are_built():
    df = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=80, freq="H", tz="UTC"),
        "pair": ["EUR/USD"] * 80,
        "close": [1.10 + i * 0.0005 for i in range(80)],
        "open": [1.10 + i * 0.0005 for i in range(80)],
        "high": [1.11 + i * 0.0005 for i in range(80)],
        "low": [1.09 + i * 0.0005 for i in range(80)],
        "bid": [1.10 + i * 0.0005 for i in range(80)],
        "ask": [1.11 + i * 0.0005 for i in range(80)],
    })
    features = build_ml_features(df, horizon_hours=4)
    assert "target" in features.columns
    assert features.shape[0] > 0
