import pandas as pd
import pytest
from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # Prevent GUI windows from opening during tests

from econ_analysis_gbm2118.pipeline import run_pipeline


def test_pipeline_runs_end_to_end(tmp_path):
    """
    Test the full pipeline with small synthetic Harvard and QOG datasets.
    Ensures merged data, summary statistics, and extreme ranks are returned.
    """

    # Create minimal Harvard CSV
    df_harvard = pd.DataFrame({
        "country_iso3_code": ["USA", "FRA"],
        "year": [2023, 2023],
        "growth_proj": [1.1, 2.2],
        "eci_sitc": [0.5, 0.7],
        "eci_rank_sitc": [1, 2],
        "eci_hs92": [0.6, 0.8],
        "eci_rank_hs92": [1, 2],
        "eci_hs12": [0.7, 0.9],
        "eci_rank_hs12": [1, 2],
        "pwt_hci": [0.8, 0.9],
        "bti_eos": [50, 60],
        "bti_ep": [70, 80],
        "wef_gci": [5.0, 6.0],
        "mad_gdppc": [40000, 50000],
        "cname": ["United States (the)", "France"]
    })

    harvard_file = tmp_path / "harvard.csv"
    df_harvard.to_csv(harvard_file, index=False)

    # Create minimal QOG Excel
    df_qog = pd.DataFrame({
        "ccodealp": ["USA", "FRA"],
        "bti_ep": [70, 80],
        "bti_eos": [50, 60]
    })
    qog_file = tmp_path / "qog.xlsx"
    df_qog.to_excel(qog_file, index=False)

    # Run pipeline
    merged, summary, extremes = run_pipeline(str(harvard_file), str(qog_file))

    # Assertions

    # Merged dataset has correct shape
    assert merged.shape[0] == 2
    for col in ["cname", "eci_sitc", "bti_ep"]:
        assert col in merged.columns

    # Summary statistics returned as DataFrame with selected vars
    assert not summary.empty
    for var in ["growth_proj", "eci_sitc", "bti_ep"]:
        assert var in summary.index

    # Extreme ranks returned correctly
    assert not extremes.empty
    for col in ["cname", "eci_rank_sitc", "rank_col2_calc", "rank_difference"]:
        assert col in extremes.columns


def test_pipeline_handles_missing_columns(tmp_path):
    """
    Pipeline should handle missing optional columns without crashing.
    """

    # Minimal Harvard CSV with missing 'wef_gci'
    df_harvard = pd.DataFrame({
        "country_iso3_code": ["USA"],
        "year": [2023],
        "growth_proj": [1.1],
        "eci_sitc": [0.5],
        "eci_rank_sitc": [1],
        "cname": ["United States (the)"]
    })
    harvard_file = tmp_path / "harvard.csv"
    df_harvard.to_csv(harvard_file, index=False)

    # Minimal QOG Excel
    df_qog = pd.DataFrame({
        "ccodealp": ["USA"],
        "bti_ep": [70]
    })
    qog_file = tmp_path / "qog.xlsx"
    df_qog.to_excel(qog_file, index=False)

    # Should not raise exceptions
    merged, summary, extremes = run_pipeline(str(harvard_file), str(qog_file))

    # Check merged DataFrame
    assert merged.shape[0] == 1
    assert "cname" in merged.columns
    # Check summary includes only existing columns
    assert "wef_gci" not in summary.index
