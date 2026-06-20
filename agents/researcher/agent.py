"""Deborah — Researcher. Builds the dossier + source ledger and a packaging draft.

Feeds Gate 1 (Topic + Packaging lock). Reads channel-dna.md before acting.
"""

from __future__ import annotations

from typing import Any

from agents.base import Agent, AgentContext, ingest_existing, load_prompt, write_artifact
from core.jsonio import require_keys
from core.models import ART_DOSSIER, ART_PACKAGING

DOSSIER_KEYS = ["facts", "timeline", "key_figures", "hooks", "controversies", "sources", "demand_signal"]
PACKAGING_KEYS = ["title_variants", "thumbnail_concepts", "hook", "description", "tags", "chapters", "end_screen"]


class ResearcherAgent(Agent):
    key = "researcher"

    def run(self, ctx: AgentContext) -> dict[str, Any]:
        ep = ctx.episode
        if ctx.config.ingest_existing:
            ing = ingest_existing(ctx, [
                (ART_DOSSIER, "research/dossier.json", DOSSIER_KEYS),
                (ART_PACKAGING, "research/packaging.json", PACKAGING_KEYS),
            ])
            if ing is not None:
                ep.log(f"{self.badge}: ingested existing dossier + packaging (skill output).")
                return {"agent": self.badge, **ing}
        system = ctx.channel_dna + "\n\n" + load_prompt(self.key, ctx.paths)
        user = (
            f"Episode topic: {ep.topic or ep.title}\n"
            f"Working title: {ep.title}\n"
            f"Angle / thesis (Fabio's): {ep.angle}\n\n"
            "Build the research dossier and a packaging proposal for Gate 1. "
            "Every factual claim must map to a source URL in the source ledger. "
            "Include a free, YouTube-native demand signal."
        )
        result = ctx.llm.complete_json(
            system, user, tag="researcher", required_keys=["dossier", "packaging"]
        )
        dossier, packaging = result["dossier"], result["packaging"]
        require_keys(dossier, DOSSIER_KEYS, context="Deborah.dossier")
        require_keys(packaging, PACKAGING_KEYS, context="Deborah.packaging")

        write_artifact(ctx, key=ART_DOSSIER, rel_subpath="research/dossier.json", data=dossier)
        write_artifact(ctx, key=ART_PACKAGING, rel_subpath="research/packaging.json", data=packaging)
        ep.log(f"{self.badge}: dossier ({len(dossier['facts'])} facts, "
               f"{len(dossier['sources'])} sources) + packaging draft.")
        return {
            "agent": self.badge,
            "facts": len(dossier["facts"]),
            "sources": len(dossier["sources"]),
            "title_variants": len(packaging["title_variants"]),
        }


AGENT = ResearcherAgent()
