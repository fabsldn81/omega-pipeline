# The Showrunner — Orchestrator (Stub Spec)

> **Status: IMPLEMENTED (Build B).** The Showrunner lives in [`showrunner.py`](showrunner.py)
> as the `Showrunner` class (persona: **Vitória**), driven by [`../core/state_machine.py`](../core/state_machine.py)
> and the phase map in [`../core/phases.py`](../core/phases.py). This document is the contract it implements;
> run it via `python cli.py run <slug>`.

The single source of truth is [`docs/build-plan.md`](../docs/build-plan.md). Where this stub and the plan disagree, the plan wins. This document expands the plan's §2 (agent architecture), §3 (per-episode pipeline) and §4 (gate system) into the orchestrator's contract.

---

## 1. What the Showrunner is

The Showrunner is the super-agent / orchestrator — the spine of the History Tube pipeline. It is a lightweight version of JJ's Ernesto house, with far less governance. Its job is to remove friction so Fabio makes **more** creative decisions, not fewer.

In one line: it reads where every episode is, runs the right sub-agent for that phase, and **stops at the gates so Fabio can decide.**

---

## 2. Responsibilities (plan §2)

- **Read pipeline state from Fabio's Notion.** The `Episodes` database is the master record; the `Status` field on each episode row is the phase pointer. The Showrunner reads `Status` to know which phase each episode is in.
- **Know the phase.** Map the current `Status` to its active phase (see §4 state machine) and to the sub-agent that owns that phase.
- **Invoke the right sub-agent.** Call the focused agent for the active phase (Researcher, Concept writer, Critic, Scriptwriter, Director-assistant, Prompt engineer, Render orchestrator, Editor, Shorts cutter — see `agents/`). The agent drafts and proposes.
- **Pause at the gates.** At each hard gate the Showrunner posts the artifact for review and **stops** until Fabio responds. It proposes; **Fabio disposes**.
- **Advance `Status` only after the relevant gate is approved.** A phase with a gate does not advance on the agent finishing — it advances on Fabio's approval. Phases without a gate flow through automatically.
- **It NEVER publishes anything on its own.** Publication is downstream of Gate 4 and is Fabio's call. The Showrunner has no autonomous publish path.

**Ownership model.** Agents draft and propose; Fabio disposes. Fabio owns the creativity — angle/thesis, emotional beats, camera + lighting direction, and the final packaging call. The Showrunner is plumbing, never an author.

---

## 3. Operating principles

- **Gate-stop is hard, not advisory.** When a gate is reached the Showrunner writes the artifact to Notion, signals Fabio, and idles. It does not advance, retry, or substitute its own judgement for an approval.
- **One direction of trust.** Agents propose; only Fabio's recorded approval moves `Status` past a gate. No agent (and no other sub-agent) can self-approve.
- **State lives in Notion; cache lives locally.** Notion `Episodes.Status` is authoritative. The `state/` folder is a local mirror/cache for speed and offline glance — never the source of truth.
- **Stateless re-entry.** The Showrunner can be (re)started at any time and recover what to do next purely by reading `Status`. There is no hidden in-memory phase.

---

## 4. The Status state machine (plan §3 / §4)

`Episodes.Status` enum (reproduced exactly):

```
Idea → Researching → Packaging-locked → Scripting → Script-locked →
Direction → Direction-locked → Generating → Editing → Final-review →
Scheduled → Published
```

The Showrunner advances `Status` **only after the relevant gate is approved.** Phases marked "no gate" flow through automatically once the agent's work is done; gated phases hold until Fabio approves.

Ordered list — each entry: **Status → active phase → gate (if any) that must be approved to advance → next Status.**

