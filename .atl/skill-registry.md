# Video Virales Skill Registry

## Compact Rules

- **TDD Workflow**: Escribir los tests unitarios antes de la implementación de la funcionalidad. Todos los nuevos comportamientos deben tener tests que los validen.
- **Python Type Hints**: Usar anotaciones de tipos completas para todas las firmas de funciones y variables expuestas.
- **Error Handling**: Manejar excepciones de manera específica (especialmente las de `yt_dlp` como `DownloadError`) en lugar de usar bloques `except` genéricos.
- **Clean Architecture**: Mantener la lógica de descarga e información del video desacoplada de la interfaz CLI o punto de entrada.

## User Skills

| Skill | Description | Trigger Context |
|-------|-------------|-----------------|
| `sdd-init` | Inicializa el contexto de SDD | `sdd init`, `/sdd-init` |
| `sdd-explore` | Explora la base de código y opciones arquitectónicas | `/sdd-explore` |
| `sdd-propose` | Genera o actualiza la propuesta de cambio | `/sdd-propose` |
| `sdd-spec` | Escribe especificaciones detalladas | `/sdd-spec` |
| `sdd-design` | Diseña la arquitectura y lógica técnica | `/sdd-design` |
| `sdd-tasks` | Divide el diseño en tareas ejecutables | `/sdd-tasks` |
| `sdd-apply` | Aplica los cambios implementando las tareas | `/sdd-apply` |
| `sdd-verify` | Verifica la implementación contra especificaciones y tests | `/sdd-verify` |
| `sdd-archive` | Cierra y archiva el cambio actual | `/sdd-archive` |
| `tdd-workflow` | Workflow para guiar el desarrollo guiado por pruebas | Test-driven development, testing |
| `coding-standards` | Estándares universales de codificación | Codificación general |
| `backend-patterns` | Patrones de arquitectura backend y modularidad | Backend development |
