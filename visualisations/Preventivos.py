import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import math



from io import BytesIO

def generate_order_area_plot(df: pd.DataFrame) -> None:
    """
    Generate a grouped bar plot showing:
        - Cantidad de órdenes
        - Cantidad de áreas
        - Áreas con plaga
    grouped by month (Mes).

    Parameters:
    ----------
    df : pd.DataFrame
        The transformed 'preventivos' DataFrame containing columns:
        'Mes', 'Código', 'Área', 'Plagas evidenciadas'

    Returns:
    -------
    None
    """
    # Group and summarize
    summary_df = df.groupby('Mes').agg({
        'Código': pd.Series.nunique,
        'Área': pd.Series.nunique,
        'Plagas evidenciadas': lambda x: (x != 'Sin evidencia').sum()
    }).reset_index()

    summary_df.columns = ['Mes', 'Cantidad de órdenes', 'Cantidad de áreas', 'Áreas con plaga']

    # Convert to long format
    summary_long = summary_df.melt(
        id_vars='Mes',
        var_name='Variable',
        value_name='Valor'
    )

    # Sort 'Mes' if in 'Mon YYYY' format
    try:
        summary_long['Mes'] = pd.Categorical(
            summary_long['Mes'],
            categories=sorted(summary_df['Mes'], key=lambda x: pd.to_datetime(x, format='%b %Y')),
            ordered=True
        )
    except Exception as e:
        print(f"[Warning] Could not parse and sort 'Mes': {e}")

    # Crear figura y eje
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.set_style("whitegrid")

    # Graficar
    bar_plot = sns.barplot(
        data=summary_long,
        x='Mes',
        y='Valor',
        hue='Variable',
        palette=['#333333', '#8C8C8C', '#D3D3D3'],
        edgecolor='black',
        ax=ax  # <- usar eje explícito
    )

    for p in bar_plot.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(
                f'{int(height)}',
                (p.get_x() + p.get_width() / 2., height),
                ha='center', va='bottom',
                fontsize=9, color='black'
            )

    ax.set_title("Cantidad de órdenes vs Cantidad de áreas", fontsize=14, weight='bold')
    ax.set_xlabel("")
    ax.set_ylabel("Cantidad")
    ax.legend(
        title="",
        loc='center left',
        bbox_to_anchor=(1.0, 0.5),
        frameon=False
    )

    fig.tight_layout()
    return fig



def generate_plagas_timeseries_facet(df: pd.DataFrame) -> None:
    """
    Generate a faceted line/bar/point chart showing quantity of each pest species by month.

    Parameters:
    ----------
    df : pd.DataFrame
        The 'preventivos' DataFrame with pest quantity columns and a 'Mes' column.

    Returns:
    -------
    None
    """

    # Group and summarize by month
    grouped = df.groupby('Mes').agg({
        'Cantidad de Cucaracha Americana': 'sum',
        'Cantidad de Cucaracha Alemana ': 'sum',
        'Cantidad de Hormigas': 'sum',
        'Cantidad de Moscas': 'sum',
        'Cantidad de Mosquitos': 'sum',
        'Cantidad de Zancudos': 'sum',
        'Cantidad de Ratón casero': 'sum',
        'Cantidad de Rata Noruega': 'sum',
        'Cantidad de Ratón de tejado': 'sum',
        'Cantidad de Otras plagas': 'sum'
    }).reset_index()

    # Rename for display (optional)
    grouped.rename(columns={
        'Cantidad de Cucaracha Americana': 'Cucaracha Americana',
        'Cantidad de Cucaracha Alemana ': 'Cucaracha Alemana',
        'Cantidad de Hormigas': 'Hormigas',
        'Cantidad de Moscas': 'Moscas',
        'Cantidad de Mosquitos': 'Mosquitos',
        'Cantidad de Zancudos': 'Zancudos',
        'Cantidad de Ratón casero': 'Ratón casero',
        'Cantidad de Rata Noruega': 'Rata Noruega',
        'Cantidad de Ratón de tejado': 'Ratón de tejado',
        'Cantidad de Otras plagas': 'Otras plagas'
    }, inplace=True)

    # Melt into long format
    long_df = grouped.melt(id_vars='Mes', var_name='Plaga', value_name='Cantidad')

    # Ensure chronological order of months
    try:
        long_df['Mes'] = pd.Categorical(
            long_df['Mes'],
            categories=sorted(grouped['Mes'], key=lambda x: pd.to_datetime(x, format='%b %Y')),
            ordered=True
        )
    except Exception as e:
        print(f"[Warning] Could not parse and sort 'Mes': {e}")

    # Faceted plot with seaborn
    g = sns.FacetGrid(long_df, col='Plaga', col_wrap=3, sharey=False, sharex=False, height=3.5)
    g.map_dataframe(sns.barplot, x='Mes', y='Cantidad', alpha=0.1, color='steelblue')
    g.map_dataframe(sns.lineplot, x='Mes', y='Cantidad', marker="o", color='black')

    # Format each subplot
    for ax in g.axes.flatten():
        # Rotate x-axis labels using tick_params (cleaner approach)
        ax.tick_params(axis='x', rotation=45, labelsize=6)

        # Force x-axis labels to show on all subplots
        ax.tick_params(axis='x', labelbottom=True)

        # Add vertical gridlines
        ax.grid(True, axis='x', alpha=0.3, linestyle='-', linewidth=0.5, color='gray')
        # Keep existing horizontal gridlines (if any) or add them
        ax.grid(True, axis='y', alpha=0.3, linestyle='-', linewidth=0.5, color='gray')

        # Y-axis formatting
        y_min, y_max = ax.get_ylim()
        y_max = math.ceil(y_max)
        y_min = math.floor(y_min)
        step = max(1, math.ceil((y_max - y_min) / 5))
        ax.set_yticks(range(y_min, y_max + 1, step))
        ax.set_ylim(bottom=0)

    g.set_titles("{col_name}")
    g.set_axis_labels("", "Cantidad")
    g.fig.suptitle("Cantidad de plagas por especie en el tiempo", fontsize=14)
    g.fig.subplots_adjust(top=0.92)  # Leave space for the title

    plt.tight_layout()
    return g.fig


