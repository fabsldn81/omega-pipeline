# Glesy — Scriptwriter

Implemented in [`agents/scriptwriter/agent.py`](agent.py). An LLM agent: its brain is
[`prompt.md`](prompt.md), shared with the `glesy-scriptwriter` Claude skill.

## What it does

**DOES** — writes the full theatrical British narration in David Hattenborg's voice: a
cold-open hook (no throat-clear), a dramatic arc built to an emotional, theatrical
climax, and the brand-constant bookends placed verbatim. David appears only at the open
and close; the body is narration over historical b-roll. Times the narration to the
episode's target length and honours David's stance — he explores possibilities, he never
predicts the future as certainty.

**PRODUCES**
- `script/script.json` — structured narration: `hook`, `open_bookend`, `body`,
  `close_bookend`, `estimated_seconds`.
- `script/script.md` — a readable script for review (cold open, bookends, body, runtime).

## Where it sits

Phase **Scripting**. It reads the locked outline (`research/outline.json`) and renders it
into narration, then **feeds Gate 2** — the script-lock checkpoint on exit from
*Scripting* into *Script-locked*. Gate 2 is a Fabio decision, not an automated pass:
Glesy drafts and proposes; Fabio disposes. Nothing downstream (direction, prompts,
renders, edit) proceeds until Gate 2 closes, because everything after it is built on this
script — a change past the gate is a re-render, not an edit.

## How it runs

A Python module under the agent registry. It is **not invoked by hand**: the Showrunner
(Vitória) runs it when an episode reaches the *Scripting* status, then pauses at Gate 2.
`ScriptwriterAgent.run(ctx)` reads the channel DNA (`ctx.channel_dna`, prepended to the
prompt) plus the outline, calls the LLM, validates the required keys, writes both
artifacts, and logs the locked estimate. Interactively, drive the same brain through the
`glesy-scriptwriter` skill.

## Files

- [`agent.py`](agent.py) — `ScriptwriterAgent` (`key = "scriptwriter"`), the Python implementation.
- [`prompt.md`](prompt.md) — the shared brain for the Python agent and the skill.
- Claude skill: `glesy-scriptwriter` — the thin interactive wrapper around `prompt.md`.
