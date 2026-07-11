"""Tests for data cleaning behavior."""

import pandas as pd

from src.data_processing import COLUMN_NAMES, clean_heart_data


def test_clean_heart_data_imputes_missing_ca_and_thal() -> None:
    """Question-mark missing values should be converted and imputed."""
    raw_data = pd.DataFrame(
        [
            [63, 1, 1, 145, 233, 1, 2, 150, 0, 2.3, 3, "?", "6", 0],
            [67, 1, 4, 160, 286, 0, 2, 108, 1, 1.5, 2, "3", "?", 2],
            [37, 1, 3, 130, 250, 0, 0, 187, 0, 3.5, 3, "0", "3", 1],
        ],
        columns=COLUMN_NAMES,
    )

    clean_data = clean_heart_data(raw_data)

    assert clean_data[["ca", "thal"]].isna().sum().sum() == 0
    assert clean_data.loc[0, "ca"] in {0, 3}
    assert clean_data.loc[1, "thal"] in {3, 6}


def test_clean_heart_data_collapses_target_to_binary() -> None:
    """Original targets above zero should become the disease class."""
    raw_data = pd.DataFrame(
        [
            [63, 1, 1, 145, 233, 1, 2, 150, 0, 2.3, 3, 0, 6, 0],
            [67, 1, 4, 160, 286, 0, 2, 108, 1, 1.5, 2, 3, 3, 1],
            [67, 1, 4, 120, 229, 0, 2, 129, 1, 2.6, 2, 2, 7, 4],
        ],
        columns=COLUMN_NAMES,
    )

    clean_data = clean_heart_data(raw_data)

    assert clean_data["target"].tolist() == [0, 1, 1]
    assert set(clean_data["target"].unique()) == {0, 1}
