# Estado del Proyecto & Roadmap Velo 🚀

## 📌 Estado Actual (Versión 2.1.0)

Plataforma multimedia de alto rendimiento con arquitectura monolítica unificada (Flask + yt-dlp + FFmpeg) desplegada en Render con diseño **Vercel / Linear Optimus OLED** y motor de **Recorte de Clips CapCut Trim**.

### ✅ Funcionalidades Completadas & Verificadas
- [x] **Inspección de Metadatos**: Título, uploader, miniatura HD y duración.
- [x] **Filtrado & Categorización**: Video + Audio (HD/4K), Solo Audio (MP3/M4A/Opus).
- [x] **Recorte Intuitivo de Clips (`Trim & Clip`) estilo CapCut**:
  - Selector visual con doble deslizador de tiempo de inicio (In) y fin (Out).
  - Previsualización del rango seleccionado y duraciones predefinidas (`15s`, `30s`, `60s`, `Completo`).
  - Procesamiento preciso mediante `download_ranges` de `yt-dlp` y `FFmpeg`.
- [x] **Descargas Asíncronas**: Hilos en segundo plano con polling REST `/api/download/status/<id>`.
- [x] **Telemetría en Tiempo Real**: Porcentaje, bytes transferidos, MB/s y ETA.
- [x] **Diseño Optimus OLED**: Cuadrícula técnica, spotlight interactivo por cursor, isla flotante de navegación y ventana embebida macOS.
- [x] **Módulo de Donaciones PayPal**: Integración con contenedor oscuro y renderizado responsivo.
- [x] **Infraestructura de Producción**: `render.yaml` (Docker environment), `Dockerfile`, `Procfile` y `requirements.txt` con Gunicorn.
- [x] **Suite de Pruebas**: 18/18 pruebas pasadas en `pytest`.

---

## 🔮 Roadmap de Funcionalidades Futuras

### 🟡 Próximas Fases
- [ ] **Extractor de Subtítulos & Transcripciones**:
  - Selección y descarga de subtítulos en formatos `.srt`, `.vtt` y texto plano `.txt`.
- [ ] **Exportador a GIF Animado & Audio HD**:
  - Conversión directa de clips a formato `.gif` animado para redes sociales.
  - Opción de extracción de audio en calidad máster MP3 320kbps / WAV.
- [ ] **Descargas Masivas y Playlists (`Batch Download`)**:
  - Soporte para múltiples URLs y listas de reproducción comprimidas en `.zip`.
- [ ] **PWA Instalable & Web Share Target**:
  - Instalación como app nativa en teléfonos/escritorios con botón de compartir directo desde otras aplicaciones.
