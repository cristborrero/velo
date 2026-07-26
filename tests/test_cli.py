"""Tests for downloader.cli — CLI interface."""

from unittest.mock import patch, MagicMock
from io import StringIO

import pytest

from downloader.core import VideoFormat


class TestFormatTable:
    """Test the format display table rendering."""

    def test_display_formats_prints_table(self) -> None:
        """Verify that display_formats outputs a readable table to stdout."""
        from downloader.cli import display_formats

        formats = [
            VideoFormat("18", "360p", "mp4", 14.3),
            VideoFormat("22", "720p", "mp4", 47.7),
            VideoFormat("251", "audio only", "webm", "Desconocido"),
        ]

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display_formats(formats)
            output = mock_stdout.getvalue()

        assert "360p" in output
        assert "720p" in output
        assert "audio only" in output
        assert "14.3" in output
        assert "Desconocido" in output


class TestRunCli:
    """Test the main CLI interactive flow."""

    @patch("downloader.cli.VideoDownloader")
    @patch("builtins.input")
    def test_full_flow_list_and_download(
        self, mock_input: MagicMock, mock_dl_cls: MagicMock
    ) -> None:
        """Full happy-path: user enters URL, sees formats, picks one, downloads."""
        mock_dl = mock_dl_cls.return_value
        mock_dl.get_formats.return_value = [
            VideoFormat("18", "360p", "mp4", 14.3),
            VideoFormat("22", "720p", "mp4", 47.7),
        ]
        mock_dl.download.return_value = True

        # Simulate: URL → select format 2 → quit
        mock_input.side_effect = ["https://example.com/video", "2", "n"]

        with patch("sys.stdout", new_callable=StringIO):
            from downloader.cli import run_cli
            run_cli()

        mock_dl.get_formats.assert_called_once_with("https://example.com/video")
        mock_dl.download.assert_called_once_with("https://example.com/video", "22")

    @patch("downloader.cli.VideoDownloader")
    @patch("builtins.input")
    def test_invalid_selection_shows_error(
        self, mock_input: MagicMock, mock_dl_cls: MagicMock
    ) -> None:
        """User enters invalid format selection number."""
        mock_dl = mock_dl_cls.return_value
        mock_dl.get_formats.return_value = [
            VideoFormat("18", "360p", "mp4", 14.3),
        ]
        mock_dl.download.return_value = True

        # Invalid "99", then valid "1", then quit
        mock_input.side_effect = ["https://example.com/video", "99", "1", "n"]

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            from downloader.cli import run_cli
            run_cli()
            output = mock_stdout.getvalue()

        assert "inválida" in output.lower() or "invalida" in output.lower()
