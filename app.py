"""Flask web server for the video downloader."""

from __future__ import annotations

import os
import glob
import shutil
import tempfile
import threading
import uuid
import time
from typing import Any, Dict

from flask import Flask, jsonify, request, send_file, send_from_directory, make_response

from downloader.core import (
    VideoDownloader,
    cleanup_materialized_cookie_files,
    cleanup_stale_materialized_cookie_files,
    get_runtime_status,
)

app = Flask(__name__, static_folder="static", static_url_path="/static")

_dl = VideoDownloader()

_RUNTIME_MODES = {"local", "render"}
_RUNTIME_MODE = os.environ.get("VELO_RUNTIME_MODE", "local").strip().lower()
if _RUNTIME_MODE not in _RUNTIME_MODES:
    raise RuntimeError("VELO_RUNTIME_MODE must be 'local' or 'render'")
_RENDER_JOB_TTL_SECONDS = max(60, int(os.environ.get("VELO_RENDER_JOB_TTL_SECONDS", "1800")))
_RENDER_MAX_CONCURRENT_JOBS = max(1, int(os.environ.get("VELO_RENDER_MAX_CONCURRENT_JOBS", "2")))
_render_slots = threading.BoundedSemaphore(_RENDER_MAX_CONCURRENT_JOBS)
_downloads_lock = threading.RLock()

# Temp directory for downloads
_DOWNLOAD_DIR = os.path.join(tempfile.gettempdir(), "video_virales_downloads")
os.makedirs(_DOWNLOAD_DIR, exist_ok=True)

# In-memory download state: { download_id: { status, percent, speed, eta, ... } }
_downloads: Dict[str, Dict[str, Any]] = {}


def get_runtime_mode(value: str | None = None) -> str:
    """Return the validated runtime mode used by the process."""
    mode = (value if value is not None else os.environ.get("VELO_RUNTIME_MODE", "local")).strip().lower()
    if mode not in _RUNTIME_MODES:
        raise ValueError("VELO_RUNTIME_MODE must be 'local' or 'render'")
    return mode


def _cleanup_job(download_id: str, dl_dir: str) -> None:
    """Delete all Render job state and files, including partial downloads."""
    with _downloads_lock:
        _downloads.pop(download_id, None)
    shutil.rmtree(dl_dir, ignore_errors=True)
    cleanup_materialized_cookie_files()


def _cleanup_stale_render_jobs() -> None:
    if _RUNTIME_MODE != "render":
        return
    cutoff = time.time() - _RENDER_JOB_TTL_SECONDS
    for entry in os.scandir(_DOWNLOAD_DIR):
        if entry.is_dir() and entry.stat().st_mtime < cutoff:
            shutil.rmtree(entry.path, ignore_errors=True)
    cleanup_stale_materialized_cookie_files()
    cleanup_materialized_cookie_files()


_cleanup_stale_render_jobs()


def _resolve_download_file(filepath: str, dl_dir: str) -> str:
    """Resolve yt-dlp output without guessing between arbitrary files."""
    root = os.path.realpath(dl_dir)
    if filepath:
        candidate = os.path.realpath(filepath)
        if candidate.startswith(root + os.sep) and os.path.isfile(candidate):
            return candidate
    files = sorted(
        os.path.realpath(path)
        for path in glob.glob(os.path.join(dl_dir, "*"))
        if os.path.isfile(path) and not path.endswith((".part", ".ytdl"))
    )
    if len(files) == 1:
        return files[0]
    raise ValueError("Download completed but its output file could not be identified safely.")


def _send_file_with_render_cleanup(path: str, download_name: str, job_dir: str):
    response = send_file(path, as_attachment=True, download_name=download_name)
    if _RUNTIME_MODE == "render":
        response.call_on_close(lambda: shutil.rmtree(job_dir, ignore_errors=True))
        response.call_on_close(cleanup_materialized_cookie_files)
    return response


def _expire_job_if_needed(download_id: str, state: Dict[str, Any]) -> bool:
    """Expire Render jobs before serving stale status or file requests."""
    created_at = state.get("created_at", time.time())
    if _RUNTIME_MODE != "render" or time.time() - created_at <= _RENDER_JOB_TTL_SECONDS:
        return False
    _cleanup_job(download_id, state.get("job_dir", ""))
    return True

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
_RUNTIME_STATUS = get_runtime_status()
print(
    "[INFO] Runtime diagnostics: "
    f"node={'yes' if _RUNTIME_STATUS['node'] else 'no'} "
    f"ffmpeg={'yes' if _RUNTIME_STATUS['ffmpeg'] else 'no'} "
    f"youtube_cookies={'yes' if _RUNTIME_STATUS['youtube_cookies'] else 'no'}"
)


