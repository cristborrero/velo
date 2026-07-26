# Proposal: Video Downloader Tool

## Intent
Crear una herramienta de CLI y biblioteca modular para descargar videos de internet mediante una URL, permitiendo al usuario consultar e inspeccionar los formatos y calidades disponibles antes de realizar la descarga.

## Scope

### In Scope
- Clase de descarga (`VideoDownloader`) que encapsula la API de `yt-dlp`.
- Extracción de formatos con metadatos: id, resolución, extensión y tamaño estimado.
- Descarga de video dada una URL y el ID de formato elegido.
- CLI interactivo para listar calidades y ejecutar la descarga.
- Tests unitarios con mocks para evitar peticiones reales de red durante las pruebas.

### Out of Scope
- Descargas concurrentes de múltiples URLs.
- Interfaz gráfica (GUI).
- Conversión/transcodificación de formatos post-descarga (ej. MP4 a MP3).

## Capabilities

### New Capabilities
- `video-downloader`: Descarga de videos y consulta previa de formatos mediante URL.

### Modified Capabilities
None

## Approach
Implementar una clase wrapper `VideoDownloader` en `downloader/core.py` utilizando la API de Python de `yt-dlp`. La CLI en `downloader/cli.py` y `main.py` interactuará con el wrapper para mostrar las opciones al usuario y procesar la descarga.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `downloader/core.py` | New | Lógica modular de interacción con `yt-dlp` |
| `downloader/cli.py` | New | Interfaz de consola e interacción con el usuario |
| `main.py` | New | Punto de entrada ejecutable de la herramienta |
| `tests/test_downloader.py` | New | Tests de la lógica de extracción y descarga |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Cambios en la firma de `yt-dlp` o bloqueos de red | Med | Manejar `DownloadError` con mensajes claros y sugerir actualización |
| Formatos sin información de tamaño/resolución | Med | Proveer fallbacks ("Desconocido") en la visualización |

## Rollback Plan
Eliminar los archivos creados en `downloader/`, `main.py`, `tests/test_downloader.py` y restaurar los tests placeholder.

## Dependencies
- `yt-dlp` (biblioteca de descarga)
- `pytest` (framework de testeo)

## Success Criteria
- [ ] Listar formatos legibles a partir de una URL válida.
- [ ] Descargar exitosamente un video en la calidad seleccionada.
- [ ] Tests unitarios implementados con 80%+ de cobertura.
