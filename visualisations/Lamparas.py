import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import numpy as np
from datetime import datetime




def plot_estado_lamparas_por_mes(df: pd.DataFrame) -> None:
    """
    Generate a faceted bar/line/point chart showing monthly lamp condition trends.

    Parameters:
    -----------
    df : pd.DataFrame
        Transformed DataFrame with columns: 'Mes', lamp status columns.

    Returns:
    --------
    None
    """
    # Group by month and aggregate lamp states
    grouped = df.groupby('Mes').agg({
        'Buena potencia': 'sum',
        'Deteriorada': 'sum',
        'Apagada': 'sum',
        'Bombillo averiado': 'sum',
        'Desconectada': 'sum',
        'Faltante': 'sum',
        'Lámina saturada': 'sum',
        'Obstruida': 'sum',
        'Baja potencia': 'sum'
    }).reset_index()

    # Melt to long format
    long_df = grouped.melt(id_vars='Mes', var_name='Estado', value_name='Cantidad')

    # Sort 'Mes' categorically if formatted as "Mon YYYY"
    try:
        long_df['Mes'] = pd.Categorical(
            long_df['Mes'],
            categories=sorted(grouped['Mes'], key=lambda x: pd.to_datetime(x, format='%b %Y')),
            ordered=True
        )
    except Exception as e:
        print(f"[Warning] Could not parse and sort 'Mes': {e}")

    # Plot
    g = sns.FacetGrid(long_df, col='Estado', col_wrap=3, sharey=False, sharex=False, height=3.5)
    g.map_dataframe(sns.barplot, x='Mes', y='Cantidad', alpha=0.1, color='steelblue', edgecolor='black')
    g.map_dataframe(sns.lineplot, x='Mes', y='Cantidad', marker='o', color='black')

    for ax in g.axes.flatten():
        # Rotate and size x-axis labels
        ax.tick_params(axis='x', rotation=45, labelsize=6)
        ax.tick_params(axis='x', labelbottom=True)

        # Gridlines
        ax.grid(True, axis='x', alpha=0.3, linestyle='-', linewidth=0.5, color='gray')
        ax.grid(True, axis='y', alpha=0.3, linestyle='-', linewidth=0.5, color='gray')

        # Y-axis scaling and ticks
        y_min, y_max = ax.get_ylim()
        y_max = math.ceil(y_max)
        y_min = math.floor(y_min)
        step = max(1, math.ceil((y_max - y_min) / 5))
        ax.set_yticks(range(y_min, y_max + 1, step))
        ax.set_ylim(bottom=0)

    g.set_titles("{col_name}")
    g.set_axis_labels("", "Cantidad de lámparas")
    g.fig.suptitle("Estado de la estación en el tiempo", fontsize=14)
    g.fig.subplots_adjust(top=0.92)

    plt.tight_layout()
    plt.show()





