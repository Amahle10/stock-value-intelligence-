from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.analytics.price_statistics import compute_returns
from app.analytics.reversals import historical_analogue_outcomes
from app.analytics.time_analysis import build_hour_day_heatmap
from app.analytics.valuation import compute_valuation_metrics
from app.data.providers.csv_provider import CSVForexProvider

router = APIRouter()
provider = CSVForexProvider()


@router.get("/api/analytics/summary/{pair:path}")
def summary(pair: str):
    try:
        df = provider.get_historical_prices(pair, limit=5000)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    processed = compute_returns(df)
    stats = compute_valuation_metrics(processed, window=48)
    return {
        "pair": pair,
        "latest_close": stats["latest_close"],
        "rolling_mean": stats["rolling_mean"],
        "rolling_median": stats["rolling_median"],
        "z_score": stats["z_score"],
        "percentile_rank": stats["percentile_rank"],
        "regime_score": stats["regime_score"],
        "regime_label": stats["regime_label"],
    }


@router.get("/api/analytics/time/{pair:path}")
def time_analysis(pair: str, metric: str = "average_return"):
    df = provider.get_historical_prices(pair, limit=5000)
    return build_hour_day_heatmap(df, metric=metric).to_dict()


@router.get("/api/analytics/valuation/{pair:path}")
def valuation(pair: str):
    df = provider.get_historical_prices(pair, limit=5000)
    return compute_valuation_metrics(df, window=48)


@router.get("/api/analytics/reversal/{pair:path}")
def reversal(pair: str, horizon: str = "4h"):
    df = provider.get_historical_prices(pair, limit=5000)
    horizon_map = {"1h": 1, "4h": 4, "1d": 24, "1w": 168}
    horizon_hours = horizon_map.get(horizon, 4)
    return historical_analogue_outcomes(df, horizon_hours=horizon_hours)


@router.get("/api/analytics/distribution/{pair:path}")
def distribution(pair: str):
    df = provider.get_historical_prices(pair, limit=5000)
    returns = compute_returns(df)["return_1"].dropna()
    return {
        "mean": float(returns.mean()),
        "median": float(returns.median()),
        "std": float(returns.std(ddof=1)),
        "p10": float(returns.quantile(0.10)),
        "p25": float(returns.quantile(0.25)),
        "p50": float(returns.quantile(0.50)),
        "p75": float(returns.quantile(0.75)),
        "p90": float(returns.quantile(0.90)),
    }
