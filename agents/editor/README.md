# Cleidiane — Editor

Implemented in [`agents/editor/agent.py`](agent.py) as `EditorAgent` (`key = "editor"`).

This is a **deterministic** agent: it has **no `prompt.md` and no Claude skill** — it is code, not an LLM. There is nothing to reason about; assembly is mechanical and fully scripted.

## What it does

**DOES** — deterministic FFmpeg/Whisper assembly. From the locked shot list and the selected render clips, it builds the finished cut:

- **Assembles** the selected clips (one `Selected` clip per shot, in shot order) to the voice-over timing — bookend shots are first/last in the concat, so the David open/close framing wraps the body.
- **Ducks** the music stem under the narration, with fades.
- **Normalises** loudness to **−14 LUFS** integrated (two-pass `loudnorm`, YouTube reference).
- **Captions** via Whisper SRT; **fades and overlays**; the **bookend template** open/close.
- Builds a **full, ordered command plan** and writes it to `final/edit_plan.json` — every step records its `argv`, whether it `executed`, and a note.
- Writes **real captions** to `final/captions.srt` immediately (dependency-free, derived from the script body), independent of whether ffmpeg runs.
- **Executes ffmpeg only with real media present** — i.e. when `higgsfield_backend == "api"` and not a dry-run. Otherwise it plans the exact commands without running them, and still emits a mock final placeholder.

**PRODUCES** — the cut for **Gate 4**: `final/edit_plan.json`, `final/captions.srt`, and a `final` Media Asset (status `Final`).

## Where it sits

Phase 8, status **Editing**. Runs after Render (Light Review picks takes) and feeds **Gate 4** (exit Final-review), where Fabio approves the cut or gives notes. The Showrunner never publishes on her own.

## How it runs

A Python module — there is no separate CLI entry. The Showrunner ([`orchestrator/showrunner.py`](../../orchestrator/showrunner.py)) invokes `EditorAgent` when the episode reaches the **Editing** status, via `python cli.py run <slug>`. It reads `shotlist` + `script`, writes the edit plan and captions, and advances toward Gate 4.

## Files

- [`agent.py`](agent.py) — `EditorAgent`, the deterministic assembler (this is the implementation).
- No `prompt.md` and no Claude skill — Cleidiane is code, not an LLM agent.

Media command-builders live in [`scripts/ffmpeg_ops.py`](../../scripts/ffmpeg_ops.py) and [`scripts/whisper_ops.py`](../../scripts/whisper_ops.py); `agent.py` orchestrates them.
