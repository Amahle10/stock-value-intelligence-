from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.data.providers.csv_provider import CSVForexProvider
from app.ml.predict import predict_probability
from app.ml.train import train_logistic_model

router = APIRouter()
provider = CSVForexProvider()
MODEL_CACHE = {}


@router.get("/api/models/status/{pair}")
def model_status(pair: str):
    return {"pair": pair, "trained": pair in MODEL_CACHE, "model_type": "LogisticRegression"}


@router.get("/api/models/prediction/{pair}")
def prediction(pair: str):
    try:
        df = provider.get_historical_prices(pair, limit=5000)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if pair not in MODEL_CACHE:
        return {"pair": pair, "model_estimated_probability": 0.5, "message": "Model not trained yet; using neutral baseline."}
    model = MODEL_CACHE[pair]["model"]
    probability = predict_probability(model, df, horizon_hours=4)
    return {"pair": pair, "model_estimated_probability": probability, "horizon": "4h"}


@router.post("/api/models/train/{pair}")
def train(pair: str):
    try:
        df = provider.get_historical_prices(pair, limit=5000)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    data = train_logistic_model(df, horizon_hours=4)
    MODEL_CACHE[pair] = data
    return {"pair": pair, "metrics": data["metrics"], "status": "trained"}
