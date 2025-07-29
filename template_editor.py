#!/usr/bin/env python3
"""
Script de ejemplo para trabajar con plantillas de prompts editables.
Este script demuestra cómo personalizar los prompts sin tocar el código principal.
"""

import yaml
import os
from llm_integration.prompt_generator import LLMPromptGenerator, preview_templates


def edit_template_example():
    """Ejemplo de cómo editar una plantilla específica."""
    
    print("🔧 EJEMPLO: Cómo personalizar plantillas de prompts")
    print("=" * 60)
    
    # 1. Mostrar plantillas actuales
    print("\n1️⃣ Plantillas actuales:")
    preview_templates()
    
    # 2. Cargar el archivo YAML
    templates_file = "config/prompt_templates.yaml"
    with open(templates_file, 'r', encoding='utf-8') as file:
        templates = yaml.safe_load(file)
    
    # 3. Ejemplo de modificación de una plantilla
    print("\n2️⃣ Modificando plantilla de ejemplo...")
    
    # Modificar la plantilla de preventivos -> order_area
    original_template = templates['table_prompts']['preventivos']['order_area']['template']
    
    # Ejemplo: añadir una instrucción específica
    templates['table_prompts']['preventivos']['order_area']['template'] = original_template + """
        
        ANÁLISIS ADICIONAL REQUERIDO:
        - Calcula el porcentaje de efectividad por mes
        - Identifica correlaciones entre órdenes y áreas con plagas
        - Sugiere optimizaciones del cronograma de mantenimiento
        """
    
    # 4. Guardar las modificaciones (opcional - descomentado para ejemplo)
    # with open(f"{templates_file}.backup", 'w', encoding='utf-8') as backup_file:
    #     yaml.dump(templates, backup_file, default_flow_style=False, allow_unicode=True)
    
    print("✅ Ejemplo de modificación completado")
    print("💡 Las plantillas se pueden editar directamente en el archivo YAML")
    
    # 5. Mostrar cómo recargar plantillas sin reiniciar
    print("\n3️⃣ Recargando plantillas modificadas...")
    generator = LLMPromptGenerator()
    generator.reload_templates()


def create_custom_template():
    """Ejemplo de cómo crear una plantilla personalizada."""
    
    print("\n🎨 EJEMPLO: Crear plantilla personalizada")
    print("=" * 50)
    
    # Plantilla personalizada de ejemplo
    custom_template = {
        'title': 'ANÁLISIS PERSONALIZADO - Mi Plantilla',
        'description': 'Análisis personalizado para casos específicos',
        'template': """
        Realiza un análisis personalizado de los datos para {sede}.
        
        CONTEXTO ESPECÍFICO: {description}
        
        DATOS A ANALIZAR:
        {table_data}
        
        INSTRUCCIONES PERSONALIZADAS:
        1. Enfócate en aspectos críticos para la gerencia
        2. Incluye métricas de costo-beneficio
        3. Proporciona alertas tempranas de problemas
        4. Sugiere KPIs específicos para seguimiento
        5. Considera impacto en la reputación institucional
        
        FORMATO DE SALIDA:
        - Resumen ejecutivo (2-3 líneas)
        - Hallazgos clave (máximo 5 puntos)
        - Recomendaciones inmediatas
        - Seguimiento sugerido
        
        Máximo 200 palabras, enfoque ejecutivo.
        """
    }
    
    print("Plantilla personalizada creada:")
    print(f"📄 Título: {custom_template['title']}")
    print(f"📝 Descripción: {custom_template['description']}")
    print("\n💡 Para agregar esta plantilla al sistema:")
    print("   1. Abre config/prompt_templates.yaml")
    print("   2. Añade la nueva plantilla en la sección apropiada")
    print("   3. Guarda el archivo")
    print("   4. El sistema la cargará automáticamente")


def backup_and_restore_templates():
    """Funciones para respaldar y restaurar plantillas."""
    
    print("\n💾 GESTIÓN DE RESPALDOS DE PLANTILLAS")
    print("=" * 50)
    
    templates_file = "config/prompt_templates.yaml"
    backup_file = f"{templates_file}.backup"
    
    # Crear respaldo
    if os.path.exists(templates_file):
        with open(templates_file, 'r', encoding='utf-8') as original:
            with open(backup_file, 'w', encoding='utf-8') as backup:
                backup.write(original.read())
        print(f"✅ Respaldo creado: {backup_file}")
    
    print("\n📋 Comandos útiles:")
    print(f"   Crear respaldo: cp {templates_file} {backup_file}")
    print(f"   Restaurar: cp {backup_file} {templates_file}")
    print("   Editar: nano/vim/code config/prompt_templates.yaml")


def validate_templates():
    """Valida que las plantillas tienen el formato correcto."""
    
    print("\n✅ VALIDACIÓN DE PLANTILLAS")
    print("=" * 40)
    
    try:
        generator = LLMPromptGenerator()
        info = generator.get_template_info()
        
        print("🔍 Validación completada:")
        print(f"   📊 Prompts de tablas: {info['table_prompts_count']}")
        print(f"   📂 Prompts de sección: {info['section_prompts_count']}")
        print(f"   📑 Prompt general: {'✅' if info['general_prompt_exists'] else '❌'}")
        
        if info['table_prompts_count'] > 0:
            print("✅ Todas las plantillas se cargaron correctamente")
        else:
            print("⚠️  No se encontraron plantillas de tabla")
            
    except Exception as e:
        print(f"❌ Error en las plantillas: {e}")
        print("💡 Verifica la sintaxis YAML del archivo")


if __name__ == "__main__":
    print("🎛️  EDITOR DE PLANTILLAS DE PROMPTS - SERVIPLAGAS")
    print("=" * 70)
    
    # Ejecutar ejemplos
    edit_template_example()
    create_custom_template()
    backup_and_restore_templates()
    validate_templates()
    
    print("\n🎯 RESUMEN:")
    print("   • Las plantillas están en config/prompt_templates.yaml")
    print("   • Edita el archivo YAML para personalizar los prompts")
    print("   • El sistema carga automáticamente los cambios")
    print("   • Siempre haz respaldos antes de modificar")
    print("   • Usa este script para validar cambios")