@app.after_request
def add_security_headers(response):
    """Inject HTTP defense-in-depth security headers."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
    if request.path.startswith('/api/') or request.path == '/api' or request.path.startswith('/api/download/file/'):
        response.headers['Cache-Control'] = 'no-store, max-age=0'
        response.headers['Pragma'] = 'no-cache'
    return response


@app.route("/")
def index():
    """Serve the main HTML page."""
    return send_from_directory("static", "index.html")


@app.route("/robots.txt")
def robots():
    """Serve robots.txt for search engines."""
    content = "User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n"
    return content, 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/api/health")
def health():
    """Expose safe production dependency diagnostics; never return secret values."""
    status = get_runtime_status()
    return jsonify({
        "status": "ok" if status["node"] and status["ffmpeg"] else "degraded",
        "runtime": {
            "node": status["node"],
            "ffmpeg": status["ffmpeg"],
        },
        "youtube": {
            "cookies_configured": status["youtube_cookies"],
        },
    })


@app.route("/sitemap.xml")
def sitemap():
    """Serve dynamic sitemap.xml for SEO indexing."""
    content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        '  <url>\n'
        '    <loc>/</loc>\n'
        '    <changefreq>daily</changefreq>\n'
        '    <priority>1.0</priority>\n'
        '  </url>\n'
        '</urlset>'
    )
    return content, 200, {"Content-Type": "application/xml; charset=utf-8"}


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
    finally:
        if _RUNTIME_MODE == "render":
            cleanup_materialized_cookie_files()

    result = info.to_dict()
    result["has_ffmpeg"] = _HAS_FFMPEG

    groups = result.get("groups", {})
    c = len(groups.get("combined", []))
    v = len(groups.get("video_only", []))
    a = len(groups.get("audio_only", []))
    print(f"[INFO] {info.title} — {len(info.formats)} formats (combined={c}, video_only={v}, audio_only={a})")
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
    format_category = (data.get("format_category") or "").strip() or None

    start_seconds = data.get("start_seconds")
    end_seconds = data.get("end_seconds")

    if start_seconds is not None:
        try: start_seconds = float(start_seconds)
        except (ValueError, TypeError): start_seconds = None

    if end_seconds is not None:
        try: end_seconds = float(end_seconds)
        except (ValueError, TypeError): end_seconds = None

    if not url or not format_id:
        return jsonify({"error": "Faltan parámetros (url, format_id)."}), 400

    download_id = uuid.uuid4().hex[:12]

    if _RUNTIME_MODE == "render" and not _render_slots.acquire(blocking=False):
        return jsonify({"error": "The service is busy. Try again shortly."}), 429

    # Every job gets an isolated directory; Render deletes it after the request lifecycle.
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
        "created_at": time.time(),
        "job_dir": dl_dir,
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
                start_seconds=start_seconds,
                end_seconds=end_seconds,
                format_category=format_category,
            )
            actual_path = _resolve_download_file(filepath, dl_dir)

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
            if _RUNTIME_MODE == "render":
                _cleanup_job(download_id, dl_dir)
        finally:
            if _RUNTIME_MODE == "render":
                _render_slots.release()

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()

    return jsonify({"download_id": download_id})


@app.route("/api/download/status/<download_id>")
def download_status(download_id: str):
    """Poll download progress."""
    state = _downloads.get(download_id)
    if not state or _expire_job_if_needed(download_id, state):
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
    if not state or _expire_job_if_needed(download_id, state) or state["status"] != "done":
        return jsonify({"error": "Archivo no disponible."}), 404

    filepath = state["filepath"]
    if not filepath or not os.path.isfile(filepath):
        return jsonify({"error": "Archivo no encontrado en disco."}), 404

    response = send_file(
        filepath,
        as_attachment=True,
        download_name=os.path.basename(filepath),
    )
    if _RUNTIME_MODE == "render":
        response.call_on_close(lambda: _cleanup_job(download_id, os.path.dirname(filepath)))
    return response


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

    try:
        path = _resolve_download_file("", dl_dir)
    except ValueError as exc:
        if _RUNTIME_MODE == "render":
            _cleanup_job("legacy", dl_dir)
        return jsonify({"error": str(exc)}), 500
    return _send_file_with_render_cleanup(path, os.path.basename(path), dl_dir)


@app.route("/sw.js")
def serve_sw():
    """Serve Service Worker file for PWA support with correct root scope header."""
    res = make_response(send_from_directory("static", "sw.js"))
    res.headers["Content-Type"] = "application/javascript"
    res.headers["Service-Worker-Allowed"] = "/"
    return res


@app.route("/api/subtitles/download", methods=["POST"])
def download_subtitles_endpoint():
    """Endpoint to download subtitle files (.srt, .vtt, .txt)."""
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    lang = (data.get("lang") or "es").strip()
    fmt = (data.get("fmt") or "srt").strip()

    if not url:
        return jsonify({"error": "Falta la URL del video."}), 400

    sub_dir = os.path.join(_DOWNLOAD_DIR, "subtitles_" + uuid.uuid4().hex[:8])
    os.makedirs(sub_dir, exist_ok=True)

    try:
        sub_path = _dl.download_subtitles(url, lang=lang, fmt=fmt, output_dir=sub_dir)
        return _send_file_with_render_cleanup(sub_path, os.path.basename(sub_path), sub_dir)
    except Exception as exc:
        if _RUNTIME_MODE == "render":
            shutil.rmtree(sub_dir, ignore_errors=True)
            cleanup_materialized_cookie_files()
        return jsonify({"error": str(exc)}), 500


@app.route("/api/convert/gif", methods=["POST"])
def convert_gif_endpoint():
    """Endpoint to export a video section to animated GIF."""
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    start_seconds = float(data.get("start_seconds") or 0.0)
    end_seconds = float(data.get("end_seconds") or 5.0)

    if not url:
        return jsonify({"error": "Falta la URL del video."}), 400

    gif_dir = os.path.join(_DOWNLOAD_DIR, "gif_" + uuid.uuid4().hex[:8])
    os.makedirs(gif_dir, exist_ok=True)

    try:
        gif_path = _dl.export_gif(url, start_seconds=start_seconds, end_seconds=end_seconds, output_dir=gif_dir)
        return _send_file_with_render_cleanup(gif_path, os.path.basename(gif_path), gif_dir)
    except Exception as exc:
        if _RUNTIME_MODE == "render":
            shutil.rmtree(gif_dir, ignore_errors=True)
            cleanup_materialized_cookie_files()
        return jsonify({"error": str(exc)}), 500


@app.route("/api/batch/start", methods=["POST"])
def batch_start_endpoint():
    """Start an async batch/playlist download for multiple URLs into a zip archive."""
    data = request.get_json(silent=True) or {}
    urls = data.get("urls") or []
    format_id = (data.get("format_id") or "best").strip()

    if isinstance(urls, str):
        urls = [u.strip() for u in urls.splitlines() if u.strip()]

    if not urls:
        return jsonify({"error": "No se proporcionaron URLs para descargar."}), 400

    if _RUNTIME_MODE == "render" and not _render_slots.acquire(blocking=False):
        return jsonify({"error": "The service is busy. Try again shortly."}), 429

    download_id = "batch_" + uuid.uuid4().hex[:12]
    dl_dir = os.path.join(_DOWNLOAD_DIR, download_id)
    os.makedirs(dl_dir, exist_ok=True)

    _downloads[download_id] = {
        "status": "downloading",
        "percent": 0.0,
        "downloaded_bytes": 0,
        "total_bytes": len(urls),
        "speed": 0.0,
        "eta": 0.0,
        "filepath": "",
        "error": "",
        "created_at": time.time(),
        "job_dir": dl_dir,
    }

    def _run() -> None:
        def _on_progress(pct: float, current: int, total: int, speed: float, eta: float) -> None:
            _downloads[download_id].update({
                "percent": round(pct, 1),
                "downloaded_bytes": current,
                "total_bytes": total,
            })

        try:
            zip_path = _dl.download_batch(urls=urls, format_id=format_id, output_dir=dl_dir, progress_callback=_on_progress)
            _downloads[download_id].update({
                "status": "done",
                "percent": 100.0,
                "filepath": zip_path,
            })
        except Exception as exc:
            _downloads[download_id].update({
                "status": "error",
                "error": str(exc),
            })
            if _RUNTIME_MODE == "render":
                _cleanup_job(download_id, dl_dir)
        finally:
            if _RUNTIME_MODE == "render":
                _render_slots.release()

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()

    return jsonify({"download_id": download_id})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"Iniciando servidor Velo en http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
