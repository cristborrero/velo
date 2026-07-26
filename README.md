<div align="center">

  # ⚡ Velo — High-Speed Multimedia Extraction Platform

  <p><b>Plataforma web de alto rendimiento y arquitectura limpia para la inspección y descarga multimedia directa en calidad original.</b></p>

  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
  [![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-007ACC?logo=python&logoColor=white)](https://python.org)
  [![Flask](https://img.shields.io/badge/Framework-Flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
  [![Tests: 17 Passed](https://img.shields.io/badge/Tests-17%20Passed-10B981.svg)](tests/)
  [![Design: Vercel / Linear](https://img.shields.io/badge/Design-Vercel%2FLinear%20Optimus-030303?logo=vercel&logoColor=white)](static/style.css)
  [![Deploy to Render](https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render&logoColor=black)](https://render.com)

  <br />

  <a href="#-demostración-y-sistema-de-diseño">Ver Interfaz</a> •
  <a href="#-características-destacadas">Características</a> •
  <a href="#-arquitectura-del-sistema">Arquitectura</a> •
  <a href="#-instalación-y-uso-local">Uso Local</a> •
  <a href="#-despliegue-en-producción-render">Despliegue Render</a>

</div>

---

## 🎯 Visión General

**Velo** combina la potencia del motor de extracción universal `yt-dlp` y procesamiento de streams `FFmpeg` con una interfaz web ultrarrápida diseñada bajo los estándares estéticos de **Vercel & Linear (Plantilla Optimus)**. 

Permite inspeccionar metadatos y descargar contenidos en resolución original (**4K, 1080p, 60fps**) y audios de alta fidelidad (**MP3, M4A, Opus**) desde más de 1,000 plataformas (YouTube, TikTok, Instagram, Twitter/X, Vimeo, Twitch, entre otras), sin anuncios, sin registros y sin límites de velocidad.

---

## 🎨 Demostración y Sistema de Diseño

El apartado visual sigue una filosofía de diseño minimalista de alto nivel:

- **Fondo OLED `#030303` con Iluminación Interactiva**: Retícula técnica ambiental con resplandor radial dinámico (`mouse spotlight`) que sigue la posición exacta del cursor.
- **Barra de Navegación Flotante (`Floating Island Nav`)**: Con desenfoque de fondo de micro-precisión (`backdrop-filter: blur(24px)`).
- **Marco de Aplicación Embebido**: La herramienta de descarga está integrada directamente en el Hero dentro de una ventana de aplicación macOS con indicador de luz `border-beam`.
- **Bento Grid Asimétrico**: Organización de características principales en tarjetas de densidad variable.
- **Módulo de Donaciones de PayPal**: Componente integrado sin fricción con renderizado de contenedor oscuro.
- **Español Neutro**: Redacción técnica profesional libre de modismos regionales.

---

## ⚡ Características Destacadas

- 🔍 **Inspección Instantánea de Metadatos**: Extrae título, creador, duración y miniatura sin descargar el contenido completo.
- 🎬 **Filtrado Inteligente de Formatos**:
  - **Video + Audio**: Formatos HD/4K combinados listos para reproducir.
  - **Solo Audio**: Extracción directa de pistas musicales y podcasts.
- ⚡ **Procesamiento Asíncrono no Bloqueante**: Ejecución de descargas en hilos de fondo (`threading.Thread`) para evitar *timeouts* HTTP en servidores web.
- 📊 **Telemetría en Tiempo Real**: Barra de progreso con indicador de porcentaje, bytes transferidos/totales, velocidad de red (`MB/s`) y tiempo restante estimado (ETA).
- 💻 **Interfaz Dual (CLI & Web)**: Servidor web Flask y menú interactivo de terminal.
- 🧪 **Suite de Pruebas de Calidad**: Cobertura unitaria y de integración automatizada mediante `pytest` (17/17 pruebas pasadas).

---

## 🏗️ Arquitectura del Sistema

```
                        ┌──────────────┐
                        │   main.py    │ (CLI Entry Point)
                        └──────┬───────┘
                               │
                        ┌──────▼───────┐
                        │    cli.py    │ (Interactive Menu)
                        └──────┬───────┘
                               │
┌────────────────────┐  ┌──────▼───────┐  ┌──────────────┐
│ static/index.html  │  │    app.py    │  │  tests/      │ (Pytest Suite)
│ static/style.css   │◄─┤ (Flask Server)│  └──────┬───────┘
│ static/app.js      │  └──────┬───────┘          │
└────────────────────┘         │                  │
                        ┌──────▼───────┐◄─────────┘
                        │   core.py    │ (VideoDownloader Engine)
                        └──────┬───────┘
                               │
                        ┌──────▼───────┐
                        │  yt-dlp API  │ + FFmpeg (Merging)
                        └──────────────┘
```

### Especificación de la API REST

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/` | Sirve la Landing Page web unificada (`index.html`) |
| `POST` | `/api/info` | Retorna metadatos y listas de formatos categorizados |
| `POST` | `/api/download/start` | Arranca la descarga en segundo plano y retorna `download_id` |
| `GET` | `/api/download/status/<id>` | Consulta el progreso, velocidad y estado (`downloading`, `done`, `error`) |
| `GET` | `/api/download/file/<id>` | Transmite el archivo final descargado hacia el navegador |

---

## 🛠️ Requisitos del Sistema

- **Python**: 3.8 o 3.11+
- **FFmpeg**: Requerido en el sistema para la combinación de flujos de video y audio separados en alta definición.

---

## 💻 Instalación y Uso Local

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/cristborrero/velo.git
   cd velo
   ```

2. **Crear e iniciar el entorno virtual**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Iniciar el servidor web**:
   ```bash
   python app.py
   ```
   Accede en tu navegador a: `http://localhost:5001`

5. **Iniciar la herramienta de terminal (CLI)**:
   ```bash
   python main.py
   ```

6. **Ejecutar la suite de pruebas automatizadas**:
   ```bash
   pytest tests/ -v
   ```

---

## 🚀 Despliegue en Producción (Render)

El proyecto incluye configuración nativa para **Render Blueprint** (`render.yaml`), **Procfile** (Gunicorn) y **Dockerfile**.

### Despliegue Unificado con Render Blueprint (Recomendado)

1. Ingresa a tu panel en **[Render.com](https://dashboard.render.com)**.
2. Haz clic en **New +** y selecciona **Blueprint**.
3. Conecta el repositorio `cristborrero/velo`.
4. Render detectará automáticamente `render.yaml` y ejecutará los siguientes pasos:
   - Instalación del paquete de sistema `ffmpeg`.
   - Instalación de dependencias Python.
   - Ejecución del servidor WSGI `gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 app:app`.

---

## 🐳 Despliegue con Docker

Construye y ejecuta el contenedor Docker en cualquier entorno (Railway, Fly.io, GCP Cloud Run, AWS):

```bash
# Construir la imagen Docker
docker build -t velo-app .

# Ejecutar el contenedor
docker run -d -p 5000:5000 --name velo velo-app
```

---

## 💖 Donaciones y Código Abierto

Velo es un proyecto de código abierto libre de publicidad y suscripciones. Incorpora integración con donaciones voluntarias de PayPal para contribuir al mantenimiento de infraestructura.

---

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT** — Libre para aprendizaje, modificación y distribución.
