# Convertidores de Markdown con Soporte Mermaid

Esta suite de herramientas Python convierte automáticamente archivos Markdown a PDF y Word manteniendo la estructura del documento y renderizando los diagramas Mermaid como imágenes embebidas.

## ✨ Características

- ✅ **Conversión completa MD → PDF/Word** con formato profesional
- 📊 **Renderización de diagramas Mermaid** como imágenes de alta calidad
- 🎨 **Estilos optimizados** para documentos técnicos
- 📑 **Soporte completo para formato Markdown**: tablas, código, **negrita**, *cursiva*, `código inline`
- 🚀 **Procesamiento en lote** de múltiples archivos
- 💻 **Compatible con Windows** sin dependencias complejas
- 🔧 **Formato de texto corregido**: texto entre `**` se convierte correctamente a negrita

## 🔧 Dependencias Instaladas

### Para conversión a PDF:
```bash
pip install markdown playwright beautifulsoup4 requests pdfkit
playwright install chromium
```

### Para conversión a Word:
```bash
pip install markdown playwright beautifulsoup4 python-docx
playwright install chromium
```

## 📁 Archivos Creados

### Convertidores PDF:
#### 1. **`simple_md_to_pdf.py`** - Convertidor principal PDF
- Extrae y renderiza diagramas Mermaid usando Playwright
- Convierte Markdown a HTML con estilos CSS profesionales
- Genera PDF usando el motor de renderizado de Chromium
- Maneja archivos temporales automáticamente

#### 2. **`batch_md_to_pdf.py`** - Procesamiento masivo PDF
- Procesa todos los archivos .md del directorio automáticamente
- Proporciona progreso detallado y estadísticas de conversión
- Genera resumen final con tamaños de archivos y tasa de éxito

### Convertidores Word:
#### 3. **`simple_md_to_word.py`** - Convertidor principal Word ⭐ **ACTUALIZADO**
- **🔥 CORRECCIONES APLICADAS**: Formato de negrita `**texto**` funciona correctamente en **todos los contextos**
- ✅ **Párrafos**: Formato de texto procesado correctamente
- ✅ **Listas**: Corregido procesamiento de formato en elementos de lista
- ✅ **Tablas**: Corregido formato en celdas (elimina asteriscos, aplica negrita)
- Extrae y renderiza diagramas Mermaid como imágenes de alta resolución
- Convierte directamente a formato .docx usando python-docx
- Preserva formato: **negrita**, *cursiva*, `código`, tablas y encabezados
- Manejo inteligente de archivos en uso (genera nombres alternativos)
- Función de prueba integrada: `python simple_md_to_word.py --test`

#### 4. **`batch_md_to_word.py`** - Procesamiento masivo Word
- Convierte todos los archivos .md del directorio a formato Word
- Estadísticas detalladas de conversión

## 🚀 Uso

### Conversión a PDF:
```bash
# Archivo individual
python simple_md_to_pdf.py archivo.md

# Todos los archivos MD del directorio
python batch_md_to_pdf.py
```

### Conversión a Word:
```bash
# Archivo individual
python simple_md_to_word.py archivo.md

# Todos los archivos MD del directorio
python batch_md_to_word.py

# Probar formato de texto (para verificar negrita, cursiva, etc.)
python simple_md_to_word.py --test
```
