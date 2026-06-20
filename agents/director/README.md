# Brenda — Director-assistant

Brenda is the **Director-assistant**. She is implemented in [`agents/director/agent.py`](agent.py) (`DirectorAgent`, key `director`).

## Identity

An LLM agent. Brenda takes the **locked script** and breaks it down into a shot list, **proposing** the look of every shot — a draft for Fabio to react to. She serves direction; she never owns it. **Agents propose; Fabio disposes.**

## What it does

**DOES** — splits the locked script into a clean **scenes → beats → shots** hierarchy and, per shot, **proposes** the visual subject, composition, camera move, lighting, mood and transition. David appears **only** in the open/close **Bookend** shots (their `beat` is marked `"Bookend"`); every other shot is historical b-roll, which sidesteps AI character-consistency problems. She reads [`config/channel-dna.md`](../../config/channel-dna.md) first so every shot serves the soul — a dramatic arc to an emotional, theatrical climax.

**PRODUCES** — `episodes/<slug>/shotlist/shotlist.json`, a **draft** shot list for Fabio. Each shot also carries `prompts`, `chosen_take` and `render_status` placeholders for the downstream stages.

## Where it sits

Phase: **Direction** (the first step past Gate 2 — Script lock). Brenda only ever runs on a **frozen script**. Her draft then feeds **Gate 3 — Direction lock**, which is **Fabio's domain**: he edits camera + light shot by shot, then locks. Nothing downstream (Sabrina's prompts, render, edit) proceeds until Gate 3 closes.

```
Scripting → [Gate 2] → Direction (BRENDA) → [Gate 3 — Fabio] → Generating → …
```

## How it runs

A Python module run by the **Showrunner** (Vitória) when she reaches the **Direction** status — there is no separate CLI for it. Drive the whole episode with `python cli.py run <slug>`; the Showrunner pauses at Gate 3 for Fabio. The same `prompt.md` brain is also wrapped by the **`brenda-director`** Claude skill for interactive use.

## Files

- [`agent.py`](agent.py) — `DirectorAgent`; reads `ART_SCRIPT`, writes `ART_SHOTLIST`.
- [`prompt.md`](prompt.md) — the shared brain for both the Python agent and the skill.
- `brenda-director` Claude skill — thin interactive wrapper around the same `prompt.md`.
