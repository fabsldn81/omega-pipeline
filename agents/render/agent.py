"""Wanessa — Render orchestrator. Clips + voice-over + Suno music ingest.

Generates clips (Higgsfield) and the voice-over (Higgsfield TTS, David's recipe), and
ingests the manually-made Suno music. Multiple takes per shot; voice and music are
SEPARATE stems. Feeds the light take-selection review.
"""

from __future__ import annotations

import os
from typing import Any

from adapters.suno import ensure_placeholder, ingest_music
from agents.base import Agent, AgentContext, add_asset, load_artifact, write_artifact
from core.models import ART_PROMPTS, ART_SCRIPT, ART_SHOTLIST, MediaAsset

_VIDEO_EXTS = (".mp4", ".mov", ".webm", ".mkv")


def _existing_clips(renders_dir, shot_id: str) -> list:
    """Real clip files already in renders/ for a shot (e.g. dropped in via the Higgsfield MCP)."""
    if not renders_dir.exists():
        return []
    return sorted(
        p for p in renders_dir.iterdir()
        if p.is_file() and p.suffix.lower() in _VIDEO_EXTS and p.stem.startswith(shot_id)
    )


class RenderAgent(Agent):
    key = "render"

    def run(self, ctx: AgentContext) -> dict[str, Any]:
        ep = ctx.episode
        shotlist = load_artifact(ctx, ART_SHOTLIST)
        prompt_sets = {p["shot_id"]: p for p in load_artifact(ctx, ART_PROMPTS)["prompts"]}
        script = load_artifact(ctx, ART_SCRIPT)
        shots = shotlist["shots"]

        is_mock = ctx.config.higgsfield_backend == "mock"
        clip_ext = ".clip.txt" if is_mock else ".mp4"
        voice_ext = ".voice.txt" if is_mock else ".wav"
        takes = max(1, int(os.environ.get("HT_TAKES", "1")))

        renders_dir = ctx.episode_dir / "renders"
        clip_count = 0
        for shot in shots:
            # Render-ingest: reuse a real clip already in renders/ (e.g. generated via the
            # Higgsfield MCP and dropped in), instead of (re)generating a placeholder.
            existing = _existing_clips(renders_dir, shot["id"]) if ctx.config.ingest_existing else []
            if existing:
                for take, clip in enumerate(existing, 1):
                    add_asset(ctx, MediaAsset(
                        id=f"{shot['id']}-t{take}", type="clip",
                        status="Selected" if take == 1 else "Raw",
                        local_path=clip.relative_to(ctx.paths.root).as_posix(),
                        shot_id=shot["id"], take=take))
                    clip_count += 1
                shot["render_status"] = "ingested"
                shot["chosen_take"] = 1
                continue
            ps = prompt_sets.get(shot["id"], {})
            prompt_text = f"{ps.get('image_prompt', shot['visual_subject'])}\n{ps.get('motion_prompt', '')}"
            for take in range(1, takes + 1):
                out = renders_dir / f"{shot['id']}_take{take}{clip_ext}"
                path = ctx.higgsfield.generate_clip(prompt_text, out, shot_id=shot["id"], take=take)
                add_asset(ctx, MediaAsset(
                    id=f"{shot['id']}-t{take}",
                    type="clip",
                    status="Selected" if take == 1 else "Raw",
                    local_path=path.relative_to(ctx.paths.root).as_posix(),
                    shot_id=shot["id"],
                    take=take,
                ))
                clip_count += 1
            shot["render_status"] = "rendered"
            shot["chosen_take"] = 1  # default selection; Fabio re-picks at the light review

        # Voice-over (whole narration), recipe-driven.
        narration = f"{script['hook']}\n\n{script['body']}"
        voice_path = ctx.higgsfield.tts(
            narration, ctx.config.voice_recipe,
            ctx.episode_dir / "audio" / "voice" / f"{ep.slug}{voice_ext}",
        )
        add_asset(ctx, MediaAsset(
            id=f"{ep.slug}-voice", type="voice", status="Selected",
            local_path=voice_path.relative_to(ctx.paths.root).as_posix(),
        ))

        # Music: Suno is manual. Ingest whatever Fabio dropped, else a placeholder stem.
        music_dir = ctx.episode_dir / "audio" / "music"
        tracks = ingest_music(music_dir)
        if not tracks:
            tracks = [ensure_placeholder(music_dir)]
        for i, track in enumerate(tracks, 1):
            add_asset(ctx, MediaAsset(
                id=f"{ep.slug}-music-{i}", type="music", status="Selected",
                local_path=track.relative_to(ctx.paths.root).as_posix(),
            ))

        write_artifact(ctx, key=ART_SHOTLIST, rel_subpath="shotlist/shotlist.json", data={"shots": shots})
        ep.log(f"{self.badge}: {clip_count} clip take(s), 1 voice stem, {len(tracks)} music stem(s).")
        return {"agent": self.badge, "clips": clip_count, "takes": takes, "music_stems": len(tracks)}


AGENT = RenderAgent()
