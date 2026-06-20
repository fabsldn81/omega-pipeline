# Katusha — Concept writer

Implemented in `agents/concept/agent.py` (`ConceptAgent`, key `concept`). LLM agent.

## What it does

**DOES** — shapes Deborah's dossier and Fabio's angle into a **dramatic arc**: the
beats, the build, the emotional and theatrical climax, and the speculative coda
("what comes next", explored as possibility, never foretold). Structure serves the
arc — it is *not* forced into four acts. The climax is mandatory; the act count is
not. Reads the Channel DNA (`config/channel-dna.md`) and keeps its soul — making
viewers *feel* history — at the centre. It respects the dossier's controversies and
does not build the arc on a disputed claim.

**PRODUCES** — `episodes/<slug>/research/outline.json`, one JSON object with the keys
`logline`, `beats`, `climax`, `what_next`, `structure_notes`.

## Where it sits

Phase 2 — **Concept / Outline + Adversarial review** (status `Packaging-locked`).
Katusha runs alongside Tainara (the critic): Katusha shapes the arc, Tainara attacks
it, Katusha revises. There is **no hard gate** at this phase — Fabio first sees the
result downstream at **Gate 2** (exit `Scripting`), where the locked script is judged.
The outline feeds the scriptwriter (Glesy) in the next phase.

## How it runs

It is not invoked by hand. The Showrunner (Vitória) runs it automatically when the
episode reaches `Packaging-locked`:

```
python cli.py run <slug>      # advances the episode; Katusha fires at its phase
```

It loads `research/dossier.json` and `episode.angle`, prepends the Channel DNA to its
prompt, asks the LLM for a JSON outline, validates the required keys, then writes
`research/outline.json` and logs the beat count and chosen climax. Runs fully under
the mock LLM adapter — no keys, no network.

## Files

- `agent.py` — `ConceptAgent`; the registered Python implementation.
- `prompt.md` — the shared brain: outline spec, rules and theatrical register.
- `__init__.py` — module marker.
- Skill: `katusha-concept` — the thin Claude wrapper around `prompt.md` for
  interactive use. The Python agent and the skill share the one `prompt.md`.
