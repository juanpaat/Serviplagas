# 🐍 Guía de Uso del Entorno Virtual (.venv) - Serviplagas

## 📋 ¿Qué es el entorno virtual?

El entorno virtual (`.venv`) es un ambiente aislado de Python que mantiene todas las dependencias del proyecto separadas del sistema global. Esto evita conflictos entre diferentes proyectos y asegura que el proyecto funcione consistentemente.

## 🚀 Uso Básico

### 1. Activar el entorno virtual

**En macOS/Linux:**
```bash
source .venv/bin/activate
```

**En Windows:**
```bash
.venv\Scripts\activate
```

**Confirmación de activación:**
Verás `(.venv)` al inicio de tu prompt:
```bash
(.venv) usuario@computadora:~/Serviplagas$ 
```

### 2. Ejecutar el sistema

Una vez activado el entorno virtual, ejecuta:
```bash
python main.py
```

### 3. Desactivar el entorno virtual

Cuando termines de trabajar:
```bash
deactivate
```

## 🔧 Comandos Completos

### Validar y ejecutar sistema completo:
```bash
# Activar entorno
source .venv/bin/activate

# Validar sistema
python validate_system.py

# Ejecutar generación de reportes
python main.py

# Desactivar cuando termines
deactivate
```

### Instalar nuevas dependencias:
```bash
# Activar entorno
source .venv/bin/activate

# Instalar nueva dependencia
pip install nombre_paquete

# Actualizar requirements.txt
pip freeze > requirements.txt

# Desactivar
deactivate
```

## 📦 Gestión de Dependencias

### Ver dependencias instaladas:
```bash
source .venv/bin/activate
pip list
```

### Actualizar dependencias:
```bash
source .venv/bin/activate
pip install --upgrade nombre_paquete
```

### Reinstalar todas las dependencias:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## 🔍 Solución de Problemas

### Error: "command not found: python"
**Solución:** Usa `python3` en lugar de `python`:
```bash
source .venv/bin/activate
python3 main.py
```

### Error: El entorno no se activa
**Solución:** Verifica que estés en el directorio correcto:
```bash
pwd  # Debe mostrar la ruta del proyecto Serviplagas
ls -la  # Debe mostrar el directorio .venv
```

### Error: Dependencias faltantes
**Solución:** Reinstala las dependencias:
```bash
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Recrear entorno virtual desde cero:
```bash
# Eliminar entorno actual
rm -rf .venv

# Crear nuevo entorno
python3 -m venv .venv

# Activar
source .venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

## 📂 Estructura del Entorno Virtual

```
.venv/
├── bin/              # Ejecutables (activate, python, pip)
├── include/          # Headers de C
├── lib/              # Dependencias Python instaladas
├── pyvenv.cfg        # Configuración del entorno
└── share/            # Archivos compartidos
```

## 🔒 Buenas Prácticas

### ✅ Hacer SIEMPRE:
- Activar el entorno antes de trabajar
- Usar `pip freeze > requirements.txt` después de instalar dependencias
- Desactivar el entorno al terminar
- No incluir `.venv/` en el control de versiones (ya está en .gitignore)

### ❌ NO Hacer:
- Instalar dependencias sin activar el entorno
- Modificar archivos dentro de `.venv/` manualmente
- Copiar el directorio `.venv/` entre computadoras
- Include `.venv` en commits de git

## 🎯 Comandos de Un Solo Paso

### Ejecutar sistema completo:
```bash
source .venv/bin/activate && python main.py && deactivate
```

### Validar y ejecutar:
```bash
source .venv/bin/activate && python validate_system.py && python main.py && deactivate
```

### Actualizar dependencias y ejecutar:
```bash
source .venv/bin/activate && pip install --upgrade -r requirements.txt && python main.py && deactivate
```

## 📊 Verificación del Entorno

### Verificar Python usado:
```bash
source .venv/bin/activate
which python  # Debe mostrar ruta que incluye .venv
python --version
```

### Verificar dependencias clave:
```bash
source .venv/bin/activate
pip show pandas matplotlib python-docx pyyaml
```

## 🆘 Ayuda Rápida

Si algo no funciona, ejecuta este comando de diagnóstico:
```bash
source .venv/bin/activate
echo "✅ Entorno activado"
python --version
pip --version
pip list | grep -E "(pandas|matplotlib|docx|yaml)"
python validate_system.py
```

---

## 📞 Información Adicional

El entorno virtual asegura que el proyecto Serviplagas funcione consistentemente con las versiones exactas de dependencias especificadas en `requirements.txt`. 

**Dependencias principales:**
- `pandas >= 2.0.0` - Procesamiento de datos
- `matplotlib >= 3.7.0` - Generación de gráficas  
- `python-docx >= 0.8.11` - Creación documentos Word
- `pyyaml >= 6.0` - Manejo plantillas YAML
- `seaborn >= 0.12.0` - Visualizaciones avanzadas

---

*Última actualización: Agosto 2025*  
*Versión del entorno: Python 3.11+*
