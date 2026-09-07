import pandas as pd

from app.data.cleaner import clean_market_data, summarize_data_quality


def test_clean_market_data_handles_bad_rows():
    df = pd.DataFrame([
        {"timestamp": "2024-01-01T00:00:00Z", "pair": "EUR/USD", "open": 1.10, "high": 1.11, "low": 1.09, "close": 1.10, "bid": 1.099, "ask": 1.101, "volume": 200},
        {"timestamp": "2024-01-01T00:00:00Z", "pair": "EUR/USD", "open": 1.10, "high": 1.11, "low": 1.09, "close": 1.10, "bid": 1.099, "ask": 1.101, "volume": 200},
        {"timestamp": "bad-date", "pair": "EUR/USD", "open": 1.12, "high": 1.13, "low": 1.11, "close": 1.12, "bid": 1.119, "ask": 1.121, "volume": 100},
        {"timestamp": "2024-01-02T00:00:00Z", "pair": "EUR/USD", "open": 0, "high": 1.0, "low": 0.9, "close": 0.95, "bid": 1.0, "ask": 1.1, "volume": 50},
    ])
    cleaned = clean_market_data(df, pair="EUR/USD")
    assert len(cleaned) >= 1
    assert "outlier_flag" in cleaned.columns
    summary = summarize_data_quality(cleaned)
    assert "rows" in summary


def test_clean_market_data_keeps_relevant_fields():
    df = pd.DataFrame([{"timestamp": "2024-01-01T00:00:00Z", "pair": "EUR/USD", "open": 1.1, "high": 1.12, "low": 1.08, "close": 1.11, "bid": 1.109, "ask": 1.111, "volume": 100}])
    cleaned = clean_market_data(df, pair="EUR/USD")
    assert {"timestamp", "pair", "open", "high", "low", "close"}.issubset(cleaned.columns)
