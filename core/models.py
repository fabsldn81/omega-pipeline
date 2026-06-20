"""Domain models managed by the store.

Episode and MediaAsset are structured dataclasses. The richer creative artifacts
(dossier, outline, critique, script, shot list, prompt set, packaging) are produced
by the LLM agents as JSON dicts, lightly validated, and written into the episode
folder; their relative paths are recorded on the Episode under `artifacts`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .status import Status

# Artifact keys recorded on Episode.artifacts (value = path relative to repo root).
ART_DOSSIER = "dossier"
ART_PACKAGING = "packaging"
ART_OUTLINE = "outline"
ART_CRITIQUE = "critique"
ART_SCRIPT = "script"
ART_SHOTLIST = "shotlist"
ART_PROMPTS = "prompts"
ART_EDIT_PLAN = "edit_plan"
ART_SHORTS = "shorts"


# Media asset Type / Status vocabularies (build plan Section 5).
ASSET_TYPES = ("clip", "voice", "music", "thumbnail", "final", "short")
ASSET_STATUSES = ("Raw", "Selected", "Final")


@dataclass
class MediaAsset:
    id: str
    type: str  # one of ASSET_TYPES
    status: str = "Raw"  # one of ASSET_STATUSES
    local_path: str = ""  # path on the machine (build plan: "Local path on Fabio's machine")
    shot_id: str | None = None
    take: int | None = None
    notes: str = ""

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "MediaAsset":
        return cls(
            id=d["id"],
            type=d["type"],
            status=d.get("status", "Raw"),
            local_path=d.get("local_path", ""),
            shot_id=d.get("shot_id"),
            take=d.get("take"),
            notes=d.get("notes", ""),
        )


@dataclass
class Episode:
    slug: str
    title: str = ""
    topic: str = ""
    angle: str = ""
    target_length_min: int = 12
    status: Status = Status.IDEA
    publish_date: str | None = None
    pending_gate: str | None = None  # Gate label awaiting Fabio's approval, if any
    artifacts: dict[str, str] = field(default_factory=dict)
    assets: list[MediaAsset] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    history: list[str] = field(default_factory=list)  # human-readable audit trail

    # --- serialisation -----------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "slug": self.slug,
            "title": self.title,
            "topic": self.topic,
            "angle": self.angle,
            "target_length_min": self.target_length_min,
            "status": self.status.value,
            "publish_date": self.publish_date,
            "pending_gate": self.pending_gate,
            "artifacts": dict(self.artifacts),
            "assets": [a.__dict__ for a in self.assets],
            "metrics": dict(self.metrics),
            "history": list(self.history),
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Episode":
        return cls(
            slug=d["slug"],
            title=d.get("title", ""),
            topic=d.get("topic", ""),
            angle=d.get("angle", ""),
            target_length_min=d.get("target_length_min", 12),
            status=Status(d.get("status", Status.IDEA.value)),
            publish_date=d.get("publish_date"),
            pending_gate=d.get("pending_gate"),
            artifacts=dict(d.get("artifacts", {})),
            assets=[MediaAsset.from_dict(a) for a in d.get("assets", [])],
            metrics=dict(d.get("metrics", {})),
            history=list(d.get("history", [])),
        )

    def log(self, message: str) -> None:
        self.history.append(message)
