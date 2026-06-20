"""Glesy — Scriptwriter. Writes the full theatrical narration in David's voice.

Strong cold-open hook, timed to target length, arc intact, with the brand-constant
bookends. Feeds Gate 2 (Script lock). Reads channel-dna.md.
"""

from __future__ import annotations

from typing import Any

from agents.base import Agent, AgentContext, ingest_existing, load_artifact, load_prompt, write_artifact, write_text
from core.jsonio import require_keys
from core.models import ART_OUTLINE, ART_SCRIPT

SCRIPT_KEYS = ["hook", "open_bookend", "body", "close_bookend", "estimated_seconds"]


class ScriptwriterAgent(Agent):
    key = "scriptwriter"

    def run(self, ctx: AgentContext) -> dict[str, Any]:
        ep = ctx.episode
        if ctx.config.ingest_existing:
            ing = ingest_existing(ctx, [(ART_SCRIPT, "script/script.json", SCRIPT_KEYS)])
            if ing is not None:
                ep.log(f"{self.badge}: ingested existing script (skill output).")
                return {"agent": self.badge, **ing}
        outline = load_artifact(ctx, ART_OUTLINE)
        system = ctx.channel_dna + "\n\n" + load_prompt(self.key, ctx.paths)
        user = (
            f"Target length: ~{ep.target_length_min} minutes.\n"
            f"Logline: {outline.get('logline')}\n"
            f"Beats: {outline.get('beats')}\n"
            f"Climax (build to this): {outline.get('climax')}\n"
            f"What comes next: {outline.get('what_next')}\n\n"
            "Write the full narration in David's theatrical British voice. Open with a "
            "hook, not a throat-clear. Include the brand-constant bookends verbatim."
        )
        script = ctx.llm.complete_json(
            system, user, tag="scriptwriter", required_keys=SCRIPT_KEYS
        )
        require_keys(script, SCRIPT_KEYS, context="Glesy.script")
        write_artifact(ctx, key=ART_SCRIPT, rel_subpath="script/script.json", data=script)

        readable = (
            f"# {ep.title or ep.slug} — Script\n\n"
            f"## Cold open (hook)\n{script['hook']}\n\n"
            f"## Open bookend\n{script['open_bookend']}\n\n"
            f"## Body\n{script['body']}\n\n"
            f"## Close bookend\n{script['close_bookend']}\n\n"
            f"_Estimated: {script['estimated_seconds']}s_\n"
        )
        write_text(ctx, "script/script.md", readable)
        ep.log(f"{self.badge}: locked script (~{script['estimated_seconds']}s).")
        return {"agent": self.badge, "estimated_seconds": script["estimated_seconds"]}


AGENT = ScriptwriterAgent()
