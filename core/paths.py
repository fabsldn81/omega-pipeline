"""Filesystem layout helpers — OS-agnostic via pathlib.

The per-episode working folder mirrors build plan Section 8. All paths are built
with pathlib so they behave identically on macOS (dev) and Windows (Fabio).
"""

from __future__ import annotations

from pathlib import Path

# Per-episode subfolders (Section 8). `audio` holds voice + music stems SEPARATELY.
EPISODE_SUBDIRS = (
    "research",
    "script",
    "shotlist",
    "renders",
    "audio",
    "audio/voice",
    "audio/music",
    "thumbnails",
    "final",
)


def repo_root(start: Path | None = None) -> Path:
    """Find the repo root by walking up to the directory holding pyproject.toml."""
    here = Path(start or __file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    # Fallback: the parent of the `core` package.
    return Path(__file__).resolve().parent.parent


class Paths:
    """Resolved locations for one repo checkout."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = Path(root) if root else repo_root()

    @property
    def config(self) -> Path:
        return self.root / "config"

    @property
    def episodes(self) -> Path:
        return self.root / "episodes"

    @property
    def state(self) -> Path:
        return self.root / "state"

    def episode_dir(self, slug: str) -> Path:
        return self.episodes / slug

    def ensure_episode_dirs(self, slug: str) -> Path:
        base = self.episode_dir(slug)
        for sub in EPISODE_SUBDIRS:
            (base / sub).mkdir(parents=True, exist_ok=True)
        return base
