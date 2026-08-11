"""Core module: VideoDownloader wrapper over yt-dlp."""

from __future__ import annotations

import os
import glob
import shutil
import tempfile
import threading
from typing import Any, Callable, Dict, List, Optional, Union

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, download_range_func


# Extensions that are not real downloadable media
_SKIP_EXTENSIONS = frozenset({"mhtml", "json"})

# Substrings identifying a dropped/reset connection rather than a real bot block
_TRANSIENT_NETWORK_MARKERS = (
    "broken pipe",
    "errno 32",
    "errno 54",
    "errno 104",
    "connection reset",
    "connection aborted",
    "remote end closed connection",
    "timed out",
)

_JS_RUNTIME_MARKERS = (
    "no supported javascript runtime",
    "javascript runtime is not available",
    "javascript runtime was not found",
    "could not find node",
    "node was not found",
)

_MATERIALIZED_COOKIE_FILES = set()
_COOKIE_FILES_LOCK = threading.Lock()


def _is_transient_network_error(err_str: str) -> bool:
    err_lower = err_str.lower()
    return any(marker in err_lower for marker in _TRANSIENT_NETWORK_MARKERS)


def _is_js_runtime_error(err_str: str) -> bool:
    """Return whether yt-dlp explicitly reported a missing JS runtime."""
    err_lower = err_str.lower()
    return any(marker in err_lower for marker in _JS_RUNTIME_MARKERS)


def _cookie_file_candidates() -> List[str]:
    return [
        os.environ.get("YOUTUBE_COOKIES"),
        os.environ.get("COOKIES_FILE"),
        "cookies.txt",
        os.path.join(os.path.dirname(__file__), "..", "cookies.txt"),
        os.path.join(os.path.dirname(__file__), "..", "assets", "cookies.txt"),
        os.path.join(tempfile.gettempdir(), "youtube_cookies.txt"),
    ]


def _has_youtube_cookies() -> bool:
    """Check cookie presence without reading or exposing cookie contents."""
    if os.environ.get("YOUTUBE_COOKIES_TEXT", "").strip():
        return True
    return any(path and os.path.isfile(path) for path in _cookie_file_candidates())


def _has_node_runtime() -> bool:
    return shutil.which("node") is not None


def get_runtime_status() -> Dict[str, bool]:
    """Return safe deployment diagnostics without exposing secret values or paths."""
    return {
        "node": _has_node_runtime(),
        "ffmpeg": shutil.which("ffmpeg") is not None,
        "youtube_cookies": _has_youtube_cookies(),
    }


def cleanup_materialized_cookie_files() -> None:
    """Remove cookie files materialized from environment secrets."""
    with _COOKIE_FILES_LOCK:
        paths = list(_MATERIALIZED_COOKIE_FILES)
        _MATERIALIZED_COOKIE_FILES.clear()
    for path in paths:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
        except OSError:
            continue


def cleanup_stale_materialized_cookie_files() -> None:
    """Remove secret-derived cookie files left by an earlier process."""
    pattern = os.path.join(tempfile.gettempdir(), "velo-youtube-cookies-*.txt")
    for path in glob.glob(pattern):
        try:
            os.remove(path)
        except OSError:
            continue


def _youtube_runtime_error(err_str: str = "") -> str:
    """Build an actionable, secret-safe YouTube dependency error."""
    if not _has_node_runtime() or _is_js_runtime_error(err_str):
        return (
            "El servidor no tiene un runtime Node.js compatible para resolver los "
            "desafíos JavaScript de YouTube. Reconstruye la imagen de producción "
            "con Node.js 22 o superior."
        )
    if not _has_youtube_cookies():
        return (
            "YouTube requiere autenticación anti-bot y no hay cookies configuradas. "
            "Configura el secreto YOUTUBE_COOKIES_TEXT en Render; no se puede usar "
            "un archivo de cookies ignorado por git en producción."
        )
    return (
        "YouTube rechazó la autenticación configurada. Genera cookies.txt válidas "
        "y actualiza el secreto YOUTUBE_COOKIES_TEXT en Render."
    )


