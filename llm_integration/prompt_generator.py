"""
Módulo para generar prompts para el LLM basados en plantillas de configuración.
Este módulo carga plantillas de prompts desde archivos YAML y genera las tablas 
de datos dinámicamente para insertar en las plantillas.
"""

import pandas as pd
import yaml
import os
from typing import Dict, List, Tuple


class LLMPromptGenerator:
    """Generador de prompts para LLM basado en plantillas configurables."""
    
    def __init__(self, templates_file: str = "config/prompt_templates.yaml"):
        self.templates_file = templates_file
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict:
        """Carga las plantillas de prompts desde el archivo YAML."""
        try:
            with open(self.templates_file, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"⚠️  Archivo de plantillas no encontrado: {self.templates_file}")
            return self._get_default_templates()
        except Exception as e:
            print(f"❌ Error cargando plantillas: {e}")
            return self._get_default_templates()
    
    def _get_default_templates(self) -> Dict:
        """Plantillas por defecto en caso de error al cargar el archivo YAML."""
        return {
            'table_prompts': {},
            'section_prompts': {},
            'general_prompt': {}
        }
    
    def generate_table_description_prompt(self, table_data: pd.DataFrame, 
                                        table_type: str, 
                                        table_subtype: str,
                                        sede: str) -> str:
        """
        Genera un prompt para describir una tabla específica usando plantillas configurables.
        
        Args:
            table_data: DataFrame con los datos de la tabla
            table_type: Tipo de tabla (preventivos, roedores, lamparas)
            table_subtype: Subtipo específico de la tabla
            sede: Sede para la cual se genera el reporte
            
        Returns:
            String con el prompt para el LLM
        """
        # Obtener la plantilla específica
        try:
            template_config = self.templates['table_prompts'][table_type][table_subtype]
            template = template_config['template']
            description = template_config['description']
        except KeyError:
            # Plantilla por defecto si no existe la configuración
            template = self._get_default_table_template()
            description = f"Datos de {table_type} - {table_subtype}"
        
        # Convertir DataFrame a string para incluir en el prompt
        table_str = table_data.to_string(index=False)
        
        # Reemplazar variables en la plantilla
        prompt = template.format(
            sede=sede,
            description=description,
            table_data=table_str
        )
        
        return prompt.strip()
    
    def _get_default_table_template(self) -> str:
        """Plantilla por defecto para tablas."""
        return """
        Analiza la siguiente tabla de datos del reporte de Serviplagas para la sede {sede}.
        
        CONTEXTO: {description}
        
        DATOS:
        {table_data}
        
        INSTRUCCIONES:
        1. Analiza los datos presentados en la tabla
        2. Identifica tendencias, patrones o valores destacables
        3. Menciona cualquier cambio significativo entre períodos
        4. Destaca los valores más altos y más bajos
        5. Proporciona una interpretación clara y concisa de lo que revelan estos datos
        6. Mantén un tono profesional y técnico apropiado para un reporte de control de plagas
        
        Genera una descripción analítica de máximo 150 palabras sobre estos datos.
        """
    
    def generate_section_summary_prompt(self, section_tables: Dict[str, pd.DataFrame], 
                                      section_type: str, 
                                      sede: str) -> str:
        """
        Genera un prompt para resumir todas las tablas de una sección usando plantillas.
        
        Args:
            section_tables: Diccionario con todas las tablas de la sección
            section_type: Tipo de sección (preventivos, roedores, lamparas)
            sede: Sede para la cual se genera el reporte
            
        Returns:
            String con el prompt para el LLM
        """
        # Obtener la plantilla para la sección
        try:
            template_config = self.templates['section_prompts'][section_type]
            template = template_config['template']
        except KeyError:
            # Plantilla por defecto si no existe la configuración
            template = self._get_default_section_template()
        
        # Crear resumen de todas las tablas de la sección
        section_data = self._format_section_data(section_tables)
        
        # Reemplazar variables en la plantilla
        prompt = template.format(
            sede=sede,
            section_data=section_data
        )
        
        return prompt.strip()
    
    def _format_section_data(self, section_tables: Dict[str, pd.DataFrame]) -> str:
        """Formatea los datos de una sección para incluir en el prompt."""
        section_data = ""
        for table_name, table_data in section_tables.items():
            section_data += f"\n--- {table_name.upper()} ---\n"
            section_data += table_data.to_string(index=False)
            section_data += "\n"
        return section_data
    
    def _get_default_section_template(self) -> str:
        """Plantilla por defecto para resúmenes de sección."""
        return """
        Genera un resumen ejecutivo para esta sección del reporte de Serviplagas para la sede {sede}.
        
        DATOS DE LA SECCIÓN:
        {section_data}
        
        INSTRUCCIONES:
        1. Proporciona un resumen ejecutivo que integre los hallazgos de todas las tablas de esta sección
        2. Identifica los aspectos más relevantes del rendimiento en esta área
        3. Menciona tendencias generales y patrones importantes
        4. Destaca cualquier área que requiera atención especial
        5. Evalúa la efectividad general de las medidas de control implementadas
        6. Mantén un enfoque profesional y orientado a la toma de decisiones
        
        Genera un resumen ejecutivo de máximo 200 palabras.
        """
    
    def generate_general_summary_prompt(self, all_data: Dict[str, Dict[str, pd.DataFrame]], 
                                      sede: str) -> str:
        """
        Genera un prompt para el resumen general usando plantillas configurables.
        
        Args:
            all_data: Diccionario con todos los datos organizados por sección
            sede: Sede para la cual se genera el reporte
            
        Returns:
            String con el prompt para el LLM
        """
        # Obtener la plantilla para el resumen general
        try:
            template_config = self.templates['general_prompt']
            template = template_config['template']
        except KeyError:
            # Plantilla por defecto si no existe la configuración
            template = self._get_default_general_template()
        
        # Crear un resumen compacto de todos los datos
        all_data_formatted = self._format_all_data(all_data)
        
        # Reemplazar variables en la plantilla
        prompt = template.format(
            sede=sede,
            all_data=all_data_formatted
        )
        
        return prompt.strip()
    
    def _format_all_data(self, all_data: Dict[str, Dict[str, pd.DataFrame]]) -> str:
        """Formatea todos los datos para el resumen general."""
        data_summary = ""
        section_names = {
            'preventivos': 'SERVICIOS PREVENTIVOS',
            'roedores': 'CONTROL DE ROEDORES', 
            'lamparas': 'CONTROL DE INSECTOS VOLADORES'
        }
        
        for section_type, section_tables in all_data.items():
            data_summary += f"\n=== {section_names.get(section_type, section_type.upper())} ===\n"
            
            for table_name, table_data in section_tables.items():
                # Solo incluir un resumen de cada tabla para no sobrecargar el prompt
                if not table_data.empty:
                    data_summary += f"\n{table_name}:\n"
                    # Incluir solo las primeras y últimas filas para un resumen
                    if len(table_data) > 4:
                        summary_data = pd.concat([table_data.head(2), table_data.tail(2)])
                    else:
                        summary_data = table_data
                    data_summary += summary_data.to_string(index=False)
                    data_summary += "\n"
        
        return data_summary
    
    def _get_default_general_template(self) -> str:
        """Plantilla por defecto para el resumen general."""
        return """
        Genera un resumen ejecutivo integral del reporte mensual de control de plagas para {sede}.
        
        DATOS CONSOLIDADOS DEL REPORTE:
        {all_data}
        
        INSTRUCCIONES:
        1. Proporciona una evaluación integral del estado del programa de control de plagas
        2. Identifica las tendencias más significativas across todas las áreas de control
        3. Evalúa la efectividad general de las medidas preventivas y correctivas implementadas
        4. Destaca los logros principales y las áreas que requieren mejora
        5. Proporciona recomendaciones estratégicas para el próximo período
        6. Incluye una evaluación del riesgo general de plagas en la instalación
        7. Mantén un enfoque ejecutivo apropiado para la dirección de la institución
        
        Genera un resumen ejecutivo integral de máximo 300 palabras que sirva como conclusión del reporte.
        """
    
    def get_template_info(self) -> Dict:
        """Retorna información sobre las plantillas cargadas."""
        info = {
            'templates_file': self.templates_file,
            'table_prompts_count': 0,
            'section_prompts_count': 0,
            'general_prompt_exists': bool(self.templates.get('general_prompt')),
            'sections': []
        }
        
        if 'table_prompts' in self.templates:
            for section, tables in self.templates['table_prompts'].items():
                info['table_prompts_count'] += len(tables)
                info['sections'].append({
                    'section': section,
                    'tables': list(tables.keys())
                })
        
        if 'section_prompts' in self.templates:
            info['section_prompts_count'] = len(self.templates['section_prompts'])
        
        return info
    
    def reload_templates(self):
        """Recarga las plantillas desde el archivo."""
        self.templates = self._load_templates()
        print(f"✅ Plantillas recargadas desde: {self.templates_file}")


