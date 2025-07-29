import pandas as pd
from typing import Union
import os

def load_data(source: str) -> pd.DataFrame:
    """
    Carga datos desde un archivo CSV local o una URL.
    
    Args:
        source: Ruta al archivo CSV local o URL
        
    Returns:
        pd.DataFrame: DataFrame con los datos cargados
        
    Raises:
        RuntimeError: Si hay error al cargar los datos
    """
    try:
        # Determinar si es archivo local o URL
        if source.startswith(('http://', 'https://')):
            print(f"📡 Cargando datos desde URL: {source[:50]}...")
            return pd.read_csv(source, sep=';', low_memory=False)
        else:
            # Verificar que el archivo existe
            if not os.path.exists(source):
                raise FileNotFoundError(f"Archivo no encontrado: {source}")
                
            print(f"📁 Cargando datos desde archivo: {source}")
            return pd.read_csv(source, sep=';', low_memory=False)
            
    except Exception as e:
        raise RuntimeError(f"Error cargando datos desde {source}: {e}")


def load_data_with_fallback(local_path: str, url_fallback: str) -> pd.DataFrame:
    """
    Intenta cargar datos desde archivo local, si falla usa URL como fallback.
    
    Args:
        local_path: Ruta al archivo CSV local
        url_fallback: URL de fallback si no se encuentra el archivo local
        
    Returns:
        pd.DataFrame: DataFrame con los datos cargados
    """
    try:
        return load_data(local_path)
    except (FileNotFoundError, RuntimeError) as e:
        print(f"⚠️  No se pudo cargar archivo local: {e}")
        print(f"🔄 Intentando cargar desde URL fallback...")
        return load_data(url_fallback)
