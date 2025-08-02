#!/usr/bin/env python3
"""
Script para verificar que los prompts están correctamente integrados en los documentos Word.
Este script lee los documentos generados y muestra un resumen de los prompts incluidos.
"""

from docx import Document
import os


def verify_prompts_in_document(docx_path: str):
    """Verifica que los prompts estén incluidos en el documento Word."""
    
    if not os.path.exists(docx_path):
        print(f"❌ Archivo no encontrado: {docx_path}")
        return False
    
    try:
        doc = Document(docx_path)
        
        # Contar elementos relacionados con prompts
        prompt_headings = 0
        response_headings = 0
        warning_found = False
        
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            
            # Buscar títulos de prompts
            if "🤖 PROMPT LLM:" in text:
                prompt_headings += 1
                
            # Buscar títulos de respuestas
            if "📝 RESPUESTA DEL LLM:" in text:
                response_headings += 1
                
            # Buscar advertencia de documento de revisión
            if "DOCUMENTO DE REVISIÓN" in text:
                warning_found = True
        
        print(f"📄 Documento: {os.path.basename(docx_path)}")
        print(f"   🤖 Prompts LLM encontrados: {prompt_headings}")
        print(f"   📝 Placeholders de respuesta: {response_headings}")
        print(f"   ⚠️  Advertencia de revisión: {'Sí' if warning_found else 'No'}")
        
        if prompt_headings > 0:
            print(f"   ✅ Documento en modo REVISIÓN")
        else:
            print(f"   📋 Documento en modo PRODUCCIÓN")
            
        return prompt_headings > 0
        
    except Exception as e:
        print(f"❌ Error leyendo documento: {e}")
        return False


def verify_all_documents():
    """Verifica todos los documentos en la carpeta outputs."""
    
    print("🔍 VERIFICACIÓN DE PROMPTS EN DOCUMENTOS")
    print("=" * 60)
    
    outputs_dir = "outputs"
    if not os.path.exists(outputs_dir):
        print(f"❌ Carpeta {outputs_dir} no encontrada")
        return
    
    docx_files = [f for f in os.listdir(outputs_dir) if f.endswith('.docx') and not f.startswith('~$')]
    
    if not docx_files:
        print(f"❌ No se encontraron archivos .docx en {outputs_dir}")
        return
    
    print(f"📁 Analizando {len(docx_files)} documentos...\n")
    
    revision_docs = 0
    production_docs = 0
    
    for docx_file in sorted(docx_files):
        docx_path = os.path.join(outputs_dir, docx_file)
        is_revision = verify_prompts_in_document(docx_path)
        
        if is_revision:
            revision_docs += 1
        else:
            production_docs += 1
        print()
    
    # Resumen
    print("📊 RESUMEN:")
    print(f"   📝 Documentos en modo REVISIÓN (con prompts): {revision_docs}")
    print(f"   📋 Documentos en modo PRODUCCIÓN (sin prompts): {production_docs}")
    
    if revision_docs > 0:
        print(f"\n💡 Los documentos de revisión contienen:")
        print(f"   • Prompts completos de LLM para análisis")
        print(f"   • Placeholders donde irán las respuestas")
        print(f"   • Advertencia de documento temporal")
        print(f"   • Estructura completa para validación")


def show_prompt_structure():
    """Muestra la estructura esperada de prompts en un documento."""
    
    print("\n📋 ESTRUCTURA ESPERADA DE PROMPTS POR DOCUMENTO:")
    print("=" * 60)
    
    expected_prompts = [
        "🔍 PROMPTS DE TABLAS INDIVIDUALES:",
        "   • Preventivos - Order Area",
        "   • Preventivos - Plagas Species", 
        "   • Preventivos - Total Trend",
        "   • Roedores - Station Status",
        "   • Roedores - Elimination Trend",
        "   • Lámparas - Status Monthly",
        "   • Lámparas - Status Legend",
        "   • Lámparas - Captures Species",
        "   • Lámparas - Captures Trend",
        "",
        "📂 PROMPTS DE RESUMEN POR SECCIÓN:",
        "   • Resumen Ejecutivo - Servicios Preventivos",
        "   • Resumen Ejecutivo - Control de Roedores",
        "   • Resumen Ejecutivo - Control de Insectos Voladores",
        "",
        "📑 PROMPT DE RESUMEN GENERAL:",
        "   • Resumen Ejecutivo Integral",
        "",
        "📊 TOTAL ESPERADO: 13 prompts por documento"
    ]
    
    for line in expected_prompts:
        print(line)


if __name__ == "__main__":
    print("🔍 VERIFICADOR DE PROMPTS EN DOCUMENTOS - SERVIPLAGAS")
    print("=" * 70)
    
    # Verificar todos los documentos
    verify_all_documents()
    
    # Mostrar estructura esperada
    show_prompt_structure()
    
    print(f"\n🎯 PRÓXIMOS PASOS:")
    print(f"   1. Revisa los documentos .docx generados")
    print(f"   2. Verifica que los prompts están en las ubicaciones correctas")
    print(f"   3. Confirma que las tablas de datos están incluidas en cada prompt")
    print(f"   4. Usa estos prompts para enviar al LLM de tu elección")
    print(f"   5. Para cambiar a modo producción: python document_mode_config.py")
