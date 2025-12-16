import pandas as pd
import numpy as np
import pytest

from econ_analysis_gbm2118.cleaning import (
    merge_datasets,
    fill_and_clip_numeric,
    clean_country_names,
    clean_merged_data,
)


def test_merge_datasets_left_join_and_drop_columns():
    df_harvard = pd.DataFrame({
        "country_iso3_code": ["USA", "FRA"],
        "year": [2023, 2023],
        "value": [10, 20],
    })

    df_qog = pd.DataFrame({
        "ccodealp": ["USA"],
        "qog_score": [1.5],
    })

    merged = merge_datasets(df_harvard, df_qog)

    # Left join preserves all Harvard rows
    assert len(merged) == 2

    # Columns dropped
    assert "ccodealp" not in merged.columns
    assert "year" not in merged.columns

    # QOG value merged correctly
    assert merged.loc[merged["country_iso3_code"] == "USA", "qog_score"].iloc[0] == 1.5
    assert pd.isna(merged.loc[merged["country_iso3_code"] == "FRA", "qog_score"]).iloc[0]


def test_fill_and_clip_numeric_fills_nan_with_median():
    df = pd.DataFrame({
        "a": [1.0, 2.0, np.nan],
        "b": [10, 20, 30],
        "c": ["x", "y", "z"],  # non-numeric column
    })

    cleaned = fill_and_clip_numeric(df.copy())

    # Median of column a = 1.5
    assert cleaned["a"].isna().sum() == 0
    assert 1.0 <= cleaned["a"].iloc[2] <= 2.0

    # Non-numeric column unchanged
    assert cleaned["c"].tolist() == ["x", "y", "z"]


def test_fill_and_clip_numeric_clips_outliers():
    df = pd.DataFrame({
        "x": [1, 2, 3, 1000],  # extreme outlier
    })

    cleaned = fill_and_clip_numeric(df.copy())

    upper = cleaned["x"].quantile(0.99)
    lower = cleaned["x"].quantile(0.01)

    assert cleaned["x"].max() <= upper
    assert cleaned["x"].min() >= lower


def test_clean_country_names_removes_the_suffix():
    df = pd.DataFrame({
        "cname": ["Bahamas (the)", "Netherlands (the)", "France"],
    })

    cleaned = clean_country_names(df.copy())

    assert cleaned["cname"].tolist() == ["Bahamas", "Netherlands", "France"]


def test_clean_country_names_handles_missing_column():
    df = pd.DataFrame({
        "country": ["USA", "FRA"]
    })

    cleaned = clean_country_names(df.copy())

    # DataFrame unchanged
    pd.testing.assert_frame_equal(cleaned, df)


def test_clean_merged_data_full_pipeline():
    df_harvard = pd.DataFrame({
        "country_iso3_code": ["USA", "FRA"],
        "year": [2023, 2023],
        "value": [1, np.nan],
        "cname": ["United States (the)", "France"],
    })

    df_qog = pd.DataFrame({
        "ccodealp": ["USA"],
        "qog_score": [2.5],
    })

    cleaned = clean_merged_data(df_harvard, df_qog)

    # Pipeline ran correctly
    assert "year" not in cleaned.columns
    assert "ccodealp" not in cleaned.columns

    # NaN filled
    assert cleaned["value"].isna().sum() == 0

    # Country names cleaned
    assert cleaned.loc[cleaned["country_iso3_code"] == "USA", "cname"].iloc[0] == "United States"
