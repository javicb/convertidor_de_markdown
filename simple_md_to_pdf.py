#!/usr/bin/env python3
"""
Convertidor simplificado de Markdown a PDF usando navegador headless
Compatible con Windows, sin dependencias complejas
"""

import os
import re
import asyncio
import tempfile
import shutil
from pathlib import Path
from typing import List, Tuple
import markdown
from playwright.async_api import async_playwright

class SimpleMdToPdfConverter:
    def __init__(self):
        self.temp_dir = None
        self.mermaid_counter = 0
        
    def setup_temp_directory(self) -> str:
        """Crear directorio temporal para archivos de trabajo"""
        self.temp_dir = tempfile.mkdtemp(prefix="md_to_pdf_")
        return self.temp_dir
        
    def cleanup(self):
        """Limpiar archivos temporales"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    async def extract_mermaid_diagrams(self, content: str) -> List[Tuple[str, str]]:
        """Extraer diagramas Mermaid del contenido Markdown"""
        mermaid_pattern = r'```mermaid\n(.*?)\n```'
        diagrams = []
        
        matches = re.finditer(mermaid_pattern, content, re.DOTALL)
        for match in matches:
            mermaid_code = match.group(1).strip()
            self.mermaid_counter += 1
            placeholder_id = f"mermaid_diagram_{self.mermaid_counter}"
            diagrams.append((mermaid_code, placeholder_id))
            
        return diagrams
    
    async def render_mermaid_to_image(self, mermaid_code: str, output_path: str) -> bool:
        """Renderizar diagrama Mermaid a imagen usando Playwright con alta resolución"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                # Configurar viewport más grande para mejor resolución
                await page.set_viewport_size({"width": 1920, "height": 1080})
                
                # Configurar factor de escala para mayor resolución
                await page.emulate_media(media='screen')
                await page.add_style_tag(content="""
                    * {
                        -webkit-font-smoothing: antialiased;
                        -moz-osx-font-smoothing: grayscale;
                    }
                """)
                
                html_template = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
                    <style>
                        body {{
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                            margin: 40px;
                            background: white;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            min-height: calc(100vh - 80px);
                        }}
                        .mermaid {{
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            width: 100%;
                            min-height: 400px;
                            font-size: 18px;
                            padding: 30px;
                        }}
                        .mermaid svg {{
                            width: 100% !important;
                            min-width: 800px !important;
                            height: auto !important;
                            font-size: 18px !important;
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
                        }}
                        .mermaid svg text {{
                            font-size: 14px !important;
                            font-weight: 500 !important;
                        }}
                        .mermaid svg .node text {{
                            font-size: 16px !important;
                            font-weight: 600 !important;
                        }}
                    </style>
                </head>
                <body>
                    <div class="mermaid">
                        {mermaid_code}
                    </div>
                    <script>
                        mermaid.initialize({{
                            startOnLoad: true,
                            theme: 'default',
                            flowchart: {{
                                useMaxWidth: true,
                                htmlLabels: true,
                                curve: 'basis'
                            }},
                            themeVariables: {{
                                primaryColor: '#3498db',
                                primaryTextColor: '#2c3e50',
                                primaryBorderColor: '#2980b9',
                                lineColor: '#34495e',
                                sectionBkgColor: '#ecf0f1',
                                altSectionBkgColor: '#bdc3c7',
                                gridColor: '#95a5a6',
                                secondaryColor: '#e74c3c',
                                tertiaryColor: '#f39c12'
                            }}
                        }});
                    </script>
                </body>
                </html>
                """
                
                await page.set_content(html_template)
                await page.wait_for_load_state('networkidle')
                await page.wait_for_selector('.mermaid svg', timeout=15000)
                
                # Esperar un poco más para asegurar renderizado completo
                await page.wait_for_timeout(2000)
                
                # Tomar screenshot del elemento Mermaid con alta calidad
                mermaid_element = await page.query_selector('.mermaid')
                if mermaid_element:
                    # Configurar dispositivo para mayor densidad de píxeles
                    await page.emulate_media(media='screen')
                    
                    await mermaid_element.screenshot(
                        path=output_path, 
                        type='png',
                        omit_background=False  # Mantener fondo blanco para mejor contraste
                    )
                    await browser.close()
                    return True
                else:
                    await browser.close()
                    return False
                    
        except Exception as e:
            print(f"Error renderizando diagrama Mermaid: {e}")
            return False
    
    def replace_mermaid_with_images(self, content: str, diagrams: List[Tuple[str, str]], temp_dir: str) -> str:
        """Reemplazar bloques Mermaid con referencias a imágenes"""
        modified_content = content
        
        for i, (mermaid_code, placeholder_id) in enumerate(diagrams):
            image_filename = f"{placeholder_id}.png"
            image_path = os.path.join(temp_dir, image_filename)
            
            print(f"🔄 Reemplazando diagrama {i+1}: {placeholder_id}")
            
            # Buscar el bloque Mermaid exacto
            mermaid_block = f"```mermaid\n{mermaid_code}\n```"
            
            # Verificar si la imagen existe
            if os.path.exists(image_path):
                print(f"   📷 Imagen encontrada: {image_path}")
                import base64
                try:
                    with open(image_path, 'rb') as img_file:
                        img_data = base64.b64encode(img_file.read()).decode()
                        
                    image_html = f'''<div style="text-align: center; margin: 40px 0; page-break-inside: avoid;">
<img src="data:image/png;base64,{img_data}" alt="Diagrama {i+1}" style="width: 100%; max-width: 100%; height: auto; border: 2px solid #34495e; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.15); background: white; padding: 25px; image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges;">
<p style="font-size: 1.0em; color: #2c3e50; margin-top: 15px; font-weight: 600; text-align: center;">Diagrama {i+1}: Arquitectura del Sistema</p>
</div>'''
                    
                    # Reemplazar el bloque completo
                    if mermaid_block in modified_content:
                        modified_content = modified_content.replace(mermaid_block, image_html)
                        print(f"   ✅ Diagrama reemplazado exitosamente")
                    else:
                        print(f"   ⚠️  No se encontró el bloque Mermaid en el contenido")
                        
                except Exception as e:
                    print(f"   ❌ Error procesando imagen: {e}")
            else:
                print(f"   ❌ Imagen no encontrada: {image_path}")
        
        return modified_content
    
    async def process_mermaid_diagrams(self, content: str, temp_dir: str) -> str:
        """Procesar todos los diagramas Mermaid en el contenido"""
        # Resetear contador para cada archivo
        self.mermaid_counter = 0
        
        diagrams = await self.extract_mermaid_diagrams(content)
        
        if not diagrams:
            return content
        
        print(f"📊 Encontrados {len(diagrams)} diagramas Mermaid")
        
        # Primero generar todas las imágenes
        for mermaid_code, placeholder_id in diagrams:
            image_path = os.path.join(temp_dir, f"{placeholder_id}.png")
            print(f"🎨 Generando imagen para {placeholder_id}...")
            
            success = await self.render_mermaid_to_image(mermaid_code, image_path)
            if success:
                print(f"   ✅ Imagen generada: {placeholder_id}.png")
            else:
                print(f"   ❌ Error generando: {placeholder_id}")
        
        # Luego reemplazar en el contenido
        modified_content = self.replace_mermaid_with_images(content, diagrams, temp_dir)
        return modified_content
    
    def markdown_to_html(self, content: str) -> str:
        """Convertir Markdown a HTML con estilos mejorados"""
        md = markdown.Markdown(
            extensions=[
                'markdown.extensions.tables',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
                'markdown.extensions.fenced_code'
            ],
            extension_configs={
                'codehilite': {'css_class': 'highlight'},
                'toc': {'permalink': True}
            }
        )
        
        html_content = md.convert(content)
        
        css_styles = """
        <style>
            @media print {
                @page {
                    size: A4;
                    margin: 2cm;
                }
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
            }
            
            h1, h2, h3, h4, h5, h6 {
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 8px;
                margin-top: 25px;
                margin-bottom: 15px;
                page-break-after: avoid;
            }
            
            h1 { font-size: 2.2em; }
            h2 { font-size: 1.8em; }
            h3 { font-size: 1.4em; }
            
            code {
                background-color: #f8f9fa;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', Courier, monospace;
                color: #e83e8c;
                font-size: 0.9em;
            }
            
            pre {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                border-left: 4px solid #3498db;
                overflow-x: auto;
                margin: 15px 0;
                page-break-inside: avoid;
            }
            
            pre code {
                background-color: transparent;
                padding: 0;
                color: inherit;
            }
            
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
                page-break-inside: avoid;
            }
            
            table th, table td {
                border: 1px solid #ddd;
                padding: 8px 12px;
                text-align: left;
            }
            
            table th {
                background-color: #f2f2f2;
                font-weight: bold;
            }
            
            table tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            
            img {
                max-width: 100%;
                height: auto;
                display: block;
                margin: 20px auto;
                page-break-inside: avoid;
                image-rendering: -webkit-optimize-contrast;
                image-rendering: crisp-edges;
            }
            
            /* Estilos específicos para contenedores de diagramas */
            div[style*="text-align: center"] {
                break-inside: avoid;
                page-break-inside: avoid;
            }
            
            ul, ol {
                margin: 10px 0;
                padding-left: 25px;
            }
            
            li { margin: 3px 0; }
            
            blockquote {
                border-left: 4px solid #3498db;
                margin: 15px 0;
                padding-left: 15px;
                color: #666;
                font-style: italic;
            }
            
            .page-break {
                page-break-before: always;
            }
        </style>
        """
        
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Documento PDF</title>
            {css_styles}
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
    
    async def html_to_pdf_with_playwright(self, html_content: str, output_path: str) -> bool:
        """Convertir HTML a PDF usando Playwright"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                await page.set_content(html_content, wait_until='networkidle')
                
                # Configuración para PDF con mayor calidad
                pdf_options = {
                    'path': output_path,
                    'format': 'A4',
                    'print_background': True,
                    'prefer_css_page_size': True,
                    'display_header_footer': False,
                    'margin': {
                        'top': '2cm',
                        'right': '2cm', 
                        'bottom': '2cm',
                        'left': '2cm'
                    },
                    # Configuraciones adicionales para mejor calidad
                    'scale': 1.0,
                    'width': '21cm',
                    'height': '29.7cm'
                }
                
                await page.pdf(**pdf_options)
                await browser.close()
                
                return True
                
        except Exception as e:
            print(f"❌ Error generando PDF: {e}")
            return False
    
    async def convert_markdown_to_pdf(self, input_path: str, output_path: str) -> bool:
        """Convertir archivo Markdown a PDF"""
        try:
            temp_dir = self.setup_temp_directory()
            
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"📖 Procesando: {os.path.basename(input_path)}")
            
            # Procesar diagramas Mermaid
            processed_content = await self.process_mermaid_diagrams(content, temp_dir)
            
            # Convertir a HTML
            html_content = self.markdown_to_html(processed_content)
            
            # Generar PDF
            success = await self.html_to_pdf_with_playwright(html_content, output_path)
            
            if success:
                file_size = os.path.getsize(output_path) / (1024 * 1024)
                print(f"✅ PDF generado: {os.path.basename(output_path)} ({file_size:.2f} MB)")
            
            return success
            
        except Exception as e:
            print(f"❌ Error en conversión: {e}")
            return False
        finally:
            self.cleanup()

async def main():
    """Función principal para probar la conversión"""
    converter = SimpleMdToPdfConverter()
    
    input_file = "02-arquitectura-destino.md"
    output_file = "02-arquitectura-destino.pdf"
    
    print("🔄 CONVERTIDOR MD → PDF")
    print("="*40)
    
    if os.path.exists(input_file):
        print(f"🚀 Iniciando conversión de {input_file}")
        success = await converter.convert_markdown_to_pdf(input_file, output_file)
        
        if success:
            print(f"🎉 ¡Conversión completada exitosamente!")
        else:
            print(f"❌ Error en la conversión")
    else:
        print(f"❌ Archivo no encontrado: {input_file}")

if __name__ == "__main__":
    asyncio.run(main())