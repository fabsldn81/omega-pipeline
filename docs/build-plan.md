# History Tube — Production Pipeline Build Plan

> Stored verbatim in-repo. **This document is the single source of truth: when in doubt, it wins.**

**Purpose.** This is the blueprint for an agentic content-production pipeline that takes a History Tube episode from a spark of an idea to a finished, packaged YouTube video. Paste this into Claude Code and build it in the staged order described in Section 9. This document is the single source of truth: when in doubt, it wins.

**Who owns what.** The agents do the heavy lifting — research, drafting, prompt generation, rendering, assembly. **Fabio owns the creativity**: the angle and thesis, the emotional beats, the camera and lighting direction, and the final packaging call. The pipeline is built to *remove friction so Fabio makes more creative decisions, not fewer*. Every checkpoint exists either to protect time/money or to put a creative decision back in Fabio's hands.

**Build-and-transfer model.** Development happens inside JJ's (macOS) Claude environment, then transfers to Fabio's **Windows** machine via a GitHub repo. This forces one hard rule:

> ⚠️ **OS-AGNOSTIC MANDATE.** No macOS `osascript` / AppleScript anywhere. Every script must run on Windows. Use pure Python/Node + FFmpeg CLI + Whisper CLI. Anything that only works on a Mac is a bug, not a feature.

---

## 1. Channel DNA (the creative constitution)

Store this verbatim in `config/channel-dna.md`. Every writing/critique agent reads it before acting.

- **The soul (non-negotiable):** historical narration that *builds a dramatic arc to an emotional, theatrical climax*. We make viewers *feel* history, not just learn it.
- **The host:** David Hattenborg — archaeologist, historian, explorer from 2060. Wise, curious, optimistic. A storyteller, never a lecturer. He explores possibilities; he never predicts the future as certainty.
- **The signature artifact:** the Chronos Compass — part ancient instrument, part future tech. Opens and closes journeys.
- **David appears ONLY at the open and the close** (the bookends). The body of the episode is historical b-roll. *This is a deliberate architectural choice that sidesteps AI character-consistency problems.*
- **Voice & register:** British English, theatrical, dramatic.
- **Format:** long-form, one video per week.
- **Structure is a servant, not a template.** The 4-act shape (Origins → Rise → Decline/Legacy → The Future) is *one available structure*, chosen episode by episode. What is mandatory is the dramatic arc and the emotional climax — not a fixed act count.
- **Brand constants (bake into a template):**
  - Open: David activates the Chronos Compass → *"Sit down. Here comes the story."*
  - Close: *"The past is fixed. The future is not."* → Compass activates → *"I'll see you in the next story."*
- **Business posture:** this is a business with an aggressive growth target. Packaging and retention are first-class citizens, not afterthoughts.

---

## 2. Agent architecture (the "house")

A lightweight version of JJ's Ernesto house — same idea, far less governance.

**The Showrunner (super-agent / orchestrator).** Reads pipeline state from Notion, knows which phase each episode is in, invokes the right sub-agent, and **pauses at the gates** to wait for Fabio. It proposes; Fabio disposes. It never publishes anything on its own.

**Sub-agents (by function).** Each is a focused skill the Showrunner calls. Build them one at a time (Section 9).

| Function | Does | Produces |
|---|---|---|
| Researcher | Gathers facts, timeline, hooks, controversies, sources | Research dossier + source ledger |
| Concept writer | Shapes dossier + Fabio's angle into a dramatic arc | Outline with beats + the climax + the "what comes next" |
| Adversarial critic | Attacks accuracy, originality, retention risk, **dramatic arc + climax strength**, and sensitive-topic landmines | Critique → revisions |
| Scriptwriter | Writes the full British-English theatrical narration, timed, in David's voice | Locked script |
| Director-assistant | Splits the locked script into scenes/beats/shots and *proposes* camera move, lighting, composition, transition per shot | Draft shot list for Fabio |
| Prompt engineer | Converts each approved shot (with Fabio's direction) into model-ready prompts | Prompt set per shot |
| Render orchestrator | Calls Higgsfield (clips + voice TTS); ingests Suno music; manages takes | Raw renders + voice stems + music stems |
| Editor | FFmpeg assembly: clips to VO timing, ducked music, captions, fades, bookend template | The cut |
| Shorts cutter | Extracts 1–2 vertical Shorts from the long-form | Short(s) for growth |

> 🎭 **Naming is Fabio's creative act.** These are function labels. Give each agent a name/persona if you want (David's "crew"). The plan uses the function names; rename freely in the build.

