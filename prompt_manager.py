"""
Script para manipular y trabajar con los prompts generados del sistema Serviplagas.
Este script permite cargar, editar, revisar y enviar prompts a LLM de forma controlada.
"""

import os
import json
from typing import Dict, List, Optional
from data_processing.data_loader import load_data_with_fallback
from data_processing.data_cleaner import (
    transform_preventivos_df, 
    transform_roedores_df, 
    transform_lamparas_df
)
from reports.report_builder import generate_enhanced_report
from config.settings import API_URLS, LOCAL_FILES, SEDES


class PromptManager:
    """Gestor para manipular prompts generados del sistema Serviplagas."""
    
    def __init__(self, data_manager=None):
        self.data_manager = data_manager
        self.prompts_data = None
        
    def load_prompts_from_data_manager(self, data_manager):
        """Carga prompts desde un ReportDataManager."""
        self.data_manager = data_manager
        self.prompts_data = data_manager.get_all_prompts()
        
    def list_available_prompts(self):
        """Lista todos los prompts disponibles."""
        if not self.prompts_data:
            print("❌ No hay prompts cargados. Ejecutar generate_report_with_prompts() primero.")
            return
        
        print("📋 PROMPTS DISPONIBLES PARA MANIPULACIÓN")
        print("=" * 60)
        
        # Prompts de tablas
        print(f"\n🔍 PROMPTS DE TABLAS INDIVIDUALES ({len(self.prompts_data['table_prompts'])})")
        for i, prompt_data in enumerate(self.prompts_data['table_prompts'], 1):
            print(f"   {i}. {prompt_data['title']} (ID: {prompt_data['id']})")
        
        # Prompts de sección
        print(f"\n📂 PROMPTS DE SECCIÓN ({len(self.prompts_data['section_prompts'])})")
        for section, prompt_data in self.prompts_data['section_prompts'].items():
            print(f"   • {prompt_data['title']} (ID: section_{section})")
        
        # Prompt general
        if self.prompts_data['general_prompt']:
            print(f"\n🌐 PROMPT GENERAL")
            print(f"   • {self.prompts_data['general_prompt']['title']} (ID: general)")
        
        print(f"\nTotal de prompts: {self.get_total_prompts_count()}")
    
    def get_prompt_by_id(self, prompt_id: str) -> Optional[Dict]:
        """Obtiene un prompt específico por su ID."""
        if not self.prompts_data:
            return None
        
        # Buscar en prompts de tabla
        for prompt_data in self.prompts_data['table_prompts']:
            if prompt_data['id'] == prompt_id:
                return prompt_data
        
        # Buscar en prompts de sección
        for section, prompt_data in self.prompts_data['section_prompts'].items():
            if f"section_{section}" == prompt_id:
                return prompt_data
        
        # Verificar prompt general
        if prompt_id == "general" and self.prompts_data['general_prompt']:
            return self.prompts_data['general_prompt']
        
        return None
    
    def display_prompt(self, prompt_id: str):
        """Muestra un prompt específico con formato."""
        prompt_data = self.get_prompt_by_id(prompt_id)
        if not prompt_data:
            print(f"❌ Prompt con ID '{prompt_id}' no encontrado.")
            return
        
        print("=" * 80)
        print(f"🤖 PROMPT: {prompt_data['title']}")
        print("=" * 80)
        print(prompt_data['prompt'])
        print("=" * 80)
        
        # Mostrar tabla si está disponible
        if 'table_data' in prompt_data and not prompt_data['table_data'].empty:
            print("\n📊 TABLA ASOCIADA:")
            print("-" * 40)
            print(prompt_data['table_data'].to_string(index=False))
            print("-" * 40)
    
    def edit_prompt(self, prompt_id: str, new_prompt: str):
        """Edita un prompt específico."""
        if self.data_manager:
            success = self.data_manager.update_prompt(prompt_id, new_prompt)
            if success:
                print(f"✅ Prompt '{prompt_id}' actualizado exitosamente.")
                # Actualizar datos locales también
                prompt_data = self.get_prompt_by_id(prompt_id)
                if prompt_data:
                    prompt_data['prompt'] = new_prompt
            else:
                print(f"❌ No se pudo actualizar el prompt '{prompt_id}'.")
        else:
            print("❌ No hay data_manager disponible para editar prompts.")
    
    def export_prompt_for_llm(self, prompt_id: str, filename: Optional[str] = None):
        """Exporta un prompt específico listo para copiar a LLM."""
        prompt_data = self.get_prompt_by_id(prompt_id)
        if not prompt_data:
            print(f"❌ Prompt con ID '{prompt_id}' no encontrado.")
            return
        
        if not filename:
            filename = f"prompt_{prompt_id.replace('_', '-')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"PROMPT PARA LLM: {prompt_data['title']}\n")
            f.write("=" * 60 + "\n\n")
            f.write(prompt_data['prompt'])
            f.write("\n\n")
            f.write("INSTRUCCIONES DE USO:\n")
            f.write("1. Copiar todo el contenido del prompt\n")
            f.write("2. Pegar en ChatGPT, Claude, o el LLM de tu preferencia\n")
            f.write("3. Ajustar si es necesario antes de enviar\n")
        
        print(f"✅ Prompt exportado a: {filename}")
        return filename
    
    def get_total_prompts_count(self) -> int:
        """Retorna el número total de prompts generados."""
        if not self.prompts_data:
            return 0
        
        table_count = len(self.prompts_data['table_prompts'])
        section_count = len(self.prompts_data['section_prompts'])
        general_count = 1 if self.prompts_data['general_prompt'] else 0
        
        return table_count + section_count + general_count
    
    def save_prompts_to_json(self, filename: str = "prompts_data.json"):
        """Guarda todos los prompts en formato JSON para manipulación programática."""
        if not self.prompts_data:
            print("❌ No hay prompts para guardar.")
            return
        
        # Preparar datos para JSON (convertir DataFrames a dict)
        json_data = {
            'table_prompts': [],
            'section_prompts': {},
            'general_prompt': None
        }
        
        # Procesar prompts de tabla
        for prompt_data in self.prompts_data['table_prompts']:
            json_prompt = prompt_data.copy()
            if 'table_data' in json_prompt:
                json_prompt['table_data'] = json_prompt['table_data'].to_dict('records')
            json_data['table_prompts'].append(json_prompt)
        
        # Procesar prompts de sección
        for section, prompt_data in self.prompts_data['section_prompts'].items():
            json_prompt = prompt_data.copy()
            if 'section_tables' in json_prompt:
                section_tables_json = {}
                for table_name, table_df in json_prompt['section_tables'].items():
                    section_tables_json[table_name] = table_df.to_dict('records')
                json_prompt['section_tables'] = section_tables_json
            json_data['section_prompts'][section] = json_prompt
        
        # Procesar prompt general
        if self.prompts_data['general_prompt']:
            json_prompt = self.prompts_data['general_prompt'].copy()
            if 'all_data' in json_prompt:
                all_data_json = {}
                for section, section_tables in json_prompt['all_data'].items():
                    section_json = {}
                    for table_name, table_df in section_tables.items():
                        section_json[table_name] = table_df.to_dict('records')
                    all_data_json[section] = section_json
                json_prompt['all_data'] = all_data_json
            json_data['general_prompt'] = json_prompt
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Prompts guardados en JSON: {filename}")
        return filename


