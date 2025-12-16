import pandas as pd
import matplotlib
import pytest

# Use a non-interactive backend to prevent GUI windows
matplotlib.use("Agg")

from econ_analysis_2118.visualization import plot_eci_vs_gci


def test_plot_runs_with_basic_data():
    df = pd.DataFrame({
        "eci_sitc": [1, 2, 3],
        "wef_gci": [10, 20, 30]
    })

    # Should run without error
    plot_eci_vs_gci(df)


def test_plot_handles_missing_values():
    df = pd.DataFrame({
        "eci_sitc": [1, None, 3],
        "wef_gci": [10, 20, None]
    })

    # Should drop rows with NaN and still run
    plot_eci_vs_gci(df)


def test_plot_custom_columns():
    df = pd.DataFrame({
        "x_custom": [1, 2, 3],
        "y_custom": [10, 20, 30]
    })

    # Should accept custom x_var and y_var
    plot_eci_vs_gci(df, x_var="x_custom", y_var="y_custom")


def test_plot_empty_dataframe():
    df = pd.DataFrame({
        "eci_sitc": [],
        "wef_gci": []
    })

    # Should not crash on empty data
    plot_eci_vs_gci(df)
