# Velo — High-Speed Multimedia Extraction 🚀

**Velo** es una plataforma web y herramienta de línea de comandos de alto rendimiento para inspeccionar metadatos y descargar videos/audios en resolución original desde más de 1000 plataformas en la web (YouTube, TikTok, Instagram, Twitter/X, Vimeo, Twitch y más), construida sobre **Python (Flask)**, **yt-dlp**, **FFmpeg** y un sistema visual de alta gama inspirado en el diseño de **Vercel / Linear / Optimus**.

---

## ⚡ Características Principales

- **Inspección Instantánea de Metadatos**: Extrae título, canal/creador, duración y miniatura en tiempo real.
- **Categorización de Formatos**:
  - **Video + Audio**: Formatos listos para reproducir (1080p, 4K, 60fps).
  - **Solo Audio**: Extracción directa de sonido en formatos nativos (MP3, M4A, Opus).
- **Lógica Asíncrona sin Timeout**: Motor con procesamiento en hilos de fondo y actualización de estado en tiempo real via API REST polling.
- **Barra de Progreso Interactiva**: Porcentaje, velocidad de red (`MB/s`), total transferido y tiempo estimado de descarga (ETA).
- **Diseño Optimus (Vercel / Linear Tier)**:
  - Estética OLED `#030303` con retícula técnica ambiental e iluminación interactiva por cursor (`mouse spotlight`).
  - Barra de navegación en isla flotante de cristal (`backdrop-filter: blur(24px)`).
  - Ventana de producto embebida con acabados de macOS e iluminación `border-beam`.
  - Layout en Bento Grid asimétrico para la sección de capacidades.
  - Módulo de donaciones integrado con PayPal (`Hosted Buttons`).
- **Español Neutro**: Copy 100% profesional sin modismos regionales.
- **Suite de Pruebas Automatizadas**: Pruebas de unidad e integración con `pytest` (17/17 pruebas).

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

### Flujo de Descarga Asíncrona

1. **`POST /api/info`**: Recibe la URL del contenido, inspecciona la API de `yt-dlp` y retorna metadatos y categorías de formato.
2. **`POST /api/download/start`**: Arranca un `threading.Thread` en segundo plano en Flask, asigna un `download_id` único y responde de inmediato.
3. **`GET /api/download/status/<id>`**: El cliente realiza polling (cada 500ms) para consultar el porcentaje de avance, velocidad y ETA.
4. **`GET /api/download/file/<id>`**: Transmite el archivo final desde el servidor hacia el navegador del cliente.

---

## 🛠️ Requisitos Previos

- **Python**: 3.8, 3.11 o superior.
- **FFmpeg**: Requerido en el sistema para combinar flujos de video HD y audio separados.

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

4. **Ejecutar el Servidor Web**:
   ```bash
   python app.py
   ```
   Abre en tu navegador: `http://localhost:5000` (o el puerto asignado).

5. **Ejecutar la interfaz de Línea de Comandos (CLI)**:
   ```bash
   python main.py
   ```

6. **Ejecutar Suite de Pruebas**:
   ```bash
   pytest tests/ -v
   ```

---

## 🚀 Guía de Despliegue en Producción

### Opción 1: Despliegue en Render (Recomendado)

Render permite desplegar Velo fácilmente utilizando el archivo `render.yaml` o mediante Docker.

#### Método A: Render Blueprint (con `render.yaml`)
1. Conecta tu cuenta de GitHub con [Render.com](https://render.com).
2. Crea un nuevo **Blueprint Project** y selecciona el repositorio de Velo.
3. Render detectará automáticamente `render.yaml` e instalará `ffmpeg`, Python 3.11, las dependencias y ejecutará Gunicorn mediante:
   ```bash
   gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 app:app
   ```

#### Método B: Render con Docker Container
1. En Render, crea un **Web Service**.
2. Selecciona **Docker** como el entorno de ejecución.
3. Render construirá la imagen automáticamente desde el `Dockerfile` del proyecto (que incluye Python 3.11, FFmpeg y Gunicorn pre-configurados).

---

### Opción 2: Despliegue con Docker (Cualquier Proveedor)

Puedes construir y ejecutar el contenedor Docker localmente o en servicios como Railway, Fly.io, GCP Cloud Run o AWS App Runner:

1. **Construir la imagen**:
   ```bash
   docker build -t velo-app .
   ```

2. **Ejecutar el contenedor**:
   ```bash
   docker run -d -p 5000:5000 --name velo velo-app
   ```
   Accede en: `http://localhost:5000`

---

## 💖 Donaciones & Código Abierto

Velo es un proyecto de código abierto libre de publicidad y suscripciones. Incorpora integración nativa con botones de donación voluntaria de PayPal para el mantenimiento de infraestructura de servidores.

---

## 📄 Licencia

Licencia MIT — Proyecto desarrollado para aprendizaje y uso libre.
