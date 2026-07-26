"""Flask web server for the video downloader."""

from __future__ import annotations

import os
import glob
import shutil
import tempfile
import threading
import uuid
from typing import Any, Dict

from flask import Flask, jsonify, request, send_file, send_from_directory

from downloader.core import VideoDownloader

app = Flask(__name__, static_folder="static", static_url_path="/static")

_dl = VideoDownloader()

# Temp directory for downloads
_DOWNLOAD_DIR = os.path.join(tempfile.gettempdir(), "video_virales_downloads")
os.makedirs(_DOWNLOAD_DIR, exist_ok=True)

# In-memory download state: { download_id: { status, percent, speed, eta, ... } }
_downloads: Dict[str, Dict[str, Any]] = {}

def check_ffmpeg() -> bool:
    if shutil.which("ffmpeg") is not None:
        return True
    # Fallback to common macOS installation paths
    for path in ["/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg"]:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            # Prepend to PATH so subprocesses can find it too
            os.environ["PATH"] = os.path.dirname(path) + os.pathsep + os.environ.get("PATH", "")
            return True
    return False

_HAS_FFMPEG = check_ffmpeg()



@app.route("/")
def index():
    """Serve the main HTML page."""
    return send_from_directory("static", "index.html")


@app.route("/api/info", methods=["POST"])
def get_info():
    """Return video metadata and categorized formats."""
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()

    if not url:
        return jsonify({"error": "No se proporcionó ninguna URL."}), 400

    try:
        info = _dl.get_info(url)
    except Exception as exc:
        print(f"[ERROR] get_info failed for {url}: {exc}")
        return jsonify({"error": str(exc)}), 422

    result = info.to_dict()
    result["has_ffmpeg"] = _HAS_FFMPEG

    print(f"[INFO] {info.title} — {len(info.formats)} formats")
    return jsonify(result)


# Legacy endpoint for backward compatibility
@app.route("/api/formats", methods=["POST"])
def get_formats():
    """Legacy: return flat format list."""
    return get_info()


# --- Async download ---

@app.route("/api/download/start", methods=["POST"])
def download_start():
    """Start an async download. Returns a download_id for polling."""
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    format_id = (data.get("format_id") or "").strip()

    if not url or not format_id:
        return jsonify({"error": "Faltan parámetros (url, format_id)."}), 400

    download_id = uuid.uuid4().hex[:12]

    # Create a dedicated directory for this download
    dl_dir = os.path.join(_DOWNLOAD_DIR, download_id)
    os.makedirs(dl_dir, exist_ok=True)

    _downloads[download_id] = {
        "status": "downloading",
        "percent": 0.0,
        "downloaded_bytes": 0,
        "total_bytes": 0,
        "speed": 0.0,
        "eta": 0.0,
        "filepath": "",
        "error": "",
    }

    def _run() -> None:
        def _on_progress(pct: float, dl_bytes: int, total: int, speed: float, eta: float) -> None:
            _downloads[download_id].update({
                "percent": round(pct, 1),
                "downloaded_bytes": dl_bytes,
                "total_bytes": total,
                "speed": round(speed, 1) if speed else 0.0,
                "eta": round(eta, 1) if eta else 0.0,
            })

        try:
            filepath = _dl.download(
                url=url,
                format_id=format_id,
                output_dir=dl_dir,
                progress_callback=_on_progress,
            )
            # Find actual file (yt-dlp might change the extension)
            files = glob.glob(os.path.join(dl_dir, "*"))
            actual_path = files[0] if files else filepath

            _downloads[download_id].update({
                "status": "done",
                "percent": 100.0,
                "filepath": actual_path,
            })
        except Exception as exc:
            print(f"[ERROR] Download {download_id} failed: {exc}")
            _downloads[download_id].update({
                "status": "error",
                "error": str(exc),
            })

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()

    return jsonify({"download_id": download_id})


@app.route("/api/download/status/<download_id>")
def download_status(download_id: str):
    """Poll download progress."""
    state = _downloads.get(download_id)
    if not state:
        return jsonify({"error": "Descarga no encontrada."}), 404

    return jsonify({
        "status": state["status"],
        "percent": state["percent"],
        "downloaded_bytes": state["downloaded_bytes"],
        "total_bytes": state["total_bytes"],
        "speed": state["speed"],
        "eta": state["eta"],
        "error": state["error"],
    })


@app.route("/api/download/file/<download_id>")
def download_file(download_id: str):
    """Serve the downloaded file."""
    state = _downloads.get(download_id)
    if not state or state["status"] != "done":
        return jsonify({"error": "Archivo no disponible."}), 404

    filepath = state["filepath"]
    if not filepath or not os.path.isfile(filepath):
        return jsonify({"error": "Archivo no encontrado en disco."}), 404

    return send_file(
        filepath,
        as_attachment=True,
        download_name=os.path.basename(filepath),
    )


# Legacy sync endpoint (kept for old tests)
@app.route("/api/download", methods=["POST"])
def download_video_legacy():
    """Legacy sync download."""
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    format_id = (data.get("format_id") or "").strip()

    if not url or not format_id:
        return jsonify({"error": "Faltan parámetros (url, format_id)."}), 400

    dl_dir = os.path.join(_DOWNLOAD_DIR, "legacy")
    os.makedirs(dl_dir, exist_ok=True)
    for old in glob.glob(os.path.join(dl_dir, "*")):
        try:
            os.remove(old)
        except OSError:
            pass

    try:
        _dl.download(url=url, format_id=format_id, output_dir=dl_dir)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 422

    files = glob.glob(os.path.join(dl_dir, "*"))
    if not files:
        return jsonify({"error": "Descarga terminó pero no se encontró el archivo."}), 500

    return send_file(files[0], as_attachment=True, download_name=os.path.basename(files[0]))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
