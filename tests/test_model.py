"""Tests for model prediction behavior."""

import pandas as pd

from src.modeling import build_logistic_regression_pipeline
from src.train import load_features_and_target


def test_model_predicts_binary_labels_with_valid_probabilities() -> None:
    """A fitted pipeline should return binary labels and probabilities."""
    features, target = load_features_and_target()
    model = build_logistic_regression_pipeline()
    model.fit(features, target)

    sample = features.head(5)
    predictions = model.predict(sample)
    probabilities = model.predict_proba(sample)

    assert predictions.shape == (5,)
    assert probabilities.shape == (5, 2)
    assert set(predictions).issubset({0, 1})
    assert ((probabilities >= 0) & (probabilities <= 1)).all()
    assert pd.Series(probabilities.sum(axis=1)).round(6).eq(1.0).all()
