# Sabrina — Prompt engineer

Implemented in `agents/prompt_engineer/agent.py` (`PromptEngineerAgent`, crew key `prompt_engineer`).

## Identity

Sabrina is the **Prompt engineer** — Phase 6 of the History Tube pipeline. She is **deterministic** (no LLM): she takes the frozen, Fabio-approved shot list and converts each shot into model-ready Higgsfield prompts. She does not interpret; she translates. The creative decisions — angle, camera, light — are already locked by Fabio at Gate 3, so there is nothing for her to invent.

## What it does

**DOES** — DETERMINISTIC (no LLM). For each shot in the locked shot list she:

- builds an **image prompt** from the shot's `visual_subject`, `composition`, `lighting` and `mood`, plus a fixed cinematic-documentary style suffix;
- builds a **motion prompt** from the shot's `camera_move` and `transition`;
- attaches a shared **negative** prompt (modern objects, on-screen text, watermark, distorted faces, extra fingers, low quality);
- **selects the model** per shot from [`config/models.json`](../../config/models.json) — using `shot_type_overrides` when set, otherwise the default `motion` model. The category is inferred from the shot (bookend, map/cartography, architecture, battle/crowd, landscape/establishing, or artifact close-up);
- attaches the locked **David / Chronos Compass** reference images to **bookend** shots (`beat == "Bookend"`), so the host and series motif stay on-model across episodes.

**PRODUCES**

- `episodes/<slug>/shotlist/prompts.json` — one prompt set per shot (`shot_id`, `model`, `category`, `image_prompt`, `motion_prompt`, `negative`, `references`);
- the prompts written **back onto the shot list** (`shotlist/shotlist.json` — each shot gains a `prompts` field) for traceability.

No new gate: a quick sanity glance only. No `prompt.md` and no Claude skill — Sabrina is code, not an LLM agent.

## Where it sits

Phase 6 — **Direction-locked → Generating**. Sabrina runs *after* Gate 3 (the Director's shot list lock, Fabio's domain) and feeds the render stage (Wanessa) and ultimately the **Light Review** gate at the exit of Generating. She adds **no gate** of her own.

```
… → Director → [GATE 3: Shot list lock] → SABRINA (Prompt engineer) → Render → [Light Review] → …
```

## How it runs

A Python module, invoked by the Showrunner (Vitória) when the episode reaches the `Direction-locked` status — there is no standalone CLI step. Being deterministic, the same shot list always yields the same prompts.

```python
from agents.prompt_engineer.agent import AGENT
AGENT.run(ctx)  # ctx: AgentContext for the episode
```

## Files

- `agents/prompt_engineer/agent.py` — the implementation; the shared "brain" is the code itself.
- No `prompt.md`, no Claude skill: deterministic code, not an LLM agent.

---

*British English throughout. A faithful translation of a frozen, Fabio-directed shot list into Higgsfield-ready prompts.*
