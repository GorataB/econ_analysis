import pandas as pd
from pathlib import Path

def load_harvard_data(file_path: str) -> pd.DataFrame:
    """
    Load Harvard Atlas of Economic Complexity data and filter for the year 2023.

    This function reads a CSV file containing Harvard Atlas data and filters
    the dataset to include only observations from 2023 if a ``year`` column
    is present.

    Parameters
    ----------
    file_path : str
        Path to the CSV file containing Harvard Atlas data.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing Harvard Atlas data for the year 2023.

    Raises
    ------
    FileNotFoundError
        If the specified file path does not exist.
    pandas.errors.EmptyDataError
        If the CSV file is empty.
    """
    df = pd.read_csv(file_path)
    if 'year' in df.columns:
        df = df[df['year'] == 2023].copy()
    return df

def load_qog_data(file_path: str) -> pd.DataFrame:
    """
    Load Quality of Governance (QoG) data from an Excel file.

    This function reads Quality of Governance data from a local file path
    or a remote URL. If a URL is provided, only the file name is used for
    internal processing, but the full path/URL is passed to `pandas.read_excel`.

    Parameters
    ----------
    file_path : str
        Path to the local Excel file or URL of the Excel file containing
        Quality of Governance data.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing Quality of Governance data.

    Notes
    -----
    - This function currently does not handle authentication for protected URLs.
    - Missing or inaccessible files will raise an error from `pandas.read_excel`.
    """
    path = Path(file_path)

    # If path has URL-like parts, just use the filename
    if "://" in file_path:
        path = Path(file_path).name

    df = pd.read_excel(file_path)
    return df
