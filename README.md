<div align="center">

  # ⚡ VELO (v3.0.0 Pro)

  **Descargador de Video, Audio HD, GIF Animados y Subtítulos de Nivel Enterprise**

  [![License: MIT](https://img.shields.io/badge/License-MIT-white.svg?style=flat-square)](LICENSE)
  [![Python](https://img.shields.io/badge/Python-3.11+-white.svg?style=flat-square&logo=python&logoColor=black)](https://www.python.org/)
  [![Flask](https://img.shields.io/badge/Framework-Flask-white.svg?style=flat-square&logo=flask&logoColor=black)](https://flask.palletsprojects.com/)
  [![PWA Ready](https://img.shields.io/badge/PWA-Installable-white.svg?style=flat-square&logo=pwa&logoColor=black)](/sw.js)
  [![Build Status](https://img.shields.io/badge/Tests-24%2F24%20PASSED-brightgreen.svg?style=flat-square)](tests/)
  [![Design](https://img.shields.io/badge/Design-Optimus%20OLED-white.svg?style=flat-square)](static/style.css)
  [![Deploy](https://img.shields.io/badge/Deploy-Render%20%2F%20Docker-white.svg?style=flat-square&logo=render&logoColor=black)](render.yaml)

  [Visión General](#-visión-general) • [Características](#-características-clave) • [Arquitectura](#-arquitectura-del-sistema) • [Referencia API](#-referencia-de-la-api) • [Uso Local](#-instalación-y-uso-local) • [Despliegue](#-despliegue-en-producción)

</div>

---

## 🌟 Visión General

**Velo** es un descargador multiplataforma de vanguardia diseñado con arquitectura minimalista OLED. Permite extraer contenido audiovisual en máxima resolución (4K/HD), recortar clips con un selector de tiempo de alta precisión estilo CapCut, convertir videos a GIF animado de alta fidelidad, extraer audio en calidad máster MP3 320kbps/WAV, descargar transcripciones y procesar listas de reproducción masivas en formato `.zip`.

---

## ✨ Características Clave

- 🎬 **Extracción en Máxima Calidad**: Soporte para formatos combinados y separados (hasta 4K/60fps) mediante combinación asíncrona con `FFmpeg`.
- ✂️ **Recorte de Clips CapCut Trim**: Selector visual de doble rango (In/Out) con ajustes rápidos (`15s`, `30s`, `60s`, `Completo`).
- 💬 **Extractor de Subtítulos**: Descarga de transcripciones automáticas y oficiales en `.srt`, `.vtt` y texto plano `.txt`.
- 🎞️ **Exportador a GIF Animado**: Conversión con filtros `palettegen` y `paletteuse` de dos pasadas para GIFs nítidos sin degradación de color.
- 🎵 **Audio HD Máster**: Salida en MP3 320kbps y WAV no comprimido.
- 📦 **Descarga Masiva en Lote (`Batch Zip`)**: Descarga paralela de listas de reproducción y múltiples enlaces comprimidos automáticamente en `.zip`.
- ⚡ **PWA Instalable & Web Share Target**: Instalación como app nativa en dispositivos móviles/escritorio y recepción directa de enlaces compartidos desde otras aplicaciones.
- 🖤 **Diseño Optimus OLED**: Interfaz en modo oscuro profundo con spotlight reactivo al cursor, isla de navegación flotante y respuesta táctil sutil.

---

## 📐 Arquitectura del Sistema

```
  ┌─────────────────────────────────────────────────────────────┐
  │                    Cliente Web / PWA (App Shell)             │
  │     (HTML5 + Vanilla CSS Optimus OLED + JavaScript ES6)     │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼ REST API (Flask 3.x)
  ┌─────────────────────────────────────────────────────────────┐
  │                 Servidor REST (app.py)                       │
  │   /api/info   /api/download/start   /api/subtitles/download   │
  │   /sw.js      /api/convert/gif      /api/batch/start         │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼ Motor de Extracción
  ┌─────────────────────────────────────────────────────────────┐
  │            VideoDownloader Core (downloader/core.py)        │
  │        yt-dlp Engine + FFmpeg Post-Processor Pipelines        │
  └─────────────────────────────────────────────────────────────┘
```

---

## 🔌 Referencia de la API

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/api/info` | Extrae metadatos (título, miniatura, duración, subtítulos y formatos). |
| `POST` | `/api/download/start` | Inicia la descarga asíncrona de un video/clip en segundo plano. |
| `GET` | `/api/download/status/<id>` | Consulta la telemetría en tiempo real (porcentaje, MB/s, ETA). |
| `GET` | `/api/download/file/<id>` | Descarga el archivo procesado al cliente. |
| `POST` | `/api/subtitles/download` | Descarga transcripciones en formato `.srt`, `.vtt` o `.txt`. |
| `POST` | `/api/convert/gif` | Exporta una sección del video a GIF animado de alta fidelidad. |
| `POST` | `/api/batch/start` | Inicia la descarga en lote de múltiples URLs empaquetadas en `.zip`. |
| `GET` | `/sw.js` | Sirve el Service Worker para soporte PWA Offline. |

---

## 🛠️ Instalación y Uso Local

### Prerrequisitos
- **Python**: 3.11 o superior.
- **FFmpeg**: Requerido para fusión de formatos de video/audio y generación de GIFs.

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
# Ejecutar la suite completa con pytest (24/24 pruebas)
pytest tests/ -v
```

---

## ☁️ Despliegue en Producción

### Despliegue con Docker / Render
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
