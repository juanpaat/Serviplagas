import pandas as pd
import calendar

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













'''
def concatenate_non_nulls(row):
    # Filter out null values and concatenate the rest
    return ' '.join(row.dropna().astype(str))

preventivos['Área'] = preventivos[['Ubicación Bloque 1','Ubicación Bloque 2','Ubicación Bloque 3',
                                   'Ubicación Bloque 4', 'Ubicación Bloque 5 (verde)', 'Ubicación Bloque 6', 'Ubicación Bloque 7',
                                   'Ubicación Bloque 8', 'Ubicación Bloque 9', 'Ubicación Bloque 10', 'Ubicación Bloque 11',
                                   'Ubicación Bloque 12', 'Ubicación Bloque 13', 'Ubicación Bloque 14', 'Ubicación Bloque 15',
                                   'Ubicación Bloque 16', 'Ubicación Bloque 17','Acopio de Basuras y portería',
                                   'Plantas de Emergencias', 'Áreas Quirúrgicas', 'Cuartos técnicos y gases medicinales',
                                   'Zona externa', 'Torre A', 'Torre B', 'Torre C', 'Torre D']].apply(concatenate_non_nulls, axis=1)
preventivos['Bloque/Torre'] = preventivos[['Torre o Área','Bloque o Área']].apply(concatenate_non_nulls, axis=1)

# List of 'Técnicos' columns
tecnicos_cols = [col for col in preventivos.columns if col.startswith('Técnicos/')]

# Function to concatenate names
def concatenate_tecnicos(row):
    return ', '.join([col.split('/')[1] for col in tecnicos_cols if row[col] == 1])

preventivos['Técnicos'] = preventivos[tecnicos_cols].apply(concatenate_tecnicos, axis=1)

preventivos.columns = [col.replace('Evidencia de plagas/', '') for col in preventivos.columns]
# Select columns that start with "Cantidad"
cantidad_columns = [col for col in preventivos.columns if col.startswith('Cantidad')]

# Convert these columns to integers, replacing nulls with 0
for col in cantidad_columns:
    preventivos[col] = preventivos[col].fillna(0).astype(int)

# Assuming df is your DataFrame and 'fecha' is the column to be converted
preventivos['Fecha'] = pd.to_datetime(preventivos['Fecha'])

# Function to format the month and year
def format_mes_ano(dt):
    month_name = calendar.month_name[dt.month]
    return f"{month_name[:3]} {dt.year}"

# Apply the function to create the 'Mes' column
preventivos['Mes'] = preventivos['Fecha'].apply(format_mes_ano)

preventivos.rename(columns={'Evidencia de plagas': 'Plagas evidenciadas',
                            'Cantidad de hallazgos de ${Otras_plagas_evidenciadas}': 'Cantidad de Otras plagas',
                            'Detalles del hallazgo de ${Otras_plagas_evidenciadas}': 'Detalles del hallazgo de Otras plagas',
                            'Servicio verificado por': 'Acompañante',
                            'OBSERVACIONES' : 'Observaciones',
                            'Cuales otras plagase evidenció?':'Otras plagas',
                            'Plaguicidas': 'Plaguicidas utilizados',
                            '_index' : 'ID'},
                   inplace=True)

# identificar las columnas que empiezan por 'Detalles del hallazgo de '
detail_columns = [col for col in preventivos.columns if col.startswith('Detalles del hallazgo de ')]

# Step 2: Define the concatenation function
def concatenate_details(row):
    # Concatenate non-NA values with the column name and a colon
    details = [f"{col}: {row[col]}" for col in detail_columns if pd.notna(row[col])]
    return ', '.join(details)

# Step 3: Apply the function to create the 'Hallazgos' column
preventivos['Hallazgos'] = preventivos.apply(concatenate_details, axis=1)


# Replace 'Cantidad de hallazgos de ' with 'Cantidad de ' for each relevant column
preventivos.columns = [col.replace('Cantidad de hallazgos ', 'Cantidad ') if col.startswith('Cantidad de hallazgos ') else col for col in preventivos.columns]


preventivos['Otras plagas'] = preventivos['Otras plagas'].fillna('No')
preventivos['Observaciones'] = preventivos['Observaciones'].fillna('Sin observaciones')


preventivos = preventivos[['ID','Fecha', 'Mes', 'Sede', 'Código','Bloque/Torre','Área', 'Técnicos', 'Plagas evidenciadas',
                           'Cucaracha Americana', 'Cucaracha Alemana', 'Hormigas', 'Moscas',
                           'Mosquitos', 'Ratón casero', 'Rata Noruega', 'Ratón de tejado', 'Otras',
                           'Sin evidencia', 'Zancudos', 'Otras plagas',
                           'Cantidad de Cucaracha Americana',
                           'Cantidad de Cucaracha Alemana ',
                           'Cantidad de Hormigas',
                           'Cantidad de Moscas',
                           'Cantidad de Mosquitos',
                           'Cantidad de Zancudos',
                           'Cantidad de Ratón casero',
                           'Cantidad de Rata Noruega',
                           'Cantidad de Ratón de tejado',
                           'Cantidad de Otras plagas','Plaguicidas utilizados', 'Acompañante',
                           'Observaciones' ]]

'''