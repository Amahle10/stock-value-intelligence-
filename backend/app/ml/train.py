from __future__ import annotations

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score

from app.analytics.features import build_ml_features


def train_logistic_model(df, horizon_hours: int = 4):
    features = build_ml_features(df, horizon_hours=horizon_hours)
    if len(features) < 50:
        raise ValueError("Not enough data to train the model.")

    split_idx = int(len(features) * 0.7)
    valid_split = int(len(features) * 0.85)

    train = features.iloc[:split_idx]
    test = features.iloc[valid_split:]

    X_train = train.drop(columns=["target"])
    y_train = train["target"]
    X_test = test.drop(columns=["target"])
    y_test = test["target"]

    model = LogisticRegression(max_iter=2000, class_weight="balanced")
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    proba = model.predict_proba(X_test)[:, 1]

    naive_baseline = float(np.bincount(y_test.astype(int)).argmax() / len(y_test))
    metrics = {
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision": float(precision_score(y_test, pred, zero_division=0)),
        "recall": float(recall_score(y_test, pred, zero_division=0)),
        "f1": float(f1_score(y_test, pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, proba)),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
        "naive_baseline": naive_baseline,
        "beats_baseline": accuracy_score(y_test, pred) > naive_baseline,
    }
    return {"model": model, "metrics": metrics, "features": features}
