from __future__ import annotations

from app.analytics.features import build_ml_features


def predict_probability(model, df, horizon_hours: int = 4):
    features = build_ml_features(df, horizon_hours=horizon_hours).drop(columns=["target"])
    if features.empty:
        return 0.5
    latest = features.iloc[-1]
    prob = model.predict_proba(latest.to_frame().T)[0, 1]
    return float(prob)
