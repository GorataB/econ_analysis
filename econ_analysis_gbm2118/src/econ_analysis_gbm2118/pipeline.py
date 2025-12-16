from econ_analysis_gbm2118.data import load_harvard_data, load_qog_data
from econ_analysis_gbm2118.cleaning import clean_merged_data
from econ_analysis_gbm2118.analysis import summary_statistics, extreme_rank_countries
from econ_analysis_gbm2118.visualization import plot_eci_vs_gci


def run_pipeline(
    harvard_csv: str,
    qog_source: str,
):
    """
    Run full data pipeline:
    - load datasets
    - merge & clean
    - generate summary statistics
    - produce plots
    """

    # Load
    df_harvard = load_harvard_data(harvard_csv)
    df_qog = load_qog_data(qog_source)

    # Clean & merge
    merged = clean_merged_data(df_harvard, df_qog)

    # Summary stats
    vars_of_interest = [
        "growth_proj", "eci_sitc", "eci_rank_sitc",
        "eci_hs92", "eci_rank_hs92",
        "eci_hs12", "eci_rank_hs12",
        "pwt_hci", "bti_eos", "bti_ep",
        "wef_gci", "mad_gdppc",
    ]

    summary = summary_statistics(merged, vars_of_interest)
    print(summary)

    # Plot
    plot_eci_vs_gci(merged)

    # Extremes
    extremes = extreme_rank_countries(
        merged,
        rank_col1="eci_rank_sitc",
        rank_col2="bti_ep",
    )

    return merged, summary, extremes
