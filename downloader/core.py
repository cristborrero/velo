"""Core module: VideoDownloader wrapper over yt-dlp."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Union

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


# Extensions that are not real downloadable media
_SKIP_EXTENSIONS = frozenset({"mhtml", "json"})


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
    ) -> None:
        self.title = title
        self.thumbnail = thumbnail
        self.uploader = uploader
        self.duration = duration  # seconds
        self.formats = formats

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
            "groups": {
                "combined": combined,
                "video_only": video_only,
                "audio_only": audio_only,
            },
        }


# ProgressCallback signature: (percent, downloaded_bytes, total_bytes, speed, eta)
ProgressCallback = Callable[[float, int, int, float, float], None]


class VideoDownloader:
    """Wraps yt-dlp to extract format info and download videos."""

    def get_info(self, url: str) -> VideoInfo:
        """Extract video metadata and available formats.

        Returns a VideoInfo object with metadata and categorized formats.

        Raises:
            ValueError: When the URL is invalid or the site is unsupported.
        """
        opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
        }

        try:
            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
        except (DownloadError, Exception) as exc:
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

        return VideoInfo(
            title=title,
            thumbnail=thumbnail,
            uploader=uploader,
            duration=int(duration) if duration else 0,
            formats=formats,
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
    ) -> str:
        """Download a video in the selected format.

        Returns the path to the downloaded file.

        Raises:
            ValueError: On download failure.
        """
        import os
        import shutil

        # Determine if the format needs an audio merge (video-only formats)
        format_spec = format_id
        try:
            info = self.get_info(url)
            selected = [f for f in info.formats if f.format_id == format_id]
            if selected and selected[0].category == "video_only":
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
        except ValueError:
            raise
        except Exception:
            # Fallback to the raw format_id if metadata extraction fails
            pass

        outtmpl = os.path.join(output_dir, "%(title)s.%(ext)s")

        opts: Dict[str, Any] = {
            "format": format_spec,
            "outtmpl": outtmpl,
            "quiet": True,
            "no_warnings": True,
        }

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
        except (DownloadError, Exception) as exc:
            raise ValueError(f"Error al descargar el video: {exc}") from exc

        return filepath
