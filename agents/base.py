"""Agent base class, the per-run context, and small artifact helpers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from adapters.factory import Adapters
from core.config import Config
from core.errors import ArtifactMissing
from core.jsonio import load_json, save_json
from core.models import Episode, MediaAsset
from core.paths import Paths

from .crew import badge, name_of


@dataclass
class AgentContext:
    episode: Episode
    config: Config
    adapters: Adapters

    @property
    def paths(self) -> Paths:
        return self.config.paths

    @property
    def episode_dir(self) -> Path:
        return self.paths.episode_dir(self.episode.slug)

    @property
    def channel_dna(self) -> str:
        return self.config.channel_dna

    @property
    def llm(self):
        return self.adapters.llm

    @property
    def higgsfield(self):
        return self.adapters.higgsfield

    @property
    def store(self):
        return self.adapters.store


def load_prompt(key: str, paths: Paths) -> str:
    """Load agents/<key>/prompt.md (shared by the Python agent and its Claude skill)."""
    p = paths.root / "agents" / key / "prompt.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""


def write_artifact(ctx: AgentContext, *, key: str, rel_subpath: str, data: Any) -> str:
    """Save a JSON artifact under the episode folder and record it on the episode."""
    path = ctx.episode_dir / rel_subpath
    save_json(path, data)
    rel = path.relative_to(ctx.paths.root).as_posix()
    ctx.episode.artifacts[key] = rel
    return rel


def write_text(ctx: AgentContext, rel_subpath: str, text: str) -> str:
    path = ctx.episode_dir / rel_subpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path.relative_to(ctx.paths.root).as_posix()


def load_artifact(ctx: AgentContext, key: str) -> Any:
    rel = ctx.episode.artifacts.get(key)
    if not rel:
        raise ArtifactMissing(
            f"Episode '{ctx.episode.slug}' has no '{key}' artifact yet."
        )
    return load_json(ctx.paths.root / rel)


def add_asset(ctx: AgentContext, asset: MediaAsset) -> MediaAsset:
    ctx.episode.assets.append(asset)
    return asset


class Agent(ABC):
    key: str = ""

    @property
    def name(self) -> str:
        return name_of(self.key)

    @property
    def badge(self) -> str:
        return badge(self.key)

    @abstractmethod
    def run(self, ctx: AgentContext) -> dict[str, Any]:
        """Do the phase's work; write artifacts; return a short summary dict."""
        ...
