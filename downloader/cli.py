"""Interactive CLI for the video downloader."""

from __future__ import annotations

import sys
from typing import List

from downloader.core import VideoDownloader, VideoFormat


def display_formats(formats: List[VideoFormat]) -> None:
    """Print a table of available formats to stdout."""
    header = f"{'#':>4}  {'ID':>6} | {'Resolución':<10} | {'Ext':<6} | Tamaño"
    separator = "-" * len(header)

    print("\n📹 Formatos disponibles:\n")
    print(header)
    print(separator)

    for i, fmt in enumerate(formats, start=1):
        size = (
            f"{fmt.filesize:.1f} MB"
            if isinstance(fmt.filesize, (int, float))
            else fmt.filesize
        )
        print(f"{i:>4}  {fmt.format_id:>6} | {fmt.resolution:<10} | {fmt.ext:<6} | {size}")

    print()


def run_cli() -> None:
    """Main interactive loop: ask URL → show formats → download."""
    dl = VideoDownloader()

    url = input("🔗 Ingresa la URL del video: ").strip()
    if not url:
        print("❌ No se proporcionó ninguna URL.")
        return

    try:
        print("\n⏳ Extrayendo formatos disponibles...")
        formats = dl.get_formats(url)
    except ValueError as exc:
        print(f"❌ {exc}")
        return

    if not formats:
        print("⚠️  No se encontraron formatos disponibles.")
        return

    display_formats(formats)

    while True:
        choice = input("🎯 Elige el número del formato a descargar: ").strip()
        try:
            idx = int(choice) - 1
            if idx < 0 or idx >= len(formats):
                raise IndexError
            break
        except (ValueError, IndexError):
            print(f"⚠️  Selección inválida. Elige un número entre 1 y {len(formats)}.")

    selected = formats[idx]
    print(
        f"\n⬇️  Descargando: {selected.resolution} ({selected.ext}) "
        f"[ID: {selected.format_id}]..."
    )

    try:
        dl.download(url, selected.format_id)
        print("✅ ¡Descarga completada!")
    except ValueError as exc:
        print(f"❌ {exc}")
        return

    again = input("\n🔄 ¿Deseas descargar otro video? (s/n): ").strip().lower()
    if again in ("s", "si", "sí", "y", "yes"):
        run_cli()


def main() -> None:
    """Entry point."""
    print("=" * 50)
    print("  🎬 Video Downloader — Powered by yt-dlp")
    print("=" * 50)
    run_cli()
