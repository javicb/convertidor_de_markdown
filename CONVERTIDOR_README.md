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

## 📊 Resultados de Conversión

### PDF - **✅ 100% de éxito** - 12 archivos procesados:

| Archivo | Diagramas Mermaid | Tamaño PDF |
|---------|------------------|------------|
| `01-analisis-aplicacion-actual.md` | 0 | 0.14 MB |
| `02-arquitectura-destino.md` | 1 | 0.14 MB |
| `03-plan-migracion-paso-a-paso.md` | 2 | 0.21 MB |
| `04-estrategia-coexistencia.md` | 1 | 0.12 MB |
| `05-integracion-rds-energy.md` | 1 | 0.18 MB |
| `06-migracion-datos.md` | 2 | 0.16 MB |
| `07-testing-qa.md` | 1 | 0.16 MB |
| `08-seguridad-autenticacion.md` | 1 | 0.16 MB |
| `09-optimizacion-rendimiento.md` | 0 | 0.15 MB |
| `10-infraestructura-azure.md` | 1 | 0.14 MB |
| `11-despliegue-transicion.md` | 1 | 0.15 MB |
| `README.md` | 0 | 0.06 MB |

**📦 PDF Total:** 1.76 MB

### Word - **✅ 100% de éxito** - Formato completamente corregido:

- ✅ **Párrafos con negrita**: `**Frontend**`, `**Backend**` → **Frontend**, **Backend**
- ✅ **Listas con negrita**: `- **Tiempos elevados**` → • **Tiempos elevados** (sin asteriscos)
- ✅ **Tablas con negrita**: `| **Framework** |` → **Framework** en celda (sin asteriscos)
- ✅ **Diagramas Mermaid** renderizados como imágenes HD (1920x1080)
- ✅ **Formato mixto**: **negrita**, *cursiva*, `código` en mismo párrafo
- ✅ **Manejo de archivos en uso** automático con nombres alternativos

## 🎯 Tecnologías Utilizadas

### Común a ambos convertidores:
- **Playwright**: Renderizado de diagramas Mermaid de alta calidad
- **Python Markdown**: Conversión de Markdown con extensiones
- **BeautifulSoup4**: Procesamiento y manipulación de HTML
- **Mermaid.js**: Renderización de diagramas via CDN
- **Expresiones regulares**: Procesamiento avanzado de formato de texto

### Específicas para PDF:
- **CSS3**: Estilos profesionales para documentos técnicos
- **Chromium**: Motor de renderizado para generación de PDF

### Específicas para Word:
- **python-docx**: Creación nativa de documentos .docx
- **Manejo de estilos**: Formato profesional con tipografías Calibri
- **Gestión de archivos**: Detección y manejo de archivos en uso

## 📋 Características de los Documentos Generados

### PDF:
- **Formato A4** con márgenes de 2cm
- **Tipografía**: Segoe UI para legibilidad
- **Código fuente**: Resaltado con fondo gris y bordes
- **Tablas**: Bordes alternados para mejor lectura
- **Imágenes Mermaid**: Centradas y responsivas
- **Saltos de página** optimizados para elementos grandes

### Word (.docx):
- **Formato A4** con estilos profesionales
- **Tipografía**: Calibri (estándar Office)
- **Formato de texto**: **Negrita**, *cursiva*, `código` correctamente aplicados
- **Encabezados**: Jerarquía con tamaños y colores diferenciados
- **Tablas**: Estilo "Light Grid Accent 1" con encabezados en negrita
- **Imágenes Mermaid**: Alta resolución (1920x1080) centradas
- **Gestión inteligente**: Nombres alternativos si el archivo está en uso

## 💡 Ventajas vs Otras Soluciones

| Característica | Esta suite | Pandoc + plugins | LibreOffice |
|----------------|------------|-------------------|-------------|
| **Instalación** | ✅ Simple pip install | ❌ Múltiples dependencias | ⚠️ Software adicional |
| **Windows** | ✅ Nativo | ❌ Complejo | ✅ Compatible |
| **Mermaid** | ✅ Renderizado HD | ⚠️ Filtros externos | ❌ No soportado |
| **Formato texto** | ✅ **Negrita** corregida | ✅ Funcional | ✅ Básico |
| **Word nativo** | ✅ python-docx | ⚠️ Conversión | ✅ Nativo |
| **PDF calidad** | ✅ Chromium engine | ✅ LaTeX/HTML | ⚠️ Limitado |
| **Mantenimiento** | ✅ Python puro | ❌ Ecosistema complejo | ⚠️ GUI dependiente |

## 🔥 Mejoras Recientes (Diciembre 2025)

### ✅ Corrección Completa de Formato de Texto en Word:

#### 🐛 **Problemas identificados y resueltos:**
- **Listas**: Texto `**negrita**` aparecía con asteriscos en elementos de lista
- **Tablas**: Celdas mostraban `**Framework**` en lugar de **Framework** en negrita
- **Párrafos**: Funcionaban correctamente (sin cambios necesarios)

#### 🔧 **Correcciones técnicas aplicadas:**
- **Listas**: Modificado procesamiento para usar `add_formatted_text()` en lugar de texto plano
- **Tablas**: Implementado limpieza de celdas y aplicación de formato Markdown
- **Regex mejorada**: Procesamiento optimizado de segmentos de texto formateado
- **Función de prueba**: `--test` para verificar procesamiento completo
- **Manejo de errores**: Detección automática de archivos en uso

#### ✅ **Resultado final:**
- **Todos los contextos** (párrafos, listas, tablas) procesan `**negrita**` correctamente
- **Eliminación completa** de asteriscos en documentos Word generados
- **Formato profesional** mantenido en todos los elementos

La suite está **lista para uso en producción** y maneja automáticamente todos los diagramas Mermaid y formato de texto encontrados en los documentos del plan de migración.