def generate_report_with_prompts(sede: str = "Rionegro") -> PromptManager:
    """
    Genera un reporte y retorna un PromptManager para manipular los prompts.
    
    Args:
        sede: Sede para la cual generar el reporte
        
    Returns:
        PromptManager: Gestor de prompts para manipulación
    """
    print(f"🚀 Generando reporte con prompts manipulables para sede: {sede}")
    
    # Cargar datos
    df_preventivo = transform_preventivos_df(
        load_data_with_fallback(LOCAL_FILES['preventivos'], API_URLS['preventivos'])
    )
    df_roedores = transform_roedores_df(
        load_data_with_fallback(LOCAL_FILES['roedores'], API_URLS['roedores'])
    )
    df_lamparas = transform_lamparas_df(
        load_data_with_fallback(LOCAL_FILES['lamparas'], API_URLS['lamparas'])
    )
    
    # Generar reporte y obtener data_manager
    report_path, data_manager = generate_enhanced_report(
        df_preventivo, df_roedores, df_lamparas, sede
    )
    
    # Crear PromptManager
    prompt_manager = PromptManager()
    prompt_manager.load_prompts_from_data_manager(data_manager)
    
    print(f"✅ Reporte generado. Prompts listos para manipulación.")
    print(f"📊 Total de prompts: {prompt_manager.get_total_prompts_count()}")
    
    return prompt_manager