class VideoFormat:
    """Represents a single available video/audio format."""

    def __init__(
        self,
        format_id: str,
        resolution: str,
        ext: str,
        filesize: Union[float, str],
        has_video: bool = True,
        has_audio: bool = True,
        fps: Optional[int] = None,
        vcodec: str = "",
        acodec: str = "",
    ) -> None:
        self.format_id = format_id
        self.resolution = resolution
        self.ext = ext
        self.filesize = filesize
        self.has_video = has_video
        self.has_audio = has_audio
        self.fps = fps
        self.vcodec = vcodec
        self.acodec = acodec

    @property
    def category(self) -> str:
        """Classify: 'combined', 'video_only', or 'audio_only'."""
        if self.has_video and self.has_audio:
            return "combined"
        if self.has_video:
            return "video_only"
        return "audio_only"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict for JSON responses."""
        return {
            "format_id": self.format_id,
            "resolution": self.resolution,
            "ext": self.ext,
            "filesize": self.filesize,
            "has_video": self.has_video,
            "has_audio": self.has_audio,
            "fps": self.fps,
            "category": self.category,
        }

    def __repr__(self) -> str:
        size = (
            f"{self.filesize:.1f} MB"
            if isinstance(self.filesize, (int, float))
            else self.filesize
        )
        return f"{self.format_id:>6} | {self.resolution:<10} | {self.ext:<6} | {size}"


class VideoInfo:
    """Metadata about a video."""

    def __init__(
        self,
        title: str,
        thumbnail: str,
        uploader: str,
        duration: int,
        formats: List[VideoFormat],
        subtitles: Optional[List[Dict[str, str]]] = None,
    ) -> None:
        self.title = title
        self.thumbnail = thumbnail
        self.uploader = uploader
        self.duration = duration  # seconds
        self.formats = formats
        self.subtitles = subtitles or []

    @property
    def duration_formatted(self) -> str:
        """Format seconds into HH:MM:SS or MM:SS."""
        h, remainder = divmod(self.duration, 3600)
        m, s = divmod(remainder, 60)
        if h > 0:
            return f"{h}:{m:02d}:{s:02d}"
        return f"{m}:{s:02d}"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict for JSON responses."""
        combined = [f.to_dict() for f in self.formats if f.category == "combined"]
        video_only = [f.to_dict() for f in self.formats if f.category == "video_only"]
        audio_only = [f.to_dict() for f in self.formats if f.category == "audio_only"]

        return {
            "title": self.title,
            "thumbnail": self.thumbnail,
            "uploader": self.uploader,
            "duration": self.duration,
            "duration_formatted": self.duration_formatted,
            "subtitles": self.subtitles,
            "groups": {
                "combined": combined,
                "video_only": video_only,
                "audio_only": audio_only,
            },
        }


# ProgressCallback signature: (percent, downloaded_bytes, total_bytes, speed, eta)
ProgressCallback = Callable[[float, int, int, float, float], None]


def _get_default_ydl_opts() -> Dict[str, Any]:
    """Get default yt-dlp options with cookies auto-detection and player_client optimization."""
    opts: Dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "socket_timeout": 30,
        "retries": 10,
        "fragment_retries": 10,
        "extractor_retries": 3,
        # yt-dlp only enables "deno" by default; use node since that's what's installed here
        "js_runtimes": {"node": {}},
    }

    # 1. Check YOUTUBE_COOKIES_TEXT env var (raw Netscape cookie string for cloud deployment)
    cookies_text = os.environ.get("YOUTUBE_COOKIES_TEXT")
    if cookies_text:
        try:
            tmp_cookie_file = os.path.join(
                tempfile.gettempdir(), f"velo-youtube-cookies-{os.getpid()}-{id(opts)}.txt"
            )
            with open(tmp_cookie_file, "w", encoding="utf-8") as f:
                f.write(cookies_text.strip() + "\n")
            opts["cookiefile"] = tmp_cookie_file
            with _COOKIE_FILES_LOCK:
                _MATERIALIZED_COOKIE_FILES.add(tmp_cookie_file)
        except Exception:
            pass

    # 2. Check physical cookie file candidates if no cookiefile set yet
    if "cookiefile" not in opts:
        for cpath in _cookie_file_candidates():
            if cpath and os.path.isfile(cpath):
                opts["cookiefile"] = os.path.abspath(cpath)
                break

    return opts


