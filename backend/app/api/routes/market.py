from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.data.cleaner import summarize_data_quality
from app.data.providers.csv_provider import CSVForexProvider

router = APIRouter()
provider = CSVForexProvider()


@router.get("/api/market/pairs")
def get_pairs():
    return {"pairs": settings.supported_pairs}


@router.get("/api/market/latest/{pair:path}")
def get_latest(pair: str):
    try:
        return provider.get_latest_price(pair)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/api/market/history/{pair:path}")
def get_history(pair: str, limit: int = 5000):
    try:
        df = provider.get_historical_prices(pair, limit=limit)
        return df.to_dict(orient="records")
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/api/market/data-quality/{pair:path}")
def get_data_quality(pair: str):
    try:
        df = provider.get_historical_prices(pair, limit=10000)
        return summarize_data_quality(df)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