---

## 3. The per-episode pipeline (the workflow)

Nine phases, **four hard gates**, **one light review**. Fewer gates than JJ's house — placed only where money/time is committed or where Fabio's judgment must rule.

**Phase 0 — Brainstorm (Fabio leads).**
Fabio picks the topic and the *thesis/angle*. The Showrunner can surface demand-validated topic candidates from the Topic Pool (see Section 7), but the spark is Fabio's. → No gate.

**Phase 1 — Research.**
Researcher builds the dossier: timeline, key figures, the emotional hooks, the controversies, and a source ledger (every claim → a source URL).
→ 🚦 **GATE 1 — Topic + Packaging lock.** Fabio approves the angle, the working title(s), the thumbnail concept, and the hook/promise. **Nothing expensive happens before this gate.** (Packaging-first; see Section 7.)

**Phase 2 — Concept / Outline.**
Concept writer turns the dossier + approved angle into the dramatic arc: beats, the build, the climax, and the speculative "what comes next." Structure chosen to serve the arc (not forced into 4 acts).

**Phase 3 — Adversarial review.**
The critic attacks: factual accuracy, originality, retention risk, **whether it actually builds to an emotional climax**, and — for sensitive topics — balance, accuracy, and advertiser-friendliness. Concept writer revises. Critic and writer iterate. → No hard gate (Fabio sees the result at Gate 2).

**Phase 4 — Script.**
Scriptwriter writes the full narration: a strong cold-open hook, David's theatrical British voice, timed to target length, arc intact.
→ 🚦 **GATE 2 — Script lock.** Everything downstream (shots, prompts, renders, voice) is expensive and built on the script. **Freeze it here.**

