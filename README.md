# History Tube — Agentic Video-Production Pipeline

An agentic pipeline that carries a **History Tube** YouTube episode from a spark of an idea
to a finished, packaged video. The host is **David Hattenborg** — a wise, curious
historian-explorer from 2060 who appears *only* at the open and close (the "bookends");
the body of every episode is historical AI b-roll. The signature artifact is the **Chronos
Compass**. The non-negotiable soul: historical narration that **builds a dramatic arc to an
emotional, theatrical climax** — we make viewers *feel* history, not merely learn it.
British English, theatrical register, long-form, one video per week.

> This README is the front door. The full plan at [`docs/build-plan.md`](docs/build-plan.md)
> is the **single source of truth** — when in doubt, it wins.

---

## Who owns what

**Agents propose; Fabio disposes.** The agents do the heavy lifting — research, drafting,
prompt generation, rendering, assembly. **Fabio owns the creativity:** the angle and thesis,
the emotional beats, the **camera and lighting direction**, and the final **packaging** call.
The pipeline exists to remove friction so Fabio makes **more** creative decisions, not fewer.
Every gate either protects time and money or hands a creative decision back to Fabio.

---

## ⚠️ OS-agnostic mandate

> Development happens on JJ's **macOS** machine but transfers to Fabio's **Windows** machine
> via this repo. **No macOS `osascript` / AppleScript anywhere.** Every script must run on
> Windows. Use pure **Python / Node + FFmpeg CLI + Whisper CLI**. Anything that only works on
> a Mac is a **bug**, not a feature. Windows-first is the default; Mac is just where it is built.

---

## Agent architecture