def plot_estado_lamparas_con_leyenda(df: pd.DataFrame, save_path: str = None) -> None:
    """
    Alternative version with a legend showing status categories and their meanings.

    Parameters:
    -----------
    df : pd.DataFrame
        Transformed DataFrame with 'Mes', 'Lámpara', and lamp status columns.
    save_path : str, optional
        Path to save the plot. If None, plot is displayed only.

    Returns:
    --------
    None
    """


    # Validate input DataFrame
    required_cols = ['Mes', 'Lámpara']
    status_cols = ['Buena potencia', 'Deteriorada', 'Apagada', 'Bombillo averiado',
                   'Desconectada', 'Faltante', 'Lámina saturada', 'Obstruida', 'Baja potencia']

    missing_cols = [col for col in required_cols + status_cols if col not in df.columns]
    if missing_cols:
        print(f"[Error] Missing required columns: {missing_cols}")
        return

    # Find the most recent 'Mes'
    try:
        df = df.copy()  # Avoid modifying original DataFrame
        df['Mes_dt'] = pd.to_datetime(df['Mes'], format='%b %Y', errors='coerce')

        # Check if any dates were parsed successfully
        if df['Mes_dt'].isna().all():
            print("[Error] No valid dates found in 'Mes' column")
            return

        latest_month = df.loc[df['Mes_dt'].notna(), 'Mes_dt'].max()
        ult_mes_str = latest_month.strftime('%b %Y')
        caption = f"Periodo: {ult_mes_str}"

    except Exception as e:
        print(f"[Error] Failed to identify latest month: {e}")
        return

    # Filter to most recent month
    filtered = df[df['Mes_dt'] == latest_month].copy()

    if filtered.empty:
        print(f"[Warning] No data found for the latest month: {ult_mes_str}")
        return

    # Group and summarize lamp conditions
    grouped = filtered.groupby('Lámpara').agg({
        col: 'sum' for col in status_cols
    }).reset_index()

    # Add total visits
    grouped['Total de visitas'] = grouped[status_cols].sum(axis=1)

    # Remove lamps with no visits
    grouped = grouped[grouped['Total de visitas'] > 0]

    if grouped.empty:
        print("[Warning] No lamp data found for visualization")
        return

    # Melt to long format
    all_cols = status_cols + ['Total de visitas']
    long_df = grouped.melt(id_vars='Lámpara',
                           value_vars=all_cols,
                           var_name='Estado',
                           value_name='Cantidad')

    # Keep zeros for small dot visualization
    # long_df['Cantidad'] = long_df['Cantidad'].replace(0, np.nan)  # Keep zeros as small dots

    # Ensure proper ordering of status categories
    long_df['Estado'] = pd.Categorical(long_df['Estado'], categories=all_cols, ordered=True)

    # Enhanced color map
    custom_palette = {
        'Buena potencia': '#2E8B57',  # Sea Green (good condition)
        'Deteriorada': '#FF8C00',  # Dark Orange (needs attention)
        'Apagada': '#FFA500',  # Orange (inactive)
        'Bombillo averiado': '#DC143C',  # Crimson (critical)
        'Desconectada': '#B22222',  # Fire Brick (critical)
        'Faltante': '#8B0000',  # Dark Red (critical)
        'Lámina saturada': '#DAA520',  # Goldenrod (needs maintenance)
        'Obstruida': '#CD853F',  # Peru (needs cleaning)
        'Baja potencia': '#CC0000',  # Red (performance issue)
        'Total de visitas': '#2F4F4F'  # Dark Slate Gray (neutral)
    }

    # Calculate optimal figure size
    n_lamps = len(grouped['Lámpara'].unique())
    n_states = len(all_cols)
    fig_width = max(16, n_states * 0.8)  # Wider for legend
    fig_height = max(8, n_lamps * 0.5)

    # Filter out NaN values for plotting (zeros will remain as small dots)
    plot_data = long_df.dropna(subset=['Cantidad'])

    if plot_data.empty:
        print("[Warning] No data to plot after filtering")
        return

    # Create figure with subplot for legend
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(fig_width, fig_height),
                                   gridspec_kw={'width_ratios': [3, 1]})

    # Main plot on left
    scatter_plot = sns.scatterplot(
        data=plot_data,
        x='Estado',
        y='Lámpara',
        size='Cantidad',
        hue='Estado',
        palette=custom_palette,
        legend=False,
        sizes=(15, 800),  # Smaller minimum size for zeros
        edgecolor='black',
        linewidth=0.7,
        marker='o',
        alpha=0.8,
        ax=ax1
    )

    # Add text labels to main plot (only for values > 0)
    for i, row in plot_data[plot_data['Cantidad'] > 0].iterrows():
        # Choose text color based on bubble color intensity
        estado = row['Estado']
        if estado in ['Total de visitas', 'Bombillo averiado', 'Desconectada', 'Faltante', 'Baja potencia']:
            text_color = 'white'
        else:
            text_color = 'black'

        ax1.text(
            x=row['Estado'],
            y=row['Lámpara'],
            s=int(row['Cantidad']),
            ha='center',
            va='center',
            color=text_color,
            fontsize=8,
            fontweight='bold'
        )

    # Format main plot
    ax1.set_title("Estado de las lámparas por área", fontsize=16, fontweight='bold', pad=20)
    ax1.set_xlabel("Estado de la lámpara", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Área/Lámpara", fontsize=12, fontweight='bold')
    ax1.tick_params(axis='x', rotation=45, labelsize=10)
    ax1.tick_params(axis='y', labelsize=10)
    ax1.grid(True, axis='both', linestyle='--', alpha=0.3, linewidth=0.5)

    # Create custom legend on right
    ax2.axis('off')
    status_meanings = {
        'Buena potencia': 'Funcionando correctamente',
        'Deteriorada': 'Requiere mantenimiento',
        'Apagada': 'Sin funcionamiento',
        'Bombillo averiado': 'Bombillo dañado',
        'Desconectada': 'Sin conexión eléctrica',
        'Faltante': 'Lámpara ausente',
        'Lámina saturada': 'Superficie sucia/saturada',
        'Obstruida': 'Visión obstruida',
        'Baja potencia': 'Potencia insuficiente',
        'Total de visitas': 'Total de inspecciones'
    }

    # Only show legend items that exist in the data
    existing_estados = plot_data['Estado'].unique()

    y_pos = 0.95
    ax2.text(0.05, 0.98, "Leyenda", fontsize=14, fontweight='bold',
             transform=ax2.transAxes, va='top')

    for estado, descripcion in status_meanings.items():
        if estado in existing_estados:
            # Draw colored circle
            ax2.scatter(0.1, y_pos, s=300, c=custom_palette[estado],
                        edgecolor='black', linewidth=1, transform=ax2.transAxes)

            # Add text description
            ax2.text(0.2, y_pos, f"{estado}",
                     fontsize=10, va='center', ha='left', fontweight='bold',
                     transform=ax2.transAxes)
            ax2.text(0.2, y_pos - 0.03, f"{descripcion}",
                     fontsize=9, va='center', ha='left', style='italic',
                     transform=ax2.transAxes, color='gray')
            y_pos -= 0.08

    # Add size legend
    if y_pos > 0.2:  # Only if there's space
        ax2.text(0.05, y_pos - 0.05, "Tamaño del círculo:", fontsize=11, fontweight='bold',
                 transform=ax2.transAxes)
        ax2.text(0.05, y_pos - 0.08, "= Cantidad de casos", fontsize=10,
                 transform=ax2.transAxes, color='gray')

    # Add overall title and caption
    fig.suptitle("Estatus de las estaciones en cada una de las visitas realizadas en el mes",
                 fontsize=14, y=0.98)
    fig.text(0.99, 0.01, caption, horizontalalignment='right',
             fontsize=10, style='italic', alpha=0.7)

    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.92, bottom=0.08)

    # Save or show the plot
    if save_path:
        try:
            plt.savefig(save_path, dpi=300, bbox_inches='tight',
                        facecolor='white', edgecolor='none')
            print(f"Plot saved to: {save_path}")
        except Exception as e:
            print(f"[Error] Failed to save plot: {e}")

    plt.show()