class VideoDownloader:
    """Wraps yt-dlp to extract format info and download videos."""

    def get_info(self, url: str) -> VideoInfo:
        """Extract video metadata and available formats.

        Returns a VideoInfo object with metadata and categorized formats.

        Raises:
            ValueError: When the URL is invalid or the site is unsupported.
        """
        opts = _get_default_ydl_opts()
        opts["skip_download"] = True

        info = None
        try:
            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
        except (DownloadError, Exception) as exc:
            err_str = str(exc)

            if _is_transient_network_error(err_str):
                # Connection was dropped mid-request; retry once with a fresh connection
                # before falling through to the anti-bot recovery chain.
                try:
                    with YoutubeDL(opts) as ydl_retry:
                        info = ydl_retry.extract_info(url, download=False)
                except Exception as retry_exc:
                    exc, err_str = retry_exc, str(retry_exc)

            needs_recovery = (
                info is None
                and (
                    "Sign in to confirm you're not a bot" in err_str
                    or "bot" in err_str.lower()
                    or "confirm" in err_str.lower()
                    or _is_transient_network_error(err_str)
                )
            )

            if info is None and (_is_js_runtime_error(err_str) or (needs_recovery and not _has_node_runtime())):
                raise ValueError(_youtube_runtime_error(err_str)) from exc

            if needs_recovery:
                # Attempt 1: Browser cookie auto-extraction fallback (Chrome, Safari, Brave, Firefox, Edge)
                for browser_name in ("chrome", "safari", "brave", "firefox", "edge"):
                    try:
                        b_opts = dict(opts)
                        b_opts["cookiesfrombrowser"] = (browser_name,)
                        with YoutubeDL(b_opts) as ydl_b:
                            info = ydl_b.extract_info(url, download=False)
                            if info:
                                break
                    except Exception:
                        continue

                if info is None:
                    # Attempt 2: Multi-tier modern player_clients fallback matrix
                    client_matrix = [
                        ["android", "ios"],
                        ["ios", "mweb"],
                        ["web_creator", "mweb"],
                        ["android"],
                    ]
                    for clients in client_matrix:
                        try:
                            fb_opts = dict(opts)
                            fb_opts["extractor_args"] = {"youtube": {"player_client": clients}}
                            with YoutubeDL(fb_opts) as ydl_fb:
                                info = ydl_fb.extract_info(url, download=False)
                                if info:
                                    break
                        except Exception:
                            continue

                if info is None:
                    if _is_transient_network_error(err_str):
                        raise ValueError(
                            f"La conexión con YouTube se cortó repetidamente: {err_str}"
                        ) from exc
                    raise ValueError(_youtube_runtime_error(err_str)) from exc
            else:
                raise ValueError(
                    f"No se pudo extraer información del video: {exc}"
                ) from exc

        if info is None:
            raise ValueError("No se pudo extraer información del video.")

        # Extract metadata
        title = info.get("title") or "Sin título"
        thumbnail = info.get("thumbnail") or ""
        uploader = info.get("uploader") or info.get("channel") or "Desconocido"
        duration = info.get("duration") or 0

        # Parse formats
        raw_formats = info.get("formats") or []
        formats: List[VideoFormat] = []

        for fmt in raw_formats:
            ext = str(fmt.get("ext", "?"))

            if ext in _SKIP_EXTENSIONS:
                continue
            if fmt.get("protocol") in ("mhtml",) and not fmt.get("url"):
                continue

            raw_size = fmt.get("filesize") or fmt.get("filesize_approx")
            if raw_size is not None:
                size: Union[float, str] = round(raw_size / (1024 * 1024), 1)
            else:
                size = "Desconocido"

            resolution = fmt.get("resolution") or "audio only"
            vcodec = fmt.get("vcodec") or "none"
            acodec = fmt.get("acodec") or "none"

            has_video = vcodec != "none"
            has_audio = acodec != "none"

            # If both are "none", skip — not a real format
            if not has_video and not has_audio:
                continue

            formats.append(
                VideoFormat(
                    format_id=str(fmt.get("format_id", "?")),
                    resolution=resolution,
                    ext=ext,
                    filesize=size,
                    has_video=has_video,
                    has_audio=has_audio,
                    fps=fmt.get("fps"),
                    vcodec=vcodec if has_video else "",
                    acodec=acodec if has_audio else "",
                )
            )

        # Parse subtitles / captions
        subtitles_dict = info.get("subtitles") or {}
        auto_captions = info.get("automatic_captions") or {}
        sub_langs: List[Dict[str, str]] = []
        seen_codes = set()

        for code, sub_list in subtitles_dict.items():
            if code not in seen_codes:
                name = sub_list[0].get("name") if sub_list and isinstance(sub_list, list) else code
                sub_langs.append({"code": code, "name": name or code, "type": "manual"})
                seen_codes.add(code)

        for code, sub_list in auto_captions.items():
            if code not in seen_codes:
                name = sub_list[0].get("name") if sub_list and isinstance(sub_list, list) else code
                sub_langs.append({"code": code, "name": f"{name or code} (auto)", "type": "auto"})
                seen_codes.add(code)

        return VideoInfo(
            title=title,
            thumbnail=thumbnail,
            uploader=uploader,
            duration=int(duration) if duration else 0,
            formats=formats,
            subtitles=sub_langs,
        )

    # Keep backward compatibility
    def get_formats(self, url: str) -> List[VideoFormat]:
        """Legacy method — returns flat format list."""
        return self.get_info(url).formats

    def download(
        self,
        url: str,
        format_id: str,
        output_dir: str = ".",
        progress_callback: Optional[ProgressCallback] = None,
        start_seconds: Optional[float] = None,
        end_seconds: Optional[float] = None,
        format_category: Optional[str] = None,
    ) -> str:
        """Download a video in the selected format with optional time range clipping.

        Returns the path to the downloaded file.

        Raises:
            ValueError: On download failure.
        """
        import os
        import shutil

        # Special Master Audio HD Formats
        format_spec = format_id
        is_audio_postproc = False
        audio_codec = ""
        audio_quality = ""

        if format_id == "mp3_320k":
            format_spec = "bestaudio/best"
            is_audio_postproc = True
            audio_codec = "mp3"
            audio_quality = "320"
        elif format_id == "wav":
            format_spec = "bestaudio/best"
            is_audio_postproc = True
            audio_codec = "wav"
            audio_quality = "0"
        else:
            # Determine if the format needs an audio merge (video-only formats).
            # A caller that already knows the category (e.g. the web UI, which
            # fetched /api/info earlier) can pass it directly to skip this
            # extra metadata round-trip — each yt-dlp call is another chance
            # to hit YouTube's bot-detection challenge.
            needs_merge = format_category == "video_only"
            if format_category is None:
                try:
                    info = self.get_info(url)
                    selected = [f for f in info.formats if f.format_id == format_id]
                    needs_merge = bool(selected and selected[0].category == "video_only")
                except ValueError:
                    raise
                except Exception:
                    # Fallback to the raw format_id if metadata extraction fails
                    needs_merge = False

            if needs_merge:
                has_ffmpeg = shutil.which("ffmpeg") is not None
                if not has_ffmpeg:
                    for p in ["/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg"]:
                        if os.path.isfile(p) and os.access(p, os.X_OK):
                            os.environ["PATH"] = os.path.dirname(p) + os.pathsep + os.environ.get("PATH", "")
                            has_ffmpeg = True
                            break
                if not has_ffmpeg:
                    raise ValueError(
                        "Esta calidad de video requiere 'ffmpeg' instalado en el servidor para poder combinarla con audio."
                    )
                format_spec = f"{format_id}+bestaudio/best"
                pass

        outtmpl = os.path.join(output_dir, "%(title)s.%(ext)s")

        opts: Dict[str, Any] = _get_default_ydl_opts()
        opts["format"] = format_spec
        opts["outtmpl"] = outtmpl

        if is_audio_postproc:
            opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_codec,
                "preferredquality": audio_quality,
            }]

        # Configure time range clipping if specified.
        # Deliberately NOT setting force_keyframes_at_cuts: that flag forces a
        # full ffmpeg re-encode for frame-exact cuts, which is slow even on
        # a real machine and effectively unusable on Render's shared free-tier
        # CPU. Without it, yt-dlp stream-copies the range (cut aligned to the
        # nearest keyframe, off by at most a couple seconds) — fast and light.
        if start_seconds is not None or end_seconds is not None:
            start_val = float(start_seconds) if start_seconds is not None else 0.0
            end_val = float(end_seconds) if end_seconds is not None else float("inf")
            try:
                opts["download_ranges"] = download_range_func([], [[start_val, end_val]])
            except Exception:
                pass

        if progress_callback:
            def _hook(d: Dict[str, Any]) -> None:
                if d.get("status") == "downloading":
                    total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                    downloaded = d.get("downloaded_bytes") or 0
                    speed = d.get("speed") or 0.0
                    eta = d.get("eta") or 0.0
                    pct = (downloaded / total * 100) if total > 0 else 0.0
                    progress_callback(pct, downloaded, total, speed, eta)
                elif d.get("status") == "finished":
                    progress_callback(100.0, 0, 0, 0.0, 0.0)

            opts["progress_hooks"] = [_hook]

        filepath = ""

        try:
            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if info:
                    filepath = ydl.prepare_filename(info)
                    if is_audio_postproc and audio_codec:
                        # Fix extension if ffmpeg audio extraction changed it
                        base = os.path.splitext(filepath)[0]
                        converted_path = f"{base}.{audio_codec}"
                        if os.path.exists(converted_path):
                            filepath = converted_path
        except (DownloadError, Exception) as exc:
            err_str = str(exc)
            is_youtube_challenge = "bot" in err_str.lower() or "confirm" in err_str.lower() or "sign in" in err_str.lower()
            if _is_js_runtime_error(err_str) or (is_youtube_challenge and not _has_node_runtime()):
                raise ValueError(_youtube_runtime_error(err_str)) from exc
            if is_youtube_challenge:
                client_matrix = [
                    ["android", "ios"],
                    ["ios", "mweb"],
                    ["web_creator", "mweb"],
                ]
                downloaded_ok = False
                for clients in client_matrix:
                    try:
                        fb_opts = dict(opts)
                        fb_opts["extractor_args"] = {"youtube": {"player_client": clients}}
                        with YoutubeDL(fb_opts) as ydl_fb:
                            info = ydl_fb.extract_info(url, download=True)
                            if info:
                                filepath = ydl_fb.prepare_filename(info)
                                if is_audio_postproc and audio_codec:
                                    base = os.path.splitext(filepath)[0]
                                    converted_path = f"{base}.{audio_codec}"
                                    if os.path.exists(converted_path):
                                        filepath = converted_path
                                downloaded_ok = True
                                break
                    except Exception:
                        continue

                if not downloaded_ok:
                    raise ValueError(_youtube_runtime_error(err_str)) from exc
            else:
                raise ValueError(f"Error al descargar el video: {exc}") from exc

        return filepath

    def download_subtitles(
        self,
        url: str,
        lang: str = "es",
        fmt: str = "srt",
        output_dir: str = "/tmp",
    ) -> str:
        """Download subtitle transcript in .srt, .vtt, or .txt format."""
        import os
        import glob

        opts = _get_default_ydl_opts()
        opts["skip_download"] = True
        opts["writesubtitles"] = True
        opts["writeautomaticsub"] = True
        opts["subtitleslangs"] = [lang, "es", "en"]
        opts["subtitlesformat"] = "vtt/srt/best"
        opts["outtmpl"] = os.path.join(output_dir, "%(title)s.%(ext)s")

        try:
            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get("title") or "subtitles"
        except Exception as exc:
            raise ValueError(f"No se pudieron extraer subtítulos: {exc}") from exc

        # Find extracted subtitle file
        sub_files = glob.glob(os.path.join(output_dir, f"{title}*.vtt")) + glob.glob(os.path.join(output_dir, f"{title}*.srt"))
        if not sub_files:
            sub_files = glob.glob(os.path.join(output_dir, "*.vtt")) + glob.glob(os.path.join(output_dir, "*.srt"))

        if not sub_files:
            raise ValueError(f"No se encontraron subtítulos disponibles en el idioma seleccionado.")

        sub_path = sub_files[0]

        # Convert to plain text transcript if requested
        if fmt == "txt":
            txt_path = sub_path.rsplit(".", 1)[0] + ".txt"
            with open(sub_path, "r", encoding="utf-8", errors="ignore") as f_in:
                lines = f_in.readlines()
            clean_lines = []
            for line in lines:
                l = line.strip()
                if not l or l.startswith("WEBVTT") or "-->" in l or l.isdigit():
                    continue
                if l not in clean_lines:
                    clean_lines.append(l)
            with open(txt_path, "w", encoding="utf-8") as f_out:
                f_out.write("\n".join(clean_lines))
            return txt_path

        return sub_path

    def export_gif(
        self,
        url: str,
        start_seconds: float = 0.0,
        end_seconds: float = 5.0,
        output_dir: str = "/tmp",
    ) -> str:
        """Export video section to high quality animated GIF using FFmpeg palettegen."""
        import os
        import subprocess

        video_path = self.download(url, "best", output_dir=output_dir, start_seconds=start_seconds, end_seconds=end_seconds)
        if not os.path.exists(video_path):
            raise ValueError("No se pudo obtener el clip de video para convertir a GIF.")

        gif_path = video_path.rsplit(".", 1)[0] + ".gif"
        palette_path = video_path.rsplit(".", 1)[0] + "_palette.png"

        try:
            cmd1 = [
                "ffmpeg", "-y", "-i", video_path,
                "-vf", "fps=15,scale=480:-1:flags=lanczos,palettegen",
                palette_path
            ]
            subprocess.run(cmd1, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            cmd2 = [
                "ffmpeg", "-y", "-i", video_path, "-i", palette_path,
                "-filter_complex", "fps=15,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse",
                gif_path
            ]
            subprocess.run(cmd2, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            if os.path.exists(palette_path):
                os.remove(palette_path)
            if os.path.exists(video_path):
                os.remove(video_path)

            return gif_path
        except Exception:
            try:
                cmd_fb = ["ffmpeg", "-y", "-i", video_path, "-vf", "fps=12,scale=360:-1", gif_path]
                subprocess.run(cmd_fb, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if os.path.exists(video_path):
                    os.remove(video_path)
                return gif_path
            except Exception as exc:
                raise ValueError(f"Error al generar el GIF animado: {exc}") from exc

    def download_batch(
        self,
        urls: List[str],
        format_id: str = "best",
        output_dir: str = "/tmp",
        progress_callback: Optional[ProgressCallback] = None,
    ) -> str:
        """Download multiple URLs / Playlists and compress output files into a single .zip archive."""
        import os
        import zipfile
        import time

        batch_id = f"velo_batch_{int(time.time())}"
        batch_dir = os.path.join(output_dir, batch_id)
        os.makedirs(batch_dir, exist_ok=True)

        downloaded_files: List[str] = []
        total_urls = len(urls)

        for i, url in enumerate(urls, start=1):
            u = url.strip()
            if not u:
                continue
            try:
                fp = self.download(u, format_id, output_dir=batch_dir)
                if os.path.exists(fp):
                    downloaded_files.append(fp)
            except Exception:
                pass
            if progress_callback:
                progress_callback(float(i / total_urls * 100), i, total_urls, 0.0, 0.0)

        if not downloaded_files:
            raise ValueError("No se pudo descargar ningún video de la lista proporcionada.")

        zip_path = os.path.join(output_dir, f"{batch_id}.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in downloaded_files:
                zipf.write(file, os.path.basename(file))

        return zip_path
