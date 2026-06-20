"""Configuration loading and adapter selection.

Reads the three config files (channel-dna.md, models.json, voice-recipe.json) and
the adapter knobs from environment variables. Defaults select the MOCK adapters so a
fresh checkout runs end-to-end with no keys and no network.

Environment variables (all optional):
  HT_LLM=mock|anthropic            (default: mock)
  HT_STORE=local|notion            (default: local)
  HT_HIGGSFIELD=mock|api           (default: mock)
  HT_LLM_MODEL=<model id>          (default: claude-opus-4-8 — only used by AnthropicLLM)
  HT_DRY_RUN=1                      (force editing scripts to plan-only, never exec)
  HT_INGEST=1                      (writing agents reuse an artifact already on disk
                                    instead of generating it — lets the Claude Code
                                    skills produce the content with no API key)
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .jsonio import load_json
from .paths import Paths


def _env(name: str, default: str) -> str:
    return os.environ.get(name, default).strip().lower()


@dataclass
class Config:
    paths: Paths
    channel_dna: str
    models: dict[str, Any]
    voice_recipe: dict[str, Any]
    llm_backend: str = "mock"
    store_backend: str = "local"
    higgsfield_backend: str = "mock"
    llm_model: str = "claude-opus-4-8"
    dry_run: bool = False
    ingest_existing: bool = False

    @property
    def is_fully_mocked(self) -> bool:
        return (
            self.llm_backend == "mock"
            and self.store_backend == "local"
            and self.higgsfield_backend == "mock"
        )


def load_config(root: Path | None = None, *, overrides: dict[str, str] | None = None) -> Config:
    paths = Paths(root)
    overrides = overrides or {}

    def pick(env_name: str, key: str, default: str) -> str:
        if key in overrides:
            return str(overrides[key]).strip().lower()
        return _env(env_name, default)

    channel_dna = ""
    dna_path = paths.config / "channel-dna.md"
    if dna_path.exists():
        channel_dna = dna_path.read_text(encoding="utf-8")

    models: dict[str, Any] = {}
    models_path = paths.config / "models.json"
    if models_path.exists():
        models = load_json(models_path)

    voice: dict[str, Any] = {}
    voice_path = paths.config / "voice-recipe.json"
    if voice_path.exists():
        voice = load_json(voice_path)

    dry = pick("HT_DRY_RUN", "dry_run", "0") in {"1", "true", "yes", "on"}
    ingest = pick("HT_INGEST", "ingest", "0") in {"1", "true", "yes", "on"}

    return Config(
        paths=paths,
        channel_dna=channel_dna,
        models=models,
        voice_recipe=voice,
        llm_backend=pick("HT_LLM", "llm", "mock"),
        store_backend=pick("HT_STORE", "store", "local"),
        higgsfield_backend=pick("HT_HIGGSFIELD", "higgsfield", "mock"),
        llm_model=os.environ.get("HT_LLM_MODEL", overrides.get("llm_model", "claude-opus-4-8")),
        dry_run=dry,
        ingest_existing=ingest,
    )
