"""
Ejemplo simple de cómo usar el nuevo sistema de prompts manipulables.
"""

from prompt_manager import generate_report_with_prompts


def ejemplo_uso_prompts():
    """Ejemplo de cómo trabajar con prompts generados."""
    
    print("🎯 EJEMPLO: Trabajando con Prompts Manipulables")
    print("=" * 60)
    
    # 1. Generar reporte y obtener prompts
    print("1️⃣ Generando reporte y prompts...")
    prompt_manager = generate_report_with_prompts("Rionegro")
    
    # 2. Listar prompts disponibles
    print("\n2️⃣ Prompts disponibles:")
    prompt_manager.list_available_prompts()
    
    # 3. Trabajar con un prompt específico
    print("\n3️⃣ Ejemplo: Manipulando primer prompt de tabla")
    if prompt_manager.prompts_data['table_prompts']:
        # Obtener el primer prompt
        primer_prompt = prompt_manager.prompts_data['table_prompts'][0]
        prompt_id = primer_prompt['id']
        
        print(f"📋 Prompt original (ID: {prompt_id}):")
        prompt_manager.display_prompt(prompt_id)
        
        # Exportar para usar en LLM
        archivo_exportado = prompt_manager.export_prompt_for_llm(prompt_id)
        print(f"📄 Prompt exportado a: {archivo_exportado}")
        
        # Ejemplo de edición (opcional)
        respuesta = input("\n¿Desea editar este prompt? (y/n): ").strip().lower()
        if respuesta == 'y':
            print("💡 Ingrese su versión modificada del prompt:")
            print("(Puede agregar instrucciones específicas, cambiar el formato, etc.)")
            print("Termine con una línea que contenga solo 'END'")
            
            lineas_nuevo_prompt = []
            while True:
                linea = input()
                if linea.strip() == "END":
                    break
                lineas_nuevo_prompt.append(linea)
            
            nuevo_prompt = "\n".join(lineas_nuevo_prompt)
            prompt_manager.edit_prompt(prompt_id, nuevo_prompt)
            
            # Mostrar prompt editado
            print("\n✅ Prompt editado:")
            prompt_manager.display_prompt(prompt_id)
    
    # 4. Exportar todos los prompts
    print("\n4️⃣ Exportando todos los prompts...")
    if prompt_manager.data_manager:
        archivo_todos = "outputs/ejemplo_todos_los_prompts.txt"
        prompt_manager.data_manager.export_prompts_to_file(archivo_todos)
        print(f"📁 Todos los prompts disponibles en: {archivo_todos}")
    
    # 5. Guardar en JSON para manipulación programática
    print("\n5️⃣ Guardando en JSON...")
    archivo_json = prompt_manager.save_prompts_to_json("ejemplo_prompts.json")
    
    print("\n🎉 EJEMPLO COMPLETADO!")
    print("🔧 Opciones de manipulación disponibles:")
    print("   • Editar prompts directamente en código")
    print("   • Exportar prompts individuales para copiar/pegar")
    print("   • Guardar en diferentes formatos (TXT, JSON)")
    print("   • Acceso programático a datos de tablas")
    
    return prompt_manager


def ejemplo_acceso_directo_datos():
    """Ejemplo de cómo acceder directamente a los datos de las tablas."""
    
    print("\n🔍 EJEMPLO: Acceso Directo a Datos de Tablas")
    print("=" * 60)
    
    # Generar prompts
    pm = generate_report_with_prompts("Rionegro")
    
    # Acceder a datos específicos
    for prompt_data in pm.prompts_data['table_prompts']:
        if 'table_data' in prompt_data:
            print(f"\n📊 Tabla: {prompt_data['title']}")
            print(f"   Filas: {len(prompt_data['table_data'])}")
            print(f"   Columnas: {list(prompt_data['table_data'].columns)}")
            print(f"   Primeras 3 filas:")
            print(prompt_data['table_data'].head(3).to_string(index=False))
            print("-" * 40)


if __name__ == "__main__":
    # Ejecutar ejemplo principal
    prompt_manager = ejemplo_uso_prompts()
    
    # Ejemplo adicional de acceso a datos
    respuesta = input("\n¿Desea ver ejemplo de acceso directo a datos? (y/n): ").strip().lower()
    if respuesta == 'y':
        ejemplo_acceso_directo_datos()
