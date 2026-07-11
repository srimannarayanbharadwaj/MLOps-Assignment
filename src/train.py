"""Train and compare Heart Disease classification models."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.model_selection import train_test_split

from src.modeling import get_candidate_models


DATA_PATH = Path("data/processed/heart_cleveland_clean.csv")
METRICS_PATH = Path("report/generated/model_cv_metrics.csv")
SUMMARY_PATH = Path("report/generated/model_selection_summary.md")
ARTIFACT_DIR = Path("report/generated/mlflow_artifacts")
MLFLOW_EXPERIMENT_NAME = "heart-disease-classification"
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


def save_confusion_matrix(
    model_name: str,
    fitted_pipeline,
    features_test: pd.DataFrame,
    target_test: pd.Series,
) -> Path:
    """Save a holdout confusion matrix plot for an MLflow artifact."""
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = ARTIFACT_DIR / f"{model_name}_confusion_matrix.png"
    predictions = fitted_pipeline.predict(features_test)

    display = ConfusionMatrixDisplay.from_predictions(
        target_test,
        predictions,
        display_labels=["No disease", "Disease"],
        cmap="Blues",
        colorbar=False,
    )
    display.ax_.set_title(f"{model_name.replace('_', ' ').title()} Confusion")
    plt.tight_layout()
    plt.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close()
    return output_path


def log_model_runs(
    metrics: pd.DataFrame,
    features: pd.DataFrame,
    target: pd.Series,
) -> None:
    """Log candidate model runs, metrics, and artifacts to MLflow."""
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
    split_data = train_test_split(
        features,
        target,
        test_size=0.2,
        stratify=target,
        random_state=42,
    )
    train_features, test_features, train_target, test_target = split_data
    metrics_by_model = metrics.set_index("model").to_dict(orient="index")

    for model_name, pipeline in get_candidate_models().items():
        pipeline.fit(train_features, train_target)
        row = metrics_by_model[model_name]
        model_step = pipeline.named_steps["model"]
        confusion_path = save_confusion_matrix(
            model_name,
            pipeline,
            test_features,
            test_target,
        )

        with mlflow.start_run(run_name=model_name):
            mlflow.log_param("model_type", model_step.__class__.__name__)
            for param_name, param_value in model_step.get_params().items():
                mlflow.log_param(param_name, param_value)

            for metric_name, metric_value in row.items():
                mlflow.log_metric(metric_name, float(metric_value))

            mlflow.log_artifact(str(METRICS_PATH))
            mlflow.log_artifact(str(SUMMARY_PATH))
            mlflow.log_artifact(str(confusion_path))
            mlflow.sklearn.log_model(
                sk_model=pipeline,
                name="model",
            )


def main() -> None:
    """Run model comparison and MLflow tracking."""
    features, target = load_features_and_target()
    metrics = evaluate_models(features, target)
    save_outputs(metrics)
    log_model_runs(metrics, features, target)

    print(metrics.round(4).to_string(index=False))
    print(f"Saved metrics to {METRICS_PATH}")
    print(f"Saved summary to {SUMMARY_PATH}")
    print("Logged MLflow runs for all candidate models.")


if __name__ == "__main__":
    main()
