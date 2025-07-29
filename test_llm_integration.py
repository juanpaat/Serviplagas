"""
Script de prueba para verificar la funcionalidad de los prompts LLM
usando datos CSV locales en lugar de APIs.
"""

from data_processing.data_loader import load_data
from data_processing.data_cleaner import (
    transform_preventivos_df, 
    transform_roedores_df, 
    transform_lamparas_df
)
from reports.report_builder import generate_enhanced_report


def test_llm_integration():
    """Prueba la integración LLM con datos locales."""
    
    print("🧪 INICIANDO PRUEBA DE INTEGRACIÓN LLM")
    print("=" * 50)
    
    try:
        # Cargar datos locales (comentar si no tienes los archivos CSV)
        print("📁 Cargando datos locales...")
        
        # Intentar cargar desde archivos locales primero
        try:
            df_preventivo = transform_preventivos_df(load_data('data/Preventivos.csv'))
            df_roedores = transform_roedores_df(load_data('data/Roedores.csv'))
            df_lamparas = transform_lamparas_df(load_data('data/Lámparas.csv'))
            print("✅ Datos CSV locales cargados exitosamente")
        except Exception as e:
            print(f"⚠️  No se pudieron cargar datos locales: {e}")
            print("📡 Intentando cargar desde APIs...")
            
            # Fallback a APIs
            df_preventivo = transform_preventivos_df(load_data('https://kf.kobotoolbox.org/api/v2/assets/aB3FoJyiCjAoXF5ejP69Au/export-settings/esKWukg9yLKZkandHs49J3K/data.csv'))
            df_roedores = transform_roedores_df(load_data('https://kf.kobotoolbox.org/api/v2/assets/a9E2TU2PJxCqH3JWtZv9Lb/export-settings/esKnrocymz3R8tnVC99afC7/data.csv'))
            df_lamparas = transform_lamparas_df(load_data('https://kf.kobotoolbox.org/api/v2/assets/aJQdE5dQrEh3j8Q26LzGUo/export-settings/esR8A6WquxNsjcsqihXgCMx/data.csv'))
            print("✅ Datos de API cargados exitosamente")
        
        # Verificar que tenemos datos
        print(f"📊 Datos cargados:")
        print(f"   - Preventivos: {len(df_preventivo)} registros")
        print(f"   - Roedores: {len(df_roedores)} registros") 
        print(f"   - Lámparas: {len(df_lamparas)} registros")
        
        # Verificar sedes disponibles
        sedes_preventivos = df_preventivo['Sede'].unique() if 'Sede' in df_preventivo.columns else []
        sedes_roedores = df_roedores['Sede'].unique() if 'Sede' in df_roedores.columns else []
        sedes_lamparas = df_lamparas['Sede'].unique() if 'Sede' in df_lamparas.columns else []
        
        print(f"🏢 Sedes disponibles:")
        print(f"   - Preventivos: {list(sedes_preventivos)}")
        print(f"   - Roedores: {list(sedes_roedores)}")
        print(f"   - Lámparas: {list(sedes_lamparas)}")
        
        # Generar reporte mejorado (solo para la primera sede disponible)
        if len(sedes_preventivos) > 0:
            sede_test = sedes_preventivos[0]
            print(f"\n🚀 Generando reporte de prueba para sede: {sede_test}")
            
            output_path = generate_enhanced_report(
                df_preventivo, df_roedores, df_lamparas, sede=sede_test
            )
            
            print(f"\n✅ Prueba completada exitosamente!")
            print(f"📄 Reporte generado en: {output_path}")
            
        else:
            print("❌ No se encontraron sedes en los datos de preventivos")
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_llm_integration()
