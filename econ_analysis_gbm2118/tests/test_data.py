import pandas as pd
from pathlib import Path
import pytest

from econ_analysis_gbm2118.data import load_harvard_data, load_qog_data


def test_load_harvard_data_filters_2023(tmp_path):
    """Should only keep rows from year 2023."""
    df = pd.DataFrame({
        "country": ["A", "B", "C"],
        "year": [2022, 2023, 2023],
        "value": [1, 2, 3]
    })

    file_path = tmp_path / "growth_proj_eci_rankings.csv"
    df.to_csv(file_path, index=False)

    result = load_harvard_data(file_path)

    assert len(result) == 2
    assert (result["year"] == 2023).all()


def test_load_harvard_data_no_year_column(tmp_path):
    """If no year column exists, data should be returned unchanged."""
    df = pd.DataFrame({
        "country": ["A", "B"],
        "value": [10, 20]
    })

    file_path = tmp_path / "growth_proj_eci_rankings.csv"
    df.to_csv(file_path, index=False)

    result = load_harvard_data(file_path)

    assert len(result) == 2
    assert "year" not in result.columns


def test_load_qog_data_from_excel(tmp_path):
    """Should load an Excel file correctly."""
    df = pd.DataFrame({
        "ccodealp": ["USA", "FRA"],
        "score": [1.2, 2.3]
    })

    file_path = tmp_path / "https://www.qogdata.pol.gu.se/data/qog_bas_cs_jan23.xlsx"
    df.to_excel(file_path, index=False)

    result = load_qog_data(file_path)

    pd.testing.assert_frame_equal(result, df)
