# Fabio's Setup Checklist (Windows side)

> **Scaffold stub — Build A.** Actionable, once-through setup for Fabio's **Windows** machine. Expands Section 10 of the build plan with detail from Sections 6 and 11. Work top to bottom; later steps assume the earlier ones are done.
>
> Single source of truth: [`docs/build-plan.md`](./build-plan.md). When this checklist and the plan disagree, the plan wins.

---

## YouTube

- [ ] Channel created.
- [ ] AdSense account linked to the channel.
- [ ] 2-step verification turned on.
- [ ] Country eligibility for monetisation confirmed.

> Reference (not a setup blocker): full YouTube Partner Program needs 1,000 subscribers + 4,000 watch hours in 12 months, or 10M Shorts views in 90 days. Account must be ≥ 30 days old, with AdSense + 2FA in place. See build-plan Section 7 for the honest monetisation reality.

---

## Accounts

- [ ] **Higgsfield** — paid plan with credits for video generation (clips + David's TTS voice). Main recurring spend; track against the business goal.
- [ ] **Suno** — paid plan, for music. Used **manually in the Suno web app** — there is no Suno MCP. Generate 1–3 tracks per episode and drop the files into the episode's `audio/` folder.
- [ ] *Optional, later:* **VidIQ** or **TubeBuddy** — a YouTube-native paid signal tool, on Fabio's own account.

> **No Semrush.** Semrush is web-SEO, not YouTube, and Fabio has no account. Demand validation uses free YouTube-native signals (autocomplete, Trends, competitor scan) per build-plan Section 7.

---

## MCP connections on Fabio's Claude

- [ ] **Higgsfield** — connected to Fabio's own account (eventually; can run on JJ's during dev).
- [ ] **Notion** — connected to Fabio's own Notion workspace.
- [ ] **Suno** — *not applicable.* Suno is manual (no MCP).
- [ ] **ElevenLabs** — *only if* David's voice ever moves there. The portable voice **recipe** (not an account-bound asset) is the default approach; ElevenLabs is the fallback if a fully ownable bespoke voice is ever wanted.

---

## Local install (Windows)

Install on Fabio's Windows machine. Windows-friendly hints only — **no mac-only commands anywhere**.

- [ ] **FFmpeg** — e.g. `winget install Gyan.FFmpeg` or `choco install ffmpeg`.
- [ ] **Whisper** (CLI) — install per its docs (typically via Python: `pip install` the chosen Whisper package).
- [ ] **Python** (and/or **Node**) — e.g. `winget install Python.Python.3.12` and/or `winget install OpenJS.NodeJS`.
- [ ] **Git** — e.g. `winget install Git.Git`.
- [ ] **Confirm everything is on PATH.** In a fresh terminal, each of these should print a version: `ffmpeg -version`, `whisper --help`, `python --version`, `node --version`, `git --version`. If any is "not recognised", fix PATH before continuing.
- [ ] **Clone the repo** — `git clone <omega-pipeline repo URL>` into Fabio's working directory.
- [ ] **Create the `episodes/` media folder structure** — one working folder per episode (`research/`, `script/`, `shotlist/`, `renders/`, `audio/` for SEPARATE voice + music stems, `thumbnails/`, `final/`). See build-plan Section 8.

> ⚠️ **Every script in this repo must run on Windows.** Pure Python/Node + FFmpeg CLI + Whisper CLI. No `osascript` / AppleScript. Anything mac-only is a bug — report it, don't work around it.

---

## Drop-ins

- [ ] **David's locked voice recipe** → `config/voice-recipe.json` (preset + exact delivery-prompt text + settings; auditioned and locked at build time per build-plan Section 11).
- [ ] **David + Chronos Compass visual references** → `config/visual-refs/` (the locked Higgsfield Soul / reference image for David, plus the locked Chronos Compass asset; reused for every episode's bookends).

---

## Notion workspace

- [ ] **Schema built once Notion MCP is connected.** Claude Code builds the workspace schema **in Fabio's Notion** (not JJ's) from [`docs/notion-schema-spec.md`](./notion-schema-spec.md). This is a one-time setup step, run after the Notion MCP connection above is live.

---

> **OS-agnostic mandate:** everything here must run on Windows via pure Python/Node + FFmpeg CLI + Whisper CLI — no macOS `osascript` / AppleScript, ever. Once this checklist is complete, run **Build G (transfer + parity run)** in [`docs/build-plan.md`](./build-plan.md) to confirm the Windows run matches the dev run.
