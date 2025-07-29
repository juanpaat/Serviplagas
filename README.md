# 🐞 Sistema de Reportes Automatizados – Serviplagas

Un sistema automatizado para generar reportes de control de plagas que integra análisis de datos, visualizaciones avanzadas y generación de prompts para LLM.

## 🆕 Nuevas Características (Versión con Plantillas Configurables)

### 🎛️ Plantillas de Prompts Editables
- **Prompts definidos en archivos YAML** configurables
- **Edición sin tocar código** - solo modifica `config/prompt_templates.yaml`
- **Recarga automática** de plantillas sin reiniciar el sistema
- **Plantillas por tipo de análisis** personalizables
- **Variables dinámicas** para datos y contexto

### 🤖 Integración LLM Mejorada
- **Generación automática de prompts** usando plantillas configurables
- **Separación clara** entre lógica y contenido de prompts
- **Resúmenes por sección** con plantillas personalizables
- **Análisis contextual** con instrucciones específicas editables

### 📊 Gestión Avanzada de Plantillas
- **Editor de plantillas** (`template_editor.py`) para personalización
- **Validación automática** de sintaxis YAML
- **Sistema de respaldos** para cambios seguros
- **Previsualización** de plantillas disponibles

### 📊 Gestión Mejorada de Datos
- **Almacenamiento estructurado** de tablas para análisis LLM
- **Carga con fallback** (archivos locales → APIs)
- **Documentación completa** de funciones y clases
- **Manejo robusto de errores**

### 🏗️ Arquitectura Refactorizada
- **Separación de responsabilidades** clara
- **Módulo LLM independiente** (`llm_integration/`)
- **Gestión centralizada de datos** (`ReportDataManager`)
- **Funciones modulares** para cada sección del reporte

## 📁 Estructura del Proyecto (Actualizada)

```bash
Serviplagas/
├── data/                          # Conjuntos de datos (CSV locales)
│   ├── Preventivos.csv
│   ├── Roedores.csv
│   └── Lámparas.csv
├── data_processing/               # Carga y limpieza de datos
│   ├── data_loader.py            # ✨ Mejorado con fallback
│   └── data_cleaner.py
├── llm_integration/               # 🆕 Módulo para integración LLM
│   ├── __init__.py
│   └── prompt_generator.py       # Generador de prompts
├── visualisations/               # Generación de gráficos
│   ├── Preventivos.py
│   ├── Roedores.py
│   └── Lamparas.py
├── reports/                      # Construcción de reportes
│   └── report_builder.py        # ✨ Refactorizado con LLM
├── outputs/                      # Reportes generados
├── Logo/                        # Recursos gráficos
├── main.py                      # ✨ Orquestador mejorado (automático)
├── prompt_manager.py            # 🆕 Gestor de prompts manipulables  
├── ejemplo_uso_prompts.py       # 🆕 Ejemplos de manipulación
├── test_llm_integration.py     # 🆕 Script de pruebas
├── requirements.txt
└── README.md                    # 📖 Documentación actualizada
```

## 🧩 Cómo Usar el Sistema Mejorado

### 🚀 Uso Rápido (Automático)
```bash
# Generar reportes + prompts automáticamente
python main.py

# Resultado: 
# ✅ outputs/reporte_serviplagas_Rionegro.docx
# ✅ outputs/prompts_generados_Rionegro.txt
```

### 🔧 Uso Avanzado (Manipulación de Prompts)
```bash
# Trabajar interactivamente con prompts
python prompt_manager.py

# O usar programáticamente
python ejemplo_uso_prompts.py
```

### 🎯 Ejemplo de Manipulación
```python
from prompt_manager import generate_report_with_prompts

# 1. Generar prompts
pm = generate_report_with_prompts("Rionegro")

# 2. Listar prompts disponibles  
pm.list_available_prompts()

# 3. Ver prompt específico con tabla incluida
pm.display_prompt("preventivos_order_area")

# 4. Exportar para copiar a ChatGPT/Claude
pm.export_prompt_for_llm("preventivos_order_area", "mi_analisis.txt")

# 5. Editar prompt si necesario
pm.edit_prompt("preventivos_order_area", "Prompt personalizado...")
```

## 🤖 Funcionalidad LLM (ACTUALIZADA)

### ⚡ **NUEVA FORMA DE TRABAJAR**: Prompts Manipulables

En lugar de mostrar automáticamente los prompts en consola, el sistema ahora:

