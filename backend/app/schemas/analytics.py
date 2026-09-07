from typing import Any, Dict, Optional

from pydantic import BaseModel


class SummaryResponse(BaseModel):
    pair: str
    latest_close: float
    rolling_mean: Optional[float] = None
    rolling_median: Optional[float] = None
    z_score: Optional[float] = None
    percentile_rank: Optional[float] = None
    regime_score: Optional[float] = None
    model_probability: Optional[float] = None


class ModelMetrics(BaseModel):
    pair: str
    horizon: str
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1: Optional[float] = None
    roc_auc: Optional[float] = None
    naive_baseline: Optional[float] = None
    beats_baseline: Optional[bool] = None
    confusion_matrix: Optional[Dict[str, Any]] = None
