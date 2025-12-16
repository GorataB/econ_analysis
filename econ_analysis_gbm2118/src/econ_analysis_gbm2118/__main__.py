import argparse
from econ_analysis_gbm2118.pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(description="Run economic data pipeline")
    parser.add_argument(
        "--harvard",
        required=True,
        help="growth_proj_eci_rankings.csv",
    )
    parser.add_argument(
        "--qog",
        required=True,
        help="https://www.qogdata.pol.gu.se/data/qog_bas_cs_jan23.xlsx",
    )

    args = parser.parse_args()

    run_pipeline(
        harvard_csv=args.harvard,
        qog_source=args.qog,
    )


if __name__ == "__main__":
    main()