1. **🔄 Genera silenciosamente** todos los prompts con las tablas incluidas
2. **💾 Almacena** los prompts para manipulación posterior
3. **📁 Exporta** automáticamente a archivos de texto
4. **🔧 Permite editar** y personalizar cada prompt
5. **📋 Provee acceso directo** a datos y tablas asociadas

### 🎯 Flujo de Trabajo Mejorado

#### 1. Generación de Prompts
```python
from prompt_manager import generate_report_with_prompts

# Generar reporte y obtener gestor de prompts
pm = generate_report_with_prompts("Rionegro")

# Los prompts están listos para manipulación
pm.list_available_prompts()
```

#### 2. Manipulación de Prompts
```python
# Ver prompt específico
pm.display_prompt("preventivos_order_area")

# Editar prompt
pm.edit_prompt("preventivos_order_area", "Mi prompt personalizado...")

# Exportar para LLM
pm.export_prompt_for_llm("preventivos_order_area", "mi_prompt.txt")
```

#### 3. Acceso a Datos
```python
# Obtener todos los prompts
all_prompts = pm.get_all_prompts()

# Acceder a tabla específica
tabla_data = all_prompts['table_prompts'][0]['table_data']
```

### 📊 Tipos de Prompts Generados

#### 1. **Prompts de Tablas Individuales** (8 prompts)
- ✅ Preventivos: órdenes/áreas, especies, tendencia
- ✅ Roedores: estado estaciones, eliminación
- ✅ Lámparas: estado mensual, estado detallado, capturas especies, tendencia

#### 2. **Prompts de Resumen por Sección** (3 prompts)
- ✅ Resumen Preventivos
- ✅ Resumen Roedores  
- ✅ Resumen Lámparas

#### 3. **Prompt de Resumen General** (1 prompt)
- ✅ Análisis integral del programa

## 📌 Descripción de Módulos Actualizados

| Módulo                    | Descripción                                              |
| ------------------------- | -------------------------------------------------------- |
| `data/`                  | Datos CSV locales (opcional)                            |
| `data_processing/`       | ✨ Carga mejorada con fallback a APIs                   |
| `llm_integration/`       | 🆕 Generación de prompts para análisis LLM              |
| `visualisations/`        | Generación de gráficos (sin cambios)                    |
| `reports/`               | ✨ Constructor refactorizado con integración LLM         |
| `outputs/`               | Reportes Word generados                                  |

## 🔧 Funciones Principales

### Nueva API Mejorada

```python
# ✨ NUEVO: Generación con prompts manipulables
from prompt_manager import generate_report_with_prompts

pm = generate_report_with_prompts("Rionegro")
pm.list_available_prompts()
pm.display_prompt("preventivos_order_area")
pm.export_prompt_for_llm("preventivos_order_area")

# ⚡ Función principal mejorada (automática)
from reports.report_builder import generate_enhanced_report

report_path, data_manager = generate_enhanced_report(
    df_preventivo, df_roedores, df_lamparas, "Rionegro"
)

# Acceso directo a prompts generados
all_prompts = data_manager.get_all_prompts()
```

### Compatibilidad Hacia Atrás

```python
# Función legacy (aún disponible)
from reports.report_builder import generate_report_in_memory

generate_report_in_memory(df_preventivo, df_roedores, df_lamparas, "Rionegro")
```

## 🚀 Mejoras Implementadas

### 🔄 Manejo de Datos
- ✅ Carga automática con fallback (local → API)
- ✅ Validación robusta de datos
- ✅ Logging mejorado del proceso
- ✅ Gestión centralizada de tablas

### 🤖 Análisis LLM
- ✅ Prompts contextuales para cada tabla
- ✅ Resúmenes estructurados por sección
- ✅ Análisis integral del reporte
- ✅ Instrucciones específicas por tipo de dato

### 🏗️ Arquitectura
- ✅ Separación clara de responsabilidades
- ✅ Módulos independientes y reutilizables
- ✅ Documentación completa
- ✅ Pruebas integradas

### 📋 Documentación
- ✅ Docstrings en todas las funciones
- ✅ Tipos hint para mejor IDE support
- ✅ README actualizado con ejemplos
- ✅ Script de pruebas incluido

## 🔮 Próximos Pasos

1. **Integración API LLM Real**: Conectar con OpenAI, Claude, etc.
2. **Dashboard Web**: Interfaz web para visualizar reportes
3. **Alertas Automáticas**: Notificaciones por email/Slack
4. **Base de Datos**: Almacenamiento histórico de datos
5. **Métricas KPI**: Dashboard de indicadores clave

