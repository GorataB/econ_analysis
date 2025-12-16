import pandas as pd

def summary_statistics(df: pd.DataFrame, vars_of_interest: list) -> pd.DataFrame:
    """
    Compute descriptive statistics for selected variables.

    This function returns standard descriptive statistics (count, mean,
    standard deviation, minimum, maximum, and quartiles) for a specified
    subset of variables. Variables not found in the DataFrame are ignored,
    with a warning printed to the console.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset containing variables of interest.
    vars_of_interest : list of str
        List of column names for which descriptive statistics
        should be computed.

    Returns
    -------
    pandas.DataFrame
        A DataFrame of descriptive statistics with variables as rows
        and summary measures as columns.

    Notes
    -----
    Columns listed in ``vars_of_interest`` that are not present in
    ``df`` are excluded from the output.
    """
    missing_vars = set(vars_of_interest) - set(df.columns)
    if missing_vars:
        print("Warning: Missing columns:", missing_vars)
    available_vars = [v for v in vars_of_interest if v in df.columns]
    return df[available_vars].describe().T

def extreme_rank_countries(df: pd.DataFrame, rank_col1: str, rank_col2: str, top_n: int = 5) -> pd.DataFrame:
    """
   Identify countries with the largest rank differences between two indicators.

   This function computes the difference between an existing rank variable
   and a calculated rank derived from a second indicator. Countries with
   the largest positive rank differences are returned.

   Parameters
   ----------
   df : pandas.DataFrame
       Dataset containing country names and ranking variables.
   rank_col1 : str
       Name of the first ranking column (precomputed ranks).
   rank_col2 : str
       Name of the second column from which ranks will be calculated.
   top_n : int, default=5
       Number of countries with the largest rank differences to return.

   Returns
   -------
   pandas.DataFrame
       A DataFrame containing country names, both ranking measures,
       and the calculated rank difference, sorted in descending order.

   Raises
   ------
   ValueError
       If ``rank_col2`` is not found in the DataFrame.

   Notes
   -----
   The second ranking is computed in descending order, where higher
   values receive better (lower numeric) ranks.
   """
    if rank_col2 not in df.columns:
        raise ValueError(f"{rank_col2} not found in dataframe")
    df['rank_col2_calc'] = df[rank_col2].rank(ascending=False)
    temp = df[['cname', rank_col1, 'rank_col2_calc']].copy()
    temp['rank_difference'] = temp[rank_col1] - temp['rank_col2_calc']
    return temp.sort_values('rank_difference', ascending=False).head(top_n)

