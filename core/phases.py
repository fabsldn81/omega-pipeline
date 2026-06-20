"""The per-episode phase map: status -> the work done to leave it.

Binds the nine pipeline phases (build plan Section 3) onto the twelve statuses.
For each status we record:
  * the phase number + human name,
  * the ordered agent keys that run while the episode sits in that status,
  * the gate (if any) that authorises exit,
  * the status it advances to,
  * whether the work is Fabio's (no agent runs; he acts).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .gates import Gate, gate_for_status
from .status import Status, next_in_order


@dataclass(frozen=True)
class Phase:
    status: Status
    number: int
    name: str
    agents: tuple[str, ...]
    gate: Gate | None
    advances_to: Status | None
    fabio_owned: bool
    description: str


def _phase(
    status: Status,
    number: int,
    name: str,
    *,
    agents: tuple[str, ...] = (),
    fabio_owned: bool = False,
    description: str = "",
) -> Phase:
    return Phase(
        status=status,
        number=number,
        name=name,
        agents=agents,
        gate=gate_for_status(status),
        advances_to=next_in_order(status),
        fabio_owned=fabio_owned,
        description=description,
    )


# Ordered by status. `agents` are the sub-agent keys (see agents/ registry).
PHASES: dict[Status, Phase] = {
    Status.IDEA: _phase(
        Status.IDEA, 0, "Brainstorm",
        fabio_owned=True,
        description="Fabio picks the topic and thesis/angle. The Showrunner may surface "
        "demand-validated candidates from the Topic Pool, but the spark is Fabio's.",
    ),
    Status.RESEARCHING: _phase(
        Status.RESEARCHING, 1, "Research",
        agents=("researcher",),
        description="Researcher builds the dossier (timeline, figures, hooks, "
        "controversies, source ledger) and a packaging proposal for Gate 1.",
    ),
    Status.PACKAGING_LOCKED: _phase(
        Status.PACKAGING_LOCKED, 2, "Concept / Outline + Adversarial review",
        agents=("concept", "critic"),
        description="Concept writer shapes the dramatic arc; the critic attacks it and "
        "the writer revises. No hard gate — Fabio sees the result at Gate 2.",
    ),
    Status.SCRIPTING: _phase(
        Status.SCRIPTING, 4, "Script",
        agents=("scriptwriter",),
        description="Scriptwriter writes the full theatrical narration in David's voice, "
        "timed, arc intact, with a strong cold-open hook.",
    ),
    Status.SCRIPT_LOCKED: _phase(
        Status.SCRIPT_LOCKED, 5, "Direction / shot breakdown (draft)",
        agents=("director",),
        description="Director-assistant splits the locked script into scenes -> beats -> "
        "shots and proposes camera/light/composition/transition. A draft for Fabio.",
    ),
    Status.DIRECTION: _phase(
        Status.DIRECTION, 5, "Direction review (Fabio)",
        fabio_owned=True,
        description="Fabio edits camera + lighting shot by shot. His sacred creative act.",
    ),
    Status.DIRECTION_LOCKED: _phase(
        Status.DIRECTION_LOCKED, 6, "Prompt generation",
        agents=("prompt_engineer",),
        description="Prompt engineer converts each approved shot into model-ready prompts. "
        "Deterministic translation of a frozen shot list — quick sanity glance only.",
    ),
    Status.GENERATING: _phase(
        Status.GENERATING, 7, "Render",
        agents=("render",),
        description="Render orchestrator generates clips + voice-over and ingests Suno "
        "music, multiple takes per shot. Feeds the light take-selection review.",
    ),
    Status.EDITING: _phase(
        Status.EDITING, 8, "Edit / assembly",
        agents=("editor",),
        description="Editor assembles clips to VO timing, ducked music, captions, fades, "
        "overlays and the bookend template. Produces the cut for Final-review.",
    ),
    Status.FINAL_REVIEW: _phase(
        Status.FINAL_REVIEW, 8, "Final review (Fabio)",
        fabio_owned=True,
        description="Fabio watches the assembled cut and confirms final packaging at Gate 4.",
    ),
    Status.SCHEDULED: _phase(
        Status.SCHEDULED, 8, "Hand-off / publish",
        fabio_owned=True,
        description="The approved video + packaging are queued for upload. The Showrunner "
        "never performs the publish itself.",
    ),
    Status.PUBLISHED: _phase(
        Status.PUBLISHED, 9, "Published (+ Shorts spin-off)",
        description="Terminal for the long-form. Phase 9 (Shorts cutter) runs off the "
        "finished long-form using assets that already exist.",
    ),
}


def phase_for(status: Status) -> Phase:
    return PHASES[status]
