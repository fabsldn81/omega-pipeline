"""Suno music ingest — manual by design (build plan Section 6: no Suno MCP).

Fabio generates 1–3 tracks in the Suno web app and drops the files into the
episode's `audio/music/` folder. This module just discovers them. For a dry-run with
no real tracks, `ensure_placeholder` writes a stand-in stem so the edit plan is whole.
"""

from __future__ import annotations

from pathlib import Path

MUSIC_EXTENSIONS = (".mp3", ".wav", ".aac", ".flac", ".m4a", ".ogg")


def ingest_music(music_dir: Path) -> list[Path]:
    """Return the music stems Fabio dropped into the episode's audio/music folder."""
    music_dir = Path(music_dir)
    if not music_dir.exists():
        return []
    return sorted(
        p for p in music_dir.iterdir()
        if p.is_file() and p.suffix.lower() in MUSIC_EXTENSIONS
    )


def ensure_placeholder(music_dir: Path) -> Path:
    """Write a placeholder music stem when none is present (dry-run only)."""
    music_dir = Path(music_dir)
    music_dir.mkdir(parents=True, exist_ok=True)
    placeholder = music_dir / "score.placeholder.txt"
    placeholder.write_text(
        "[MOCK MUSIC STEM] Drop a real Suno track here (.mp3/.wav). "
        "Voice and music stay SEPARATE; the editor ducks this under the narration.\n",
        encoding="utf-8",
    )
    return placeholder
