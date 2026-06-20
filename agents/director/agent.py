"""Brenda — Director-assistant. Splits the locked script into a DRAFT shot list.

Proposes per shot: visual subject, composition, camera move, lighting, mood,
transition. This is a draft for Fabio — Gate 3 (Direction lock) is HIS domain; he
edits camera + light shot by shot. Brenda serves, never owns.
"""

from __future__ import annotations

from typing import Any

from agents.base import Agent, AgentContext, load_artifact, load_prompt, write_artifact
from core.jsonio import require_keys
from core.models import ART_SCRIPT, ART_SHOTLIST

SHOT_KEYS = ["id", "scene", "beat", "visual_subject", "composition", "camera_move", "lighting", "mood", "transition"]


class DirectorAgent(Agent):
    key = "director"

    def run(self, ctx: AgentContext) -> dict[str, Any]:
        ep = ctx.episode
        script = load_artifact(ctx, ART_SCRIPT)
        system = ctx.channel_dna + "\n\n" + load_prompt(self.key, ctx.paths)
        user = (
            "Split this locked narration into scenes -> beats -> shots. David appears "
            "ONLY in the open and close bookend shots; everything else is historical "
            "b-roll. Propose camera + light per shot as a DRAFT for Fabio.\n\n"
            f"Hook: {script.get('hook')}\n\nBody:\n{script.get('body')}"
        )
        result = ctx.llm.complete_json(
            system, user, tag="director", required_keys=["shots"]
        )
        shots = result["shots"]
        if not isinstance(shots, list) or not shots:
            from core.errors import ValidationError

            raise ValidationError("Brenda.shotlist: 'shots' must be a non-empty list.")
        for i, shot in enumerate(shots):
            require_keys(shot, SHOT_KEYS, context=f"Brenda.shot[{i}]")
            shot.setdefault("prompts", [])
            shot.setdefault("chosen_take", None)
            shot.setdefault("render_status", "pending")

        write_artifact(ctx, key=ART_SHOTLIST, rel_subpath="shotlist/shotlist.json", data={"shots": shots})
        ep.log(f"{self.badge}: draft shot list, {len(shots)} shots (for Fabio at Gate 3).")
        return {"agent": self.badge, "shots": len(shots)}


AGENT = DirectorAgent()