def plot_capturas_especies_por_mes(df: pd.DataFrame) -> None:
    """
    Generate a faceted bar/line/point chart showing monthly captures of various insect species.

    Parameters:
    -----------
    df : pd.DataFrame
        Transformed lamparas DataFrame with 'Mes' and species capture columns.

    Returns:
    --------
    None
    """
    # Ensure 'Otras especies' is numeric
    df['Otras especies'] = pd.to_numeric(df['Otras especies'], errors='coerce').fillna(0).astype(int)

    # Group and summarize by month
    grouped = df.groupby('Mes').agg({
        'mariposas': 'sum',
        'moscas': 'sum',
        'mosquitos': 'sum',
        'polillas': 'sum',
        'zancudos': 'sum',
        'avispas': 'sum',
        'abejas': 'sum',
        'grillos': 'sum',
        'coleópteros': 'sum',
        'Otras especies': 'sum'
    }).reset_index()

    # Melt to long format
    long_df = grouped.melt(id_vars='Mes', var_name='Especie', value_name='Cantidad')

    # Ensure Mes is ordered chronologically
    try:
        long_df['Mes'] = pd.Categorical(
            long_df['Mes'],
            categories=sorted(grouped['Mes'], key=lambda x: pd.to_datetime(x, format='%b %Y')),
            ordered=True
        )
    except Exception as e:
        print(f"[Warning] Could not parse and sort 'Mes': {e}")

    # Faceted plot
    g = sns.FacetGrid(long_df, col='Especie', col_wrap=3, sharey=False, sharex=False, height=3.5)
    g.map_dataframe(sns.barplot, x='Mes', y='Cantidad', alpha=0.1, color='steelblue', edgecolor='black')
    g.map_dataframe(sns.lineplot, x='Mes', y='Cantidad', marker='o', color='black')

    # Style each axis
    for ax in g.axes.flatten():
        ax.tick_params(axis='x', rotation=45, labelsize=6)
        ax.tick_params(axis='x', labelbottom=True)
        ax.grid(True, axis='x', alpha=0.3, linestyle='-', linewidth=0.5, color='gray')
        ax.grid(True, axis='y', alpha=0.3, linestyle='-', linewidth=0.5, color='gray')

        # Adjust y-ticks dynamically
        y_min, y_max = ax.get_ylim()
        y_max = math.ceil(y_max)
        y_min = math.floor(y_min)
        step = max(1, math.ceil((y_max - y_min) / 5))
        ax.set_yticks(range(y_min, y_max + 1, step))
        ax.set_ylim(bottom=0)

    g.set_titles("{col_name}")
    g.set_axis_labels("", "Cantidad")
    g.fig.suptitle("Cantidad de capturas de especies por mes", fontsize=14)
    g.fig.subplots_adjust(top=0.92)

    plt.tight_layout()
    plt.show()




