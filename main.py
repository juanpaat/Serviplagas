from data_processing.data_loader import load_data_with_fallback
from data_processing.data_cleaner import (
    transform_preventivos_df, 
    transform_roedores_df, 
    transform_lamparas_df
)
from reports.report_builder import generate_enhanced_report
from config.settings import API_URLS, LOCAL_FILES, SEDES

def main():
    """
    Función principal para generar reportes de Serviplagas con análisis LLM.
    Intenta cargar datos locales primero, luego usa APIs como fallback.
    """
    print("🚀 Iniciando sistema de reportes Serviplagas")
    print("=" * 50)
    
    # Cargar y transformar datos con fallback
    print("📊 Cargando y transformando datos...")
    
    df_preventivo = transform_preventivos_df(
        load_data_with_fallback(LOCAL_FILES['preventivos'], API_URLS['preventivos'])
    )
    
    df_roedores = transform_roedores_df(
        load_data_with_fallback(LOCAL_FILES['roedores'], API_URLS['roedores'])
    )
    
    df_lamparas = transform_lamparas_df(
        load_data_with_fallback(LOCAL_FILES['lamparas'], API_URLS['lamparas'])
    )

    print("✅ Datos cargados y transformados exitosamente")
    
    # Generar reportes para todas las sedes configuradas
    print("\n📄 Generando reportes...")
    for sede in SEDES:
        print(f"🏢 Procesando sede: {sede}")
        report_path, data_manager = generate_enhanced_report(df_preventivo, df_roedores, df_lamparas, sede=sede)
        
        # Mostrar resumen de prompts generados
        all_prompts = data_manager.get_all_prompts()
        table_count = len(all_prompts['table_prompts'])
        section_count = len(all_prompts['section_prompts'])
        general_count = 1 if all_prompts['general_prompt'] else 0
        
        print(f"   📊 Prompts generados: {table_count} tablas, {section_count} secciones, {general_count} general")
    
    print("\n🎉 Proceso completado exitosamente!")


if __name__ == "__main__":
    main()