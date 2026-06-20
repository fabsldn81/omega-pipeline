# `state/` — Local State Mirror / Cache

> **Build status:** Stub folder for **Build B** (the Showrunner / orchestrator). Nothing reads or writes here yet. This README defines the contract so Build B can fill it in.

## What this folder is

`state/` is a **lightweight local reflection** of the pipeline's status, kept on whichever machine is running the Showrunner. It exists for one reason: to let the orchestrator answer "where is each episode, and what's already been done?" quickly and offline, without a network round-trip to Notion on every step.

It is a **convenience mirror and a scratch cache** — never a system of record.

## Source of truth

**Notion is the source of truth for pipeline status.** Specifically, the **`Episodes.Status`** field (see `docs/notion-schema-spec.md`) is authoritative. Anything in `state/` is a derived copy that may be stale.

Rules of the road:

- On any disagreement, **Notion wins**. The Showrunner reconciles by re-reading Notion and overwriting the local mirror — never the other way round.
- The mirror is **rebuildable from scratch** at any time. Deleting `state/` must never lose real work; at worst it forces a re-sync from Notion.
- Treat `state/` as **disposable**. If it looks corrupt, delete it and let the Showrunner repopulate.

## What lives here (planned, Build B)

| Path | Purpose | Tracked in git? |
| --- | --- | --- |
| `state/*.local.json` | Mirror of Notion pipeline state (e.g. episode list, per-episode `Status`, last-synced timestamps). | **No** — gitignored |
| `state/cache/` | Derived caches: research lookups, prompt/render intermediates, anything regenerable. | **No** — gitignored |
| `state/README.md` | This file. | Yes |

Exact filenames and JSON shapes are defined by the Showrunner in Build B and documented in `docs/build-plan.md` (Section 8). This stub deliberately does not lock them.

## Git policy

Contents are **gitignored** so machine-local state never travels through the repo. The patterns already live in the repo root `.gitignore`:

```gitignore
# --- Local state / cache (folder structure kept via README) ---
state/cache/
state/*.local.json
```

Only this `README.md` is committed, so the empty folder survives a clone. Per-machine state stays per-machine.

## OS-agnostic note

This folder is plain JSON on the local filesystem and carries **no platform assumptions**. Development happens on macOS (JJ); production runs on Windows (Fabio). Build B must read and write `state/` using pure Python/Node path handling (e.g. `pathlib` / `path.join`) — **no hard-coded path separators, no macOS-only tooling, no `osascript`/AppleScript anywhere**. Anything mac-only here is a bug.

## Relationship to the rest of the pipeline

- The **Showrunner** (`orchestrator/`, Build B) owns this folder: it syncs from Notion, reads the mirror to decide the next step, and writes back the cache.
- Per-episode working files (scripts, renders, audio, final cuts) do **not** live here — they live under `episodes/`.
- Locked references (David, the Chronos Compass) do **not** live here — they live under `config/visual-refs/`.

See `docs/build-plan.md` (the single source of truth) for the full picture.