def generate_total_plagas_trend_plot(df: pd.DataFrame) -> None:
    """
    Generate a single plot showing the monthly trend of total pests eliminated.

    Parameters:
    ----------
    df : pd.DataFrame
        The DataFrame with pest count columns

    Returns:
    -------
    None
    """
    # Define pest columns more efficiently
    pest_columns = [
        'Cantidad de Cucaracha Americana',
        'Cantidad de Cucaracha Alemana ',  # Note the trailing space
        'Cantidad de Hormigas',
        'Cantidad de Moscas',
        'Cantidad de Mosquitos',
        'Cantidad de Zancudos',
        'Cantidad de Ratón casero',
        'Cantidad de Rata Noruega',
        'Cantidad de Ratón de tejado',
        'Cantidad de Otras plagas'
    ]

    # Group and sum all pest columns
    trend_df = df.groupby('Mes')[pest_columns].sum().sum(axis=1).reset_index()
    trend_df.columns = ['Mes', 'total']

    # Sort 'Mes' categorically if formatted as 'Mon YYYY'
    try:
        trend_df['Mes'] = pd.Categorical(
            trend_df['Mes'],
            categories=sorted(trend_df['Mes'], key=lambda x: pd.to_datetime(x, format='%b %Y')),
            ordered=True
        )
        trend_df = trend_df.sort_values('Mes')
    except Exception as e:
        print(f"[Warning] Could not parse and sort 'Mes': {e}")

    # Crear figura y eje
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.set_style("whitegrid")


    # Bars
    bars = sns.barplot(data=trend_df, x='Mes', y='total', alpha=0.1, color='steelblue',
                       edgecolor='black', linewidth=0.5, ax=ax)

    # Line
    sns.lineplot(data=trend_df, x='Mes', y='total', color='black', marker='o',
                 markersize=8, linewidth=2, ax=ax)

    # Etiquetas de valores
    for i, (idx, row) in enumerate(trend_df.iterrows()):
        x_pos = bars.patches[i].get_x() + bars.patches[i].get_width() / 2
        y_pos = row['total']
        ax.text(x_pos, y_pos + max(trend_df['total']) * 0.02,
                str(int(row['total'])),
                ha='center', va='bottom',
                fontsize=9, weight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none'))

    # Formato del gráfico
    ax.set_title("Tendencia de eliminación mensual de plagas", fontsize=14, weight='bold', pad=20)
    ax.set_ylabel("Total de plagas eliminadas", fontsize=12)
    ax.set_xlabel("")
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)
    ax.grid(True, axis='y', alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)

    # Eje Y dinámico
    y_max = trend_df['total'].max()
    ax.set_ylim(0, y_max * 1.1)

    if y_max > 1000:
        from matplotlib.ticker import FuncFormatter
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'{int(x):,}'))

    fig.tight_layout()
    return fig









