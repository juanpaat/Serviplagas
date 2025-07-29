"""
Configuración del sistema Serviplagas.
Este archivo contiene configuraciones globales para el sistema de reportes.
"""

# =============================================================================
# CONFIGURACIÓN DE DATOS
# =============================================================================

# URLs de las APIs de KoBoToolbox
API_URLS = {
    'preventivos': 'https://kf.kobotoolbox.org/api/v2/assets/aB3FoJyiCjAoXF5ejP69Au/export-settings/esKWukg9yLKZkandHs49J3K/data.csv',
    'roedores': 'https://kf.kobotoolbox.org/api/v2/assets/a9E2TU2PJxCqH3JWtZv9Lb/export-settings/esKnrocymz3R8tnVC99afC7/data.csv',
    'lamparas': 'https://kf.kobotoolbox.org/api/v2/assets/aJQdE5dQrEh3j8Q26LzGUo/export-settings/esR8A6WquxNsjcsqihXgCMx/data.csv'
}

# Archivos CSV locales
LOCAL_FILES = {
    'preventivos': 'data/Preventivos.csv',
    'roedores': 'data/Roedores.csv',
    'lamparas': 'data/Lámparas.csv'
}

# =============================================================================
# CONFIGURACIÓN LLM
# =============================================================================

# Configuración para integración futura con APIs LLM
LLM_CONFIG = {
    'enabled': False,  # Cambiar a True cuando se tenga API key
    'provider': 'openai',  # 'openai', 'anthropic', 'local'
    'model': 'gpt-4',
    'max_tokens': 500,
    'temperature': 0.3
}

# Claves API (usar variables de entorno en producción)
API_KEYS = {
    'openai': None,  # os.getenv('OPENAI_API_KEY')
    'anthropic': None,  # os.getenv('ANTHROPIC_API_KEY')
}

# =============================================================================
# CONFIGURACIÓN DEL REPORTE
# =============================================================================

# Configuración del documento Word
DOCUMENT_CONFIG = {
    'logo_path': 'Logo/logo2021.png',
    'logo_width_inches': 3.25,
    'table_style': 'Table Grid',
    'figure_width_inches': 5.5,
    'figure_dpi': 300,
    # 🆕 Configuración para mostrar prompts en documentos (solo para revisión)
    'include_prompts_in_document': True,  # Cambiar a False para versión final sin prompts
    'prompt_style': 'detailed',  # 'detailed' o 'compact'
    'show_llm_placeholders': True  # Mostrar marcadores donde irían las respuestas del LLM
}

# Texto introductorio del reporte
REPORT_INTRO = (
    "A continuación, el resultado del ejercicio del séptimo mes (marzo) del ciclo de análisis de 12 meses "
    "con un nuevo recorrido mensual del PROGRAMA DE PREVENCIÓN DE PLAGAS DE IMPORTANCIA EN SALUD PÚBLICA (PPPISP) "
    "en las instalaciones del Hospital San Vicente Rionegro, se realizaron rondas preventivas del cronograma mensual "
    "con el propósito de controlar la presencia de insectos rastreros, voladores y roedores de menor importancia "
    "en los 4 bloques asistenciales y administrativos. Adicionalmente, se llevaron a cabo inspecciones en las "
    "estaciones de control de roedores y en las estaciones de luz para a combatir los insectos voladores. "
    "Asimismo, se efectuaron labores de mantenimiento en áreas verdes, espacios comunes, sumideros y sistemas "
    "de alcantarillado. Por último, se atendieron todas las novedades y mantenimientos correctivos solicitados "
    "a través del formato o por medio del grupo de WhatsApp."
)

# =============================================================================
# CONFIGURACIÓN DE SEDES
# =============================================================================

SEDES = ['Rionegro', 'Medellín']

# =============================================================================
# CONFIGURACIÓN DE LOGGING
# =============================================================================

LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file_path': 'logs/serviplagas.log'
}

# =============================================================================
# CONFIGURACIÓN DE PROMPTS LLM
# =============================================================================

# Configuración para los prompts del LLM
PROMPT_CONFIG = {
    'max_table_rows_display': 20,  # Máximo número de filas a mostrar en prompts
    'analysis_max_words': 150,     # Máximo de palabras para análisis individual
    'section_summary_max_words': 200,  # Máximo de palabras para resumen de sección
    'general_summary_max_words': 300,  # Máximo de palabras para resumen general
    'language': 'spanish',
    'professional_tone': True
}
