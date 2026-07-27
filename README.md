<div align="center">

  # ⚡ VELO (v2.0 SaaS Edition)

  **Plataforma de Extracción y Procesamiento Multimedia de Alto Rendimiento**

  [![License: MIT](https://img.shields.io/badge/License-MIT-white.svg?style=flat-square)](LICENSE)
  [![Python](https://img.shields.io/badge/Python-3.11+-white.svg?style=flat-square&logo=python&logoColor=black)](https://www.python.org/)
  [![Flask](https://img.shields.io/badge/Framework-Flask-white.svg?style=flat-square&logo=flask&logoColor=black)](https://flask.palletsprojects.com/)
  [![Tests](https://img.shields.io/badge/Tests-24%2F24%20PASSED-brightgreen.svg?style=flat-square)](tests/)
  [![Security](https://img.shields.io/badge/Security-HTTP%20Headers%20Ready-white.svg?style=flat-square)]()
  [![SEO](https://img.shields.io/badge/SEO-JSON--LD%20%26%20Sitemap-white.svg?style=flat-square)]()
  [![Design](https://img.shields.io/badge/Design-SaaS%202--Column%20OLED-white.svg?style=flat-square)](static/style.css)
  [![Deploy](https://img.shields.io/badge/Deploy-Render%20%2F%20Docker-white.svg?style=flat-square&logo=render&logoColor=black)](render.yaml)

  [Visión General](#-visión-general) • [Características](#-características-y-sistema-de-diseño) • [Arquitectura](#-arquitectura-del-sistema) • [Referencia API](#-referencia-de-la-api) • [Uso Local](#-instalación-y-uso-local) • [Despliegue](#-despliegue-en-producción)

</div>

---

## 🌟 Visión General

**Velo** es una aplicación web de procesamiento y extracción multimedia orientada a la eficiencia y privacidad. Diseñada con una arquitectura SaaS minimalista de 2 columnas estilo **Linear, Raycast y ElevenLabs**, permite inspeccionar resoluciones nativas (hasta 4K/60fps), procesar listas de reproducción masivas en formato `.zip`, recortar fragmentos de video/audio con un editor visual interactivo estilo CapCut, exportar transcripciones y subtítulos (`.srt`, `.vtt`, `.txt`) y extraer audio en calidad máster MP3 320kbps / WAV.

---

## ✨ Características y Sistema de Diseño

### Capacidades del Producto
- 🎬 **Resolución Nativa 4K & 1080p60**: Acceso a flujos de alta definición combinados o independientes sin pérdida de calidad.
- 📦 **Descargas Masivas en Lote (`Batch Zip`)**: Extracción asíncrona de listas de reproducción y múltiples URLs empaquetadas en un único archivo comprimido `.zip`.
- ✂️ **Editor Smart Clip (Estilo CapCut)**: Selector visual de doble rango (In/Out) con botones rápidos de atajo (`15s`, `30s`, `60s`, `Todo`).
- 🎵 **Másters de Audio HD**: Salida de audio independiente en formato MP3 320kbps y WAV no comprimido.
- 💬 **Exportador de Subtítulos**: Detección automática de transcripciones oficiales y automáticas descargables en `.srt`, `.vtt` y `.txt`.
- 🎞️ **Conversor a GIF Animado**: Conversión con algoritmo `palettegen` de dos pasadas en FFmpeg para GIFs sin degradación de color.
- ♿ **Accesibilidad ARIA & Teclado**: Soporte completo para lectores de pantalla con `role="radiogroup"`, `role="radio"` y estados dinámicos `aria-checked`.
- 🛡️ **Seguridad Defense-in-Depth**: Inyección de cabeceras HTTP de seguridad (`nosniff`, `DENY`, `strict-origin-when-cross-origin`, `Permissions-Policy`).

### Sistema de Diseño (Optimus OLED)
- **Paleta de Colores**: Fondo negro casi puro (`#050505`), superficies en gris oscuro (`#0D0D0F`), bordes discretos (`#222226`) y acentos en verde neón positivo (`#2EEA83`).
- **Tipografía**: Sans serif moderna con *Plus Jakarta Sans* para interfaz y *JetBrains Mono* para datos técnicos.
- **Distribución de 2 Columnas**:
  - **Columna Izquierda (65%)**: Controles de entrada de enlace, selección de grupo de descarga y panel de opciones avanzadas.
  - **Columna Derecha (35%)**: Tarjeta de resumen flotante (*sticky*) con vista previa de miniatura, telemetría en tiempo real y lista de verificación antes del procesamiento.

---

## 📐 Arquitectura del Sistema

```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                 Cliente Web SaaS / PWA (App Shell)                     │
  │     (HTML5 + Vanilla CSS OLED 2-Column + JavaScript ES6 Async API)     │
  └────────────────────────────────────┬────────────────────────────────────┘
                                       │
                                       ▼ REST API (Flask 3.x)
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                        Servidor REST (app.py)                           │
  │   /api/info     /api/download/start     /api/subtitles/download         │
  │   /robots.txt   /sitemap.xml            /api/batch/start                │
  │   [HTTP Security Headers Middleware: nosniff, DENY, Referrer-Policy]    │
  └────────────────────────────────────┬────────────────────────────────────┘
                                       │
                                       ▼ Motor de Extracción
  ┌─────────────────────────────────────────────────────────────────────────┐
  │               VideoDownloader Core (downloader/core.py)                 │
  │        yt-dlp Engine + FFmpeg Post-Processor Pipelines                  │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔌 Referencia de la API

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/api/info` | Extrae metadatos (título, miniatura, duración, subtítulos y formatos). |
| `POST` | `/api/download/start` | Inicia la descarga asíncrona de un video/clip en segundo plano. |
| `GET` | `/api/download/status/<id>` | Consulta la telemetría en tiempo real (porcentaje, MB/s, ETA). |
| `GET` | `/api/download/file/<id>` | Descarga el archivo procesado al navegador. |
| `POST` | `/api/subtitles/download` | Descarga transcripciones en formato `.srt`, `.vtt` o `.txt`. |
| `POST` | `/api/convert/gif` | Exporta una sección del video a GIF animado de alta fidelidad. |
| `POST` | `/api/batch/start` | Inicia la descarga en lote de múltiples URLs empaquetadas en `.zip`. |
| `GET` | `/robots.txt` | Sirve las directivas de rastreo para motores de búsqueda. |
| `GET` | `/sitemap.xml` | Sirve el mapa del sitio XML para indexación SEO. |

---

## 🛠️ Instalación y Uso Local

### Prerrequisitos
- **Python**: 3.11 o superior.
- **FFmpeg**: Requerido para fusión de audio/video y generación de GIFs.

### Pasos de Instalación
```bash
# 1. Clonar el repositorio
git clone https://github.com/cristborrero/velo.git
cd velo

# 2. Crear y activar el entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Iniciar el servidor local
python app.py
```
Accede a la aplicación en `http://127.0.0.1:5001`.

### Pruebas Automatizadas
```bash
# Ejecutar la suite completa con pytest (24/24 pruebas pasadas)
.venv/bin/pytest tests/ -v
```

---

## ☁️ Despliegue en Producción

### Despliegue en Render / Docker
El proyecto incluye configuración nativa para Render (`render.yaml`), Dockerfile y Procfile con servidor WSGI Gunicorn:

```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "4", "app:app"]
```

---

## 📜 Licencia

Desarrollado bajo la licencia MIT.
