import pandas as pd
import calendar
from typing import List


################################################
################ Preventivos ###################
################################################


UBICACION_COLUMNS = ['Ubicación Bloque 1','Ubicación Bloque 2','Ubicación Bloque 3',
                                   'Ubicación Bloque 4', 'Ubicación Bloque 5 (verde)', 'Ubicación Bloque 6', 'Ubicación Bloque 7',
                                   'Ubicación Bloque 8', 'Ubicación Bloque 9', 'Ubicación Bloque 10', 'Ubicación Bloque 11',
                                   'Ubicación Bloque 12', 'Ubicación Bloque 13', 'Ubicación Bloque 14', 'Ubicación Bloque 15',
                                   'Ubicación Bloque 16', 'Ubicación Bloque 17','Acopio de Basuras y portería',
                                   'Plantas de Emergencias', 'Áreas Quirúrgicas', 'Cuartos técnicos y gases medicinales',
                                   'Zona externa', 'Torre A', 'Torre B', 'Torre C', 'Torre D']

BLOQUE_TORRE_COLUMNS = ['Torre o Área', 'Bloque o Área']

COLUMN_RENAMES = {'Evidencia de plagas': 'Plagas evidenciadas',
                            'Cantidad de hallazgos de ${Otras_plagas_evidenciadas}': 'Cantidad de Otras plagas',
                            'Detalles del hallazgo de ${Otras_plagas_evidenciadas}': 'Detalles del hallazgo de Otras plagas',
                            'Servicio verificado por': 'Acompañante',
                            'OBSERVACIONES' : 'Observaciones',
                            'Cuales otras plagase evidenció?':'Otras plagas',
                            'Plaguicidas': 'Plaguicidas utilizados',
                            '_index' : 'ID'}

def concatenate_non_nulls(row):
    """Concatenate non-null values in a row, separated by a space."""
    return ' '.join(row.dropna().astype(str))

def concatenate_tecnicos(row, tecnicos_cols):
    """Concatenate technician names from one-hot encoded columns."""
    return ', '.join([col.split('/')[1] for col in tecnicos_cols if row[col] == 1])


def format_mes_ano(date):
    """Format a datetime as 'Mon YYYY'."""
    if pd.isnull(date):
        return None
    return f"{calendar.month_name[date.month][:3]} {date.year}"


def concatenate_details(row, detail_columns):
    """Concatenate details with column name prefix for non-null values."""
    return ', '.join([f"{col}: {row[col]}" for col in detail_columns if pd.notna(row[col])])


def transform_preventivos_df(df: pd.DataFrame) -> pd.DataFrame:
    """Transform the 'preventivos' DataFrame according to the business rules."""
    df = df.copy()

    # Create 'Área' and 'Bloque/Torre' columns
    df['Área'] = df[UBICACION_COLUMNS].apply(concatenate_non_nulls, axis=1)
    df['Bloque/Torre'] = df[BLOQUE_TORRE_COLUMNS].apply(concatenate_non_nulls, axis=1)

    # Process Técnicos
    tecnicos_cols = [col for col in df.columns if col.startswith('Técnicos/')]
    df['Técnicos'] = df.apply(lambda row: concatenate_tecnicos(row, tecnicos_cols), axis=1)

    # Clean column names for 'Evidencia de plagas/'
    df.columns = [col.replace('Evidencia de plagas/', '') for col in df.columns]

    # Convert 'Cantidad' columns to int
    cantidad_cols = [col for col in df.columns if col.startswith('Cantidad')]
    df[cantidad_cols] = df[cantidad_cols].fillna(0).astype(int)

    # Format Fecha and Mes
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    df['Mes'] = df['Fecha'].apply(format_mes_ano)

    # Rename columns
    df.rename(columns=COLUMN_RENAMES, inplace=True)

    # Concatenate hallazgos (details)
    detail_cols = [col for col in df.columns if col.startswith('Detalles del hallazgo de ')]
    df['Hallazgos'] = df.apply(lambda row: concatenate_details(row, detail_cols), axis=1)

    # Clean column names starting with 'Cantidad de hallazgos'
    df.columns = [col.replace('Cantidad de hallazgos ', 'Cantidad ') if col.startswith('Cantidad de hallazgos ') else col for col in df.columns]

    # Fill missing values
    df['Otras plagas'] = df['Otras plagas'].fillna('No')
    df['Observaciones'] = df['Observaciones'].fillna('Sin observaciones')

    # Final column selection
    final_columns = [
        'ID', 'Fecha', 'Mes', 'Sede', 'Código', 'Bloque/Torre', 'Área', 'Técnicos', 'Plagas evidenciadas',
        'Cucaracha Americana', 'Cucaracha Alemana', 'Hormigas', 'Moscas', 'Mosquitos', 'Ratón casero',
        'Rata Noruega', 'Ratón de tejado', 'Otras', 'Sin evidencia', 'Zancudos', 'Otras plagas',
        'Cantidad de Cucaracha Americana', 'Cantidad de Cucaracha Alemana ', 'Cantidad de Hormigas',
        'Cantidad de Moscas', 'Cantidad de Mosquitos', 'Cantidad de Zancudos', 'Cantidad de Ratón casero',
        'Cantidad de Rata Noruega', 'Cantidad de Ratón de tejado', 'Cantidad de Otras plagas',
        'Plaguicidas utilizados', 'Acompañante', 'Observaciones'
    ]
    return df[final_columns]





