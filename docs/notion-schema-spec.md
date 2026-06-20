# Notion Workspace — Build Specification

> **⚠️ BUILD THIS IN FABIO'S NOTION, AT SETUP TIME — NOT NOW, NOT IN JJ'S WORKSPACE.**
> This document is a *specification*, not a live build. The databases below are to be created by Claude Code **inside Fabio's Notion** once **Fabio's Notion MCP is connected** (see Build G and `docs/fabio-setup-checklist.md`). Do **not** create any of these in JJ's workspace, and do **not** create them now. This file defines the target schema; the live build is a one-off setup step on Fabio's side.

This schema mirrors the single source of truth — `docs/build-plan.md`, Section 5 — adapted for video production. The episode `Status` field is the spine the Showrunner reads to know which phase each episode is in and where to pause for Fabio (see `docs/build-plan.md` Sections 3 and 4).

Each property below carries a **suggested Notion property type** in parentheses. Treat types as recommendations to confirm at build time, not hard constraints — but keep the `Status` enum and its order exactly as written.

---

## DB: Episodes *(master)*

The control table. One row per episode; its `Status` drives the whole pipeline.

| Property | Suggested type | Notes |
|---|---|---|
| Title | **Title** | Working title; topic-first, character-second (David is brand, not search term). |
| Slug | **Text** | Filesystem-safe; matches the local `episodes/<slug>/` working folder on Fabio's machine. |
| Status | **Status** (or **Select**) | Exact enum + order below. The Showrunner advances this only after the relevant gate is approved. |
| Topic / Civilisation | **Text** or **Select** | Use Select once a stable taxonomy emerges; Text is fine at first. |
| Angle / Thesis | **Text** | Fabio's spark — the creative core. Set at Phase 0. |
| Target length | **Number** or **Text** | Number (minutes) preferred; Text if a range is wanted (e.g. "12–15 min"). |
| Publish date | **Date** | Planned or scheduled upload date. |
| Research Dossiers | **Relation** → Research Dossiers | |
| Shot List | **Relation** → Shot List / Storyboard | |
| Media Assets | **Relation** → Media Assets | |
| Packaging | **Relation** → Packaging | |
| Views | **Number** | Post-publication; filled later. |
| Watch time | **Number** | Post-publication; filled later. |
| CTR | **Number** | Post-publication; filled later (per-cent). |
| Avg. retention | **Number** | Post-publication; filled later (per-cent). |

### Episodes — Status enum (exact, in order)

Reproduce verbatim, in this order:

1. Idea
2. Researching
3. Packaging-locked
4. Scripting
5. Script-locked
6. Direction
7. Direction-locked
8. Generating
9. Editing
10. Final-review
11. Scheduled
12. Published

---

## DB: Topic Pool

Demand-validated candidate topics the Showrunner can surface; the spark itself stays Fabio's (Phase 0).

| Property | Suggested type | Notes |
|---|---|---|
| Candidate topic | **Title** | |
| Demand signal | **Text** | Notes from YouTube search autocomplete / Google Trends / competitor scan. Directional, not precise keyword volumes. |
| Competition notes | **Text** | Comparable history channels' top performers — titles + view counts. |
| Status | **Select** | Options: `New`, `Approved`, `Parked`, `Done`. |
| Episodes | **Relation** → Episodes | Links a topic to the episode it spawned. |

---

## DB: Research Dossiers

The Researcher's output, one dossier per episode. Every claim must map to a source.

| Property | Suggested type | Notes |
|---|---|---|
| Per-episode facts | **Text** | |
| Timeline | **Text** | |
| Key figures | **Text** | |
| Hooks | **Text** | The emotional hooks that feed the dramatic arc. |
| Controversies / landmines | **Text** | Sensitive-topic flags for the critic gate. |
| Source ledger | **Text** (with **URL** where one claim = one row) | Every claim → a source URL. If modelled as one claim per row in a sub-table, use a **URL** property; otherwise a single rich-text ledger. |
| Episodes | **Relation** → Episodes | |

---

## DB: Shot List / Storyboard *(the spine of Fabio's direction)*

One row **per shot**. This is where Fabio exercises Gate 3 — editing camera and light shot by shot.

| Property | Suggested type | Notes |
|---|---|---|
| Scene | **Text** or **Select** | |
| Beat | **Text** | |
| Visual subject | **Text** | |
| Composition | **Text** | |
| Camera move | **Text** | **Fabio's domain** — proposed by the Director-assistant, owned by Fabio. |
| Lighting | **Text** | **Fabio's domain** — same. |
| Mood | **Text** or **Select** | |
| Transition | **Text** or **Select** | |
| Prompt(s) | **Text** | Model-ready prompt(s) from the Prompt engineer, carrying Fabio's direction. |
| Chosen take | **Text** or **Relation** → Media Assets | Set at Light Review. Relation preferred so the take points at its asset row. |
| Render status | **Select** | Suggested options: `Pending`, `Rendering`, `Rendered`, `Re-roll`, `Selected`. |
| Episodes | **Relation** → Episodes | |

