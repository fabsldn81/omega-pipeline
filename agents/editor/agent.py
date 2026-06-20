"""Cleidiane — Editor. FFmpeg/Whisper assembly into the cut.

Cuts the selected clips to VO timing, layers ducked music, captions (Whisper SRT),
fades, overlays and the bookend template; loudness target -14 LUFS. Produces the cut
for Final-review (Gate 4). Builds a full, ordered command plan; executes ffmpeg only
when real media + ffmpeg are present, otherwise plans (and still writes real captions).
"""

from __future__ import annotations

from typing import Any

from agents.base import Agent, AgentContext, add_asset, load_artifact, write_artifact, write_text
from core.models import ART_EDIT_PLAN, ART_SCRIPT, ART_SHOTLIST, MediaAsset
from scripts import ffmpeg_ops as ff
from scripts.tooling import run
from scripts.whisper_ops import synthesize_srt_from_text, transcribe_srt_cmd


class EditorAgent(Agent):
    key = "editor"

    def run(self, ctx: AgentContext) -> dict[str, Any]:
        ep = ctx.episode
        shotlist = load_artifact(ctx, ART_SHOTLIST)
        script = load_artifact(ctx, ART_SCRIPT)
        order = [s["id"] for s in shotlist["shots"]]

        # Selected clip per shot, in shot order.
        selected = {a.shot_id: a for a in ep.assets if a.type == "clip" and a.status == "Selected"}
        clip_paths = [ctx.paths.root / selected[sid].local_path for sid in order if sid in selected]
        voice = next((ctx.paths.root / a.local_path for a in ep.assets if a.type == "voice"), None)
        music = next((ctx.paths.root / a.local_path for a in ep.assets if a.type == "music"), None)

        ed = ctx.episode_dir
        assembled = ed / "renders" / "assembled.mp4"
        voice_norm = ed / "audio" / "voice" / f"{ep.slug}.norm.wav"
        mix = ed / "audio" / "voice" / f"{ep.slug}.mix.wav"
        cut = ed / "final" / f"{ep.slug}.cut.mp4"
        captioned = ed / "final" / f"{ep.slug}.captioned.mp4"
        srt = ed / "final" / "captions.srt"
        duration = float(script.get("estimated_seconds", 720))

        # Real captions now (dependency-free), plus the production Whisper command.
        synthesize_srt_from_text(script.get("body", ""), srt, total_seconds=duration)

        steps: list[dict[str, Any]] = []

        def plan(name: str, argv: list[str]) -> None:
            # Execute only with real media (api backend) + ffmpeg present + not dry-run.
            execute = ctx.config.higgsfield_backend == "api" and not ctx.config.dry_run
            res = run(argv, dry_run=not execute)
            steps.append({"name": name, "argv": res.argv, "executed": res.executed, "note": res.note})

        if clip_paths:
            plan("assemble picture (concat, bookends included)", ff.assembly_cmd(clip_paths, assembled))
        if voice:
            plan("measure voice loudness", ff.loudnorm_measure_cmd(voice))
            plan("normalise voice to -14 LUFS", ff.loudnorm_apply_cmd(voice, voice_norm))
        if voice_norm and music:
            plan("duck music under narration + fades", ff.duck_cmd(voice_norm, music, mix, duration=duration))
        plan("mux picture + mixed audio", ff.mux_cmd(assembled, mix, cut))
        plan("captions (production: Whisper)", transcribe_srt_cmd(mix, ed / "final"))
        plan("burn captions", ff.burn_captions_cmd(cut, srt, captioned))

        edit_plan = {
            "target_lufs": ff.TARGET_LUFS,
            "captions": srt.relative_to(ctx.paths.root).as_posix(),
            "bookend_note": "Open/close David bookend shots are first/last in the concat.",
            "executed": any(s["executed"] for s in steps),
            "steps": steps,
        }
        write_artifact(ctx, key=ART_EDIT_PLAN, rel_subpath="final/edit_plan.json", data=edit_plan)

        final_rel = write_text(
            ctx, f"final/{ep.slug}.final.txt",
            f"[CUT — {ep.title or ep.slug}]\n"
            f"Shots: {len(order)} | Captions: {srt.name} | Loudness target: {ff.TARGET_LUFS} LUFS\n"
            f"Steps planned: {len(steps)} (executed: {edit_plan['executed']})\n"
            "Mock final: wire ffmpeg + real Higgsfield clips to render the actual .mp4.\n",
        )
        add_asset(ctx, MediaAsset(
            id=f"{ep.slug}-final", type="final", status="Final", local_path=final_rel,
        ))
        ep.log(f"{self.badge}: cut assembled — {len(steps)} steps, captions written.")
        return {"agent": self.badge, "steps": len(steps), "captions": edit_plan["captions"], "final": final_rel}


AGENT = EditorAgent()
