# Tasks: Video Downloader Tool

## Phase 1: Foundation & Infrastructure

- [ ] 1.1 Crear el archivo `downloader/__init__.py` vacío para definir el paquete.
- [ ] 1.2 Declarar los esqueletos vacíos y firmas de tipo de `VideoFormat` y `VideoDownloader` en `downloader/core.py`.
- [ ] 1.3 Crear el archivo principal `main.py` para invocar la CLI.

## Phase 2: Core Downloader (TDD Cycle)

- [ ] 2.1 Escribir test unitario RED en `tests/test_downloader.py` que valide la extracción de formatos del video.
- [ ] 2.2 Implementar `VideoDownloader.get_formats` en `downloader/core.py` mapeando la respuesta de `yt-dlp` a `VideoFormat` (GREEN).
- [ ] 2.3 Escribir test unitario RED en `tests/test_downloader.py` que valide la descarga de video usando mock de `yt-dlp`.
- [ ] 2.4 Implementar `VideoDownloader.download` en `downloader/core.py` y verificar que pasa el test de descarga (GREEN).
- [ ] 2.5 Refactorizar lógica y tests para limpiar código y manejo de excepciones específicas (REFACTOR).

## Phase 3: CLI Interface & Wiring

- [ ] 3.1 Escribir test unitario RED en `tests/test_cli.py` para la lógica de presentación del menú.
- [ ] 3.2 Implementar menú interactivo y parseo de argumentos en `downloader/cli.py` (GREEN).
- [ ] 3.3 Conectar el script de entrada `main.py` con el método principal de la CLI.

## Phase 4: Verification

- [ ] 4.1 Ejecutar suite completa con `pytest` y validar cobertura del 80%+.
- [ ] 4.2 Realizar prueba manual ejecutando `python main.py` con una URL de prueba para certificar descarga y calidades.
