# `episodes/` — Per-Episode Working Folders

This directory holds one working folder per History Tube episode. It is **local
scratch space on Fabio's Windows machine** — the place where a single episode is
assembled from idea to packaged video. The folder *structure* is documented and
tracked here; the *heavy media* it contains is git-ignored (see
[What is committed](#what-is-committed-and-what-is-not) below).

> Reference: Build Plan **Section 8 — Per-Episode Working Folders**. The full
> plan at `docs/build-plan.md` is the single source of truth; this README is a
> convenience summary of that section.

---

## One folder per episode

Each episode lives at:

```
episodes/<slug>/
```

`<slug>` **must match the `Slug` field of the episode's row in the Notion
Episodes DB**, exactly — same characters, same casing, no trailing variations.
The slug is the join key between Notion (where the episode is planned, reviewed
and dispositioned by Fabio) and the local filesystem (where the work happens).
If the two disagree, the orchestrator cannot reliably locate the working folder.

**Slug conventions**

- Lower-case, hyphen-separated, ASCII only (e.g. `fall-of-constantinople`,
  `chronos-and-the-antikythera`).
- No spaces, no slashes, no accented or special characters — the slug is also a
  folder name and must be valid on **both Windows and macOS**.
- One slug, one folder, one Notion row. Never reuse a slug.

---

## Subfolder layout

Every episode folder follows the same fixed layout:

```
episodes/<slug>/
├── research/      # Researcher output: sources, citations, fact ledger, dossier
├── script/        # Scriptwriter drafts + locked narration; David bookend lines
├── shotlist/      # Director shotlist + Prompt-Engineer per-shot prompts
├── renders/       # Generated AI b-roll clips (per shot)            [git-ignored]
├── audio/         # Voice stems + music stems — SEPARATE            [git-ignored]
│   ├── voice/     #   David VO + narration stems (one per segment)
│   └── music/     #   Score / ambience / sound-design stems
├── thumbnails/    # Thumbnail candidates + chosen packaging frame    [git-ignored]
└── final/         # Editor output: mixed, packaged master(s)         [git-ignored]
```

What each holds:

- **`research/`** — Everything the Researcher gathers and the Critic checks:
  primary/secondary sources, a citation list, and the fact ledger that backs the
  narration. Text-based; committed.
- **`script/`** — Scriptwriter drafts and the locked narration script, including
  the **David Hattenborg bookend lines** (open and close only — the body is
  b-roll). Text-based; committed.
- **`shotlist/`** — The Director's shotlist (one entry per shot, with Fabio's
  camera and lighting direction) and the Prompt-Engineer's resolved generation
  prompts per shot. Text/JSON; committed.
- **`renders/`** — The AI-generated historical b-roll clips, one set per shot.
  Heavy and regenerable; git-ignored.
- **`audio/`** — Voice and music kept as **separate stems** (see below). Heavy;
  git-ignored.
- **`thumbnails/`** — Candidate thumbnail frames and the final chosen frame for
  packaging. Heavy and regenerable; git-ignored.
- **`final/`** — The Editor's deliverable: the fully mixed, packaged master ready
  for Fabio's final call and upload. Heavy; git-ignored.

---

## Voice and music are separate stems — mixed only at edit time

`audio/voice/` and `audio/music/` are kept **strictly separate** for the whole
production. They are **never pre-mixed**. The two are brought together only at
**edit time**, where the Editor performs **ducking** — automatically dipping the
music under the narration so David's voice and the historical VO always sit on
top, then lifting it again in the gaps for the dramatic, theatrical swell.

Keeping the stems separate means the mix is **reproducible and re-tunable**: a
single line of VO can be re-rendered, or the ducking re-balanced, without
re-exporting or degrading the music bed. The mixed result lands in `final/`.

All mixing and ducking runs through the **OS-agnostic** scripts in
`scripts/` (pure Python/Node wrapping the **FFmpeg** and **Whisper** CLIs).
There is **no macOS-only tooling** anywhere in this pipeline — no `osascript`,
no AppleScript. Everything must run identically on Fabio's Windows machine.

---

## What is committed, and what is not

These folders hold **local working files**. The repository tracks the **folder
structure and the lightweight text artefacts**, not the heavy media.

Git-ignored (regenerable, large — kept local only):

- `episodes/**/renders/`
- `episodes/**/audio/`
- `episodes/**/thumbnails/`
- `episodes/**/final/`
- Media extensions anywhere: `*.mp4 *.mov *.mkv *.wav *.mp3 *.aac *.srt`,
  and generated stills `*.png *.jpg *.jpeg`
  (locked references under `config/visual-refs/` are the deliberate exception).

Committed (small, reviewable):

- `research/`, `script/`, `shotlist/` text and JSON artefacts.
- This README and any per-folder `.gitkeep` / `README.md` that preserve the
  empty structure.

> The git-ignore rules above are defined once in the repo-root `.gitignore`.
> If you change the subfolder names here, update `.gitignore` to match, or heavy
> media will start being committed.

---

## Ownership

Agents draft and propose into these folders; **Fabio disposes**. The angle and
thesis, the emotional beats, the camera and lighting direction, and the final
packaging call are Fabio's. These working folders exist to remove friction so
Fabio makes **more** creative decisions, not fewer.
