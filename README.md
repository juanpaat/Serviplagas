# 🐞 Sistema de Reportes Automatizados – Serviplagas
Este repositorio contiene una canalización modular para la generación automatizada de reportes, diseñada específicamente para Serviplagas. El sistema carga datos, genera visualizaciones, crea resúmenes (incluyendo con modelos de lenguaje) y exporta reportes mensuales en formato .docx.

## 📁 Estructura del Proyecto

```bash
automated_reporting/
├── data/                      # Conjuntos de datos crudos y/o limpios
├── outputs/                   # Reportes generados automáticamente
├── reports/                   # Código y plantillas para generación de reportes
├── visualizations/            # Utilidades para generación de gráficos
├── summarizer/                # Estadísticas y scripts relacionados con LLM
├── ingestion/                 # Lógica de carga y limpieza de datos
├── config/                    # Configuraciones, claves API, constantes
├── main.py                    # Orquestador del pipeline
├── requirements.txt           # Dependencias de Python
├── README.md                  # Descripción general y guía de uso
└── .gitignore                 # Exclusiones: datos, claves, etc.
```
## 🚀 Características Principales
- Generación de Reportes Automatizada: Crea reportes mensuales en .docx a partir de datos.
- Ingesta de Datos: Carga y limpieza de archivos .csv.
- Visualización: Generación automática de gráficos.
- Resumen Inteligente: Usa estadísticas y modelos de lenguaje (LLMs) para narrativas automáticas.
- Diseño Modular: Separación clara entre carga de datos, visualización, resumen y reporte. 

## ⚙️ Instalación y Configuración
1. Clona el repositorio

```
git clone https://github.com/tu-org/automated_reporting.git
cd automated_reporting
```

2. Instala las dependencias

```
pip install -r requirements.txt
```

3. Configura el sistema

- Edita config/config.yaml con tus claves API o configuraciones necesarias.

## 🧩 Cómo Usarlo
1. Prepara tus datos de entrada

- Coloca archivos .csv dentro de data/ (por ejemplo, sample_data.csv).

2. Ejecuta el pipeline principal

```
python main.py
```

3. Consulta el resultado

El reporte generado estará disponible en outputs/ (por ejemplo, monthly_report.docx).

## 📌 Descripción de Módulos  

| Módulo            | Descripción                                              |
| ----------------- | -------------------------------------------------------- |
| `data/`           | Datos de entrada (crudos o limpios)                      |
| `ingestion/`      | Carga y limpieza de datos (`data_loader.py`)             |
| `summarizer/`     | Generación de resúmenes estadísticos y narrativas (LLMs) |
| `visualizations/` | Generación de gráficos a partir de los datos             |
| `reports/`        | Construcción del reporte final (`report_builder.py`)     |
| `config/`         | Configuraciones generales y claves API                   |
| `outputs/`        | Carpeta con los reportes generados                       |


## 🛠 Personalización
- Cambiar Fuente de Datos: Sustituye el archivo en data/ o ajusta data_loader.py.
- Agregar Nuevos Gráficos: Modifica plot_generator.py.
- Editar la Plantilla del Reporte: Cambia la lógica de report_builder.py.

## 🧾 Licencia
Este proyecto es propietario y mantenido por Serviplagas. Solo para uso interno.

## 🤝 Contribuciones
Para sugerencias o mejoras, abre un issue o contacta al equipo de desarrollo interno.# Automated Reporting System
