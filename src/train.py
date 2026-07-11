"""Train and compare Heart Disease classification models."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate

from src.modeling import get_candidate_models


DATA_PATH = Path("data/processed/heart_cleveland_clean.csv")
METRICS_PATH = Path("report/generated/model_cv_metrics.csv")
SUMMARY_PATH = Path("report/generated/model_selection_summary.md")
TARGET_COLUMN = "target"
SCORING = {
    "accuracy": "accuracy",
    "precision": "precision",
    "recall": "recall",
    "roc_auc": "roc_auc",
}


def load_features_and_target(
    data_path: Path = DATA_PATH,
) -> tuple[pd.DataFrame, pd.Series]:
    """Load model features and the binary target."""
    data = pd.read_csv(data_path)
    features = data.drop(columns=[TARGET_COLUMN])
    target = data[TARGET_COLUMN]
    return features, target


def evaluate_models(
    features: pd.DataFrame,
    target: pd.Series,
) -> pd.DataFrame:
    """Evaluate candidate models with stratified cross-validation."""
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    rows = []

    for model_name, pipeline in get_candidate_models().items():
        scores = cross_validate(
            pipeline,
            features,
            target,
            cv=cv,
            scoring=SCORING,
            n_jobs=None,
        )

        row = {"model": model_name}
        for metric in SCORING:
            values = scores[f"test_{metric}"]
            row[f"{metric}_mean"] = values.mean()
            row[f"{metric}_std"] = values.std()
        rows.append(row)

    return pd.DataFrame(rows).sort_values(
        by=["roc_auc_mean", "recall_mean"],
        ascending=False,
    )


def build_selection_summary(metrics: pd.DataFrame) -> str:
    """Create a short model-selection note for the report."""
    best = metrics.iloc[0]
    model_label = best["model"].replace("_", " ").title()
    return (
        "# Phase 2 Model Selection Summary\n\n"
        f"The best cross-validation performer is **{model_label}**. "
        "Selection is based primarily on ROC-AUC, with recall used as a "
        "secondary clinical-risk metric because missing a likely heart "
        "disease case can be more serious than a false positive screening "
        "flag.\n\n"
        "Use this as a starting point and rewrite the final report "
        "explanation in your own words after reviewing the metric table.\n"
    )


def save_outputs(metrics: pd.DataFrame) -> None:
    """Persist Phase 2 metrics and selection notes."""
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(METRICS_PATH, index=False)
    SUMMARY_PATH.write_text(
        build_selection_summary(metrics),
        encoding="utf-8",
    )


def main() -> None:
    """Run Phase 2 model comparison."""
    features, target = load_features_and_target()
    metrics = evaluate_models(features, target)
    save_outputs(metrics)

    print(metrics.round(4).to_string(index=False))
    print(f"Saved metrics to {METRICS_PATH}")
    print(f"Saved summary to {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
