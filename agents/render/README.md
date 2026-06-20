# Wanessa — Render orchestrator.

Implemented in [`agents/render/agent.py`](agent.py).

## Identity

Wanessa is the Render orchestrator (function key `render`) — where the locked script
becomes footage and sound. She is a **code** agent, not an LLM agent: deterministic
control flow plus media adapters. There is no `prompt.md` and no Claude skill, because
there is no brain to share — only orchestration.

## What it does

**DOES** — DETERMINISTIC + adapters.
- Generates the **clips** via the Higgsfield adapter — one job per shot, driven by the
  Phase 6 prompt set, which already carries Fabio's Gate 3 camera, light, and composition.
- Generates the **voice-over** via Higgsfield TTS using David's recipe
  (`ctx.config.voice_recipe`). The locked script is the text; the recipe is the delivery.
- Ingests the **manually-made Suno music** — Fabio makes it by hand and drops it into the
  episode folder. Wanessa ingests and registers it; she does not call Suno or generate music.
  When no track is present, a placeholder stem is registered.
- Renders **multiple takes per shot** (`HT_TAKES`, default 1) so the Light Review has real
  choice; take 1 defaults to `Selected`, the rest to `Raw`.
- Keeps **voice and music as SEPARATE stems** — nothing is baked together.

**PRODUCES** — clip / voice / music `MediaAsset`s.
- Clip takes under `episodes/<slug>/renders/`.
- Voice stem under `episodes/<slug>/audio/voice/`.
- Music stem(s) under `episodes/<slug>/audio/music/`.
- Updates `shotlist/shotlist.json` with each shot's `render_status` and a default `chosen_take`.

## Where it sits

- **Phase 7 — Generating** in the pipeline (Idea → … → Direction-locked → **Generating** →
  Editing → …).
- **Feeds the Light Review** (exit Generating) — the one *light* checkpoint, where **Fabio
  picks the best take per shot and flags re-rolls**. Wanessa presents the takes; she never selects.
- Downstream of the Light Review, the Editor (Cleidiane) assembles the chosen takes to VO
  timing and layers the separate stems.

## How it runs

Python module: `agents/render/agent.py` exposes `AGENT = RenderAgent()` (`key = "render"`).
It runs when the Showrunner (Vitória) advances an episode to the **Generating** status — she
orchestrates the call; Wanessa never advances status and never publishes on her own. Set
`HT_TAKES` to render more takes per shot; with `HT_HIGGSFIELD=mock` clips and voice are
written as text stubs for hermetic dry runs.

## Files

- [`agent.py`](agent.py) — the implementation (`RenderAgent`).
- No `prompt.md`, no Claude skill — Wanessa is deterministic code with no shared LLM brain.

---

*OS-agnostic: pure Python plus the Higgsfield/Suno adapters, no `osascript`/AppleScript —
runs on Fabio's Windows machine. British English throughout. Soul first.*
