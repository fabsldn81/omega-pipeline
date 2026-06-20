# Locked Visual Refs — David Hattenborg + Chronos Compass

**Status: TO LOCK at build time** (see `docs/build-plan.md`, Section 11).
This folder is currently empty. Generate and audition the references in JJ's
Higgsfield workspace, then drop the final, chosen files here.

---

## What this folder is

This folder holds the **locked visual identity** that is reused, unchanged,
for **every episode bookend** — the open and the close where David appears on
screen. See `docs/build-plan.md`, **Section 6 (the bookends)** and
**Section 11 (locking the visual identity)**.

The body of each episode is historical AI b-roll and never shows David. He
appears **only at the open and the close**. That single constraint is what
makes a single locked reference workable: because David is on screen for only
two short moments per episode, we sidestep the AI character-consistency
problems that plague any character asked to appear continuously throughout a
video. Lock him once, reuse him every week.

---

## Contents

Two locked references live here:

### 1. David Hattenborg

Pick **one** of the following — not both:

- **A single fixed reference image** — `david-reference.png`.
  The simplest, most portable option: one canonical still of David, reused as
  the identity reference for every bookend generation.

- **A trained Higgsfield "Soul" identity** — if David is instead locked as a
  Higgsfield Soul (a trained, reusable character identity), do **not** commit a
  large model artefact. Instead record the Soul's id in a small text file:
  `david-soul.txt` (one line: the Soul id). The bookend generations then
  reference that id directly in Higgsfield.

### 2. Chronos Compass

- `chronos-compass-reference.png` — the locked reference for the signature
  artifact. One canonical look, reused everywhere it appears.

---

## Suggested filenames

| File | Purpose |
| --- | --- |
| `david-reference.png` | Single fixed reference image for David (Option A) |
| `david-soul.txt` | Higgsfield Soul id for David, if using a Soul instead (Option B) |
| `chronos-compass-reference.png` | Locked Chronos Compass reference |

Use **either** `david-reference.png` **or** `david-soul.txt`, depending on the
approach chosen at lock time.

---

## Why these images ARE version-controlled

This is the **one** folder whose images are intentionally committed to git.

The repo `.gitignore` ignores images globally (`*.png`, `*.jpg`, `*.jpeg`) so
that heavy, regenerable stills and thumbnails never bloat the repository — but
it then **negates** `config/visual-refs/**`. The net effect: the locked
references in this folder travel with the repo, so when it transfers to Fabio's
Windows machine he has David and the Chronos Compass already in hand, identical
to JJ's.

> These refs are the shared source of visual truth. Do not edit or replace them
> casually — relocking the identity is a deliberate, planned step (Section 11),
> not an incidental change.

---

## Locking procedure (at build time)

1. In **JJ's Higgsfield** workspace, generate and audition candidates for David
   and for the Chronos Compass.
2. With Fabio's sign-off (Fabio disposes; he owns the final look), choose the
   canonical references.
3. Drop the final files into this folder using the filenames above
   (`david-reference.png` **or** `david-soul.txt`; `chronos-compass-reference.png`).
4. Commit. The negated `.gitignore` rule carries them to Fabio with the repo.

Cross-references: `docs/build-plan.md` Section 6 (bookends) and Section 11
(locking the visual identity).
