# 🏥 Sistema de Reportes Automatizados – Hospital San Vicente

Un sistema completamente automatizado para generar reportes oficiales de control de plagas para el Hospital San Vicente, basado en las plantillas y especificaciones oficiales.

## 🆕 NUEVA VERSIÓN - HOSPITAL SAN VICENTE (v2.0)

### 🎯 Características Principales

- **📋 Plantilla Oficial Integrada**: Basada en `PLANTILLA_BASE_INFORME_TECNICO_HOSPITAL_SAN_VICENTE`
- **📚 Guía Práctica Implementada**: Sigue `GUIA_PRACTICA_ELABORACION_INFORMES_MENSUALES`
- **🔄 Variables Dinámicas Automatizadas**: Cálculo automático de métricas y fechas
- **🏥 Formato Hospitalario**: Cumple estándares de salud pública
- **🧹 Limpieza Automática**: Elimina archivos de desarrollo al finalizar
- **📄 Listo para Producción**: Documentos Word finales sin intervención manual

### 🚀 Uso Rápido

```bash
# Generar todos los reportes automatizados
python main.py

# Resultado inmediato:
# ✅ outputs/informe_hospital_san_vicente_rionegro_2025_agosto.docx
# ✅ outputs/informe_hospital_san_vicente_medellin_2025_agosto.docx
# ✅ Sistema limpio y listo para producción
```

## 📁 Estructura del Proyecto (Optimizada)

```bash
Serviplagas/
├── 📄 main.py                                    # ⭐ Punto de entrada principal
├── 📄 system_cleaner.py                         # 🧹 Limpieza automática
├── config/
│   ├── 📄 hospital_san_vicente_template.yaml    # 🏥 Plantilla oficial
│   ├── 📄 settings.py                           # ⚙️ Configuración
│   └── 📄 prompt_templates.yaml                 # 🤖 Templates LLM
├── reports/
│   ├── 📄 hospital_san_vicente_generator.py     # ⭐ Generador principal
│   └── 📄 report_builder.py                     # 🔧 Generador estándar
├── data_processing/                              # 📊 Procesamiento de datos
├── visualisations/                               # 📈 Gráficas
├── llm_integration/                              # 🤖 Integración LLM
├── outputs/                                      # 📁 Reportes generados
└── Logo/                                         # 🖼️ Recursos gráficos
```

## 🏥 Características Hospital San Vicente

### 📋 Variables Dinámicas Automatizadas

El sistema calcula automáticamente:

- **📅 Fechas**: Último día del mes, mes del ciclo, año actual
- **📊 Métricas**: Órdenes SAP, porcentaje cumplimiento, áreas controladas
- **🐛 Análisis de Plagas**: Conteo por especies, grado de infestación
- **🏢 Datos por Sede**: Bloques, estaciones, teléfonos, direcciones
- **📈 Tendencias**: Comparativas mensuales y análisis estadístico

### 🏥 Diferencias por Sede

#### 🏢 Rionegro
- **Bloques**: 4 asistenciales
- **Estaciones Roedores**: 43-46
- **Lámparas**: 7 unidades
- **Contenido Específico**: Control Larvicida en Reservorio
- **Recomendaciones**: Compostaje, bromelias, recirculación agua

#### 🏢 Medellín  
- **Bloques**: 17 asistenciales
- **Estaciones Roedores**: 100+
- **Lámparas**: Variable
- **Contenido Específico**: Hospital Infantil, Dengue, Nuevas Áreas
- **Recomendaciones**: Control palomas, madrigueras, lámparas exteriores

### 📊 Grados de Infestación (Automáticos)

| Grado | Rango | Cumplimiento | Color |
|-------|-------|-------------|--------|
| **BAJO** | ≤ 50 plagas | 80-83% | 🟢 Verde |
| **MEDIO** | 51-200 plagas | 75-80% | 🟡 Amarillo |
| **ALTO** | > 200 plagas | < 75% | 🔴 Rojo |

## 🔄 Flujo Automatizado

### 1. Carga de Datos
```
📊 Datos CSV locales → APIs KoBoToolbox (fallback)
🔄 Transformación automática
✅ Validación de integridad
```

### 2. Generación de Reportes
```
🏥 Plantilla Hospital San Vicente
📋 Variables dinámicas calculadas
📈 Gráficas y tablas generadas
📄 Documento Word final
```

