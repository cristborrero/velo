# Design: Video Downloader Tool

## Technical Approach
Implementaremos una biblioteca modular para la interacción con `yt-dlp` y un punto de entrada CLI interactivo en Python. Esto separa la lógica de interacción con APIs externas de la lógica de presentación del usuario.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|----------|--------|-------------------------|-----------|
| Librería base | `yt-dlp` importable | `pytube`, `youtube-dl` | `yt-dlp` es la única activamente mantenida y robusta frente a cambios en plataformas. |
| Estructura CLI | Interactivo por consola | click, typer | Permite la selección interactiva de calidades listadas de forma natural usando prompts numéricos. |

## Data Flow
```
 CLI (cli.py) ───────> VideoDownloader (core.py) ─────> yt-dlp API (extract_info)
      │                                                     │
      │ <─────── Retorna formatos limpios <─────────────────┘
      ▼
 Muestra menú ───────> Entrada de usuario (Opción)
      │
      ▼
 Llama download(url, format_id) ──> yt-dlp API ───────> Descarga en disco
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `downloader/__init__.py` | Create | Inicializador del módulo Python |
| `downloader/core.py` | Create | Lógica central y clase wrapper `VideoDownloader` |
| `downloader/cli.py` | Create | Menú interactivo CLI y parseo de argumentos |
| `main.py` | Create | Script de inicio y pasarela hacia CLI |
| `tests/test_downloader.py` | Create | Cobertura de tests unitarios usando mocks de yt-dlp |

## Interfaces / Contracts

```python
# downloader/core.py
from typing import List, Dict, Union

class VideoFormat:
    def __init__(self, format_id: str, resolution: str, ext: str, filesize: Union[float, str]):
        self.format_id = format_id
        self.resolution = resolution
        self.ext = ext
        self.filesize = filesize # en MB o "Desconocido"

class VideoDownloader:
    def get_formats(self, url: str) -> List[VideoFormat]:
        """Extrae la información del video y parsea sus formatos."""
        pass
        
    def download(self, url: str, format_id: str) -> bool:
        """Descarga el formato seleccionado usando yt-dlp."""
        pass
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | Extracción de calidades con datos simulados | Testear `get_formats` inyectando un mock en `YoutubeDL.extract_info` para simular respuestas (con/sin `filesize`). |
| Unit | Descarga de video y manejo de excepciones | Mockear `YoutubeDL.download` para asegurar que recibe el `format_id` correcto y validar el manejo de `DownloadError`. |

## Migration / Rollout
No migration required.

## Open Questions
None.
