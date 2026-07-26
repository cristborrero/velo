# video-downloader Specification

## Purpose
Definir los requisitos funcionales de la herramienta para extraer información de formatos de videos en internet y ejecutar la descarga del video en una calidad seleccionada.

## Requirements

### Requirement: Listar formatos disponibles (Formats Extraction)
El sistema MUST extraer e identificar de forma estructurada todos los formatos de video y audio disponibles para una URL dada.
Cada formato MUST proveer la siguiente información:
- `format_id`: Identificador único del formato de descarga.
- `resolution`: Resolución del video (ej. '1080p', '720p') o 'audio' si es un archivo de solo sonido.
- `ext`: Extensión del archivo resultante (ej. 'mp4', 'webm', 'm4a').
- `filesize`: Tamaño estimado del archivo en megabytes (MB) o 'Desconocido' si no se reporta.

#### Scenario: Extracción de formatos en video estándar
- GIVEN una URL válida de video con múltiples formatos disponibles
- WHEN el usuario solicita inspeccionar las calidades
- THEN el sistema retorna una lista con al menos un formato estructurado conteniendo format_id, resolution, ext y filesize.

#### Scenario: Formato con tamaño de archivo no reportado
- GIVEN una URL válida de video donde algunas calidades no reportan `filesize`
- WHEN el usuario solicita inspeccionar las calidades
- THEN el sistema retorna los formatos
- AND asigna la etiqueta 'Desconocido' al campo filesize de las calidades afectadas.

### Requirement: Descargar video por URL y Calidad (Video Downloading)
El sistema MUST descargar el video a partir de la URL y el identificador de formato (`format_id`) seleccionado, guardando el archivo resultante en el directorio actual.

#### Scenario: Descarga exitosa de video en formato seleccionado
- GIVEN una URL válida de video y un `format_id` válido obtenido de la extracción
- WHEN se ejecuta la acción de descarga
- THEN el archivo de video se descarga y se guarda en el almacenamiento local.

#### Scenario: Error ante URL no válida o no soportada
- GIVEN una URL inválida o correspondiente a un sitio no soportado
- WHEN se inicia cualquier operación de extracción o descarga
- THEN el sistema lanza una excepción controlada descriptiva y detiene la ejecución.
