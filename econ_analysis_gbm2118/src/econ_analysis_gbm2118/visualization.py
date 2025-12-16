import seaborn as sns
import matplotlib.pyplot as plt

def plot_eci_vs_gci(df, x_var='eci_sitc', y_var='wef_gci'):
    """
    Plot a scatterplot comparing Economic Complexity Index (ECI) and
    Global Competitiveness Index (GCI).

    This function creates a scatterplot of two variables after dropping
    observations with missing values in either variable. The plot is
    displayed using seaborn styling.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset containing ECI, GCI, or related variables.
    x_var : str, default='eci_sitc'
        Name of the column to be plotted on the x-axis.
    y_var : str, default='wef_gci'
        Name of the column to be plotted on the y-axis.

    Returns
    -------
    None
        This function produces a visualization and does not return
        any objects.

    Notes
    -----
    The function drops rows with missing values in either ``x_var`` or
    ``y_var`` prior to plotting.
    """
    if x_var not in df.columns or y_var not in df.columns:
        return None

    df_plot = df.dropna(subset=[x_var, y_var])

    if df_plot.empty:
        return None

    plt.scatter(df_plot[x_var], df_plot[y_var])
    plt.xlabel(x_var)
    plt.ylabel(y_var)
    plt.title("ECI vs GCI")
    plt.show()
