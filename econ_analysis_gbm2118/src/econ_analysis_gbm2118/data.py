import pandas as pd

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

def load_qog_data(url: str) -> pd.DataFrame:
    """
    Load Quality of Governance (QoG) data from an Excel file.

    This function reads Quality of Governance data from either a remote URL
    or a local Excel file path and returns the data as a pandas DataFrame.

    Parameters
    ----------
    url : str
        URL or local file path to the Quality of Governance Excel file.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing Quality of Governance data.

    Raises
    ------
    FileNotFoundError
        If the specified file path does not exist.
    ValueError
        If the Excel file cannot be read.
    """
    df = pd.read_excel(url)
    return df
