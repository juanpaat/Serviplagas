"""
Script de validación para el sistema Hospital San Vicente
Verifica que todos los componentes funcionen correctamente antes de producción
"""

import os
import yaml
import pandas as pd
from datetime import datetime
import traceback
from typing import Dict, List, Tuple

class HospitalSanVicenteValidator:
    """Valida la integridad y funcionalidad del sistema."""
    
    def __init__(self):
        self.validation_results = {
            'files': [],
            'configuration': [],
            'data_processing': [],
            'report_generation': [],
            'errors': [],
            'warnings': []
        }
    
    def validate_required_files(self) -> bool:
        """Valida que todos los archivos requeridos estén presentes."""
        print("📁 Validando archivos requeridos...")
        
        required_files = [
            'main.py',
            'system_cleaner.py',
            'config/hospital_san_vicente_template.yaml',
            'config/settings.py',
            'reports/hospital_san_vicente_generator.py',
            'reports/report_builder.py',
            'README_HOSPITAL_SAN_VICENTE.md',
            'requirements.txt'
        ]
        
        all_present = True
        for file_path in required_files:
            if os.path.exists(file_path):
                self.validation_results['files'].append(f"✅ {file_path}")
                print(f"   ✅ {file_path}")
            else:
                self.validation_results['files'].append(f"❌ {file_path}")
                self.validation_results['errors'].append(f"Archivo faltante: {file_path}")
                print(f"   ❌ FALTANTE: {file_path}")
                all_present = False
        
        return all_present
    
    def validate_template_configuration(self) -> bool:
        """Valida la configuración de la plantilla YAML."""
        print("\n⚙️ Validando configuración de plantilla...")
        
        template_path = 'config/hospital_san_vicente_template.yaml'
        
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            
            # Validar secciones requeridas
            required_sections = [
                'document_config',
                'sedes',
                'plantillas_texto',
                'grados_infestacion',
                'contenido_fijo',
                'contacto',
                'configuracion_temporal'
            ]
            
            for section in required_sections:
                if section in config:
                    self.validation_results['configuration'].append(f"✅ Sección '{section}' presente")
                    print(f"   ✅ Sección '{section}' presente")
                else:
                    self.validation_results['configuration'].append(f"❌ Sección '{section}' faltante")
                    self.validation_results['errors'].append(f"Sección faltante en plantilla: {section}")
                    print(f"   ❌ Sección '{section}' faltante")
                    return False
            
            # Validar datos de sedes
            if 'sedes' in config:
                for sede in ['Rionegro', 'Medellín']:
                    if sede in config['sedes']:
                        sede_data = config['sedes'][sede]
                        required_fields = ['nombre_completo', 'codigo_sede', 'direccion', 'telefono']
                        
                        for field in required_fields:
                            if field in sede_data:
                                print(f"   ✅ {sede}.{field}: {sede_data[field]}")
                            else:
                                self.validation_results['errors'].append(f"Campo faltante: {sede}.{field}")
                                print(f"   ❌ {sede}.{field} faltante")
                                return False
                    else:
                        self.validation_results['errors'].append(f"Sede faltante: {sede}")
                        print(f"   ❌ Sede {sede} no configurada")
                        return False
            
            print("   ✅ Configuración de plantilla válida")
            return True
            
        except yaml.YAMLError as e:
            self.validation_results['errors'].append(f"Error YAML: {e}")
            print(f"   ❌ Error en YAML: {e}")
            return False
        except FileNotFoundError:
            self.validation_results['errors'].append(f"Plantilla no encontrada: {template_path}")
            print(f"   ❌ Plantilla no encontrada: {template_path}")
            return False
    
    def validate_data_loading(self) -> bool:
        """Valida que la carga de datos funcione correctamente."""
        print("\n📊 Validando carga de datos...")
        
        try:
            from data_processing.data_loader import load_data_with_fallback
            from data_processing.data_cleaner import (
                transform_preventivos_df, 
                transform_roedores_df, 
                transform_lamparas_df
            )
            from config.settings import LOCAL_FILES, API_URLS
            
            # Intentar cargar datos
            for data_type in ['preventivos', 'roedores', 'lamparas']:
                try:
                    print(f"   🔄 Cargando {data_type}...")
                    raw_data = load_data_with_fallback(
                        LOCAL_FILES[data_type], 
                        API_URLS[data_type]
                    )
                    
                    if raw_data is not None and not raw_data.empty:
                        print(f"   ✅ {data_type}: {len(raw_data)} registros cargados")
                        self.validation_results['data_processing'].append(
                            f"✅ {data_type}: {len(raw_data)} registros"
                        )
                        
                        # Intentar transformación
                        if data_type == 'preventivos':
                            transformed = transform_preventivos_df(raw_data)
                        elif data_type == 'roedores':
                            transformed = transform_roedores_df(raw_data)
                        else:
                            transformed = transform_lamparas_df(raw_data)
                        
                        if transformed is not None and not transformed.empty:
                            print(f"   ✅ {data_type} transformado: {len(transformed)} registros")
                        else:
                            print(f"   ⚠️  {data_type} transformado pero vacío")
                            self.validation_results['warnings'].append(f"{data_type} sin datos después de transformación")
                    else:
                        print(f"   ⚠️  {data_type}: Sin datos disponibles")
                        self.validation_results['warnings'].append(f"{data_type}: Sin datos disponibles")
                        
                except Exception as e:
                    print(f"   ❌ Error cargando {data_type}: {e}")
                    self.validation_results['errors'].append(f"Error carga {data_type}: {e}")
                    return False
            
            return True
            
        except ImportError as e:
            self.validation_results['errors'].append(f"Error importación módulos: {e}")
            print(f"   ❌ Error importando módulos: {e}")
            return False
    
    def validate_report_generation(self) -> bool:
        """Valida que la generación de reportes funcione."""
        print("\n📄 Validando generación de reportes...")
        
        try:
            from reports.hospital_san_vicente_generator import HospitalSanVicenteReportGenerator
            
            # Crear generador
            generator = HospitalSanVicenteReportGenerator()
            print("   ✅ Generador instanciado correctamente")
            
            # Crear datos de prueba
            test_data_preventivo = pd.DataFrame({
                'Sede': ['Rionegro', 'Medellín'] * 5,
                'Fecha': [datetime.now()] * 10,
                'Cucarachas Alemanas': [0, 1, 0, 2, 0, 0, 1, 0, 0, 0],
                'Moscas': [0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
            })
            
            test_data_roedores = pd.DataFrame({
                'Sede': ['Rionegro', 'Medellín'] * 3,
                'Estacion': ['E1', 'E2', 'E3', 'E4', 'E5', 'E6'],
                'Consumo': [0, 5, 0, 10, 0, 2]
            })
            
            test_data_lamparas = pd.DataFrame({
                'Sede': ['Rionegro', 'Medellín'] * 2,
                'Lampara': ['L1', 'L2', 'L3', 'L4'],
                'Estado': ['Funcional', 'Saturada', 'Funcional', 'Dañada'],
                'Capturas': [10, 25, 8, 0]
            })
            
            print("   ✅ Datos de prueba creados")
            
            # Validar cálculo de variables dinámicas
            for sede in ['Rionegro', 'Medellín']:
                try:
                    variables = generator.calculate_dynamic_variables(
                        test_data_preventivo, test_data_roedores, test_data_lamparas, sede
                    )
                    
                    required_vars = [
                        'fecha_elaboracion', 'mes_nombre', 'año', 'sede',
                        'ordenes_solicitadas', 'porcentaje_cumplimiento',
                        'grado_infestacion'
                    ]
                    
                    for var in required_vars:
                        if var in variables:
                            print(f"   ✅ {sede}.{var}: {variables[var]}")
                        else:
                            print(f"   ❌ {sede}.{var}: Faltante")
                            return False
                    
                    self.validation_results['report_generation'].append(
                        f"✅ Variables dinámicas {sede}: {len(variables)} calculadas"
                    )
                    
                except Exception as e:
                    print(f"   ❌ Error calculando variables para {sede}: {e}")
                    self.validation_results['errors'].append(f"Error variables {sede}: {e}")
                    return False
            
            print("   ✅ Generación de reportes validada")
            return True
            
        except ImportError as e:
            self.validation_results['errors'].append(f"Error importación generador: {e}")
            print(f"   ❌ Error importando generador: {e}")
            return False
        except Exception as e:
            self.validation_results['errors'].append(f"Error validación reportes: {e}")
            print(f"   ❌ Error en validación: {e}")
            return False
    
    def validate_system_cleaner(self) -> bool:
        """Valida que el sistema de limpieza funcione."""
        print("\n🧹 Validando sistema de limpieza...")
        
        try:
            from system_cleaner import ServiplaGasSystemCleaner
            
            cleaner = ServiplaGasSystemCleaner()
            print("   ✅ Sistema de limpieza instanciado")
            
            # Validar identificación de archivos (sin eliminar)
            files_to_clean = cleaner.identify_cleanup_files()
            print(f"   ✅ Archivos identificados para limpieza: {len(files_to_clean)}")
            
            # Mostrar algunos archivos candidatos
            for i, file_path in enumerate(files_to_clean[:5]):
                if os.path.exists(file_path):
                    print(f"   📄 Candidato: {file_path}")
            
            return True
            
        except ImportError as e:
            self.validation_results['errors'].append(f"Error importación limpiador: {e}")
            print(f"   ❌ Error importando limpiador: {e}")
            return False
        except Exception as e:
            self.validation_results['errors'].append(f"Error validación limpieza: {e}")
            print(f"   ❌ Error en validación limpieza: {e}")
            return False
    
    def run_complete_validation(self) -> Dict:
        """Ejecuta validación completa del sistema."""
        print("🔍 VALIDACIÓN COMPLETA DEL SISTEMA HOSPITAL SAN VICENTE")
        print("=" * 60)
        
        validation_steps = [
            ("Archivos Requeridos", self.validate_required_files),
            ("Configuración Plantilla", self.validate_template_configuration),
            ("Carga de Datos", self.validate_data_loading),
            ("Generación Reportes", self.validate_report_generation),
            ("Sistema Limpieza", self.validate_system_cleaner)
        ]
        
        all_passed = True
        for step_name, validation_func in validation_steps:
            try:
                result = validation_func()
                if not result:
                    all_passed = False
                    print(f"\n❌ FALLÓ: {step_name}")
                else:
                    print(f"\n✅ EXITOSO: {step_name}")
            except Exception as e:
                all_passed = False
                error_msg = f"Error en {step_name}: {e}"
                self.validation_results['errors'].append(error_msg)
                print(f"\n💥 EXCEPCIÓN en {step_name}: {e}")
                print(f"Traceback: {traceback.format_exc()}")
        
        # Generar reporte final
        self._generate_validation_report(all_passed)
        
        return {
            'success': all_passed,
            'results': self.validation_results,
            'summary': self._get_validation_summary()
        }
    
    def _generate_validation_report(self, success: bool):
        """Genera reporte de validación."""
        print(f"\n" + "=" * 60)
        if success:
            print("🎉 VALIDACIÓN COMPLETADA EXITOSAMENTE")
            print("✅ Sistema listo para producción")
        else:
            print("❌ VALIDACIÓN FALLÓ")
            print("⚠️  Se requieren correcciones antes de producción")
        
        print("=" * 60)
        
        # Mostrar resumen
        print(f"\n📊 RESUMEN:")
        print(f"   ✅ Validaciones exitosas: {self._count_successes()}")
        print(f"   ❌ Errores encontrados: {len(self.validation_results['errors'])}")
        print(f"   ⚠️  Advertencias: {len(self.validation_results['warnings'])}")
        
        # Mostrar errores si los hay
        if self.validation_results['errors']:
            print(f"\n❌ ERRORES DETECTADOS:")
            for error in self.validation_results['errors']:
                print(f"   • {error}")
        
        # Mostrar advertencias si las hay
        if self.validation_results['warnings']:
            print(f"\n⚠️  ADVERTENCIAS:")
            for warning in self.validation_results['warnings']:
                print(f"   • {warning}")
    
    def _count_successes(self) -> int:
        """Cuenta validaciones exitosas."""
        total = 0
        for category in ['files', 'configuration', 'data_processing', 'report_generation']:
            total += len([item for item in self.validation_results[category] if item.startswith('✅')])
        return total
    
    def _get_validation_summary(self) -> Dict:
        """Obtiene resumen de validación."""
        return {
            'successes': self._count_successes(),
            'errors': len(self.validation_results['errors']),
            'warnings': len(self.validation_results['warnings']),
            'timestamp': datetime.now().isoformat()
        }


def run_system_validation():
    """Ejecuta validación completa del sistema."""
    validator = HospitalSanVicenteValidator()
    return validator.run_complete_validation()


if __name__ == "__main__":
    # Ejecutar validación completa
    results = run_system_validation()
    
    if results['success']:
        print(f"\n🚀 SISTEMA VALIDADO - LISTO PARA EJECUTAR:")
        print(f"   python main.py")
        exit(0)
    else:
        print(f"\n🛑 SISTEMA REQUIERE CORRECCIONES")
        print(f"   Revisa los errores mostrados arriba")
        exit(1)
