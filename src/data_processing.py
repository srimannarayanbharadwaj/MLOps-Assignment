"""Data cleaning utilities for the UCI Heart Disease Cleveland dataset."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


COLUMN_NAMES = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
    "target",
]

NUMERIC_FEATURES = [
    "age",
    "trestbps",
    "chol",
    "thalach",
    "oldpeak",
]

CATEGORICAL_FEATURES = [
    "sex",
    "cp",
    "fbs",
    "restecg",
    "exang",
    "slope",
    "ca",
    "thal",
]


def load_raw_data(path: str | Path) -> pd.DataFrame:
    """Load the Cleveland data file and attach readable column names."""
    return pd.read_csv(path, names=COLUMN_NAMES, na_values="?")


def clean_heart_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    """Clean raw rows and collapse the target to binary labels."""
    data = raw_data.copy()
    data = data.replace("?", pd.NA)

    for column in COLUMN_NAMES:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    for column in ["ca", "thal"]:
        mode_value = data[column].mode(dropna=True)[0]
        data[column] = data[column].fillna(mode_value)

    data["target"] = (data["target"] > 0).astype(int)
    return data


def save_clean_data(
    raw_path: str | Path,
    output_path: str | Path,
) -> pd.DataFrame:
    """Load, clean, and save the processed Cleveland dataset."""
    raw_data = load_raw_data(raw_path)
    clean_data = clean_heart_data(raw_data)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    clean_data.to_csv(output_path, index=False)
    return clean_data