---

## DB: Media Assets

Every generated artifact — clips, voice stems, music stems, thumbnails. Voice and music are **always separate stems** (never baked together).

| Property | Suggested type | Notes |
|---|---|---|
| Name | **Title** | Asset identifier. |
| Type | **Select** | Suggested options: `Clip`, `Voice stem`, `Music stem`, `Thumbnail`. |
| Status | **Select** | Options: `Raw`, `Selected`, `Final`. |
| Local path on Fabio's machine | **Text** | Path under `episodes/<slug>/...` on Fabio's Windows machine. |
| Episodes | **Relation** → Episodes | |
| Shots | **Relation** → Shot List / Storyboard | Links an asset to the shot it belongs to. |

---

## DB: Packaging

The Gate 1 (concepts) and Gate 4 (final confirmation) packaging record, one row per episode.

| Property | Suggested type | Notes |
|---|---|---|
| Title variants | **Text** | Several candidates generated at Gate 1. |
| Thumbnail concepts / files | **Files** (and/or **Text**) | Files for actual images; Text for concept descriptions. |
| Description | **Text** | |
| Tags | **Multi-select** | |
| Chapters | **Text** | |
| End-screen plan | **Text** | |
| Episodes | **Relation** → Episodes | |

---

## DB: Performance Snapshot — **DEFERRED (Phase 2)**

> **Do not build this at setup time.** Intended for a weekly analytics pull. For a brand-new channel, **manual review in YouTube Studio is fine at first**. Build this only in Phase 2, once there is enough traffic to justify automated snapshots. (Early post-publication metrics live on the Episodes row in the meantime.)

---

## Status → Gate map

The Showrunner advances `Status` only after the authorising gate is approved. Gates are explicit human checkpoints: the Showrunner posts the artifact and stops until Fabio responds (`docs/build-plan.md` Section 4).

| From Status | Authorising gate | Advances to |
|---|---|---|
| Idea | *(no gate — Phase 0 brainstorm, Fabio leads)* | Researching |
| Researching | **Gate 1 — Topic + Packaging** (angle, title(s), thumbnail concept, hook) | Packaging-locked |
| Packaging-locked | *(no gate — Phases 2–3: concept + adversarial review run automatically)* | Scripting |
| Scripting | **Gate 2 — Script** (final script frozen) | Script-locked |
| Script-locked | *(no gate — Phase 5 produces the draft shot list for Fabio)* | Direction |
| Direction | **Gate 3 — Direction** (camera + light per shot — **Fabio's domain**) | Direction-locked |
| Direction-locked | *(no gate — Phase 6 prompt generation is a deterministic translation; quick sanity glance only)* | Generating |
| Generating | **Light Review — Take selection** (best take per shot; flag re-rolls) | Editing |
| Editing | *(no gate — the Editor produces the cut; Fabio's review happens at the next status)* | Final-review |
| Final-review | **Gate 4 — Final cut + publish** (the video + final packaging) | Scheduled |
| Scheduled | *(no gate — publication per the scheduled date)* | Published |

Gate reference (full detail in `docs/build-plan.md` Section 4):

- **Gate 1 — Topic + Packaging** — protects against expensive work on a weak idea or weak packaging. Nothing expensive happens before this gate.
- **Gate 2 — Script** — freezes the foundation everything downstream is built on.
- **Gate 3 — Direction** — Fabio's creative ownership; camera + light per shot, the one thing he never delegates.
- **Light Review — Takes** — quality control without heavy process (a contact-sheet review).
- **Gate 4 — Final cut** — nothing reaches the public unapproved.

---

## How to build

Build this **via the Notion MCP, in Fabio's workspace, at setup time** — once Fabio's Notion MCP is connected (Build G / `docs/fabio-setup-checklist.md`). Suggested order:

1. Create the seven databases above (skip **Performance Snapshot** — it is deferred to Phase 2).
2. Create the **Episodes** `Status` field first, with the twelve options in the exact order listed.
3. Add the remaining properties per database, using the suggested types.
4. Wire the **Relations** last, so both sides exist before linking (Episodes ↔ Research Dossiers, Shot List, Media Assets, Packaging; Media Assets ↔ Shots).
5. Confirm with Fabio before treating the workspace as live.

Do **not** create or mirror any of this in JJ's Notion.
