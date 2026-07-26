"""Tests for downloader.core — VideoDownloader."""

from unittest.mock import patch, MagicMock

import pytest

from downloader.core import VideoDownloader, VideoFormat, VideoInfo


# --- Fixtures ---

FAKE_INFO_DICT = {
    "title": "Test Video",
    "thumbnail": "https://example.com/thumb.jpg",
    "uploader": "TestUser",
    "duration": 185,
    "formats": [
        {
            "format_id": "18",
            "resolution": "360p",
            "ext": "mp4",
            "filesize": 15_000_000,
            "vcodec": "avc1",
            "acodec": "mp4a",
            "fps": 30,
        },
        {
            "format_id": "22",
            "resolution": "720p",
            "ext": "mp4",
            "filesize": 50_000_000,
            "vcodec": "avc1",
            "acodec": "mp4a",
            "fps": 30,
        },
        {
            "format_id": "137",
            "resolution": "1080p",
            "ext": "mp4",
            "filesize": 80_000_000,
            "vcodec": "avc1",
            "acodec": "none",
            "fps": 30,
        },
        {
            "format_id": "251",
            "resolution": "audio only",
            "ext": "webm",
            "filesize": None,
            "vcodec": "none",
            "acodec": "opus",
        },
        {
            "format_id": "sb0",
            "resolution": "320x180",
            "ext": "mhtml",
            "filesize": None,
            "vcodec": "none",
            "acodec": "none",
        },
    ],
}


# === Metadata extraction ===

class TestGetInfo:
    """Tests for get_info (metadata + categorized formats)."""

    @patch("downloader.core.YoutubeDL")
    def test_returns_video_info_with_metadata(self, mock_ydl_cls: MagicMock) -> None:
        """get_info returns a VideoInfo with title, thumbnail, uploader, duration."""
        instance = mock_ydl_cls.return_value.__enter__.return_value
        instance.extract_info.return_value = FAKE_INFO_DICT

        dl = VideoDownloader()
        info = dl.get_info("https://example.com/video")

        assert isinstance(info, VideoInfo)
        assert info.title == "Test Video"
        assert info.thumbnail == "https://example.com/thumb.jpg"
        assert info.uploader == "TestUser"
        assert info.duration == 185
        assert info.duration_formatted == "3:05"

    @patch("downloader.core.YoutubeDL")
    def test_filters_storyboard_formats(self, mock_ydl_cls: MagicMock) -> None:
        """mhtml storyboard formats are excluded."""
        instance = mock_ydl_cls.return_value.__enter__.return_value
        instance.extract_info.return_value = FAKE_INFO_DICT

        dl = VideoDownloader()
        info = dl.get_info("https://example.com/video")

        exts = [f.ext for f in info.formats]
        assert "mhtml" not in exts

    @patch("downloader.core.YoutubeDL")
    def test_categorizes_formats_correctly(self, mock_ydl_cls: MagicMock) -> None:
        """Formats are categorized into combined, video_only, audio_only."""
        instance = mock_ydl_cls.return_value.__enter__.return_value
        instance.extract_info.return_value = FAKE_INFO_DICT

        dl = VideoDownloader()
        info = dl.get_info("https://example.com/video")
        d = info.to_dict()

        assert len(d["groups"]["combined"]) == 2      # 18, 22
        assert len(d["groups"]["video_only"]) == 1     # 137
        assert len(d["groups"]["audio_only"]) == 1     # 251

    @patch("downloader.core.YoutubeDL")
    def test_filesize_unknown_shows_desconocido(self, mock_ydl_cls: MagicMock) -> None:
        """Formats without filesize show 'Desconocido'."""
        instance = mock_ydl_cls.return_value.__enter__.return_value
        instance.extract_info.return_value = FAKE_INFO_DICT

        dl = VideoDownloader()
        info = dl.get_info("https://example.com/video")

        audio = [f for f in info.formats if f.format_id == "251"][0]
        assert audio.filesize == "Desconocido"

    @patch("downloader.core.YoutubeDL")
    def test_filesize_converted_to_mb(self, mock_ydl_cls: MagicMock) -> None:
        """Filesize bytes are converted to MB."""
        instance = mock_ydl_cls.return_value.__enter__.return_value
        instance.extract_info.return_value = FAKE_INFO_DICT

        dl = VideoDownloader()
        info = dl.get_info("https://example.com/video")

        fmt_18 = [f for f in info.formats if f.format_id == "18"][0]
        assert isinstance(fmt_18.filesize, float)
        assert abs(fmt_18.filesize - 14.3) < 0.1

    @patch("downloader.core.YoutubeDL")
    def test_invalid_url_raises(self, mock_ydl_cls: MagicMock) -> None:
        """Invalid URLs raise ValueError."""
        from yt_dlp.utils import DownloadError

        instance = mock_ydl_cls.return_value.__enter__.return_value
        instance.extract_info.side_effect = DownloadError("Unsupported URL")

        dl = VideoDownloader()
        with pytest.raises(ValueError, match="No se pudo extraer"):
            dl.get_info("https://invalid.example/nope")

    @patch("downloader.core.YoutubeDL")
    def test_duration_formatting_hours(self, mock_ydl_cls: MagicMock) -> None:
        """Duration > 1 hour uses HH:MM:SS format."""
        info_dict = {**FAKE_INFO_DICT, "duration": 3723}
        instance = mock_ydl_cls.return_value.__enter__.return_value
        instance.extract_info.return_value = info_dict

        dl = VideoDownloader()
        info = dl.get_info("https://example.com/video")
        assert info.duration_formatted == "1:02:03"


# === Download ===

