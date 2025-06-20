import pandas as pd

def load_data(filepath: str) -> pd.DataFrame:
    try:
        return pd.read_csv(filepath, sep = ';', low_memory=False)
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")
