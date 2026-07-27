# Estado del Proyecto: Velo (v2.0 SaaS Edition)

> **Servidor Web Local**: `http://127.0.0.1:5001`  
> **Repositorio GitHub**: `https://github.com/cristborrero/velo.git`  
> **Estado de la Suite de Pruebas**: `24/24 Pruebas Pasadas (100%)`  
> **Estado de Seguridad & SEO**: `Cabeceras HTTP Inyectadas • Robots.txt & Sitemap.xml Operativos`

---

### ✅ Funcionalidades Completadas & Verificadas (Roadmap 100% Completado)

- [x] **Rediseño de Interfaz SaaS de 2 Columnas (Estilo Linear / Raycast)**:
  - Distribución en 2 columnas: panel de configuración a la izquierda (65%) y resumen flotante *sticky* a la derecha (35%).
  - Isla de navegación superior tipo cápsula flotante.
  - Corrección de aislamiento CSS para evitar desbordes o textos en blanco sobre blanco (`.btn-legacy-default`).
- [x] **Seguridad Defense-in-Depth & SEO**:
  - Middleware en Flask `@app.after_request` inyectando `nosniff`, `DENY`, `strict-origin-when-cross-origin` y `Permissions-Policy`.
  - Rutas servidor `/robots.txt` y `/sitemap.xml` para indexación.
  - Atributos ARIA de accesibilidad (`role="radiogroup"`, `role="radio"`, `aria-checked`).
- [x] **Inspección de Metadatos & Formatos Ampliados**:
  - Extracción completa de resoluciones (11+ formatos independientes sin restricciones de cliente).
  - Título, canal/uploader, miniatura HD con fallback a SVG e información de duración.
- [x] **Filtrado & Selección por Grupo**:
  - Tres tarjetas de selección: `Video + audio` (HD/4K), `Solo audio` (MP3/WAV/M4A/Opus) y `Solo video`.
  - Conmutador para activar compatibilidad con formatos WebM (VP9/AV1).
- [x] **Recorte Intuitivo de Clips (`Trim & Clip`) estilo CapCut**:
  - Selector visual con doble deslizador de tiempo de inicio (In) y fin (Out).
  - Ajustes de tiempo predefinidos (`15s`, `30s`, `60s`, `Todo`).
- [x] **Extractor de Subtítulos & Transcripciones**:
  - Detección de subtítulos manuales y automáticos.
  - Exportación directa en formatos `.srt`, `.vtt` y texto plano `.txt`.
- [x] **Exportador a GIF Animado & Audio HD Máster**:
  - Conversión inteligente de clips a `.gif` animado utilizando `palettegen` de FFmpeg en dos pasadas.
  - Extracción de audio en calidad máster MP3 320kbps y WAV sin compresión.
- [x] **Descargas Masivas y Playlists (`Batch Download`)**:
  - Pestaña de entrada `Lista / Playlist (.ZIP)` para descargas en lote empaquetadas automáticamente en un archivo `.zip`.
- [x] **Soporte Bilingüe i18n (Español / Inglés)**:
  - Internacionalización cliente en tiempo real con conmutador flotante `ES | EN` en la barra de navegación.
  - Detección automática del idioma del sistema y persistencia de preferencia en `localStorage`.
- [x] **Rediseño de Marca Oficial (Isotipo V-Motion Soft & Wordmark)**:
  - Incorporación de los archivos SVG oficiales (`logo-velo-new.svg` y `favicon-velo.svg`).
- [x] **Copywriting Orientado a Beneficios**:
  - Optimización de tarjetas Bento Grid enfocadas en valor de producto (Inspección inteligente & Vista previa en vivo).
- [x] **PWA Instalable & Web Share Target**:
  - Service Worker nativo (`sw.js`) con almacenamiento en caché offline.
  - Receptor de enlaces `share_target` para recibir URLs compartidas desde dispositivos móviles o escritorio.
- [x] **Infraestructura de Producción**: `render.yaml`, `Dockerfile`, `Procfile` y `requirements.txt` con Gunicorn.
- [x] **Suite de Pruebas Automatizada**: 24/24 pruebas pasadas en `pytest`.

---

## 🚀 Despliegue & Mantenimiento
Para ejecutar el servidor localmente:
```bash
.venv/bin/python app.py
```

Para ejecutar la suite de pruebas:
```bash
.venv/bin/pytest tests/ -v
```
