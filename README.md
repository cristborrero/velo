<div align="center">

  # ⚡ VELO (v2.0 SaaS Edition)

  **High-Performance Multimedia Processing & Extraction Platform**

  [![English](https://img.shields.io/badge/Language-English-blue.svg?style=flat-square)](README.md)
  [![Español](https://img.shields.io/badge/Idioma-Español-green.svg?style=flat-square)](README.es.md)
  [![License: MIT](https://img.shields.io/badge/License-MIT-white.svg?style=flat-square)](LICENSE)
  [![Python](https://img.shields.io/badge/Python-3.11+-white.svg?style=flat-square&logo=python&logoColor=black)](https://www.python.org/)
  [![Flask](https://img.shields.io/badge/Framework-Flask-white.svg?style=flat-square&logo=flask&logoColor=black)](https://flask.palletsprojects.com/)
  [![Tests](https://img.shields.io/badge/Tests-30%2F30%20PASSED-brightgreen.svg?style=flat-square)](tests/)
  [![Security](https://img.shields.io/badge/Security-HTTP%20Headers%20Ready-white.svg?style=flat-square)]()
  [![SEO](https://img.shields.io/badge/SEO-JSON--LD%20%26%20Sitemap-white.svg?style=flat-square)]()
  [![Design](https://img.shields.io/badge/Design-SaaS%202--Column%20OLED-white.svg?style=flat-square)](static/style.css)
  [![Deploy](https://img.shields.io/badge/Deploy-Render%20%2F%20Docker-white.svg?style=flat-square&logo=render&logoColor=black)](render.yaml)

  **[ 🇺🇸 English ](README.md)** • **[ 🇪🇸 Español ](README.es.md)**

  [Overview](#-overview) • [Features](#-features--design-system) • [Architecture](#-system-architecture) • [API Reference](#-api-reference) • [Local Usage](#-installation--local-usage) • [Deployment](#-production-deployment)

</div>

---

## 🌟 Overview

**Velo** is a privacy-first, high-efficiency web application for multimedia extraction and processing. Built with a minimal 2-column SaaS architecture inspired by **Linear, Raycast, and ElevenLabs**, Velo allows users to inspect native resolutions (up to 4K/60fps), process bulk playlist downloads into `.zip` archives, trim video/audio clips with a CapCut-style dual-range visual editor, export subtitles (`.srt`, `.vtt`, `.txt`), and extract master-quality audio in MP3 320kbps and uncompressed WAV.

---

## ✨ Features & Design System

### Product Capabilities
- 🎬 **Native 4K & 1080p60 Resolution**: Direct access to combined or split high-definition media streams without quality loss.
- 📦 **Bulk Batch Downloads (`Batch Zip`)**: Asynchronous extraction of playlists and multi-link batches packaged into a single compressed `.zip` file.
- ✂️ **Smart Clip Editor (CapCut Style)**: Dual-range visual selector (In/Out) with quick preset shortcut buttons (`15s`, `30s`, `60s`, `Full`).
- 🎵 **HD Audio Masters**: Independent audio extraction in MP3 320kbps and uncompressed WAV format.
- 💬 **Subtitle Exporter**: Automatic detection of official and auto-generated transcripts exported directly to `.srt`, `.vtt`, and `.txt`.
- 🎞️ **Animated GIF Converter**: Two-pass FFmpeg `palettegen` conversion for crisp GIFs without color degradation.
- ♿ **ARIA Accessibility & Keyboard Support**: Full screen-reader support with `role="radiogroup"`, `role="radio"`, and dynamic `aria-checked` states.
- 🛡️ **Defense-in-Depth Security**: HTTP security header injection (`nosniff`, `DENY`, `strict-origin-when-cross-origin`, `Permissions-Policy`).

### Design System (Optimus OLED)
- **Color Palette**: Deep dark OLED background (`#050505`), dark gray surfaces (`#0D0D0F`), discrete subtle borders (`#222226`), and positive neon green accents (`#2EEA83`).
- **Typography**: Modern sans-serif with *Plus Jakarta Sans* for UI and *JetBrains Mono* for technical telemetry.
- **2-Column Layout**:
  - **Left Column (65%)**: Input URL controls, download group selector cards, and advanced options panel.
  - **Right Column (35%)**: Floating *sticky* summary card featuring thumbnail preview, real-time telemetry, and pre-flight validation checklist.

---

## 📐 System Architecture

```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                 SaaS Web Client / PWA (App Shell)                      │
  │     (HTML5 + Vanilla CSS OLED 2-Column + JavaScript ES6 Async API)     │
  └────────────────────────────────────┬────────────────────────────────────┘
                                       │
                                       ▼ REST API (Flask 3.x)
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                        REST Server (app.py)                             │
  │   /api/info     /api/download/start     /api/subtitles/download         │
  │   /robots.txt   /sitemap.xml            /api/batch/start                │
  │   [HTTP Security Headers Middleware: nosniff, DENY, Referrer-Policy]    │
  └────────────────────────────────────┬────────────────────────────────────┘
                                       │
                                       ▼ Extraction Engine
  ┌─────────────────────────────────────────────────────────────────────────┐
  │               VideoDownloader Core (downloader/core.py)                 │
  │        yt-dlp Engine + FFmpeg Post-Processor Pipelines                  │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔌 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/info` | Extracts media metadata (title, thumbnail, duration, subtitles, and available formats). |
| `POST` | `/api/download/start` | Starts asynchronous background download for a video/clip. |
| `GET` | `/api/download/status/<id>` | Polls real-time download telemetry (percentage, MB/s, ETA). |
| `GET` | `/api/download/file/<id>` | Transfers the processed file to the browser. |
| `POST` | `/api/subtitles/download` | Exports transcripts in `.srt`, `.vtt`, or `.txt` format. |
| `POST` | `/api/convert/gif` | Exports a video section into a high-fidelity animated GIF. |
| `POST` | `/api/batch/start` | Starts batch download of multiple URLs compressed into a `.zip` file. |
| `GET` | `/robots.txt` | Serves search engine crawling directives. |
| `GET` | `/sitemap.xml` | Serves XML sitemap for SEO indexing. |

---

## 🛠️ Installation & Local Usage

### Prerequisites
- **Python**: 3.11 or higher.
- **FFmpeg**: Required for media stream merging and GIF generation.

### Installation Steps
```bash
# 1. Clone the repository
git clone https://github.com/cristborrero/velo.git
cd velo

# 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the local server
python app.py
```
Access the application at `http://127.0.0.1:5001`.

### Automated Testing
```bash
# Run complete test suite with pytest (30/30 tests passing)
.venv/bin/pytest tests/ -v
```

---

## ☁️ Production Deployment

### Docker / Render Deployment
The project includes native configuration for Render (`render.yaml`), Dockerfile, and Procfile using Gunicorn WSGI server:

```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5001
# Download state is process-local, so keep a single worker.
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "1", "--threads", "4", "--worker-class", "gthread", "app:app"]
```

---

## 📜 License

Distributed under the MIT License.
