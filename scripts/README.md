# scripts/ — OS-Agnostic Editing & Utility Scripts

> **Status: IMPLEMENTED (Build E).** Command builders + runners live in
> [`ffmpeg_ops.py`](ffmpeg_ops.py), [`whisper_ops.py`](whisper_ops.py) and
> [`tooling.py`](tooling.py). Each `*_cmd` function is **pure** — it returns an argv list and
> runs nothing, so the test suite verifies the exact invocation without ffmpeg/whisper
> installed; the `run`/`run_cmd` wrappers execute only when the binary is on PATH, else they
> return the planned command. See [`docs/build-plan.md`](../docs/build-plan.md) Sections 6 and 8.

This folder holds the editing and utility scripts that the **Editor** sub-agent ([`agents/editor/`](../agents/editor/)) and **Shorts cutter** ([`agents/shorts/`](../agents/shorts/)) call to turn raw renders, voice stems and music stems into the finished cut and its Shorts spin-offs.

These scripts are thin **wrappers around the FFmpeg and Whisper command-line tools**. They exist so that the same command produces an identical result on JJ's macOS dev machine and on Fabio's Windows machine — the editor logic lives here once, not duplicated per platform.

---

## ⚠️ Hard rule — OS-agnostic mandate

> **Pure Python/Node + FFmpeg CLI + Whisper CLI. Must run on Windows. NO `osascript` / AppleScript. No mac-only dependencies of any kind.**

Development happens on JJ's macOS machine but everything transfers to Fabio's **Windows** machine via this repo (Build G). Therefore:

- **No** `osascript`, AppleScript, `say`, `afplay`, `sips`, or any other macOS-only binary.
- **No** shell-isms that only work in `zsh`/`bash` — invoke FFmpeg/Whisper as subprocesses from Python or Node, never from a `.sh` that assumes a POSIX shell.
- **No** hard-coded POSIX paths or `/`-only path joins — use the language's path library (`pathlib` / `path.join`) so paths resolve on Windows too.
- FFmpeg and Whisper must be **invoked as CLI subprocesses** (resolved from `PATH`), never via a platform-specific library binding.
- Anything that only works on a Mac is a **bug, not a feature.**

Every script in this folder is expected to behave identically on macOS (dev) and Windows (Fabio). Cross-platform parity is verified at the Build G checkpoint.

---

## 🔊 Hard rule — audio stems are always separate

> **Voice and music are NEVER baked together.** They are separate stems, mixed only at edit time.

- The render stage delivers **voice stems** and **music stems** as distinct files (see [`agents/render/`](../agents/render/) and the `audio/` folder in each episode working directory).
- Mixing happens **only** here, at edit time: music is **ducked** under narration (drops in level when David speaks) and **fades** are applied.
- A clip whose audio arrives pre-mixed (voice + music welded into one track) is a **broken edit** — it cannot be re-balanced, re-ducked, or re-timed. Reject it upstream.

---

## Planned scripts

Each script below is **to build in Build E**. Names are indicative; one-line purpose each.

| Script | Purpose | Wraps |
|---|---|---|
| **assembly** | Cut and concatenate the chosen render takes to the voice-over timing, producing the picture spine of the cut. | FFmpeg |
| **loudness** | Two-pass loudness normalisation of the final mix, target **≈ −14 LUFS** (YouTube reference). | FFmpeg (`loudnorm`) |
| **captions** | Generate a Whisper SRT from the narration, then burn-in or attach the captions. | Whisper CLI + FFmpeg |
| **ducking** | Mix the **separate** voice and music stems — sidechain or volume-automate the music down under narration, with fades in/out. | FFmpeg |
| **overlays** | Apply on-screen overlays and the **open/close bookend template** (the David open and close, per Channel DNA). | FFmpeg |
| **shorts-reframe** | Re-frame the finished long-form to vertical **9:16** for 1–2 Shorts (Phase 9 growth lever). | FFmpeg |

### Notes on individual scripts

- **assembly** — driven by the locked shot list and the selected takes; cuts to the voice-over timing so picture follows narration, not the reverse.
- **loudness** — two-pass (`loudnorm` analyse → apply) for accurate, consistent loudness rather than a single-pass approximation; ≈ −14 LUFS integrated.
- **captions** — Whisper produces the SRT from the voice stem; the same script can either burn the captions into the picture or attach them as a soft subtitle track.
- **ducking** — operates strictly on the two **separate** stems (see the audio rule above); never accepts a pre-mixed track. Applies fades alongside the duck.
- **overlays** — also carries the bookend template so every episode opens and closes with the consistent David / Chronos Compass framing.
- **shorts-reframe** — re-frames to 9:16 from assets that already exist in the long-form, keeping the marginal cost of each Short low.

---

## How these are invoked

The **Editor** and **Shorts cutter** sub-agents call these scripts; they are **not** run by hand in normal operation. Inputs (render takes, voice stems, music stems) come from the per-episode working folder under [`episodes/`](../episodes/); outputs are written back there. Local media paths are recorded in the Notion **Media Assets** DB (see [`docs/notion-schema-spec.md`](../docs/notion-schema-spec.md)).

Because every script wraps the **FFmpeg / Whisper CLIs**, behaviour is identical on macOS (dev) and Windows (Fabio) — that parity is the whole reason this folder exists.