class TestDownload:
    """Tests for download method."""

    @patch("downloader.core.YoutubeDL")
    def test_download_success(self, mock_ydl_cls: MagicMock) -> None:
        """Successful download returns a filepath."""
        instance = mock_ydl_cls.return_value.__enter__.return_value
        instance.download.return_value = 0
        instance.extract_info.return_value = {"ext": "mp4", "title": "test"}
        instance.prepare_filename.return_value = "/tmp/test.mp4"

        dl = VideoDownloader()
        result = dl.download("https://example.com/video", "22", output_dir="/tmp")

        assert result == "/tmp/test.mp4"

    @patch("downloader.core.YoutubeDL")
    def test_download_passes_format_id(self, mock_ydl_cls: MagicMock) -> None:
        """Verify yt-dlp receives the format option."""
        instance = mock_ydl_cls.return_value.__enter__.return_value
        instance.download.return_value = 0
        instance.extract_info.return_value = {"ext": "mp4", "title": "test", "formats": FAKE_INFO_DICT["formats"]}
        instance.prepare_filename.return_value = "/tmp/test.mp4"

        dl = VideoDownloader()
        dl.download("https://example.com/video", "18", output_dir="/tmp")

        call_args = mock_ydl_cls.call_args
        opts = call_args[0][0] if call_args[0] else {}
        assert opts.get("format") == "18"

    @patch("downloader.core.YoutubeDL")
    @patch("shutil.which")
    def test_download_combines_video_only_with_audio(self, mock_which: MagicMock, mock_ydl_cls: MagicMock) -> None:
        """Verify video-only formats download as format_id+bestaudio."""
        mock_which.return_value = "/usr/bin/ffmpeg" # simulate ffmpeg exists
        instance = mock_ydl_cls.return_value.__enter__.return_value
        instance.download.return_value = 0
        instance.extract_info.return_value = FAKE_INFO_DICT
        instance.prepare_filename.return_value = "/tmp/test.mp4"

        dl = VideoDownloader()
        # 137 is 1080p video-only in our FAKE_INFO_DICT
        dl.download("https://example.com/video", "137", output_dir="/tmp")

        call_args = mock_ydl_cls.call_args
        opts = call_args[0][0] if call_args[0] else {}
        assert opts.get("format") == "137+bestaudio/best"

    @patch("downloader.core.YoutubeDL")
    def test_download_with_trim_parameters(self, mock_ydl_cls: MagicMock) -> None:
        """Verify yt-dlp receives download_ranges when start_seconds and end_seconds are passed."""
        instance = mock_ydl_cls.return_value.__enter__.return_value
        instance.download.return_value = 0
        instance.extract_info.return_value = {"ext": "mp4", "title": "test", "formats": FAKE_INFO_DICT["formats"]}
        instance.prepare_filename.return_value = "/tmp/test.mp4"

        dl = VideoDownloader()
        dl.download("https://example.com/video", "18", output_dir="/tmp", start_seconds=10.0, end_seconds=45.0)

        call_args = mock_ydl_cls.call_args_list[-1]
        opts = call_args[0][0] if call_args[0] else {}
        assert "download_ranges" in opts
        assert opts.get("force_keyframes_at_cuts") is True


    @patch("downloader.core.YoutubeDL")
    def test_download_failure_raises(self, mock_ydl_cls: MagicMock) -> None:
        """Download errors raise ValueError."""
        from yt_dlp.utils import DownloadError

        instance = mock_ydl_cls.return_value.__enter__.return_value
        
        calls = [0]
        def fake_extract(*args, **kwargs):
            calls[0] += 1
            if calls[0] == 1:
                return FAKE_INFO_DICT
            raise DownloadError("Network error")

        instance.extract_info.side_effect = fake_extract

        dl = VideoDownloader()
        with pytest.raises(ValueError, match="Error al descargar"):
            dl.download("https://example.com/video", "22")



    @patch("downloader.core.YoutubeDL")
    def test_progress_callback_is_invoked(self, mock_ydl_cls: MagicMock) -> None:
        """Progress callback receives updates during download."""
        instance = mock_ydl_cls.return_value.__enter__.return_value

        # Simulate yt-dlp calling the progress hook
        def fake_extract(url, download=True):
            opts = mock_ydl_cls.call_args[0][0]
            hooks = opts.get("progress_hooks", [])
            for hook in hooks:
                hook({"status": "downloading", "downloaded_bytes": 500, "total_bytes": 1000, "speed": 250.0, "eta": 2.0})
                hook({"status": "finished"})
            return {"ext": "mp4", "title": "test"}

        instance.extract_info.side_effect = fake_extract
        instance.prepare_filename.return_value = "/tmp/test.mp4"

        progress_calls = []

        def on_progress(pct, dl_bytes, total, speed, eta):
            progress_calls.append({"pct": pct, "speed": speed})

        dl = VideoDownloader()
        dl.download("https://example.com/video", "22", output_dir="/tmp", progress_callback=on_progress)

        assert len(progress_calls) == 2
        assert progress_calls[0]["pct"] == 50.0
        assert progress_calls[1]["pct"] == 100.0


# === Backward compatibility ===

class TestLegacy:
    """Ensure get_formats still works."""

    @patch("downloader.core.YoutubeDL")
    def test_get_formats_returns_flat_list(self, mock_ydl_cls: MagicMock) -> None:
        instance = mock_ydl_cls.return_value.__enter__.return_value
        instance.extract_info.return_value = FAKE_INFO_DICT

        dl = VideoDownloader()
        formats = dl.get_formats("https://example.com/video")

        assert all(isinstance(f, VideoFormat) for f in formats)
        assert len(formats) == 4  # excludes mhtml storyboard
