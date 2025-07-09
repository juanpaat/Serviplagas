from data_processing.data_loader import load_data

from data_processing.data_cleaner import transform_preventivos_df
from data_processing.data_cleaner import transform_roedores_df
from data_processing.data_cleaner import transform_lamparas_df

from reports.report_builder import generate_report_in_memory

def main():
    # Cargar y transformar datos
    df_preventivo = transform_preventivos_df(load_data('data/Preventivos.csv'))
    df_roedores = transform_roedores_df(load_data('data/Roedores.csv'))
    df_lamparas = transform_lamparas_df(load_data('data/Lámparas.csv'))

    # Generar reporte Rionegro
    generate_report_in_memory(df_preventivo, df_roedores, df_lamparas, sede="Rionegro")
    # Generar reporte Medellín
    generate_report_in_memory(df_preventivo, df_roedores, df_lamparas, sede="Medellín")


if __name__ == "__main__":
    main()