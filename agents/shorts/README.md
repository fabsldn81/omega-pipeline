# Jucilene — Shorts cutter.

Implemented in [`agents/shorts/agent.py`](agent.py). **DETERMINISTIC** — no LLM, no
`prompt.md`, no Claude skill. It is code, not a brain.

## What it does

- **DOES:** Extracts **1–2 vertical 9:16 Shorts** from the finished long-form by
  driving [`scripts/ffmpeg_ops.reframe_vertical_cmd`](../../scripts/ffmpeg_ops.py)
  (reframe to 1080×1920). It selects standalone moments — the myth-buster cold open
  (`hook`) and the emotional `climax` — re-frames existing assets, and carries the cut
  audio across. No new b-roll, narration, or David bookends are generated. This is the
  channel's **aggressive-growth lever**: low marginal cost because every asset already
  exists in the rendered episode.
- **PRODUCES:** `final/shorts/shorts_plan.json` (per-Short angle, source, reframe argv,
  caption) plus one short `MediaAsset` per clip registered on the episode.

## Where it sits

**Phase 9** — the final agent in the pipeline. It runs off **Published**: the long-form
must already be packaged and live before Shorts are cut from it. It is strictly
downstream and never alters the long-form master. Output feeds **Fabio**, who owns the
final selection and the packaging/publishing call — agents propose, Fabio disposes.

## How it runs

A Python module (`AGENT = ShortsAgent()`, `key = "shorts"`). It is invoked by the
Showrunner (Vitória) when the episode reaches its status — there is no standalone CLI
entry point. It runs end-to-end under the mock pipeline with no keys, network, or
FFmpeg: the reframe command is built as an **argv list** and recorded in the plan, not
executed. The crew name comes from [`agents/crew.py`](../crew.py).

## Files

- [`agent.py`](agent.py) — the `ShortsAgent` implementation.
- **No `prompt.md` and no Claude skill** — this is a deterministic editing agent, so it
  has no shared LLM brain to wrap.