### 3. Limpieza Automática
```
🧹 Eliminación archivos desarrollo
📦 Backup de seguridad
✅ Sistema listo para producción
```

## 🎛️ Configuración Avanzada

### Variables Personalizables

Editar `config/hospital_san_vicente_template.yaml`:

```yaml
# Actualizar información de contacto
contacto:
  nombre: "FERNANDO QUINTERO"
  telefono: "3225241"
  email: "splagasmedellin@gmail.com"

# Modificar rangos de cumplimiento
porcentajes_cumplimiento:
  75: "Mes con incidencias menores"
  80: "Mes estándar"
  83: "Mes con buen desempeño"
```

### Configuración por Sede

```yaml
sedes:
  Rionegro:
    ordenes_tipicas: "33-46"
    estaciones_roedores: "43-46"
    recomendaciones_especificas:
      - "Control específico para Rionegro..."
```

## 🤖 Integración LLM (Opcional)

El sistema mantiene compatibilidad con análisis LLM:

```python
# Generar también prompts para LLM
from reports.report_builder import generate_enhanced_report

report_path, data_manager = generate_enhanced_report(
    df_preventivo, df_roedores, df_lamparas, "Rionegro"
)

# Acceder a prompts generados
prompts = data_manager.get_all_prompts()
```

## 📋 Contenido del Reporte Final

### 🏥 Estructura Oficial

1. **Encabezado y Datos Generales**
   - Código F-PMYV-04, Versión 06 *(FIJO)*
   - Información cliente por sede *(VARIABLE)*
   - Métricas del período *(DINÁMICO)*

2. **Descripción del Programa**
   - Texto estándar *(FIJO)*
   - Análisis del ciclo actual *(DINÁMICO)*
   - Notas consolidadas *(FIJO)*

3. **Secciones de Análisis**
   - Control Insectos Rastreros
   - Control de Roedores  
   - Control Insectos Voladores
   - Órdenes Mantenimiento
   - Zonas Comunes

4. **Recomendaciones**
   - Generales *(FIJO)*
   - Específicas por sede *(VARIABLE)*

5. **Información de Contacto** *(FIJO)*

### 📊 Gráficas Incluidas

- **Preventivos**: Órdenes vs áreas, especies, tendencias
- **Roedores**: Estado estaciones, consumo mensual
- **Lámparas**: Estado operativo, capturas, tendencias

## 🔧 Solución de Problemas

### Error: Plantilla no encontrada
```bash
# Verificar que existe el archivo
ls config/hospital_san_vicente_template.yaml
```

### Error: Datos faltantes
```bash
# El sistema usa fallback automático
# Revisa la conexión a APIs KoBoToolbox
```

### Error: Formato de fecha
```bash
# El sistema calcula fechas automáticamente
# Verifica la fecha del sistema
date
```

## 🚀 Despliegue en Producción

### Preparación
```bash
# 1. Ejecutar sistema completo
python main.py

# 2. Verificar reportes generados
ls outputs/informe_hospital_san_vicente_*.docx

# 3. Confirmar limpieza realizada
# Los archivos de desarrollo han sido eliminados automáticamente
```

### Entrega Final
- **📄 Documentos Word**: Listos para revisión y entrega
- **📋 Formato Oficial**: Cumple especificaciones Hospital San Vicente
- **🔄 Datos Actualizados**: Métricas y fechas del período actual
- **✅ Sin Intervención Manual**: Proceso completamente automatizado

## 📞 Información de Contacto

**SERVIGPLAGAS S.A.S**  
Fernando Quintero - Coordinador de Mercadeo  
📞 3225241 | 📱 311 622 60 19 - 310 469 50 50  
📧 splagasmedellin@gmail.com

---

## 🎯 Objetivos Cumplidos

✅ **Plantilla Oficial Integrada**: Basada en documentos reales  
✅ **Variables Dinámicas**: Automatización completa  
✅ **Constantes Fijas**: Mantenidas según especificaciones  
✅ **Generador Word**: Documentos finales listos  
✅ **Flujo Automatizado**: Sin intervención manual  
✅ **Sistema Limpio**: Archivos innecesarios eliminados  

**💡 RESULTADO**: Sistema completamente automatizado que genera reportes oficiales del Hospital San Vicente listos para producción.

---

*Última actualización: Agosto 2025*  
*Versión: 2.0 - Hospital San Vicente Automatizado*