################################################
################## Roedores ####################
################################################



def _extract_tecnicos(df: pd.DataFrame, prefix: str = 'Técnicos/') -> pd.Series:
    """Concatenate technician names based on one-hot encoded columns."""
    tecnicos_cols = [col for col in df.columns if col.startswith(prefix)]

    def concatenate_tecnicos(row):
        return ', '.join([col.split('/')[1] for col in tecnicos_cols if row[col] == 1])

    return df[tecnicos_cols].apply(concatenate_tecnicos, axis=1)


def _combine_station_numbers(row: pd.Series) -> str:
    """Concatenate station numbers from two locations."""
    values = []
    if pd.notna(row.get('Número de estación Medellín')):
        values.append(str(row['Número de estación Medellín']))
    if pd.notna(row.get('Número de estación Rionegro')):
        values.append(str(row['Número de estación Rionegro']))
    return ' '.join(values)


def _format_mes_ano(date: pd.Timestamp) -> str:
    """Format datetime into abbreviated month and year."""
    if pd.isnull(date):
        return ""
    return f"{calendar.month_name[date.month][:3]} {date.year}"


def _concat_estacion_estado(df: pd.DataFrame, prefix: str = 'Estado de la estación/') -> pd.Series:
    """Concatenate the station status columns into a single readable string."""
    estaciones_cols = [col for col in df.columns if col.startswith(prefix)]

    def concatenar_estaciones(row):
        return ' - '.join([col.split('/')[1] for col in estaciones_cols if row[col] == 1])

    return df[estaciones_cols].apply(concatenar_estaciones, axis=1)


def transform_roedores_df(df: pd.DataFrame) -> pd.DataFrame:
    """Transform the raw 'roedores' DataFrame according to business rules."""
    df = df.copy()

    # Técnicos
    df['Técnicos'] = _extract_tecnicos(df)

    # Número de estación
    df['Numero de estación'] = df.apply(_combine_station_numbers, axis=1)
    df['Numero de estación'] = df['Numero de estación'].astype(float).astype(int)

    # Merge consumido & consumo
    if 'Estado de la estación/Cambio de cebo por consumo' in df.columns:
        df['Estado de la estación/Consumido'] = df[[
            'Estado de la estación/Consumido',
            'Estado de la estación/Cambio de cebo por consumo'
        ]].max(axis=1)
        df.drop('Estado de la estación/Cambio de cebo por consumo', axis=1, inplace=True)

    # Convert date and extract month
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    df['Mes'] = df['Fecha'].apply(_format_mes_ano)

    # Concatenate station status columns
    df['Estado de la estación'] = _concat_estacion_estado(df)

    # Rename columns
    df.rename(columns={
        'OBSERVACIONES': 'Observaciones',
        'Plaguicida': 'Plaguicidas utilizados',
        '_index': 'ID'
    }, inplace=True)

    # Clean column names: strip status prefix
    df.columns = [
        col.replace('Estado de la estación/', '') if col.startswith('Estado de la estación/') else col
        for col in df.columns
    ]

    # Fill missing observations
    df['Observaciones'] = df['Observaciones'].fillna('Sin observaciones')

    # Final selection of columns
    final_columns = [
        'ID',
        'Fecha',
        'Mes',
        'Sede',
        'Numero de estación',
        'Técnicos',
        'Estado de la estación',
        'Consumido',
        'Instalación',
        'Sin novedad',
        'Presencia de roedores',
        'Presencia de bioindicador',
        'Cambio de cebo por deterioro',
        'Desaparecida',
        'Estación dañada',
        'Estación bloqueada',
        'Localización',
        'Plaguicidas utilizados',
        'Observaciones'
    ]

    return df[final_columns]