**Phase 5 — Direction / shot breakdown.**
Director-assistant splits the locked script into scenes → beats → shots, and *proposes* per shot: visual subject, composition, **camera move, lighting**, mood, transition. This is a **draft for Fabio**.
→ 🚦 **GATE 3 — Direction lock (FABIO'S DOMAIN).** Fabio edits camera + light shot by shot. This is his sacred creative act; the agent serves it, never owns it. Approved shot list → frozen.

**Phase 6 — Prompt generation.**
Prompt engineer converts each approved shot (carrying Fabio's camera/light direction) into model-ready prompts for the visual stack. → No new gate (deterministic translation of a frozen shot list; quick sanity glance only).

**Phase 7 — Render.**
Render orchestrator generates the clips (Higgsfield), the voice-over (Higgsfield TTS, David's recipe), and ingests the Suno music. Multiple takes per shot.
→ 🚦 **LIGHT REVIEW — Take selection.** Fabio picks the best take per shot and flags re-rolls. Lightweight — a contact-sheet review, not bureaucracy.

**Phase 8 — Edit / assembly.**
Editor assembles clips to VO timing, layers **ducked** music, adds captions (Whisper SRT), fades, overlays, and the bookend template.
→ 🚦 **GATE 4 — Final cut + publish.** Fabio watches the assembled video, approves or gives notes. **Nothing publishes without this.** Final packaging (title, thumbnail, description, chapters, tags, end screen) is confirmed here.

**Phase 9 — Shorts spin-off.**
Shorts cutter extracts 1–2 vertical Shorts from the finished long-form (assets already exist → low marginal cost) to drive subscriber growth.

---

## 4. The gate system (how the Showrunner pauses)

Each episode row in Notion carries a `status`. The Showrunner advances status only after the relevant gate is approved. Gates are explicit human checkpoints — the Showrunner posts the artifact for review and stops until Fabio responds.

| Gate | Fabio approves | Why it exists |
|---|---|---|
| **1 — Topic + Packaging** | Angle, title(s), thumbnail concept, hook | Protects against expensive work on a weak idea or weak packaging |
| **2 — Script** | Final script | Freezes the foundation everything downstream is built on |
| **3 — Direction** | Camera + light per shot | **Fabio's creative ownership** — the one thing he never delegates |
| **Light — Takes** | Best take per shot | Quality control without heavy process |
| **4 — Final cut** | The video + the packaging | Nothing reaches the public unapproved |

---

## 5. Notion workspace schema

> Built by Claude Code **in Fabio's Notion** once his Notion MCP is connected — *not* in JJ's workspace. This document defines the schema; the live build is a setup step on Fabio's side. Mirrors JJ's house, adapted for video.

**DB: Episodes** (master)
- Title · Slug · Status (`Idea → Researching → Packaging-locked → Scripting → Script-locked → Direction → Direction-locked → Generating → Editing → Final-review → Scheduled → Published`)
- Topic/Civilisation · Angle/Thesis · Target length · Publish date
- Relations → Research Dossier, Shot List, Media Assets, Packaging
- Post-publication metrics (filled later): Views · Watch time · CTR · Avg. retention

**DB: Topic Pool**
- Candidate topic · Demand signal (notes from YouTube autocomplete / Trends / competitor scan) · Competition notes · Status (`New / Approved / Parked / Done`) · Relation → Episodes

**DB: Research Dossiers**
- Per-episode facts · Timeline · Key figures · Hooks · Controversies/landmines · **Source ledger** (claim → URL) · Relation → Episodes

**DB: Shot List / Storyboard** *(the spine of Fabio's direction)*
- One row per shot: Scene · Beat · Visual subject · Composition · **Camera move** · **Lighting** · Mood · Transition · Prompt(s) · Chosen take · Render status · Relation → Episodes

**DB: Media Assets**
- Generated clips · Voice stems · Music stems · Thumbnails — with Type · Status (`Raw / Selected / Final`) · **Local path on Fabio's machine** · Relation → Episodes / Shots

**DB: Packaging**
- Title variants · Thumbnail concepts/files · Description · Tags · Chapters · End-screen plan · Relation → Episodes

**DB: Performance Snapshot** — *Phase 2 (defer).* Weekly analytics pull. For a brand-new channel, manual review in YouTube Studio is fine at first.

---

## 6. Tech stack & tooling decisions (locked)

- **Visuals — Higgsfield (pure AI).** Stills (e.g. Nano Banana Pro / Seedream) → animate (Seedance / Kling), or direct image/text-to-video. Validate which model suits which shot type at build time.
- **David's visual identity — locked reference.** Train one Higgsfield Soul (or fix a single reference image) for David, plus a locked Chronos Compass reference. Reuse for every episode's bookends. Store under `config/visual-refs/`.
- **Voice — AI-created, not cloned. Recipe-based for portability.**
  - Audition in JJ's Higgsfield (Speak 2.0 is prompt-driven: tone/emotion/delivery come from how you write the prompt).
  - Lock the **recipe** in `config/voice-recipe.json`: `{ preset, exact delivery-prompt text, settings }`. The recipe — not an account-locked asset — is what transfers to Fabio's account. (Higgsfield custom voices appear account-bound; verify empirically. ElevenLabs is the portable fallback if a fully ownable bespoke voice is ever wanted.)
- **Music — Suno, manual.** Generate 1–3 tracks per episode in the Suno web app; drop files into the episode's `audio/` folder. **No Suno MCP needed** at this volume.
- **Audio rule — separate stems, always.** Voice and music are never baked together. The editor mixes them with **ducking** (music drops under narration), synced to picture, with fades. Baked-together audio = a broken edit.
- **Editing — FFmpeg + Whisper, local, OS-agnostic.** Assembly, loudness normalisation (target ≈ −14 LUFS), captions (Whisper SRT), fades, overlays, the bookend template, and the Shorts re-frame to 9:16.
- **No Semrush.** Fabio has no account, and Semrush is web-SEO, not YouTube. Use YouTube-native free signals (Section 7). Optional future paid add-on (Fabio's account): VidIQ or TubeBuddy.

---

## 7. SEO / YouTube strategy (baked into the pipeline)

The Showrunner acts as the interface between Fabio's creative mind and YouTube reality. These rules are wired into the phases above.

- **Packaging-first (Gate 1).** Title + thumbnail + the first-30-seconds promise decide whether a video gets *clicked*; the documentary decides whether they *stay*. Lock packaging *before* expensive production. Generate several title variants and at least one thumbnail concept at Gate 1.
- **Topic = discovery; David = retention/brand.** Nobody searches "David Hattenborg"; they search "fall of the Roman Empire." Titles are topic-first, character-second.
- **Retention engineering.** Every script opens with a hook (a question, stakes, a mystery), not a slow throat-clear. The soul's dramatic arc to a climax *is* the retention strategy.
- **Demand validation (free, YouTube-native).** Researcher checks: YouTube search autocomplete on seed terms, Google Trends, a scan of comparable history channels' top-performing videos (titles + view counts), plus web search for trending anniversaries/topics. Output → Topic Pool "demand signal." *Honest limit: these are directional, not precise keyword volumes — fine for a new channel; precision comes later with a YouTube-native paid tool if desired.*
- **Aggressive-growth lever — Shorts (Phase 9).** 1–2 vertical Shorts per long-form to pull subscribers fast, cut from assets that already exist.
- **Standard hygiene.** Chapters, end screens, an organised playlist/series structure for binge-watching, consistent upload day.

> **Honest monetisation reality.** Full YouTube Partner Program = 1,000 subscribers + 4,000 watch hours in 12 months (or 10M Shorts views in 90 days); early/fan-funding tier = 500 subs + 3 public videos + 3,000 watch hours; account ≥ 30 days; AdSense + 2FA; review ≈ 1 month. **Hitting full monetisation in 2 months from zero in long-form is not realistic and not in your control** — it depends on the algorithm. A realistic 2-month outcome: pipeline live, David's look + voice dialled in, 4–6 quality videos published, packaging sharp, first traction data. Eligibility typically follows over 3–9+ months unless a video breaks out. The Shorts lever is the main accelerant.

---

## 8. Repo structure (high-level — names, not code)

```
history-tube/
  README.md
  config/
    channel-dna.md          # Section 1, verbatim
    voice-recipe.json       # David's locked voice (preset + delivery prompt)
    visual-refs/            # locked David + Chronos Compass references
    models.json             # which gen models per shot type
  orchestrator/             # the Showrunner
  agents/                   # one folder per sub-agent (built in Section 9)
    researcher/ concept/ critic/ scriptwriter/
    director/ prompt-engineer/ render/ editor/ shorts/
  scripts/                  # OS-agnostic Python: ffmpeg + whisper wrappers, re-frame, ducking
  episodes/                 # per-episode working folders (local, on Fabio's machine)
    <slug>/
      research/ script/ shotlist/ renders/
      audio/                # voice stems + music stems (SEPARATE)
      thumbnails/ final/
  state/                    # local state mirror / cache
```

---

## 9. Build phases (how Claude Code constructs the environment)

Build in this order. Each build phase ends with a checkpoint where Fabio reviews before proceeding — the build itself is gated, just like production.

- **Build A — Scaffold.** Create the repo + folder structure (Section 8), write `config/channel-dna.md`, and produce the Notion schema spec + the Fabio setup checklist (Section 10). → *Checkpoint: structure approved.*
- **Build B — Showrunner skeleton + state model.** The orchestrator that reads episode status from Notion, advances phases, and stops at gates. Define the status state machine (Section 3/4). → *Checkpoint: a dummy episode walks the state machine end-to-end with manual gate approvals.*
- **Build C — Writing agents.** Researcher → Concept → Critic → Scriptwriter, each reading `channel-dna.md`. → *Checkpoint: produce a full dossier + outline + critique + script for one real topic, with Gates 1 and 2 exercised.*
- **Build D — Direction + prompts.** Director-assistant (shot list with proposed camera/light) and Prompt engineer. → *Checkpoint: a frozen, Fabio-edited shot list (Gate 3) yields a clean prompt set.*
- **Build E — Render + edit integration.** Wire Higgsfield (clips + TTS) and Suno-manual ingest; build the FFmpeg/Whisper editor (stems, ducking, captions, bookend template) and the Shorts re-frame. → *Checkpoint: one shot rendered, voiced, scored, and a 30-second test assembly cut.*
- **Build F — End-to-end dry run.** Produce one complete test episode through all gates. Tune model choices, voice recipe, pacing. → *Checkpoint: a finished video Fabio signs off on.*
- **Build G — Transfer to Fabio (Windows).** Push to GitHub; Fabio clones, installs FFmpeg/Whisper/runtime, connects his own MCPs, recreates the Notion workspace, drops in his voice recipe. Run one episode on his machine to confirm parity. → *Checkpoint: Windows run matches the dev run.*

---

## 10. Fabio's setup checklist (Windows side)

- **YouTube:** channel created, AdSense linked, 2-step verification on, country eligibility confirmed.
- **MCP connections on Fabio's Claude:** Higgsfield (his own account, eventually), Notion. (Suno is manual — no MCP. ElevenLabs only if the voice ever moves there.)
- **Accounts:** Higgsfield (paid, credits for video gen), Suno (paid, for music). Optional later: VidIQ/TubeBuddy.
- **Local install:** FFmpeg, Whisper, Python (and/or Node), Git; clone the repo; create the `episodes/` media folder structure.
- **Drop-ins:** David's locked voice recipe (`voice-recipe.json`), David + Chronos Compass visual references (`config/visual-refs/`).

---

## 11. Decisions to finalise at build time

- **David's voice recipe** — audition in JJ's Higgsfield; lock preset + delivery prompt.
- **David's visual reference** — generate/lock the Soul or reference image + the Chronos Compass asset.
- **Higgsfield voice portability** — test empirically whether a created voice is account-bound; rely on the recipe regardless.
- **Per-shot model choices** — test Seedance / Kling / Nano Banana etc. for stills vs motion vs map/architecture shots; record in `models.json`.
- **Agent names/personas** — Fabio's call.

---

## 12. Risks & honest caveats

- **AI-video "slop" risk.** A 100% AI-generated history channel is a real bet; audiences increasingly reject generic AI footage. The David-bookends choice helps; ruthless quality control at Take Selection and Gate 4 is the defence.
- **Monetisation timeline.** As above — not 2 months for full YPP from zero. Plan the business around shipping quality + cadence; let eligibility follow.
- **Sensitive topics** (e.g. Israel & Palestine). Kept in scope per Fabio's call, handled via the **reinforced critic gate**, not avoidance. Be aware: geopolitical topics on a new channel carry genuine demonetisation and backlash risk.
- **Production capacity.** Weekly long-form, pure-AI, is demanding (many generated clips, credits, render time). Batch where possible; the gates keep expensive work from happening on weak foundations.
- **Credit cost.** Higgsfield video generation and (if ever) ElevenLabs are the main recurring spend. Track against the business goal.

---

*This plan enhances Fabio's creativity rather than replacing it: agents draft and propose; Fabio decides at every gate; camera, light, angle, and packaging stay his. Build it in the staged order above, exercise the gates from day one, and keep the channel's soul — a dramatic arc to an emotional, theatrical climax — at the centre of every episode.*