## 🐛 Solución de Problemas

### Error: No se encuentran archivos CSV
```bash
# El sistema automáticamente usará APIs como fallback
# No requiere acción adicional
```

### Error: Dependencias faltantes
```bash
pip install -r requirements.txt
```

### Error: Logo no encontrado
```bash
# Verificar que existe: Logo/logo2021.png
# O comentar líneas de logo en report_builder.py
```

---

**💡 Nota**: Esta versión refactorizada mantiene compatibilidad total con el código existente mientras añade capacidades avanzadas de análisis LLM.

## 🎛️ Personalización de Prompts con Plantillas YAML

### 📝 Archivo de Plantillas Configurables

El sistema ahora utiliza **plantillas editables** en `config/prompt_templates.yaml` que te permiten personalizar todos los prompts sin modificar código:

```bash
# Editar plantillas
code config/prompt_templates.yaml
# o 
nano config/prompt_templates.yaml

# Validar cambios
python template_editor.py

# Previsualizar plantillas
python llm_integration/prompt_generator.py
```

### 🎯 Tipos de Plantillas

#### 🔍 Prompts de Tablas Individuales
```yaml
table_prompts:
  preventivos:
    order_area:
      title: "PREVENTIVOS - Órdenes vs Áreas"
      description: "Análisis de órdenes de mantenimiento..."
      template: |
        Analiza la siguiente tabla para {sede}.
        
        DATOS:
        {table_data}
        
        INSTRUCCIONES:
        1. Tu análisis personalizado...
        2. Enfócate en aspectos específicos...
```

#### 📂 Prompts de Resumen por Sección
```yaml
section_prompts:
  preventivos:
    title: "RESUMEN EJECUTIVO - Servicios Preventivos"
    template: |
      Genera un resumen ejecutivo para {sede}.
      
      DATOS DE LA SECCIÓN:
      {section_data}
      
      INSTRUCCIONES PERSONALIZADAS:
      1. Evalúa aspectos específicos...
      2. Incluye recomendaciones...
```

### 🔄 Variables Disponibles

- `{sede}` - Nombre de la sede
- `{table_data}` - Datos de la tabla formateados
- `{description}` - Descripción de la tabla
- `{section_data}` - Datos de toda la sección
- `{all_data}` - Todos los datos del reporte

### 🛠️ Flujo de Personalización

1. **Ejecutar sistema:** `python main.py` (genera prompts con plantillas actuales)
2. **Revisar resultados** en `outputs/prompts_generados_[sede].txt`
3. **Editar plantillas** en `config/prompt_templates.yaml` según necesidades
4. **Validar cambios:** `python template_editor.py`
5. **Regenerar:** `python main.py` (usa nuevas plantillas automáticamente)

### 🎨 Ejemplo de Personalización

**Antes (prompt genérico):**
```
Analiza los datos presentados en la tabla...
Genera una descripción analítica de máximo 150 palabras.
```

**Después (personalizado para tu organización):**
```yaml
template: |
  Analiza estos datos para optimización de costos en {sede}.
  
  DATOS FINANCIEROS:
  {table_data}
  
  ANÁLISIS REQUERIDO:
  1. Calcula ROI de intervenciones
  2. Identifica áreas de mayor gasto
  3. Proporciona métricas de eficiencia
  4. Sugiere optimizaciones presupuestarias
  
  Formato ejecutivo, máximo 200 palabras con enfoque en KPIs.
```

### 📊 Ventajas del Sistema de Plantillas

✅ **Sin tocar código** - Solo editas archivos YAML  
✅ **Cambios inmediatos** - El sistema recarga automáticamente  
✅ **Plantillas específicas** - Diferentes enfoques por tipo de análisis  
✅ **Validación automática** - Detecta errores de sintaxis  
✅ **Respaldos seguros** - Sistema de versionado de plantillas  
✅ **Reutilizable** - Mismo formato para todas las sedes  

### 🔧 Herramientas de Gestión

```bash
# Editor completo con ejemplos
python template_editor.py

# Solo validación rápida
python llm_integration/prompt_generator.py

# Respaldo manual
cp config/prompt_templates.yaml config/prompt_templates.yaml.backup

# Restaurar
cp config/prompt_templates.yaml.backup config/prompt_templates.yaml
```

# Automated Reporting System
