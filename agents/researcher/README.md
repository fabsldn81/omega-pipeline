# Deborah — Researcher

**Implemented** in [`agents/researcher/agent.py`](agent.py) (`ResearcherAgent`, key `researcher`).
LLM agent: shares one brain with its Claude skill via [`prompt.md`](prompt.md).

## What it does

**DOES** — from the episode topic and Fabio's angle, gathers the raw historical
material: facts, timeline, key figures, emotional hooks, and controversies/landmines.
Runs **free, YouTube-native demand validation** (search autocomplete, Google Trends
shape, comparable-channel titles + view counts, trending anniversaries) — directional
signals, never presented as hard keyword volumes. It surfaces material; it does not
pick the topic, rank candidates, or choose the angle — those are Fabio's.

**PRODUCES** —
- `research/dossier.json` — `facts`, `timeline`, `key_figures`, `hooks`,
  `controversies`, a `sources` **claim → URL source ledger** (every factual claim
  maps to a checkable URL), and `demand_signal`.
- `research/packaging.json` — a packaging draft: `title_variants` (topic-first),
  `thumbnail_concepts`, `hook`, `description`, `tags`, `chapters`, `end_screen`.

Required keys on both artifacts are enforced at runtime (`require_keys`); a missing
key fails loud rather than passing a half-built dossier downstream.

## Where it sits

- **Phase 1 — Research**, status `Researching`.
- **Feeds Gate 1 — Topic + Packaging lock.** Nothing expensive happens before Fabio
  approves the angle, title(s), thumbnail concept and hook, so the dossier and
  packaging draft are the evidence he decides on. Hands off to the Concept writer
  (Katusha, Phase 2).

## How it runs

A Python module registered under key `researcher`. The Showrunner (Vitória) invokes
it when an episode reaches `Researching`, then pauses at Gate 1 for approval — there
is no standalone CLI verb for Deborah; she runs as a step of `python cli.py run <slug>`.

Before acting she reads [`config/channel-dna.md`](../../config/channel-dna.md) — it is
prepended to the prompt as the system message, so every hook and controversy is framed
in service of the dramatic arc. OS-agnostic: pure Python, no `osascript`.

## Files

- [`agent.py`](agent.py) — `ResearcherAgent`, the implementation.
- [`prompt.md`](prompt.md) — the shared brain (Python agent + Claude skill).
- Claude skill **`deborah-researcher`** (under `.claude/skills/`) — thin interactive
  wrapper around the same `prompt.md`.
