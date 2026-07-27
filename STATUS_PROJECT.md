# Estado del Proyecto: Velo (v3.0.0 Pro)

> **Servidor Web Local**: `http://127.0.0.1:5001`  
> **Repositorio GitHub**: `https://github.com/cristborrero/velo.git`  
> **Estado de la Suite de Pruebas**: `24/24 Pruebas Pasadas (100%)`

---

### ✅ Funcionalidades Completadas & Verificadas (Roadmap 100% Completado)

- [x] **Inspección de Metadatos**: Título, uploader, miniatura HD y duración.
- [x] **Filtrado & Categorización**: Video + Audio (HD/4K), Solo Audio (MP3/M4A/Opus), Códecs WebM alternables.
- [x] **Recorte Intuitivo de Clips (`Trim & Clip`) estilo CapCut**:
  - Selector visual con doble deslizador de tiempo de inicio (In) y fin (Out).
  - Previsualización del rango seleccionado y duraciones predefinidas (`15s`, `30s`, `60s`, `Completo`).
  - Procesamiento preciso mediante `download_ranges` de `yt-dlp` y `FFmpeg`.
- [x] **Extractor de Subtítulos & Transcripciones**:
  - Selección de idioma de subtítulos automáticos y manuales.
  - Descarga directa en formatos `.srt`, `.vtt` y texto plano `.txt`.
- [x] **Exportador a GIF Animado & Audio HD Máster**:
  - Conversión inteligente de clips a `.gif` animado utilizando dos pasadas de `palettegen` de FFmpeg.
  - Extracción de audio en calidad máster MP3 320kbps y WAV sin compresión.
- [x] **Descargas Masivas y Playlists (`Batch Download`)**:
  - Conmutador de modo de entrada (`URL Única` vs `Lista / Playlist (.ZIP)`).
  - Descarga paralela de múltiples URLs empaquetadas en un único archivo `.zip`.
- [x] **PWA Instalable & Web Share Target**:
  - Service Worker nativo (`sw.js`) con almacenamiento en caché offline.
  - Botón discreto de instalación nativa `Instalar App Velo`.
  - Receptor de enlaces `share_target` para recibir URLs de YouTube/Instagram compartidas desde Android/iOS/macOS.
- [x] **Descargas Asíncronas & Telemetría en Tiempo Real**:
  - Hilos en segundo plano con polling REST `/api/download/status/<id>`.
  - Porcentaje, bytes transferidos, MB/s y ETA.
- [x] **Diseño Optimus OLED**: Cuadrícula técnica, spotlight interactivo por cursor, isla flotante de navegación y ventana embebida macOS.
- [x] **Módulo de Donaciones PayPal**: Integración con contenedor oscuro y renderizado responsivo.
- [x] **Infraestructura de Producción**: `render.yaml` (Docker environment), `Dockerfile`, `Procfile` y `requirements.txt` con Gunicorn.
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
