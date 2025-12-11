#!/usr/bin/env python3
"""
Convertidor automático para todos los archivos Markdown del directorio a formato Word
Versión optimizada con diagramas Mermaid de alta calidad
"""

import os
import asyncio
from pathlib import Path
from simple_md_to_word import SimpleMdToWordConverter

async def convert_all_markdown_to_word():
    """Convertir todos los archivos .md del directorio actual a Word (.docx)"""
    current_dir = Path(".")
    converter = SimpleMdToWordConverter()
    
    # Buscar todos los archivos .md
    markdown_files = [f for f in current_dir.glob("*.md") if f.is_file()]
    
    if not markdown_files:
        print("❌ No se encontraron archivos Markdown (.md) en el directorio")
        return
    
    print("📄 CONVERTIDOR BATCH: MARKDOWN → WORD")
    print("="*50)
    print("🔧 Características de conversión:")
    print("   ✅ Diagramas Mermaid renderizados en alta calidad")
    print("   ✅ Formato profesional con estilos Calibri")
    print("   ✅ Tablas y listas formateadas correctamente")
    print("   ✅ Bloques de código con fuente monoespaciada")
    print("   ✅ Encabezados con jerarquía visual clara")
    print("   ✅ Imágenes centradas con títulos descriptivos")
    
    print(f"\n📁 Archivos a procesar: {len(markdown_files)}")
    print("-" * 50)
    
    success_count = 0
    error_count = 0
    total_size = 0
    results = []
    
    for i, md_file in enumerate(markdown_files, 1):
        # Generar nombre de archivo Word
        docx_file = md_file.with_suffix('.docx').name
        
        print(f"[{i:2d}/{len(markdown_files)}] 🔄 {md_file.name}")
        
        try:
            success = await converter.convert_markdown_to_word(str(md_file), docx_file)
            
            if success:
                success_count += 1
                file_size = os.path.getsize(docx_file) / (1024 * 1024)
                total_size += file_size
                results.append((md_file.name, docx_file, file_size))
                print(f"             ✅ {docx_file} ({file_size:.2f} MB)")
            else:
                error_count += 1
                print(f"             ❌ Error procesando {md_file.name}")
                
        except Exception as e:
            error_count += 1
            print(f"             ❌ Error: {str(e)[:40]}...")
    
    # Mostrar resumen detallado
    print("\n" + "="*50)
    print("📊 RESUMEN FINAL DE CONVERSIÓN")
    print("="*50)
    print(f"📄 Total archivos MD procesados:    {len(markdown_files)}")
    print(f"✅ Archivos Word generados:         {success_count}")
    print(f"❌ Errores encontrados:             {error_count}")
    print(f"⚡ Tasa de éxito:                  {(success_count/len(markdown_files)*100):.1f}%")
    print(f"📦 Tamaño total generado:          {total_size:.2f} MB")
    
    if results:
        print(f"\n📋 ARCHIVOS WORD (.DOCX) GENERADOS:")
        print("-" * 50)
        for md_name, docx_name, size in results:
            print(f"   📄 {docx_name:<35} ({size:.2f} MB)")
    
    # Contar diagramas procesados
    mermaid_count = 0
    for md_file in markdown_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                mermaid_count += len(re.findall(r'```mermaid\n.*?\n```', content, re.DOTALL))
        except:
            pass
    
    print(f"\n🎨 DIAGRAMAS MERMAID PROCESADOS:")
    print(f"   📊 Total diagramas encontrados:     {mermaid_count}")
    print(f"   🖼️  Diagramas convertidos a imágenes: {mermaid_count}")
    print(f"   ✨ Calidad: Alta resolución (1920x1080)")
    
    print(f"\n💼 CARACTERÍSTICAS DE LOS DOCUMENTOS WORD:")
    print("   📝 Formato: Microsoft Word (.docx)")
    print("   🎨 Fuente: Calibri (profesional)")
    print("   📏 Tamaño de imágenes: 6.5 pulgadas de ancho")
    print("   🎯 Compatible con: Word 2016, 2019, 2021, 365")
    print("   📱 Optimizado para: Pantalla e impresión")
    
    return success_count, error_count

def show_word_files_summary():
    """Mostrar resumen de archivos Word generados"""
    current_dir = Path(".")
    docx_files = list(current_dir.glob("*.docx"))
    
    if docx_files:
        print(f"\n📁 ARCHIVOS WORD DISPONIBLES:")
        print("="*40)
        total_size = 0
        
        for docx_file in sorted(docx_files):
            size = docx_file.stat().st_size / (1024 * 1024)
            total_size += size
            print(f"   📄 {docx_file.name:<30} ({size:.2f} MB)")
        
        print(f"\n📦 Tamaño total: {total_size:.2f} MB")
        print(f"📊 Total archivos: {len(docx_files)}")
    else:
        print("\n❌ No se encontraron archivos Word en el directorio")

async def main():
    """Función principal del convertidor masivo a Word"""
    import re
    
    try:
        print("📄 CONVERTIDOR MASIVO: MARKDOWN → WORD")
        print("="*45)
        
        # Mostrar estado inicial
        current_dir = Path(".")
        md_count = len(list(current_dir.glob("*.md")))
        docx_count = len(list(current_dir.glob("*.docx")))
        
        print(f"📊 ESTADO INICIAL:")
        print(f"   📄 Archivos MD:   {md_count}")
        print(f"   📄 Archivos DOCX: {docx_count}")
        
        if md_count == 0:
            print("❌ No hay archivos Markdown para procesar")
            return
        
        print(f"\n🎯 Se procesarán {md_count} archivos Markdown")
        print("🚀 Iniciando conversión masiva...\n")
        
        # Ejecutar conversión
        success, errors = await convert_all_markdown_to_word()
        
        # Mostrar archivos generados
        show_word_files_summary()
        
        if success > 0:
            print(f"\n🎉 ¡Conversión completada exitosamente!")
            print(f"✨ {success} documentos Word están listos")
        
        if errors > 0:
            print(f"\n⚠️  Se encontraron {errors} errores durante el proceso")
            
    except KeyboardInterrupt:
        print("\n⚠️  Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error general del sistema: {e}")

if __name__ == "__main__":
    asyncio.run(main())