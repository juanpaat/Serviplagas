"""
Script de demostración de las nuevas funcionalidades del sistema Serviplagas.
Este script muestra ejemplos de uso de las funciones refactorizadas.
"""

import pandas as pd
from llm_integration.prompt_generator import LLMPromptGenerator, print_prompt_with_separator
from reports.report_builder import ReportDataManager


def demo_llm_prompt_generation():
    """Demuestra la generación de prompts LLM con datos de ejemplo."""
    
    print("🎯 DEMOSTRACIÓN: Generación de Prompts LLM")
    print("=" * 60)
    
    # Crear datos de ejemplo para demostración
    sample_preventivos_data = pd.DataFrame({
        'Mes': ['Mar 2024', 'Apr 2024', 'May 2024'],
        'Cantidad de órdenes': [15, 18, 12],
        'Cantidad de áreas': [45, 52, 38],
        'Áreas con plaga': [8, 12, 6]
    })
    
    sample_roedores_data = pd.DataFrame({
        'Mes': ['Mar 2024', 'Apr 2024', 'May 2024'],
        'Consumido': [24, 31, 19],
        'Sin novedad': [156, 142, 168],
        'Presencia de roedores': [8, 12, 5]
    })
    
    sample_lamparas_data = pd.DataFrame({
        'Mes': ['Mar 2024', 'Apr 2024', 'May 2024'],
        'total': [1245, 1567, 998]
    })
    
    # Inicializar generador de prompts
    llm_generator = LLMPromptGenerator()
    
    # Ejemplo 1: Prompt para tabla individual
    print("\n📊 EJEMPLO 1: Análisis de tabla individual")
    prompt1 = llm_generator.generate_table_description_prompt(
        sample_preventivos_data, 
        'preventivos', 
        'order_area', 
        'Rionegro'
    )
    print_prompt_with_separator(prompt1, "Preventivos - Órdenes vs Áreas")
    
    # Ejemplo 2: Uso del ReportDataManager
    print("\n📋 EJEMPLO 2: Gestión completa de datos")
    data_manager = ReportDataManager()
    
    # Simular el proceso de almacenamiento y análisis
    data_manager.store_table_data('preventivos', 'order_area', sample_preventivos_data)
    data_manager.store_table_data('roedores', 'station_status', sample_roedores_data)
    data_manager.store_table_data('lamparas', 'captures_trend', sample_lamparas_data)
    
    # Generar resumen de sección
    data_manager.generate_section_summary_prompt('preventivos', 'Rionegro')
    
    # Generar resumen general
    data_manager.generate_general_summary_prompt('Rionegro')
    
    print("\n✅ Demostración completada!")


def demo_data_management():
    """Demuestra el manejo mejorado de datos."""
    
    print("\n🗂️  DEMOSTRACIÓN: Gestión de Datos")
    print("=" * 60)
    
    # Crear instancia del gestor
    data_manager = ReportDataManager()
    
    # Mostrar estructura de datos
    print("📁 Estructura de almacenamiento de datos:")
    for section in data_manager.section_data:
        print(f"   📂 {section.upper()}")
        if data_manager.section_data[section]:
            for table_name in data_manager.section_data[section]:
                print(f"      📄 {table_name}")
        else:
            print(f"      🈳 (vacío)")
    
    # Mostrar descripciones de tablas disponibles
    print("\n📋 Tipos de análisis disponibles:")
    for section, tables in data_manager.llm_generator.table_descriptions.items():
        print(f"\n🔹 {section.upper()}")
        for table_type, description in tables.items():
            print(f"   • {table_type}: {description}")


def demo_configuration():
    """Demuestra el uso del sistema de configuración."""
    
    print("\n⚙️  DEMOSTRACIÓN: Sistema de Configuración")
    print("=" * 60)
    
    try:
        from config.settings import API_URLS, LOCAL_FILES, LLM_CONFIG, SEDES
        
        print("🌐 URLs de APIs configuradas:")
        for data_type, url in API_URLS.items():
            print(f"   • {data_type}: {url[:50]}...")
        
        print("\n📁 Archivos locales configurados:")
        for data_type, path in LOCAL_FILES.items():
            print(f"   • {data_type}: {path}")
        
        print("\n🤖 Configuración LLM:")
        for key, value in LLM_CONFIG.items():
            print(f"   • {key}: {value}")
        
        print(f"\n🏢 Sedes configuradas: {SEDES}")
        
    except ImportError as e:
        print(f"❌ Error importando configuración: {e}")


def main():
    """Función principal de demostración."""
    
    print("🎪 DEMO DEL SISTEMA SERVIPLAGAS REFACTORIZADO")
    print("=" * 80)
    print("Este script demuestra las nuevas funcionalidades implementadas.")
    print()
    
    try:
        # Ejecutar demostraciones
        demo_configuration()
        demo_data_management() 
        demo_llm_prompt_generation()
        
        print("\n🎉 Todas las demostraciones completadas exitosamente!")
        print("\n💡 PRÓXIMOS PASOS:")
        print("   1. Ejecutar 'python main.py' para generar reportes completos")
        print("   2. Ejecutar 'python test_llm_integration.py' para pruebas")
        print("   3. Integrar API de LLM real modificando config/settings.py")
        
    except Exception as e:
        print(f"❌ Error durante la demostración: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
