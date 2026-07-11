"""Package the selected Heart Disease model for reuse."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd

from src.data_processing import CATEGORICAL_FEATURES, NUMERIC_FEATURES
from src.modeling import get_candidate_models
from src.train import DATA_PATH, METRICS_PATH, load_features_and_target


MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / "heart_disease_pipeline.joblib"
METADATA_PATH = MODEL_DIR / "model_metadata.json"
SAMPLE_INPUT_PATH = MODEL_DIR / "sample_input.json"


def select_model_name(metrics_path: Path = METRICS_PATH) -> str:
    """Select the best model based on saved CV metrics."""
    if not metrics_path.exists():
        return "logistic_regression"

    metrics = pd.read_csv(metrics_path)
    best_row = metrics.sort_values(
        by=["roc_auc_mean", "recall_mean"],
        ascending=False,
    ).iloc[0]
    return str(best_row["model"])


def build_metadata(
    model_name: str,
    features: pd.DataFrame,
    target: pd.Series,
) -> dict:
    """Build metadata describing the packaged model artifact."""
    metadata = {
        "model_name": model_name,
        "artifact_path": str(MODEL_PATH),
        "training_rows": int(features.shape[0]),
        "feature_count": int(features.shape[1]),
        "target_distribution": target.value_counts().sort_index().to_dict(),
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "metrics_file": str(METRICS_PATH),
    }

    if METRICS_PATH.exists():
        metrics = pd.read_csv(METRICS_PATH)
        selected = metrics[metrics["model"] == model_name].iloc[0].to_dict()
        metadata["cross_validation_metrics"] = selected

    return metadata


def save_sample_input(features: pd.DataFrame) -> dict:
    """Save one valid API-style sample input row."""
    sample = json.loads(features.head(1).to_json(orient="records"))[0]
    SAMPLE_INPUT_PATH.write_text(
        json.dumps(sample, indent=2),
        encoding="utf-8",
    )
    return sample


def package_selected_model() -> Path:
    """Train the selected pipeline on all clean data and save it."""
    features, target = load_features_and_target(DATA_PATH)
    model_name = select_model_name()
    candidate_models = get_candidate_models()
    pipeline = candidate_models[model_name]

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    pipeline.fit(features, target)
    joblib.dump(pipeline, MODEL_PATH)

    save_sample_input(features)
    metadata = build_metadata(model_name, features, target)
    METADATA_PATH.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )
    return MODEL_PATH


def main() -> None:
    """CLI entrypoint for Phase 4 packaging."""
    model_path = package_selected_model()
    print(f"Packaged model saved to {model_path}")
    print(f"Metadata saved to {METADATA_PATH}")
    print(f"Sample input saved to {SAMPLE_INPUT_PATH}")


if __name__ == "__main__":
    main()