def plot_tendencia_total_capturas(df: pd.DataFrame) -> None:
    """
    Generate a bar + line + point chart showing the monthly trend of total species captures.

    Parameters:
    -----------
    df : pd.DataFrame
        Transformed lamparas DataFrame with 'Mes' and species columns.

    Returns:
    --------
    None
    """
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Define species columns more efficiently
    species_cols = [
        'mariposas', 'moscas', 'mosquitos', 'polillas', 'zancudos',
        'avispas', 'abejas', 'grillos', 'coleópteros', 'Otras especies'
    ]

    # Ensure numeric conversion for aggregation
    df_clean = df.copy()
    for col in species_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0).astype(int)

    # Group and sum total captures
    trend_df = df_clean.groupby('Mes')[species_cols].sum().sum(axis=1).reset_index()
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

    # Plotting
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")

    # Create the plot
    ax = plt.gca()

    # Bars
    bars = sns.barplot(data=trend_df, x='Mes', y='total', alpha=0.1, color='steelblue',
                       edgecolor='black', linewidth=0.5, ax=ax)

    # Line
    sns.lineplot(data=trend_df, x='Mes', y='total', color='black', marker='o',
                 markersize=8, linewidth=2, ax=ax)

    # Labels on points - using the actual x positions from the plot
    for i, (idx, row) in enumerate(trend_df.iterrows()):
        # Get the actual x position from the bar plot
        x_pos = bars.patches[i].get_x() + bars.patches[i].get_width() / 2
        y_pos = row['total']

        # Add label with background for better readability
        plt.text(x_pos, y_pos + max(trend_df['total']) * 0.02,
                 str(int(row['total'])),
                 ha='center', va='bottom',
                 fontsize=9, weight='bold',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none'))

    # Formatting
    plt.title("Tendencia de capturas mensuales", fontsize=14, weight='bold', pad=20)
    plt.ylabel("Total de capturas", fontsize=12)
    plt.xlabel("")

    # Improve x-axis labels
    plt.xticks(rotation=45, ha='right', fontsize=10)

    # Add grid for better readability
    ax.grid(True, axis='y', alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)

    # Adjust y-axis to give space for labels
    y_max = trend_df['total'].max()
    ax.set_ylim(0, y_max * 1.1)

    # Format y-axis with thousand separators if values are large
    if y_max > 1000:
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))

    plt.tight_layout()
    plt.show()