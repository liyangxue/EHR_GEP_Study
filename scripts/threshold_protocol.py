"""Leakage-safe model-selection and post hoc threshold utilities.

The held-out testing set must never be passed to any function that selects an
epoch, model, hyperparameter, or threshold. Threshold pairs are selected from
training-set predictions and are then applied unchanged to testing predictions.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import product
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split


@dataclass(frozen=True)
class ThresholdResult:
    threshold_ngep: float
    threshold_gep: float
    accuracy: float
    delta_fpr: float
    delta_tpr: float
    fpr_ngep: float
    fpr_gep: float
    tpr_ngep: float
    tpr_gep: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def make_internal_selection_split(
    frame: pd.DataFrame,
    label_column: str,
    group_column: str = "GEP",
    selection_fraction: float = 0.15,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split only the official training data for epoch/configuration selection.

    The joint outcome/group key is preferred so both labels and both patient
    groups remain represented. If a joint stratum is too small, the function
    falls back to outcome-only stratification.
    """

    required = {label_column, group_column}
    missing = required.difference(frame.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")

    joint = (
        frame[label_column].astype(int).astype(str)
        + "_"
        + frame[group_column].astype(int).astype(str)
    )
    stratify = joint if joint.value_counts().min() >= 2 else frame[label_column]

    model_train, selection = train_test_split(
        frame,
        test_size=selection_fraction,
        random_state=random_state,
        stratify=stratify,
    )
    return model_train.reset_index(drop=True), selection.reset_index(drop=True)


def _rate_components(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float]:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    fpr = fp / (fp + tn) if fp + tn else 0.0
    tpr = tp / (tp + fn) if tp + fn else 0.0
    return float(fpr), float(tpr)


def apply_group_thresholds(
    probabilities: Iterable[float],
    groups: Iterable[int],
    threshold_ngep: float,
    threshold_gep: float,
) -> np.ndarray:
    probabilities = np.asarray(probabilities, dtype=float)
    groups = np.asarray(groups, dtype=int)
    if probabilities.shape != groups.shape:
        raise ValueError("probabilities and groups must have the same shape")
    if not np.isin(groups, [0, 1]).all():
        raise ValueError("groups must contain only 0 (NGEP) and 1 (GEP)")
    thresholds = np.where(groups == 1, threshold_gep, threshold_ngep)
    return (probabilities >= thresholds).astype(int)


def evaluate_threshold_pair(
    labels: Iterable[int],
    probabilities: Iterable[float],
    groups: Iterable[int],
    threshold_ngep: float,
    threshold_gep: float,
) -> ThresholdResult:
    labels = np.asarray(labels, dtype=int)
    probabilities = np.asarray(probabilities, dtype=float)
    groups = np.asarray(groups, dtype=int)
    if not (labels.shape == probabilities.shape == groups.shape):
        raise ValueError("labels, probabilities, and groups must have the same shape")

    predictions = apply_group_thresholds(
        probabilities, groups, threshold_ngep, threshold_gep
    )
    group_rates: dict[int, tuple[float, float]] = {}
    for group in (0, 1):
        mask = groups == group
        if not mask.any():
            raise ValueError(f"No observations found for group {group}")
        group_rates[group] = _rate_components(labels[mask], predictions[mask])

    fpr_ngep, tpr_ngep = group_rates[0]
    fpr_gep, tpr_gep = group_rates[1]
    return ThresholdResult(
        threshold_ngep=float(threshold_ngep),
        threshold_gep=float(threshold_gep),
        accuracy=float(accuracy_score(labels, predictions)),
        delta_fpr=abs(fpr_ngep - fpr_gep),
        delta_tpr=abs(tpr_ngep - tpr_gep),
        fpr_ngep=fpr_ngep,
        fpr_gep=fpr_gep,
        tpr_ngep=tpr_ngep,
        tpr_gep=tpr_gep,
    )


def select_threshold_pairs(
    training_labels: Iterable[int],
    training_probabilities: Iterable[float],
    training_groups: Iterable[int],
    threshold_grid: Iterable[float] | None = None,
    max_fpr_gap: float = 0.07,
) -> dict[str, ThresholdResult]:
    """Select baseline, best-accuracy, and best-fair pairs on training only.

    Best accuracy maximizes overall training accuracy. Best fair maximizes
    accuracy among pairs satisfying the prespecified Delta-FPR constraint; if
    none satisfy it, the pair with the smallest Delta-FPR is used. Deterministic
    tie breakers prefer smaller Delta-TPR and thresholds closer to 0.5.
    """

    if threshold_grid is None:
        threshold_grid = np.round(np.arange(0.05, 0.951, 0.01), 2)
    grid = [float(value) for value in threshold_grid]
    if not grid:
        raise ValueError("threshold_grid cannot be empty")
    if not 0 <= max_fpr_gap <= 1:
        raise ValueError("max_fpr_gap must be between 0 and 1")

    labels = np.asarray(training_labels, dtype=int)
    probabilities = np.asarray(training_probabilities, dtype=float)
    groups = np.asarray(training_groups, dtype=int)

    candidates = [
        evaluate_threshold_pair(labels, probabilities, groups, t0, t1)
        for t0, t1 in product(grid, repeat=2)
    ]
    baseline = evaluate_threshold_pair(labels, probabilities, groups, 0.5, 0.5)

    def accuracy_key(item: ThresholdResult) -> tuple[float, float, float, float]:
        return (
            item.accuracy,
            -item.delta_fpr,
            -item.delta_tpr,
            -(abs(item.threshold_ngep - 0.5) + abs(item.threshold_gep - 0.5)),
        )

    best_accuracy = max(candidates, key=accuracy_key)
    feasible = [item for item in candidates if item.delta_fpr <= max_fpr_gap]
    if feasible:
        best_fair = max(feasible, key=accuracy_key)
    else:
        best_fair = min(
            candidates,
            key=lambda item: (
                item.delta_fpr,
                -item.accuracy,
                item.delta_tpr,
                abs(item.threshold_ngep - 0.5) + abs(item.threshold_gep - 0.5),
            ),
        )

    return {
        "baseline": baseline,
        "best_accuracy": best_accuracy,
        "best_fair": best_fair,
    }


def evaluate_frozen_thresholds(
    testing_labels: Iterable[int],
    testing_probabilities: Iterable[float],
    testing_groups: Iterable[int],
    selected_on_training: dict[str, ThresholdResult],
) -> dict[str, ThresholdResult]:
    """Apply already selected threshold pairs to held-out testing predictions."""

    return {
        name: evaluate_threshold_pair(
            testing_labels,
            testing_probabilities,
            testing_groups,
            result.threshold_ngep,
            result.threshold_gep,
        )
        for name, result in selected_on_training.items()
    }
