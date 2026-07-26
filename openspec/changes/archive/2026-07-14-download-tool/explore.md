## Exploration: Video Downloader Tool

### Current State
El repositorio es un proyecto nuevo de Python recién inicializado con un archivo de requerimientos (`requirements.txt`) que incluye `yt-dlp` y `pytest`, y un test de prueba (`tests/test_placeholder.py`). No existe lógica de descarga implementada aún.

### Affected Areas
- `downloader/core.py` [NEW] — Contendrá la clase modular de descarga y extracción de formatos usando la API de Python de `yt-dlp`.
- `downloader/cli.py` [NEW] — Punto de entrada de la interfaz de consola para el usuario.
- `tests/test_downloader.py` [NEW] — Tests unitarios e integración para la lógica de descarga.

### Approaches
1. **Script CLI Directo (Subprocess / yt-dlp directo)**
   - Breve descripción: Un script simple que recibe parámetros por terminal y ejecuta subprocesses de `yt-dlp` o llamadas directas en un archivo plano.
   - Pros: Implementación extremadamente rápida.
   - Cons: Dificulta el testing unitario y el desacoplamiento.
   - Effort: Low

2. **Clase Wrapper Modular (`VideoDownloader`)**
   - Breve descripción: Crear un módulo centralizado (`downloader/core.py`) que use la API interna de `yt-dlp` y exponga interfaces limpias como `get_available_formats(url)` y `download_video(url, format_id)`.
   - Pros: Cumple con Clean Architecture, altamente testeable con Mocks de pytest, escalable.
   - Cons: Mayor tiempo de desarrollo inicial para configurar el wrapper y mockear la API de `yt-dlp` en los tests.
   - Effort: Medium

### Recommendation
Recomiendo la **Opción 2 (Wrapper Modular)**. Al encapsular `yt-dlp`, podemos extraer calidades de forma estructurada, testear la lógica de negocio sin realizar descargas reales (usando mocks) y mantener el punto de entrada CLI limpio de detalles de implementación de la librería de terceros.

### Risks
- **Cambios en APIs de plataformas**: Sitios como YouTube actualizan constantemente su seguridad y formatos. Dependeremos de que `yt-dlp` se mantenga actualizado.
- **Formateo de calidades**: La estructura de formatos devuelta por `yt-dlp` puede ser compleja de filtrar y limpiar. Necesitaremos un parser robusto.

### Ready for Proposal
Yes. La exploración está completa y el camino a seguir está claro.
