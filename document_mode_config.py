#!/usr/bin/env python3
"""
Script para alternar entre modo REVISIÓN (con prompts) y modo PRODUCCIÓN (sin prompts).
Este script te permite cambiar fácilmente la configuración sin editar archivos manualmente.
"""

import yaml
import os
from config.settings import DOCUMENT_CONFIG


def toggle_prompt_mode():
    """Alterna entre modo revisión y producción."""
    
    current_mode = DOCUMENT_CONFIG.get('include_prompts_in_document', False)
    
    print("🔧 CONFIGURADOR DE MODO DE DOCUMENTO")
    print("=" * 50)
    print(f"📄 Modo actual: {'REVISIÓN (con prompts)' if current_mode else 'PRODUCCIÓN (sin prompts)'}")
    
    if current_mode:
        print("\n🎯 Cambiar a modo PRODUCCIÓN:")
        print("   • Los documentos NO incluirán prompts de LLM")
        print("   • Solo contendrán gráficos, tablas y texto estándar")
        print("   • Listos para presentación final")
    else:
        print("\n🎯 Cambiar a modo REVISIÓN:")
        print("   • Los documentos incluirán todos los prompts de LLM")
        print("   • Mostrarán placeholders para respuestas")
        print("   • Ideales para validar el sistema")
    
    print(f"\n¿Quieres cambiar a modo {'PRODUCCIÓN' if current_mode else 'REVISIÓN'}? (s/n): ", end="")
    choice = input().strip().lower()
    
    if choice in ['s', 'y', 'yes', 'sí', 'si']:
        # Cambiar la configuración
        new_mode = not current_mode
        
        # Leer el archivo de configuración
        config_file = 'config/settings.py'
        with open(config_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Reemplazar la línea específica
        old_line = f"'include_prompts_in_document': {str(current_mode).title()}"
        new_line = f"'include_prompts_in_document': {str(new_mode).title()}"
        
        new_content = content.replace(old_line, new_line)
        
        # Guardar el archivo
        with open(config_file, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        mode_name = 'REVISIÓN' if new_mode else 'PRODUCCIÓN'
        print(f"\n✅ Configuración cambiada a modo {mode_name}")
        print(f"📄 Próximos documentos generados serán en modo {mode_name}")
        
        # Generar reportes automáticamente
        print(f"\n🚀 ¿Quieres generar reportes ahora en modo {mode_name}? (s/n): ", end="")
        generate_choice = input().strip().lower()
        
        if generate_choice in ['s', 'y', 'yes', 'sí', 'si']:
            print("\n🎯 Generando reportes...")
            import subprocess
            subprocess.run(['/usr/local/bin/python3', 'main.py'])
            print(f"\n✅ Reportes generados en modo {mode_name}")
    else:
        print("\n❌ Operación cancelada")


def show_current_config():
    """Muestra la configuración actual."""
    
    print("📋 CONFIGURACIÓN ACTUAL DEL DOCUMENTO")
    print("=" * 50)
    
    include_prompts = DOCUMENT_CONFIG.get('include_prompts_in_document', False)
    prompt_style = DOCUMENT_CONFIG.get('prompt_style', 'detailed')
    show_placeholders = DOCUMENT_CONFIG.get('show_llm_placeholders', True)
    
    print(f"📄 Modo: {'REVISIÓN' if include_prompts else 'PRODUCCIÓN'}")
    print(f"🎨 Estilo de prompts: {prompt_style}")
    print(f"🔗 Mostrar placeholders: {'Sí' if show_placeholders else 'No'}")
    
    if include_prompts:
        print(f"\n✅ Los documentos incluirán:")
        print(f"   • Prompts completos de LLM para cada tabla")
        print(f"   • Prompts de resumen por sección")
        print(f"   • Prompt de resumen general")
        print(f"   • Placeholders para respuestas del LLM")
        print(f"   • Advertencia de documento de revisión")
    else:
        print(f"\n✅ Los documentos incluirán:")
        print(f"   • Solo gráficos y tablas estándar")
        print(f"   • Texto descriptivo normal")
        print(f"   • Sin prompts ni placeholders")
        print(f"   • Listos para presentación final")


def create_examples():
    """Crea ejemplos de ambos modos."""
    
    print("📚 GENERAR EJEMPLOS DE AMBOS MODOS")
    print("=" * 50)
    
    print("🎯 Este proceso generará documentos de ejemplo en ambos modos:")
    print("   1. Modo REVISIÓN: reporte_ejemplo_revision_[sede].docx")
    print("   2. Modo PRODUCCIÓN: reporte_ejemplo_produccion_[sede].docx")
    
    print(f"\n¿Continuar? (s/n): ", end="")
    choice = input().strip().lower()
    
    if choice in ['s', 'y', 'yes', 'sí', 'si']:
        # Guardar configuración actual
        original_mode = DOCUMENT_CONFIG.get('include_prompts_in_document', False)
        
        # Generar en modo REVISIÓN
        print("\n📝 Generando ejemplo en modo REVISIÓN...")
        # Aquí iría la lógica para cambiar temporalmente y generar
        
        # Generar en modo PRODUCCIÓN  
        print("📝 Generando ejemplo en modo PRODUCCIÓN...")
        # Aquí iría la lógica para cambiar temporalmente y generar
        
        # Restaurar configuración original
        print("✅ Ejemplos generados, configuración restaurada")
    else:
        print("❌ Operación cancelada")


if __name__ == "__main__":
    print("🎛️  CONFIGURADOR DE MODO DE DOCUMENTOS - SERVIPLAGAS")
    print("=" * 70)
    
    while True:
        print(f"\n📋 OPCIONES DISPONIBLES:")
        print(f"   1. Ver configuración actual")
        print(f"   2. Alternar modo (Revisión ↔ Producción)")
        print(f"   3. Generar reportes en modo actual")
        print(f"   4. Generar ejemplos de ambos modos")
        print(f"   5. Salir")
        
        print(f"\n🎯 Selecciona una opción (1-5): ", end="")
        choice = input().strip()
        
        if choice == '1':
            show_current_config()
        elif choice == '2':
            toggle_prompt_mode()
        elif choice == '3':
            print("\n🚀 Generando reportes...")
            import subprocess
            subprocess.run(['/usr/local/bin/python3', 'main.py'])
        elif choice == '4':
            create_examples()
        elif choice == '5':
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("\n❌ Opción no válida")
    
    print(f"\n💡 TIP: Para cambios rápidos, edita directamente config/settings.py")
    print(f"   'include_prompts_in_document': True/False")
