"""The store — the episode database the Showrunner reads pipeline state from.

  * LocalStore — JSON file under state/ (default; the source of truth when offline).
  * NotionStore — scaffold for Fabio's Notion via the Notion MCP/API (opt-in).

On Fabio's machine Notion is authoritative; LocalStore is the convenience mirror and
the zero-dependency default for development and tests.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from core.errors import AdapterNotConfigured
from core.jsonio import load_json, save_json
from core.models import Episode
from core.paths import Paths


class Store(ABC):
    @abstractmethod
    def exists(self, slug: str) -> bool: ...

    @abstractmethod
    def get(self, slug: str) -> Episode: ...

    @abstractmethod
    def save(self, episode: Episode) -> None: ...

    @abstractmethod
    def list(self) -> list[Episode]: ...

    def create(self, episode: Episode) -> Episode:
        if self.exists(episode.slug):
            raise ValueError(f"Episode '{episode.slug}' already exists.")
        self.save(episode)
        return episode


class LocalStore(Store):
    """Episodes persisted as JSON at state/episodes.json."""

    def __init__(self, paths: Paths | None = None, db_path: Path | None = None) -> None:
        self.paths = paths or Paths()
        self.db_path = Path(db_path) if db_path else self.paths.state / "episodes.json"

    def _load(self) -> dict[str, Any]:
        if not self.db_path.exists():
            return {"episodes": {}}
        return load_json(self.db_path)

    def _save_all(self, data: dict[str, Any]) -> None:
        save_json(self.db_path, data)

    def exists(self, slug: str) -> bool:
        return slug in self._load().get("episodes", {})

    def get(self, slug: str) -> Episode:
        data = self._load().get("episodes", {})
        if slug not in data:
            raise KeyError(f"No episode '{slug}' in the store.")
        return Episode.from_dict(data[slug])

    def save(self, episode: Episode) -> None:
        data = self._load()
        data.setdefault("episodes", {})[episode.slug] = episode.to_dict()
        self._save_all(data)

    def list(self) -> list[Episode]:
        data = self._load().get("episodes", {})
        return [Episode.from_dict(v) for v in data.values()]


class NotionStore(Store):
    """Scaffold for Fabio's Notion workspace (build plan Section 5).

    Wire to the Notion MCP/API at setup time, mapping the Episodes database fields
    (Status, Angle, relations, etc.) onto the Episode model. Fails loud until then.
    """

    def __init__(self, token: str | None = None) -> None:  # pragma: no cover
        import os

        self.token = token or os.environ.get("NOTION_TOKEN")
        if not self.token:
            raise AdapterNotConfigured(
                "NOTION_TOKEN is not set (or wire the Notion MCP). Set HT_STORE=local "
                "to use the local JSON mirror."
            )

    def exists(self, slug: str) -> bool:  # pragma: no cover
        raise AdapterNotConfigured("NotionStore is a scaffold — wire it at setup time.")

    def get(self, slug: str) -> Episode:  # pragma: no cover
        raise AdapterNotConfigured("NotionStore is a scaffold — wire it at setup time.")

    def save(self, episode: Episode) -> None:  # pragma: no cover
        raise AdapterNotConfigured("NotionStore is a scaffold — wire it at setup time.")

    def list(self) -> list[Episode]:  # pragma: no cover
        raise AdapterNotConfigured("NotionStore is a scaffold — wire it at setup time.")
