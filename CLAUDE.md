# CLAUDE.md — History Tube pipeline architecture

Guidance for Claude Code working in this repo. The **single source of truth** for
*intent* is [`docs/build-plan.md`](docs/build-plan.md); this file documents *how the
code realises it*. When they disagree, the build plan wins — fix the code or flag it.

## What this is
An agentic pipeline that takes a **History Tube** YouTube episode from idea to a
packaged video. Host: **David Hattenborg**, a historian-explorer from 2060 who appears
only in the open/close **bookends**; the body is historical AI b-roll. The soul is a
dramatic arc to an emotional, theatrical climax. **Agents propose; Fabio disposes** —
he owns angle, camera, light and packaging, expressed as **gates** the pipeline pauses
at.

## ⚠️ OS-agnostic mandate (non-negotiable)
Built on JJ's macOS, run on Fabio's **Windows**. **No `osascript`/AppleScript, ever.**
Pure Python (stdlib) + FFmpeg CLI + Whisper CLI, all invoked as argv lists via
`shutil.which` / `subprocess` (no shell strings). Paths use `pathlib`. Anything
mac-only is a bug.

## Architecture (hybrid)
1. **Python core** (this package) — the orchestrator, agents, adapters, editing
   scripts and tests. Runs end-to-end with **no keys/network/ffmpeg** via mock
   adapters. This is what the test suite covers.
2. **Claude skills** under `.claude/skills/` — thin wrappers around the LLM agents'
   `prompt.md` files, for driving them interactively inside Claude with MCPs.

The Python agent and its skill share one brain: `agents/<key>/prompt.md`.

### Layout
```
core/         status enum, gates, phase map, state machine, models, config, CLI, errors
adapters/     llm (mock|anthropic), higgsfield (mock|api), suno, store (local|notion), factory
orchestrator/ showrunner.py — Vitória: runs agents, advances status, pauses at gates
agents/<key>/ agent.py (+ prompt.md for LLM agents); registry + crew names in agents/
scripts/      ffmpeg_ops.py, whisper_ops.py, tooling.py — pure cmd-builders + runners
tests/        stdlib unittest, hermetic (temp repos, no binaries/network)
config/       channel-dna.md (constitution), models.json, voice-recipe.json, visual-refs/
episodes/     per-episode working folders (gitignored; regenerate with `cli.py demo`)
state/        local Notion mirror / cache (episodes.json gitignored)
docs/         build-plan.md (source of truth), notion-schema-spec.md, fabio-setup-checklist.md
```

### The crew (function → persona; names are Fabio's, set in `agents/crew.py`)
Vitória (Showrunner) · Deborah (Researcher) · Katusha (Concept) · Tainara (Critic) ·
Glesy (Scriptwriter) · Brenda (Director) · Sabrina (Prompt engineer) ·
Wanessa (Render) · Cleidiane (Editor) · Jucilene (Shorts).

### State machine + gates (`core/status.py`, `core/gates.py`, `core/phases.py`)
12 statuses `Idea → … → Published`. Five checkpoints, each gating exit from one status:
Gate 1 ← Researching, Gate 2 ← Scripting, Gate 3 ← Direction, Light Review ← Generating,
Gate 4 ← **Final-review**. The Showrunner advances a gated status only after approval,
and **never publishes on her own** (Scheduled → Published is an explicit `publish`).

## Run it
```
python cli.py demo            # build + walk the sample episode end-to-end (mock)
python cli.py init <slug> --title "..." --angle "..."
python cli.py run <slug>      # pauses at each gate
python cli.py approve <slug>  # approve the pending gate
python cli.py run <slug> --auto   # auto-approve every gate (dry-run)
python cli.py crew
```

## Test it
```
python -m unittest discover -s tests -t .     # stdlib, no deps
# or: pip install pytest && pytest
```
Tests must stay **hermetic**: no network, no ffmpeg/whisper, temp repos only. New
editing steps assert the **argv** of the command builder, never execute it.

## Backends (env vars; all default to mock/local)
`HT_LLM=mock|anthropic` · `HT_STORE=local|notion` · `HT_HIGGSFIELD=mock|api` ·
`HT_LLM_MODEL=<id>` (default `claude-opus-4-8`) · `HT_DRY_RUN=1`. Real adapters fail
loud (`AdapterNotConfigured`) until credentials/MCPs are wired — see
`docs/fabio-setup-checklist.md`.

## Conventions
- British English everywhere (channel + code comments).
- Keep voice and music as **separate stems**; the editor ducks music under narration.
- Don't bake new deps into the default path — the mock pipeline is stdlib-only.
- Touch only what the task needs; the build itself is gated (see build plan Section 9).

## Channel creative brief (always in scope)

Full detail in [`config/channel-dna.md`](config/channel-dna.md). Key rules reproduced here so they are always in context:

**The soul.** Historical narration that builds a dramatic arc to an emotional, theatrical climax. Viewers must *feel* history, not just learn it. Retention and packaging are first-class citizens.

**David Hattenborg.** Archaeologist-historian-explorer from 2060. Wise, curious, warm, optimistic — a storyteller, never a lecturer. Appears **only in the open/close bookends**; the body is historical AI b-roll. This is a deliberate architectural choice.

**Brand constants (every episode, verbatim).**
- Open: David activates Chronos Compass → *"Sit down. Here comes the story."*
- Close: *"The past is fixed. The future is not."* → Compass activates → *"I'll see you in the next story."*

**Locked voice.** Higgsfield / ElevenLabs Arthur preset — see `config/voice-recipe.json`. LOCKED 2026-06-20.

**Visual identity.**
- Thumbnail: David always present in **piano americano** (knees-up shot). Background varies; David is constant.
- Visual refs: `config/visual-refs/` (pending lock of david-reference and chronos-compass-reference).

**Hard rules — no exceptions.**
- **Strict British English** everywhere: `-ise`, `colour`, `behaviour`, `whilst`, `programme`, etc. No American spellings ever.
- **Thumbnail always features David** in piano americano.
- **Voice + music always separate stems** — never baked together before final mix.
- David never predicts the future as certainty; he explores possibilities.

**Video specs.**
- Format: 16:9 long-form, 12–15 min, 1080p, 24 fps.
- Shorts: 9:16 vertical, 60–90 s, from long-form assets.
- Captions: Whisper SRT.

**Writing style (narration).**
- Strong cold-open hook — start in motion, never "Today we're looking at…"
- Dramatic arc mandatory; emotional climax mandatory.
- Scene painting over fact listing. Weighted sentences. Short sentences at key beats.
- No padding, no passive voice, no hedge clusters, no clichés.

**Notion store.** Episodes DB: `d21dede219684be2832f161d14b483dd`. Set `NOTION_TOKEN` + `HT_STORE=notion`.
