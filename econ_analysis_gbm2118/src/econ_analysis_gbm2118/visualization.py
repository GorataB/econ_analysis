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
    sns.set(style="whitegrid")
    df_plot = df.dropna(subset=[x_var, y_var])
    sns.scatterplot(data=df_plot, x=x_var, y=y_var)
    plt.title(f"Scatterplot of {y_var} vs {x_var}")
    plt.show()
