"""Katusha — Concept writer. Shapes the dossier + angle into a dramatic arc.

Structure serves the arc; it is not forced into four acts. Reads channel-dna.md.
"""

from __future__ import annotations

from typing import Any

from agents.base import Agent, AgentContext, ingest_existing, load_artifact, load_prompt, write_artifact
from core.jsonio import require_keys
from core.models import ART_DOSSIER, ART_OUTLINE

OUTLINE_KEYS = ["logline", "beats", "climax", "what_next", "structure_notes"]


class ConceptAgent(Agent):
    key = "concept"

    def run(self, ctx: AgentContext) -> dict[str, Any]:
        ep = ctx.episode
        if ctx.config.ingest_existing:
            ing = ingest_existing(ctx, [(ART_OUTLINE, "research/outline.json", OUTLINE_KEYS)])
            if ing is not None:
                ep.log(f"{self.badge}: ingested existing outline (skill output).")
                return {"agent": self.badge, **ing}
        dossier = load_artifact(ctx, ART_DOSSIER)
        system = ctx.channel_dna + "\n\n" + load_prompt(self.key, ctx.paths)
        user = (
            f"Angle / thesis: {ep.angle}\n\n"
            f"Dossier hooks: {dossier.get('hooks')}\n"
            f"Dossier controversies (avoid asserting): {dossier.get('controversies')}\n\n"
            "Shape this into a dramatic arc that builds to an emotional, theatrical "
            "climax. Choose the structure that serves the arc."
        )
        outline = ctx.llm.complete_json(
            system, user, tag="concept", required_keys=OUTLINE_KEYS
        )
        require_keys(outline, OUTLINE_KEYS, context="Katusha.outline")
        write_artifact(ctx, key=ART_OUTLINE, rel_subpath="research/outline.json", data=outline)
        ep.log(f"{self.badge}: outline with {len(outline['beats'])} beats; climax set.")
        return {"agent": self.badge, "beats": len(outline["beats"]), "climax": outline["climax"][:80]}


AGENT = ConceptAgent()
