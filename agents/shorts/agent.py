"""Jucilene — Shorts cutter. Extracts 1–2 vertical 9:16 Shorts from the long-form.

Runs off the finished cut using assets that already exist (low marginal cost). The
aggressive-growth lever for subscribers.
"""

from __future__ import annotations

from typing import Any

from agents.base import Agent, AgentContext, add_asset, load_artifact, write_artifact, write_text
from core.models import ART_SCRIPT, ART_SHORTS, MediaAsset
from scripts import ffmpeg_ops as ff


class ShortsAgent(Agent):
    key = "shorts"

    def run(self, ctx: AgentContext) -> dict[str, Any]:
        ep = ctx.episode
        script = load_artifact(ctx, ART_SCRIPT)
        source = next((a.local_path for a in ep.assets if a.type == "final"), f"episodes/{ep.slug}/final/")

        angles = [
            ("hook", "The myth-buster cold open", script.get("hook", "")),
            ("climax", "The emotional climax", script.get("climax", script.get("close_bookend", ""))),
        ]

        shorts = []
        shorts_dir = ctx.episode_dir / "final" / "shorts"
        for i, (tag, angle, caption) in enumerate(angles, 1):
            out = shorts_dir / f"short_{i}_{tag}.mp4"
            argv = ff.reframe_vertical_cmd(ctx.paths.root / source, out)
            placeholder_rel = write_text(
                ctx, f"final/shorts/short_{i}_{tag}.placeholder.txt",
                f"[SHORT {i}] {angle}\nsource: {source}\nreframe: 9:16 (1080x1920)\ncaption: {caption}\n",
            )
            shorts.append({
                "id": f"short_{i}",
                "angle": angle,
                "source": source,
                "out": out.relative_to(ctx.paths.root).as_posix(),
                "reframe_cmd": argv,
                "caption": caption,
            })
            add_asset(ctx, MediaAsset(
                id=f"{ep.slug}-{tag}-short", type="short", status="Raw", local_path=placeholder_rel,
            ))

        write_artifact(ctx, key=ART_SHORTS, rel_subpath="final/shorts/shorts_plan.json", data={"shorts": shorts})
        ep.log(f"{self.badge}: {len(shorts)} vertical Short(s) planned.")
        return {"agent": self.badge, "shorts": len(shorts)}


AGENT = ShortsAgent()