################################################
################## Lámparas ####################
################################################


def _format_mes_ano(date: pd.Timestamp) -> str:
    """Format a datetime object into abbreviated month and year (e.g. 'Mar 2024')."""
    if pd.isnull(date):
        return ""
    return f"{calendar.month_name[date.month][:3]} {date.year}"


def _concatenate_binary_columns(row: pd.Series, columns: List[str], prefix: str) -> str:
    """Concatenate labels from one-hot columns if their value is 1."""
    return ', '.join([col.split(f'{prefix}/')[1] for col in columns if row[col] == 1])


def _combine_non_null_values(row: pd.Series, columns: List[str]) -> str:
    """Combine values from a list of columns if not null."""
    return ' '.join([str(row[col]) for col in columns if pd.notna(row[col])])


def transform_lamparas_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the 'lamparas' DataFrame to a cleaned and structured format.

    Parameters:
    -----------
    df : pd.DataFrame
        The raw input DataFrame containing lamp inspection data.

    Returns:
    --------
    pd.DataFrame
        Transformed DataFrame ready for analysis or reporting.
    """
    df = df.copy()

    # Convert and extract formatted date
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    df['Mes'] = df['Fecha'].apply(_format_mes_ano)

    # Técnicos
    tecnicos_cols = [col for col in df.columns if col.startswith('Técnicos/')]
    df['Técnicos'] = df[tecnicos_cols].apply(
        lambda row: _concatenate_binary_columns(row, tecnicos_cols, 'Técnicos'),
        axis=1
    )

    # Concatenate lamp numbers
    df['Lámpara'] = df.apply(
        lambda row: _combine_non_null_values(row, ['Lámpara Rionegro', 'Lámparas Medellín']),
        axis=1
    )

    # Estado de la lámpara
    lamp_status_cols = [col for col in df.columns if col.startswith('Estado de la lámpara/')]
    df['Estado de la lámpara'] = df[lamp_status_cols].apply(
        lambda row: _concatenate_binary_columns(row, lamp_status_cols, 'Estado de la lámpara'),
        axis=1
    )

    # Especies encontradas
    species_cols = [col for col in df.columns if col.startswith('Especies encontradas/')]
    df['Especies encontradas'] = df[species_cols].apply(
        lambda row: _concatenate_binary_columns(row, species_cols, 'Especies encontradas'),
        axis=1
    )

    # Combine 'Cual otra especie encontró?'
    df['Especies encontradas'] = df.apply(
        lambda row: _combine_non_null_values(row, ['Especies encontradas', 'Cual otra especie encontró?']),
        axis=1
    )

    # Fill missing counts
    count_cols = [col for col in df.columns if col.startswith('Cantidad de ')]
    df[count_cols] = df[count_cols].fillna(0)

    # Clean column names and standardize
    df.rename(columns={
        'OBSERVACIONES': 'Observaciones',
        '_index': 'ID',
        'Cantidad de ${Otra_especie_encontrada}': 'Cantidad de Otras especies'
    }, inplace=True)

    df.columns = [
        col.replace('Estado de la lámpara/', '') if col.startswith('Estado de la lámpara/') else col
        for col in df.columns
    ]
    df.columns = [
        col.replace('Cantidad de ', '') if col.startswith('Cantidad de ') else col
        for col in df.columns
    ]

    # Fill missing observations
    df['Observaciones'] = df['Observaciones'].fillna('Sin observaciones')

    # Final column order
    final_columns = [
        'ID', 'Fecha', 'Mes', 'Técnicos', 'Sede', 'Lámpara', 'Estado de la lámpara',
        'Buena potencia', 'Deteriorada', 'Apagada',
        'Bombillo averiado', 'Desconectada', 'Faltante', 'Lámina saturada',
        'Obstruida', 'Baja potencia', 'Estado del tubo', 'Especies encontradas',
        'mariposas', 'moscas', 'mosquitos', 'polillas', 'zancudos',
        'avispas', 'abejas', 'grillos', 'coleópteros',
        'Otras especies', 'Observaciones'
    ]

    return df[final_columns]