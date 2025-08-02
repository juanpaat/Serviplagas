from data_processing.data_loader import load_data_with_fallback
from data_processing.data_cleaner import (
    transform_preventivos_df, 
    transform_roedores_df, 
    transform_lamparas_df
)
from reports.report_builder import generate_enhanced_report
from reports.hospital_san_vicente_generator import generate_hospital_san_vicente_report
from system_cleaner import perform_system_cleanup
from config.settings import API_URLS, LOCAL_FILES, SEDES

def main():
    """
    Función principal mejorada para generar reportes de Serviplagas.
    Ahora genera tanto reportes estándar como reportes específicos del Hospital San Vicente.
    Al final realiza limpieza automática del sistema.
    """
    print("🏥 SISTEMA DE REPORTES SERVIPLAGAS - HOSPITAL SAN VICENTE")
    print("=" * 65)
    print("📋 Generando reportes automatizados con plantilla oficial")
    print("=" * 65)
    
    # Cargar y transformar datos con fallback
    print("\n📊 CARGA DE DATOS")
    print("-" * 30)
    
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
    
    # Generar reportes mejorados para Hospital San Vicente
    print("\n🏥 GENERACIÓN DE REPORTES HOSPITAL SAN VICENTE")
    print("-" * 50)
    
    hospital_reports = []
    for sede in SEDES:
        print(f"\n🏢 Procesando sede: {sede}")
        try:
            # Generar reporte específico del Hospital San Vicente
            hospital_report_path = generate_hospital_san_vicente_report(
                df_preventivo, df_roedores, df_lamparas, sede
            )
            hospital_reports.append(hospital_report_path)
            
        except Exception as e:
            print(f"❌ Error generando reporte para {sede}: {e}")
            continue
    
    # También generar reportes estándar con prompts LLM (para comparación)
    print("\n📊 GENERACIÓN DE REPORTES ESTÁNDAR CON LLM")
    print("-" * 50)
    
    standard_reports = []
    for sede in SEDES:
        print(f"\n🔧 Procesando sede estándar: {sede}")
        try:
            report_path, data_manager = generate_enhanced_report(
                df_preventivo, df_roedores, df_lamparas, sede=sede
            )
            standard_reports.append(report_path)
            
            # Mostrar resumen de prompts generados
            all_prompts = data_manager.get_all_prompts()
            table_count = len(all_prompts['table_prompts'])
            section_count = len(all_prompts['section_prompts'])
            general_count = 1 if all_prompts['general_prompt'] else 0
            
            print(f"   📊 Prompts LLM: {table_count} tablas, {section_count} secciones, {general_count} general")
            
        except Exception as e:
            print(f"❌ Error generando reporte estándar para {sede}: {e}")
            continue
    
    # Resumen final
    print("\n" + "=" * 65)
    print("🎉 PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 65)
    
    print(f"\n📋 REPORTES GENERADOS:")
    print(f"   🏥 Hospital San Vicente: {len(hospital_reports)} reportes")
    for report in hospital_reports:
        print(f"      📄 {report}")
    
    print(f"\n   🔧 Reportes Estándar LLM: {len(standard_reports)} reportes")  
    for report in standard_reports:
        print(f"      📄 {report}")
        
    print(f"\n💡 Los reportes del Hospital San Vicente están listos para producción.")
    print(f"📁 Los archivos están disponibles en la carpeta 'outputs/'")
    
    # Realizar limpieza automática del sistema
    print(f"\n🧹 LIMPIEZA AUTOMÁTICA DEL SISTEMA")
    print("-" * 40)
    
    try:
        cleanup_summary = perform_system_cleanup(create_backup=True)
        print(f"✅ Limpieza completada. Archivos eliminados: {len(cleanup_summary['files_removed'])}")
        print(f"📦 Backup disponible: {cleanup_summary.get('backup_created', 'No creado')}")
    except Exception as e:
        print(f"⚠️  Error durante la limpieza: {e}")
        print(f"💡 El sistema continúa funcionando normalmente")
    
    print(f"\n🚀 SISTEMA LISTO PARA PRODUCCIÓN")
    
    return hospital_reports, standard_reports


if __name__ == "__main__":
    main()