**The Showrunner** (**Vitória**, `orchestrator/`). Reads pipeline state (local JSON mirror by
default; Fabio's Notion when wired), knows which phase each episode is in, invokes the right
sub-agent, and **pauses at the gates** to wait for Fabio. She proposes; Fabio disposes.
**She never publishes anything on her own** — Scheduled → Published is an explicit action.

**The nine sub-agents** — each a focused skill the Showrunner calls, one folder per agent under
`agents/`:

| Function | Does | Produces |
|---|---|---|
| **Researcher** | Gathers facts, timeline, hooks, controversies, sources | Research dossier + source ledger |
| **Concept writer** | Shapes the dossier + Fabio's angle into a dramatic arc | Outline with beats + the climax + the "what comes next" |
| **Adversarial critic** | Attacks accuracy, originality, retention risk, **dramatic arc + climax strength**, and sensitive-topic landmines | Critique → revisions |
| **Scriptwriter** | Writes the full British-English theatrical narration, timed, in David's voice | Locked script |
| **Director-assistant** | Splits the locked script into scenes/beats/shots; *proposes* camera move, lighting, composition, transition per shot | Draft shot list for Fabio |
| **Prompt engineer** | Converts each approved shot (carrying Fabio's direction) into model-ready prompts | Prompt set per shot |
| **Render orchestrator** | Calls Higgsfield (clips + voice TTS); ingests Suno music; manages takes | Raw renders + voice stems + music stems |
| **Editor** | FFmpeg assembly: clips to VO timing, ducked music, captions, fades, bookend template | The cut |
| **Shorts cutter** | Extracts 1–2 vertical Shorts from the finished long-form | Short(s) for growth |

> **David's crew** (naming is Fabio's creative act, set in `agents/crew.py`):
> **Vitória** (Showrunner) · **Deborah** (Researcher) · **Katusha** (Concept writer) ·
> **Tainara** (Adversarial critic) · **Glesy** (Scriptwriter) · **Brenda** (Director-assistant) ·
> **Sabrina** (Prompt engineer) · **Wanessa** (Render orchestrator) · **Cleidiane** (Editor) ·
> **Jucilene** (Shorts cutter).

---

## The pipeline

Nine phases, **four hard gates**, **one light review**. Gates sit only where money/time is
committed or where Fabio's judgment must rule.

**Phases**

- **0 — Brainstorm** *(Fabio leads)*. Fabio picks the topic and thesis/angle; the Showrunner may surface demand-validated candidates, but the spark is his.
- **1 — Research**. Researcher builds the dossier: timeline, key figures, hooks, controversies, source ledger.
- **2 — Concept / Outline**. Concept writer turns dossier + angle into the dramatic arc: beats, the build, the climax, the "what comes next".
- **3 — Adversarial review**. Critic attacks accuracy, originality, retention, climax strength, sensitive-topic balance; writer revises and they iterate.
- **4 — Script**. Scriptwriter writes the full narration: strong cold-open hook, David's theatrical British voice, timed, arc intact.
- **5 — Direction / shot breakdown**. Director-assistant splits the script into scenes → beats → shots and *proposes* camera, light, composition, transition per shot.
- **6 — Prompt generation**. Prompt engineer converts each approved shot into model-ready prompts for the visual stack.
- **7 — Render**. Render orchestrator generates clips (Higgsfield), voice-over (Higgsfield TTS), and ingests Suno music; multiple takes per shot.
- **8 — Edit / assembly**. Editor assembles clips to VO timing, layers ducked music, captions (Whisper SRT), fades, overlays, and the bookend template.
- **9 — Shorts spin-off**. Shorts cutter extracts 1–2 vertical Shorts from the finished long-form for subscriber growth.

**Gates**

- 🚦 **Gate 1 — Topic + Packaging lock** *(after Phase 1)*. Fabio approves the angle, working title(s), thumbnail concept, and hook. Nothing expensive happens before this.
- 🚦 **Gate 2 — Script lock** *(after Phase 4)*. Everything downstream is built on the script — freeze it here.
- 🚦 **Gate 3 — Direction lock — FABIO'S DOMAIN** *(after Phase 5)*. Fabio edits camera + light shot by shot; his sacred creative act, never delegated.
- 🔎 **Light Review — Take selection** *(after Phase 7)*. Fabio picks the best take per shot and flags re-rolls; a contact-sheet glance, not bureaucracy.
- 🚦 **Gate 4 — Final cut + publish** *(after Phase 8)*. Fabio watches the assembled video and confirms final packaging. Nothing publishes without this.

---

## Repo structure

```
omega-pipeline/            # repo root = the History Tube project
  README.md  CLAUDE.md  cli.py  pyproject.toml
  config/
    channel-dna.md         # the creative constitution (read by every writing agent)
    voice-recipe.json      # David's voice recipe (lock at build time)
    models.json            # gen model per shot type (validate at build time)
    visual-refs/           # locked David + Chronos Compass references
  core/                    # status, gates, phase map, state machine, models, config, CLI
  orchestrator/            # Vitória — the Showrunner (state engine + gates)
  agents/                  # one package per sub-agent (agent.py + prompt.md), crew.py
    researcher/ concept/ critic/ scriptwriter/
    director/ prompt_engineer/ render/ editor/ shorts/
  adapters/                # llm, higgsfield, suno, store — mock/local default, real opt-in
  scripts/                 # OS-agnostic FFmpeg + Whisper command builders/runners
  tests/                   # stdlib unittest, hermetic (49 tests)
  .claude/skills/          # hybrid interactive skills for the LLM agents
  docs/
    build-plan.md          # the full plan, verbatim (single source of truth)
    notion-schema-spec.md
    fabio-setup-checklist.md
  episodes/                # per-episode working folders (gitignored; `python cli.py demo`)
  state/                   # local Notion mirror / cache
```

---

## Build status

Each build ends in a **Fabio checkpoint** — the build itself is gated, just like production.

- [x] **Build A — Scaffold.** Repo + folder structure, `channel-dna.md`, Notion schema spec, Fabio setup checklist.
- [x] **Build B — Showrunner skeleton + state model.** `orchestrator/showrunner.py` reads status, advances phases, stops at gates.
- [x] **Build C — Writing agents.** Deborah → Katusha → Tainara → Glesy, each reading `channel-dna.md`.
- [x] **Build D — Direction + prompts.** Brenda (camera/light shot list) and Sabrina (deterministic prompts).
- [x] **Build E — Render + edit integration.** Wanessa (Higgsfield clips + TTS + Suno ingest); Cleidiane (FFmpeg/Whisper editor); Jucilene (Shorts reframe).
- [x] **Build F — End-to-end dry run.** `python cli.py demo` walks a full episode through all gates; covered by `tests/`.
- [ ] **Build G — Transfer to Fabio (Windows).** Clone, install toolchain, connect MCPs, recreate Notion, run for parity. *(Fabio's side — see [`docs/fabio-setup-checklist.md`](docs/fabio-setup-checklist.md).)*

> **First version status.** Builds A–F are implemented and the test suite is green. The
> pipeline runs end-to-end in **mock/dry-run** mode with no keys, no network and no
> ffmpeg — wire the real Higgsfield/Notion/Anthropic backends to go live (Build G).

---

## Run it

```bash
python cli.py demo               # build + walk the sample episode end-to-end (mock)
python cli.py init <slug> --title "..." --angle "..."
python cli.py run <slug>         # step through, pausing at each gate for Fabio
python cli.py approve <slug>     # approve the pending gate
python cli.py run <slug> --auto  # auto-approve every gate (dry-run)
python cli.py status <slug>      # where is this episode?
python cli.py crew               # David's crew
```

By default everything is mocked (`HT_LLM=mock`, `HT_STORE=local`, `HT_HIGGSFIELD=mock`).
Switch a backend on with env vars once credentials/MCPs are wired — see [`CLAUDE.md`](CLAUDE.md).

## Test it

```bash
python -m unittest discover -s tests -t .     # stdlib only, no install
# or:  pip install pytest && pytest
```

---

## Key files

- [`docs/build-plan.md`](docs/build-plan.md) — the full plan, **single source of truth**.
- [`config/channel-dna.md`](config/channel-dna.md) — the **creative constitution**; every writing/critique agent reads it first.
- [`docs/notion-schema-spec.md`](docs/notion-schema-spec.md) — the Notion workspace schema, built in **Fabio's** Notion at setup.
- [`docs/fabio-setup-checklist.md`](docs/fabio-setup-checklist.md) — the Windows-side setup checklist for Fabio.