1. **`Idea`**
   - **Active phase:** Phase 0 — Brainstorm (Fabio leads; the Showrunner may surface demand-validated candidates from the Topic Pool, but the spark is Fabio's).
   - **Gate:** none.
   - **Advances to:** `Researching`.

2. **`Researching`**
   - **Active phase:** Phase 1 — Research (Researcher builds the dossier + source ledger).
   - **Gate:** 🚦 **GATE 1 — Topic + Packaging lock.** Fabio approves the angle, the working title(s), the thumbnail concept, and the hook/promise. Nothing expensive happens before this gate.
   - **Advances to:** `Packaging-locked`.

3. **`Packaging-locked`**
   - **Active phase:** Phase 2 — Concept / Outline (dramatic arc, beats, climax, the "what comes next"), then Phase 3 — Adversarial review (critic ↔ concept writer iterate).
   - **Gate:** none (no hard gate; Fabio sees the result at Gate 2).
   - **Advances to:** `Scripting`.

4. **`Scripting`**
   - **Active phase:** Phase 4 — Script (full British-English theatrical narration, timed, in David's voice).
   - **Gate:** 🚦 **GATE 2 — Script lock.** Everything downstream is expensive and built on the script — freeze it here.
   - **Advances to:** `Script-locked`.

5. **`Script-locked`**
   - **Active phase:** Phase 5 — Direction / shot breakdown (Director-assistant splits the locked script into scenes → beats → shots and *proposes* camera move, lighting, composition, transition per shot — a draft for Fabio).
   - **Gate:** none yet (the draft is produced here; approval is the next state).
   - **Advances to:** `Direction`.

6. **`Direction`**
   - **Active phase:** Phase 5 continues — Fabio reviews the draft shot list.
   - **Gate:** 🚦 **GATE 3 — Direction lock (FABIO'S DOMAIN).** Fabio edits camera + lighting shot by shot. This is his sacred creative act; the agent serves it, never owns it.
   - **Advances to:** `Direction-locked`.

7. **`Direction-locked`**
   - **Active phase:** Phase 6 — Prompt generation (Prompt engineer converts each approved shot, carrying Fabio's camera/light direction, into model-ready prompts).
   - **Gate:** none — deterministic translation of a frozen shot list; **quick sanity glance only**, not a hard gate.
   - **Advances to:** `Generating`.

8. **`Generating`**
   - **Active phase:** Phase 7 — Render (Render orchestrator generates clips via Higgsfield, voice-over via Higgsfield TTS on David's recipe, ingests Suno music; multiple takes per shot).
   - **Gate:** 🚦 **LIGHT REVIEW — Take selection.** Fabio picks the best take per shot and flags re-rolls. Lightweight — a contact-sheet review, not bureaucracy.
   - **Advances to:** `Editing`.

9. **`Editing`**
   - **Active phase:** Phase 8 — Edit / assembly (Editor assembles clips to VO timing, layers **ducked** music, captions via Whisper SRT, fades, overlays, the bookend template).
   - **Gate:** none — the cut is produced here; Fabio's review happens at the next status.
   - **Advances to:** `Final-review`.

10. **`Final-review`**
    - **Active phase:** Phase 8 continues — the Showrunner posts the assembled cut and Fabio watches it.
    - **Gate:** 🚦 **GATE 4 — Final cut + publish.** Fabio approves or gives notes. Final packaging (title, thumbnail, description, chapters, tags, end screen) is confirmed here. **Nothing publishes without this.**
    - **Advances to:** `Scheduled`.

11. **`Scheduled`**
    - **Active phase:** Hand-off — the approved video + packaging are queued for upload. The Showrunner never performs the publish itself.
    - **Gate:** none (Gate 4 already cleared; publication is Fabio's action).
    - **Advances to:** `Published`.

12. **`Published`**
    - **Active phase:** Terminal for the long-form. Post-publication metrics (Views, Watch time, CTR, Avg. retention) are filled later.
    - **Gate:** none.
    - **Advances to:** terminal.

### Phase 9 — Shorts spin-off (out-of-band)

Phase 9 (Shorts cutter extracts 1–2 vertical 9:16 Shorts) runs **from the finished long-form**, after `Published`, using assets that already exist (low marginal cost). It is not a `Status` step on the long-form's main track; it is triggered off the completed episode. How Shorts are tracked (sub-rows, a flag, or a separate lane) is a Build B / schema decision — see `docs/notion-schema-spec.md`.

---

## 5. Gate summary (plan §4)

| Gate | `Status` it gates exit from | Fabio approves | Why it exists |
|---|---|---|---|
| **1 — Topic + Packaging** | `Researching` | Angle, title(s), thumbnail concept, hook | Protects against expensive work on a weak idea or weak packaging |
| **2 — Script** | `Scripting` | Final script | Freezes the foundation everything downstream is built on |
| **3 — Direction** | `Direction` | Camera + lighting per shot | **Fabio's creative ownership** — the one thing he never delegates |
| **Light — Takes** | `Generating` | Best take per shot | Quality control without heavy process |
| **4 — Final cut** | `Final-review` | The video + the packaging | Nothing reaches the public unapproved |

---

## 6. Implementation notes (Build B)

- **Language is open — Python *or* Node.** Either is acceptable; the choice is finalised in Build B.
- **⚠️ OS-AGNOSTIC MANDATE (Windows-first).** Development happens on JJ's macOS but the repo transfers to Fabio's **Windows** machine. **No macOS `osascript` / AppleScript anywhere.** Everything must run on Windows via pure Python/Node + FFmpeg CLI + Whisper CLI. Anything mac-only is a bug, not a feature — use cross-platform path handling, no shell-isms that assume a POSIX-only environment, and no Mac-specific binaries.
- **Notion is read via Fabio's Notion MCP**, connected on Fabio's side (not JJ's workspace). The Showrunner reads/writes `Episodes.Status` and posts gate artifacts there.
- **`state/`** holds the local mirror/cache only; treat Notion as authoritative.
- **Build B checkpoint:** a dummy episode walks this entire state machine end-to-end with manual gate approvals (plan §9).

---

## 7. Status note (`Final-review`)

`Final-review` is a distinct `Status` value (plan §5) and is the **Gate 4** review window: the Editor produces the cut on exit from `Editing`, the Showrunner posts it, and Fabio approves at `Final-review` before it advances to `Scheduled`. This stub and [`docs/notion-schema-spec.md`](../docs/notion-schema-spec.md) use the same mapping; the plan remains the tie-breaker.
