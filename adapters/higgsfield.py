"""Higgsfield adapter: Wanessa's render backend (clips + voice TTS).

  * MockHiggsfield — writes inspectable placeholder files (default; no keys, no
    ffmpeg, no network). Lets the whole pipeline dry-run to a finished shape.
  * HiggsfieldAPI  — scaffold for the real account (clips + Speak 2.0 TTS). Wire it
    to Fabio's Higgsfield MCP/API at build time; it fails loud until configured.

Voice is recipe-driven (config/voice-recipe.json) for portability — see Section 6.
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from core.errors import AdapterNotConfigured


class HiggsfieldAdapter(ABC):
    name = "higgsfield"

    @abstractmethod
    def generate_clip(self, prompt: str, out_path: Path, *, shot_id: str, take: int) -> Path:
        ...

    @abstractmethod
    def tts(self, text: str, recipe: dict[str, Any], out_path: Path) -> Path:
        ...


class MockHiggsfield(HiggsfieldAdapter):
    """Deterministic placeholders so the pipeline produces a tangible dry-run."""

    name = "mock"

    def generate_clip(self, prompt: str, out_path: Path, *, shot_id: str, take: int) -> Path:
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            f"[MOCK CLIP] shot={shot_id} take={take}\nprompt:\n{prompt}\n",
            encoding="utf-8",
        )
        return out_path

    def tts(self, text: str, recipe: dict[str, Any], out_path: Path) -> Path:
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        preset = recipe.get("preset") or "(recipe not locked yet)"
        out_path.write_text(
            f"[MOCK VOICE] preset={preset}\n--- narration ---\n{text}\n",
            encoding="utf-8",
        )
        return out_path


class HiggsfieldAPI(HiggsfieldAdapter):
    """Real Higgsfield account. Opt-in via HT_HIGGSFIELD=api.

    Left as a documented scaffold: on Fabio's machine, point these methods at the
    Higgsfield MCP tools (or REST) for clip generation and Speak 2.0 TTS, selecting
    the per-shot model from config/models.json and the voice recipe from
    config/voice-recipe.json.
    """

    name = "api"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.environ.get("HIGGSFIELD_API_KEY")
        if not self.api_key:
            raise AdapterNotConfigured(
                "HIGGSFIELD_API_KEY is not set (or wire the Higgsfield MCP). "
                "Set HT_HIGGSFIELD=mock to dry-run without it."
            )

    def generate_clip(self, prompt: str, out_path: Path, *, shot_id: str, take: int) -> Path:  # pragma: no cover
        raise AdapterNotConfigured(
            "HiggsfieldAPI.generate_clip is a scaffold — wire it to Fabio's Higgsfield "
            "MCP/API at build time (Build E)."
        )

    def tts(self, text: str, recipe: dict[str, Any], out_path: Path) -> Path:  # pragma: no cover
        raise AdapterNotConfigured(
            "HiggsfieldAPI.tts is a scaffold — wire it to Higgsfield Speak 2.0 with the "
            "locked voice recipe at build time (Build E)."
        )
