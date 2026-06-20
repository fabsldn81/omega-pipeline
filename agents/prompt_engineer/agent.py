"""Sabrina — Prompt engineer. Deterministic translation of the frozen shot list.

Converts each Gate-3-approved shot (carrying Fabio's camera/light direction) into
model-ready Higgsfield prompts, selecting the model from config/models.json. No new
gate — a quick sanity glance only.
"""

from __future__ import annotations

from typing import Any

from agents.base import Agent, AgentContext, load_artifact, write_artifact
from core.models import ART_PROMPTS, ART_SHOTLIST

_BOOKEND_REFS = [
    "config/visual-refs/david-reference.png",
    "config/visual-refs/chronos-compass-reference.png",
]
_NEGATIVE = "modern objects, on-screen text, watermark, distorted faces, extra fingers, low quality"


def _pick_model(models: dict[str, Any], shot: dict[str, Any]) -> tuple[str, str]:
    overrides = models.get("shot_type_overrides", {})
    subj = f"{shot.get('visual_subject', '')} {shot.get('scene', '')}".lower()
    if shot.get("beat") == "Bookend":
        cat = "david_bookend"
    elif any(w in subj for w in ("map", "globe", "cartograph")):
        cat = "map_or_cartography"
    elif any(w in subj for w in ("temple", "library", "harbour", "harbor", "building", "city", "architect")):
        cat = "architecture"
    elif any(w in subj for w in ("crowd", "battle", "army", "soldiers")):
        cat = "battle_or_crowd"
    elif any(w in subj for w in ("dawn", "landscape", "establishing", "horizon", "sky")):
        cat = "landscape_or_establishing"
    else:
        cat = "artifact_closeup"
    chosen = overrides.get(cat)
    if chosen:
        return chosen, cat
    motion = models.get("motion", {})
    model = motion.get("chosen") or (motion.get("candidates") or ["Higgsfield"])[0]
    return model, cat


class PromptEngineerAgent(Agent):
    key = "prompt_engineer"

    def run(self, ctx: AgentContext) -> dict[str, Any]:
        ep = ctx.episode
        shotlist = load_artifact(ctx, ART_SHOTLIST)
        shots = shotlist["shots"]
        models = ctx.config.models

        prompts = []
        for shot in shots:
            model, category = _pick_model(models, shot)
            image_prompt = (
                f"{shot['visual_subject']}. Composition: {shot['composition']}. "
                f"Lighting: {shot['lighting']}. Mood: {shot['mood']}. "
                "Cinematic historical documentary, photorealistic, period-accurate, "
                "volumetric light, fine detail."
            )
            motion_prompt = (
                f"Animate with a {shot['camera_move'].lower()}; {shot['transition'].lower()}. "
                "Filmic, subtle motion; consistent lighting."
            )
            references = list(_BOOKEND_REFS) if shot.get("beat") == "Bookend" else []
            entry = {
                "shot_id": shot["id"],
                "model": model,
                "category": category,
                "image_prompt": image_prompt,
                "motion_prompt": motion_prompt,
                "negative": _NEGATIVE,
                "references": references,
            }
            prompts.append(entry)
            shot["prompts"] = [image_prompt, motion_prompt]

        write_artifact(ctx, key=ART_PROMPTS, rel_subpath="shotlist/prompts.json", data={"prompts": prompts})
        # Persist the prompts back onto the shot list for traceability.
        write_artifact(ctx, key=ART_SHOTLIST, rel_subpath="shotlist/shotlist.json", data={"shots": shots})
        ep.log(f"{self.badge}: {len(prompts)} prompt sets (1 per shot).")
        return {"agent": self.badge, "prompts": len(prompts)}


AGENT = PromptEngineerAgent()
