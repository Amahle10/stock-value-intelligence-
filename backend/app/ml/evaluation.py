from __future__ import annotations

from sklearn.metrics import confusion_matrix


def calculate_confusion_matrix(y_true, y_pred):
    return confusion_matrix(y_true, y_pred).tolist()
