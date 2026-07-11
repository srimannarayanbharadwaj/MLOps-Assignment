"""Download the UCI Heart Disease Cleveland dataset."""

from __future__ import annotations

from pathlib import Path

import requests

from src.data_processing import save_clean_data


DATA_URL = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/"
    "heart-disease/processed.cleveland.data"
)
RAW_PATH = Path("data/raw/processed.cleveland.data")
PROCESSED_PATH = Path("data/processed/heart_cleveland_clean.csv")


def download_dataset(
    url: str = DATA_URL,
    output_path: Path = RAW_PATH,
) -> Path:
    """Download the Cleveland subset from UCI and save it locally."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, timeout=30)
    response.raise_for_status()
    output_path.write_text(response.text, encoding="utf-8")
    return output_path


def main() -> None:
    """Download raw data and create the cleaned CSV used by later phases."""
    raw_path = download_dataset()
    clean_data = save_clean_data(raw_path, PROCESSED_PATH)
    print(f"Raw dataset saved to {raw_path}")
    print(f"Clean dataset saved to {PROCESSED_PATH}")
    print(f"Rows: {clean_data.shape[0]}, columns: {clean_data.shape[1]}")


if __name__ == "__main__":
    main()
