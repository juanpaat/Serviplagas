"""
Sistema de limpieza automática para Serviplagas
Elimina archivos temporales, de testing y debugging que ya no son necesarios
"""

import os
import shutil
import glob
from typing import List
from datetime import datetime

class ServiplaGasSystemCleaner:
    """
    Limpiador automático del sistema Serviplagas.
    Elimina archivos de desarrollo que ya no son necesarios en producción.
    """
    
    def __init__(self):
        self.files_to_remove = []
        self.dirs_to_remove = []
        self.backup_created = False
        
    def identify_cleanup_files(self) -> List[str]:
        """Identifica archivos que deben ser eliminados."""
        cleanup_candidates = [
            # Archivos de testing y debugging
            "test_llm_integration.py",
            "ejemplo_uso_prompts.py", 
            "verify_prompts.py",
            "eval_script.py",
            "demo_new_features.py",
            "document_mode_config.py",
            "template_editor.py",
            
            # Notebooks de desarrollo
            "Notebook.ipynb",
            
            # Archivos de backup temporales
            "config/prompt_templates.yaml.backup",
            
            # Archivos de salida temporales (mantener solo los finales)
            "outputs/~$*",  # Archivos temporales de Word
            
            # Logs de desarrollo (mantener solo logs actuales)
            "logs/*.log.old",
            "logs/debug_*.log",
            
            # Archivos de cache de Python
            "__pycache__/*",
            "*/__pycache__/*",
            "*/*/__pycache__/*",
            "*.pyc",
            "*/*.pyc",
            "*/*/*.pyc",
        ]
        
        existing_files = []
        for pattern in cleanup_candidates:
            matches = glob.glob(pattern, recursive=True)
            existing_files.extend(matches)
            
        return existing_files
    
    def create_backup(self) -> str:
        """Crea un backup antes de la limpieza."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = f"backup_before_cleanup_{timestamp}"
        
        print(f"📦 Creando backup en: {backup_dir}")
        
        # Crear directorio de backup
        os.makedirs(backup_dir, exist_ok=True)
        
        # Copiar archivos importantes que serán eliminados
        files_to_backup = [f for f in self.identify_cleanup_files() 
                          if f.endswith('.py') and os.path.exists(f)]
        
        for file_path in files_to_backup:
            if os.path.isfile(file_path):
                dest_path = os.path.join(backup_dir, os.path.basename(file_path))
                shutil.copy2(file_path, dest_path)
                print(f"   📄 Backed up: {file_path}")
        
        self.backup_created = True
        return backup_dir
    
    def clean_development_files(self, create_backup: bool = True) -> dict:
        """
        Elimina archivos de desarrollo y testing.
        
        Args:
            create_backup: Si crear backup antes de eliminar
            
        Returns:
            dict: Resumen de la limpieza
        """
        cleanup_summary = {
            'files_removed': [],
            'files_failed': [],
            'dirs_removed': [],
            'backup_created': None,
            'space_freed': 0
        }
        
        # Crear backup si se solicita
        if create_backup:
            backup_dir = self.create_backup()
            cleanup_summary['backup_created'] = backup_dir
        
        print(f"\n🧹 INICIANDO LIMPIEZA DEL SISTEMA")
        print("=" * 50)
        
        # Identificar archivos a eliminar
        files_to_remove = self.identify_cleanup_files()
        
        print(f"📋 Archivos identificados para eliminación: {len(files_to_remove)}")
        
        # Eliminar archivos
        for file_path in files_to_remove:
            try:
                if os.path.exists(file_path):
                    if os.path.isfile(file_path):
                        file_size = os.path.getsize(file_path)
                        os.remove(file_path)
                        cleanup_summary['files_removed'].append(file_path)
                        cleanup_summary['space_freed'] += file_size
                        print(f"   🗑️  Eliminado: {file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        cleanup_summary['dirs_removed'].append(file_path)
                        print(f"   📁 Directorio eliminado: {file_path}")
            except Exception as e:
                cleanup_summary['files_failed'].append((file_path, str(e)))
                print(f"   ❌ Error eliminando {file_path}: {e}")
        
        # Eliminar directorios __pycache__ específicamente
        self._clean_pycache_dirs(cleanup_summary)
        
        # Limpiar archivos temporales de outputs
        self._clean_temp_outputs(cleanup_summary)
        
        return cleanup_summary
    
    def _clean_pycache_dirs(self, cleanup_summary: dict):
        """Limpia directorios __pycache__ de manera recursiva."""
        print(f"\n🔍 Limpiando cache de Python...")
        
        for root, dirs, files in os.walk('.'):
            if '__pycache__' in dirs:
                pycache_path = os.path.join(root, '__pycache__')
                try:
                    shutil.rmtree(pycache_path)
                    cleanup_summary['dirs_removed'].append(pycache_path)
                    print(f"   🗑️  Cache eliminado: {pycache_path}")
                except Exception as e:
                    cleanup_summary['files_failed'].append((pycache_path, str(e)))
    
    def _clean_temp_outputs(self, cleanup_summary: dict):
        """Limpia archivos temporales de la carpeta outputs."""
        print(f"\n🔍 Limpiando archivos temporales de outputs...")
        
        temp_patterns = [
            "outputs/~$*",
            "outputs/*.tmp",
            "outputs/temp_*",
            "outputs/debug_*"
        ]
        
        for pattern in temp_patterns:
            matches = glob.glob(pattern)
            for file_path in matches:
                try:
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)
                        os.remove(file_path)
                        cleanup_summary['files_removed'].append(file_path)
                        cleanup_summary['space_freed'] += file_size
                        print(f"   🗑️  Temporal eliminado: {file_path}")
                except Exception as e:
                    cleanup_summary['files_failed'].append((file_path, str(e)))


def perform_system_cleanup(create_backup: bool = True) -> dict:
    """
    Realiza limpieza completa del sistema Serviplagas.
    
    Args:
        create_backup: Si crear backup antes de limpiar
        
    Returns:
        dict: Resumen de la limpieza
    """
    cleaner = ServiplaGasSystemCleaner()
    
    print("🧹 SISTEMA DE LIMPIEZA AUTOMÁTICA - SERVIPLAGAS")
    print("=" * 55)
    print("📋 Eliminando archivos de desarrollo y testing...")
    print("💡 Los archivos principales de producción se mantendrán")
    print("=" * 55)
    
    # Realizar limpieza
    cleanup_summary = cleaner.clean_development_files(create_backup)
    
    print(f"\n✅ Limpieza completada")
    
    return cleanup_summary


if __name__ == "__main__":
    # Ejecutar limpieza si se ejecuta directamente
    perform_system_cleanup(create_backup=True)