import pandas as pd
import numpy as np

def merge_datasets(df_harvard: pd.DataFrame, df_qog: pd.DataFrame) -> pd.DataFrame:
    """
    Merge Harvard Atlas and Quality of Governance datasets using ISO3 country codes.

    The Harvard dataset is merged with the Quality of Governance (QoG) dataset
    using a left join on ISO3 country codes. Redundant identifier columns are
    removed after merging when present.

    Parameters
    ----------
    df_harvard : pandas.DataFrame
        Harvard Atlas dataset containing ISO3 country codes
        in the ``country_iso3_code`` column.
    df_qog : pandas.DataFrame
        Quality of Governance dataset containing ISO3 country codes
        in the ``ccodealp`` column.

    Returns
    -------
    pandas.DataFrame
        A merged DataFrame combining Harvard and QoG variables.

    Raises
    ------
    KeyError
        If required merge columns are missing from the input DataFrames.
    """
    merged = df_harvard.merge(
        df_qog,
        left_on="country_iso3_code",
        right_on="ccodealp",
        how="left",
        suffixes=("", "_qog")
    )

    # Prefer QOG versions if they exist
    for col in ["bti_ep", "bti_eos"]:
        if f"{col}_qog" in merged.columns:
            merged[col] = merged[f"{col}_qog"]
            merged.drop(columns=[f"{col}_qog"], inplace=True)

    merged.drop(columns=["ccodealp"], errors="ignore", inplace=True)
    return merged

def fill_and_clip_numeric(merged: pd.DataFrame) -> pd.DataFrame:
    """
    Impute missing numeric values and clip extreme outliers.

    All numeric columns are processed by filling missing values with the
    column median and clipping values to the 1st and 99th percentiles
    to limit the influence of extreme outliers.

    Parameters
    ----------
    merged : pandas.DataFrame
        Dataset containing numeric and non-numeric variables.

    Returns
    -------
    pandas.DataFrame
        DataFrame with missing numeric values imputed and extreme
        outliers clipped.

    Notes
    -----
    Non-numeric columns are left unchanged.
    """
    numeric_cols = merged.select_dtypes(include="number").columns

    for col in numeric_cols:
       median = merged[col].median()
       merged[col] = merged[col].fillna(median)

       lower = merged[col].quantile(0.01)
       upper = merged[col].quantile(0.99)

       merged[col] = merged[col].clip(lower=lower, upper=upper)

    return merged

def clean_country_names(merged: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize country names by removing trailing ``(the)``.

    Country names ending with the suffix ``(the)`` are cleaned using a
    regular expression. Missing values are handled safely.

    Parameters
    ----------
    merged : pandas.DataFrame
        Dataset containing a country name column named ``cname``.

    Returns
    -------
    pandas.DataFrame
        DataFrame with standardized country names.

    Notes
    -----
    If the ``cname`` column is not present, the input DataFrame is
    returned unchanged.
    """
    if 'cname' in merged.columns:
        merged['cname'] = merged['cname'].fillna("").str.replace(r"\s*\(the\)$", "", regex=True)
    return merged

def clean_merged_data(df_harvard: pd.DataFrame, df_qog: pd.DataFrame) -> pd.DataFrame:
    """
   Execute the full data merging and cleaning pipeline.

   This function merges Harvard Atlas and Quality of Governance datasets,
   imputes and clips numeric variables, and standardizes country names
   to produce an analysis-ready dataset.

   Parameters
   ----------
   df_harvard : pandas.DataFrame
       Harvard Atlas dataset.
   df_qog : pandas.DataFrame
       Quality of Governance dataset.

   Returns
   -------
   pandas.DataFrame
       Fully cleaned and merged dataset ready for downstream analysis.
   """
    merged = merge_datasets(df_harvard, df_qog)
    merged = fill_and_clip_numeric(merged)
    merged = clean_country_names(merged)
    return merged

