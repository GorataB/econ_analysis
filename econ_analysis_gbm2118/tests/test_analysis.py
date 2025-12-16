import pandas as pd
import pytest

from econ_analysis_gbm2118.analysis import summary_statistics, extreme_rank_countries


def test_summary_statistics_basic():
    df = pd.DataFrame({
        "a": [1, 2, 3],
        "b": [4, 5, 6],
        "c": [7, 8, 9]
    })

    vars_of_interest = ["a", "b"]
    result = summary_statistics(df, vars_of_interest)

    # Check result is a DataFrame
    assert isinstance(result, pd.DataFrame)
    # Check rows correspond to selected variables
    assert list(result.index) == vars_of_interest
    # Check columns include standard describe output
    expected_cols = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]
    assert all(col in result.columns for col in expected_cols)


def test_summary_statistics_missing_columns(capfd):
    df = pd.DataFrame({
        "a": [1, 2, 3],
        "b": [4, 5, 6],
    })

    vars_of_interest = ["a", "b", "x"]  # x does not exist
    result = summary_statistics(df, vars_of_interest)

    # Check missing column is ignored
    assert "x" not in result.index
    # Check warning printed
    captured = capfd.readouterr()
    assert "x" in captured.out


def test_extreme_rank_countries_basic():
    df = pd.DataFrame({
        "cname": ["A", "B", "C", "D"],
        "rank1": [1, 2, 3, 4],
        "score2": [40, 30, 20, 10]
    })

    result = extreme_rank_countries(df, "rank1", "score2", top_n=2)

    # Should return 2 rows
    assert len(result) == 2
    # Columns present
    for col in ["cname", "rank1", "rank_col2_calc", "rank_difference"]:
        assert col in result.columns
    # Largest rank difference first
    assert result["rank_difference"].iloc[0] >= result["rank_difference"].iloc[1]


def test_extreme_rank_countries_missing_rank_col2():
    df = pd.DataFrame({
        "cname": ["A", "B"],
        "rank1": [1, 2]
    })
    with pytest.raises(ValueError):
        extreme_rank_countries(df, "rank1", "score2")


def test_extreme_rank_countries_top_n_limit():
    df = pd.DataFrame({
        "cname": ["A", "B", "C", "D", "E"],
        "rank1": [5, 4, 3, 2, 1],
        "score2": [1, 2, 3, 4, 5]
    })

    # top_n larger than dataframe
    result = extreme_rank_countries(df, "rank1", "score2", top_n=10)
    assert len(result) == 5  # only 5 rows exist

    # top_n smaller
    result2 = extreme_rank_countries(df, "rank1", "score2", top_n=3)
    assert len(result2) == 3
