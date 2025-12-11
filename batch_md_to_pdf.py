#!/usr/bin/env python3
"""
Convertidor automático para todos los archivos Markdown del directorio
Versión simplificada y optimizada para Windows
"""

import os
import asyncio
from pathlib import Path
from simple_md_to_pdf import SimpleMdToPdfConverter

async def convert_all_markdown_files():
    """Convertir todos los archivos .md del directorio actual a PDF"""
    current_dir = Path(".")
    converter = SimpleMdToPdfConverter()
    
    # Buscar todos los archivos .md
    markdown_files = [f for f in current_dir.glob("*.md") if f.is_file()]
    
    if not markdown_files:
        print("❌ No se encontraron archivos Markdown (.md) en el directorio")
        return
    
    print("🔄 CONVERTIDOR BATCH: MARKDOWN → PDF")
    print("="*50)
    print(f"📁 Encontrados {len(markdown_files)} archivos Markdown:")
    
    for i, md_file in enumerate(markdown_files, 1):
        print(f"   {i:2d}. {md_file.name}")
    
    print("\n🚀 Iniciando conversión masiva...")
    print("-" * 50)
    
    success_count = 0
    error_count = 0
    processed_files = []
    
    for i, md_file in enumerate(markdown_files, 1):
        pdf_file = md_file.with_suffix('.pdf')
        
        print(f"\n[{i}/{len(markdown_files)}] {md_file.name}")
        
        try:
            success = await converter.convert_markdown_to_pdf(str(md_file), str(pdf_file))
            
            if success:
                success_count += 1
                file_size = pdf_file.stat().st_size / (1024 * 1024)
                processed_files.append((pdf_file.name, file_size))
                print(f"   ✅ Éxito → {pdf_file.name}")
            else:
                error_count += 1
                print(f"   ❌ Error → {md_file.name}")
                
        except Exception as e:
            error_count += 1
            print(f"   ❌ Error procesando {md_file.name}: {str(e)[:60]}...")
    
    # Resumen final
    print("\n" + "="*50)
    print("📊 RESUMEN FINAL")
    print("="*50)
    print(f"📄 Total archivos MD:      {len(markdown_files)}")
    print(f"✅ Conversiones exitosas:  {success_count}")
    print(f"❌ Errores encontrados:    {error_count}")
    print(f"⚡ Tasa de éxito:         {(success_count/len(markdown_files)*100):.1f}%")
    
    if processed_files:
        print(f"\n📋 ARCHIVOS PDF GENERADOS ({success_count}):")
        print("-" * 40)
        total_size = 0
        for filename, size in processed_files:
            print(f"   📄 {filename:<30} ({size:.2f} MB)")
            total_size += size
        print(f"\n📦 Tamaño total: {total_size:.2f} MB")
        print("📂 Ubicación: Directorio actual")
    
    if error_count > 0:
        print(f"\n⚠️  Se encontraron {error_count} errores durante el proceso")
        print("💡 Revisa los archivos MD que fallaron para identificar posibles problemas")

def show_available_files():
    """Mostrar archivos disponibles para conversión"""
    current_dir = Path(".")
    md_files = list(current_dir.glob("*.md"))
    pdf_files = list(current_dir.glob("*.pdf"))
    
    print("📁 ESTADO DEL DIRECTORIO")
    print("="*40)
    print(f"📄 Archivos MD disponibles: {len(md_files)}")
    print(f"📄 Archivos PDF existentes: {len(pdf_files)}")
    
    if md_files:
        print("\n📋 Archivos Markdown (.md):")
        for md_file in sorted(md_files):
            size = md_file.stat().st_size / 1024
            print(f"   • {md_file.name:<30} ({size:.1f} KB)")
    
    if pdf_files:
        print("\n📋 Archivos PDF existentes:")
        for pdf_file in sorted(pdf_files):
            size = pdf_file.stat().st_size / (1024 * 1024)
            print(f"   • {pdf_file.name:<30} ({size:.2f} MB)")

async def main():
    """Función principal del convertidor masivo"""
    try:
        # Mostrar estado inicial
        show_available_files()
        
        print("\n" + "="*50)
        
        # Confirmar ejecución
        current_dir = Path(".")
        md_count = len(list(current_dir.glob("*.md")))
        
        if md_count == 0:
            print("❌ No hay archivos Markdown para procesar")
            return
        
        print(f"🎯 Se procesarán {md_count} archivos Markdown")
        
        # Ejecutar conversión
        await convert_all_markdown_files()
        
        print(f"\n🏁 Proceso completado")
        
    except KeyboardInterrupt:
        print("\n⚠️  Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error general del sistema: {e}")

if __name__ == "__main__":
    asyncio.run(main())