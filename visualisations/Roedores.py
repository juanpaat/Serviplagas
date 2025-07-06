import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import math

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math


def generate_roedores_station_status_plot(df: pd.DataFrame) -> tuple[pd.DataFrame, plt.Figure]:
    """
    Generate a faceted bar/line/point chart showing the evolution of rodent station statuses over time.

    Parameters:
    ----------
    df : pd.DataFrame
        The 'roedores' DataFrame containing monthly station status counts and a 'Mes' column.

    Returns:
    -------
    plt.Figure
        The matplotlib figure object ready for insertion into Word document
    """

    # Group and summarize status metrics by month
    grouped = df.groupby('Mes').agg({
        'Consumido': 'sum',
        'Instalación': 'sum',
        'Sin novedad': 'sum',
        'Presencia de roedores': 'sum',
        'Presencia de bioindicador': 'sum',
        'Cambio de cebo por deterioro': 'sum',
        'Desaparecida': 'sum',
        'Estación dañada': 'sum',
        'Estación bloqueada': 'sum'
    }).reset_index()

    # Melt into long format
    long_df = grouped.melt(id_vars='Mes', var_name='Estado', value_name='Cantidad')

    # Sort 'Mes' categorically if formatted as 'Mon YYYY'
    try:
        long_df['Mes'] = pd.Categorical(
            long_df['Mes'],
            categories=sorted(grouped['Mes'], key=lambda x: pd.to_datetime(x, format='%b %Y')),
            ordered=True
        )
        long_df = long_df.sort_values('Mes')
    except Exception as e:
        print(f"[Warning] Could not parse and sort 'Mes': {e}")

    # Create FacetGrid
    g = sns.FacetGrid(long_df, col='Estado', col_wrap=3, sharey=False, sharex=False, height=3.5)

    # Map plotting functions
    g.map_dataframe(sns.barplot, x='Mes', y='Cantidad', alpha=0.1, color='steelblue')
    g.map_dataframe(sns.lineplot, x='Mes', y='Cantidad', marker='o', color='black')

    # Customize each subplot
    for ax in g.axes.flatten():
        # Rotate x-axis labels using plt.setp to avoid warnings
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=6)
        ax.tick_params(axis='x', labelbottom=True)

        # Gridlines
        ax.grid(True, axis='x', alpha=0.3, linestyle='-', linewidth=0.5, color='gray')
        ax.grid(True, axis='y', alpha=0.3, linestyle='-', linewidth=0.5, color='gray')

        # Y-axis formatting
        y_min, y_max = ax.get_ylim()
        y_max = math.ceil(y_max)
        y_min = math.floor(y_min)
        step = max(1, math.ceil((y_max - y_min) / 5))
        ax.set_yticks(range(y_min, y_max + 1, step))
        ax.set_ylim(bottom=0)

    # Set titles and labels
    g.set_titles("{col_name}")
    g.set_axis_labels("", "Cantidad")
    g.fig.suptitle("Estado de la estación en el tiempo", fontsize=14)
    g.fig.subplots_adjust(top=0.92)

    # Apply tight layout
    g.fig.tight_layout()

    # Return the figure object
    return grouped, g.fig


def plot_tendencia_eliminacion_mensual(df: pd.DataFrame) -> tuple[pd.DataFrame, plt.Figure]:
    """
    Generate a bar + line + point chart showing monthly rodent elimination trend ("Consumido").

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with rodent control data including 'Mes' and status columns

    Returns:
    --------
    plt.Figure
        The matplotlib figure object ready for insertion into Word document
    """

    # Group and summarize status metrics by month
    grouped = df.groupby('Mes').agg({
        'Consumido': 'sum',
        'Instalación': 'sum',
        'Sin novedad': 'sum',
        'Presencia de roedores': 'sum',
        'Presencia de bioindicador': 'sum',
        'Cambio de cebo por deterioro': 'sum',
        'Desaparecida': 'sum',
        'Estación dañada': 'sum',
        'Estación bloqueada': 'sum'
    }).reset_index()

    # Melt into long format
    long_df = grouped.melt(id_vars='Mes', var_name='Estado', value_name='Cantidad')

    # Filter only rows where Estado is "Consumido"
    filtered_df = long_df[long_df['Estado'] == 'Consumido'].copy()

    # Group by month and summarize
    summary = filtered_df.groupby('Mes').agg(
        **{'Total de eliminación por mes': ('Cantidad', 'sum')}
    ).reset_index()

    # Sort 'Mes' categorically if formatted as 'Mon YYYY'
    try:
        summary['Mes'] = pd.Categorical(
            summary['Mes'],
            categories=sorted(summary['Mes'], key=lambda x: pd.to_datetime(x, format='%b %Y')),
            ordered=True
        )
        summary = summary.sort_values('Mes')
    except Exception as e:
        print(f"[Warning] Could not parse and sort 'Mes': {e}")

    # Create figure and axis explicitly
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.set_style("whitegrid")

    # Bar chart
    bars = sns.barplot(
        data=summary,
        x='Mes',
        y='Total de eliminación por mes',
        alpha=0.1,
        color='steelblue',
        edgecolor='black',
        ax=ax
    )

    # Line chart
    sns.lineplot(
        data=summary,
        x='Mes',
        y='Total de eliminación por mes',
        marker='o',
        color='black',
        ax=ax
    )

    # Annotate each point with white text
    for i, row in summary.iterrows():
        ax.text(
            x=i,
            y=row['Total de eliminación por mes'],
            s=str(int(row['Total de eliminación por mes'])),
            ha='center',
            va='center',
            color='white',
            fontsize=8,
            weight='bold'
        )

    # Formatting
    ax.set_title("Tendencia de eliminación mensual", fontsize=14, weight='bold')
    ax.set_xlabel("")
    ax.set_ylabel("Tendencia de consumo por mes")

    # Fix rotation using plt.setp to avoid warnings
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    # Y-axis ticks
    y_min, y_max = ax.get_ylim()
    y_min = math.floor(y_min)
    y_max = math.ceil(y_max)
    step = max(1, 2)  # Fixed step of 2
    ax.set_yticks(range(y_min, int(y_max) + 1, step))
    ax.set_ylim(bottom=0)

    fig.tight_layout()

    # Return the figure object
    return grouped, fig




