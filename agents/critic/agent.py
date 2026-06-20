"""Tainara — Adversarial critic. Attacks the outline before it becomes a script.

Accuracy, originality, retention, and above all whether it builds to an emotional
climax. Reinforced gate for sensitive topics (balance, accuracy, advertiser-safety).
No hard gate — Fabio sees the result at Gate 2. Reads channel-dna.md.
"""

from __future__ import annotations

from typing import Any

from agents.base import Agent, AgentContext, ingest_existing, load_artifact, load_prompt, write_artifact
from core.jsonio import require_keys
from core.models import ART_CRITIQUE, ART_OUTLINE

CRITIQUE_KEYS = ["issues", "verdict", "advertiser_safe", "revisions"]


class CriticAgent(Agent):
    key = "critic"

    def run(self, ctx: AgentContext) -> dict[str, Any]:
        ep = ctx.episode
        if ctx.config.ingest_existing:
            ing = ingest_existing(ctx, [(ART_CRITIQUE, "research/critique.json", CRITIQUE_KEYS)])
            if ing is not None:
                ep.log(f"{self.badge}: ingested existing critique (skill output).")
                return {"agent": self.badge, **ing}
        outline = load_artifact(ctx, ART_OUTLINE)
        system = ctx.channel_dna + "\n\n" + load_prompt(self.key, ctx.paths)
        user = (
            f"Topic: {ep.topic or ep.title}\nAngle: {ep.angle}\n\n"
            f"Outline under review:\nlogline: {outline.get('logline')}\n"
            f"beats: {outline.get('beats')}\nclimax: {outline.get('climax')}\n\n"
            "Attack it. Does it actually build to an emotional climax? Is it accurate, "
            "original, retentive, advertiser-safe? For sensitive topics, be the "
            "reinforced gate."
        )
        critique = ctx.llm.complete_json(
            system, user, tag="critic", required_keys=CRITIQUE_KEYS
        )
        require_keys(critique, CRITIQUE_KEYS, context="Tainara.critique")
        write_artifact(ctx, key=ART_CRITIQUE, rel_subpath="research/critique.json", data=critique)
        flag = "" if critique["advertiser_safe"] else " [ADVERTISER-SAFETY FLAG]"
        ep.log(f"{self.badge}: {len(critique['issues'])} issues; "
               f"verdict — {critique['verdict'][:60]}{flag}")
        return {
            "agent": self.badge,
            "issues": len(critique["issues"]),
            "advertiser_safe": critique["advertiser_safe"],
            "verdict": critique["verdict"][:80],
        }


AGENT = CriticAgent()