def print_prompt_with_separator(prompt: str, title: str):
    """
    Imprime un prompt con separadores visuales para facilitar la lectura.
    
    Args:
        prompt: El prompt a imprimir
        title: Título del prompt
    """
    separator = "=" * 80
    print(f"\n{separator}")
    print(f"🤖 PROMPT PARA LLM: {title}")
    print(separator)
    print(prompt)
    print(separator)
    print()


def preview_templates(templates_file: str = "config/prompt_templates.yaml"):
    """
    Función utilitaria para previsualizar las plantillas disponibles.
    
    Args:
        templates_file: Ruta al archivo de plantillas
    """
    generator = LLMPromptGenerator(templates_file)
    info = generator.get_template_info()
    
    print("📋 INFORMACIÓN DE PLANTILLAS DE PROMPTS")
    print("=" * 60)
    print(f"📁 Archivo: {info['templates_file']}")
    print(f"📊 Prompts de tablas: {info['table_prompts_count']}")
    print(f"📂 Prompts de sección: {info['section_prompts_count']}")
    print(f"📑 Prompt general: {'✅' if info['general_prompt_exists'] else '❌'}")
    
    print("\n🔍 SECCIONES DISPONIBLES:")
    for section_info in info['sections']:
        print(f"   • {section_info['section'].upper()}")
        for table in section_info['tables']:
            print(f"     - {table}")
    
    print(f"\n💡 Para editar las plantillas, modifica: {templates_file}")


if __name__ == "__main__":
    # Mostrar información de las plantillas cuando se ejecuta directamente
    preview_templates()