def interactive_prompt_session():
    """Sesión interactiva para trabajar con prompts."""
    print("🎯 SESIÓN INTERACTIVA DE PROMPTS")
    print("=" * 50)
    
    # Generar prompts
    sede = input("Ingrese la sede (Rionegro/Medellín) [Rionegro]: ").strip()
    if not sede:
        sede = "Rionegro"
    
    print(f"\n📋 Generando prompts para sede: {sede}")
    prompt_manager = generate_report_with_prompts(sede)
    
    while True:
        print("\n🔧 OPCIONES DISPONIBLES:")
        print("1. Listar todos los prompts")
        print("2. Ver prompt específico")
        print("3. Editar prompt")
        print("4. Exportar prompt para LLM")
        print("5. Exportar todos los prompts")
        print("6. Guardar en JSON")
        print("0. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            prompt_manager.list_available_prompts()
        
        elif opcion == "2":
            prompt_id = input("Ingrese el ID del prompt: ").strip()
            prompt_manager.display_prompt(prompt_id)
        
        elif opcion == "3":
            prompt_id = input("Ingrese el ID del prompt a editar: ").strip()
            print("Ingrese el nuevo prompt (termine con una línea que contenga solo 'END'):")
            new_prompt_lines = []
            while True:
                line = input()
                if line.strip() == "END":
                    break
                new_prompt_lines.append(line)
            new_prompt = "\n".join(new_prompt_lines)
            prompt_manager.edit_prompt(prompt_id, new_prompt)
        
        elif opcion == "4":
            prompt_id = input("Ingrese el ID del prompt a exportar: ").strip()
            filename = input("Nombre del archivo (opcional): ").strip()
            filename = filename if filename else None
            prompt_manager.export_prompt_for_llm(prompt_id, filename)
        
        elif opcion == "5":
            if prompt_manager.data_manager:
                filename = f"outputs/todos_los_prompts_{sede}.txt"
                prompt_manager.data_manager.export_prompts_to_file(filename)
        
        elif opcion == "6":
            filename = input("Nombre del archivo JSON [prompts_data.json]: ").strip()
            filename = filename if filename else "prompts_data.json"
            prompt_manager.save_prompts_to_json(filename)
        
        elif opcion == "0":
            print("👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción no válida.")


if __name__ == "__main__":
    # Ejemplo de uso básico
    print("📝 GESTOR DE PROMPTS SERVIPLAGAS")
    print("=" * 40)
    
    # Opción 1: Uso programático
    print("\n1️⃣ Generando prompts para manipulación...")
    pm = generate_report_with_prompts("Rionegro")
    pm.list_available_prompts()
    
    # Mostrar primer prompt como ejemplo
    if pm.prompts_data['table_prompts']:
        first_prompt_id = pm.prompts_data['table_prompts'][0]['id']
        print(f"\n🔍 Ejemplo - Mostrando primer prompt (ID: {first_prompt_id}):")
        pm.display_prompt(first_prompt_id)
    
    # Opción 2: Sesión interactiva
    respuesta = input("\n¿Desea iniciar sesión interactiva? (y/n): ").strip().lower()
    if respuesta == 'y':
        interactive_prompt_session()
