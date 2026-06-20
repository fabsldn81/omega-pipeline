# Tainara — Adversarial critic.

Implemented in [`agents/critic/agent.py`](agent.py). The pipeline's designated adversary —
she attacks weak ideas cheaply, before the expensive work begins. Agents propose; Fabio
disposes.

## What it does

**DOES** — attacks the Concept writer's outline along several axes: accuracy, originality and
retention risk, and **above all whether it genuinely builds to an emotional, theatrical
climax** (the channel's soul, and her primary mandate). For sensitive and geopolitical
material she is the **reinforced gate**, applying a heightened standard on balance, accuracy
and advertiser-safety. She surfaces risk plainly; she never vetoes a topic.

**PRODUCES** — `episodes/<slug>/research/critique.json` with four keys:

- `issues` — list of `{area, severity, note}`, severity in {low, medium, high}.
- `verdict` — one or two sentences: is it strong enough to proceed?
- `advertiser_safe` — boolean (logs an `[ADVERTISER-SAFETY FLAG]` when false).
- `revisions` — concrete fixes for Katusha to apply.

She has **no hard gate of her own**. Fabio sees the result of the Critic ↔ Concept loop
downstream at **Gate 2**; her job is to make what reaches him stronger, not to add a checkpoint.

## Where it sits

Phase 3 — Adversarial review, during **Researching**. Reads the outline (`research/outline.json`)
and prepends `config/channel-dna.md` to her prompt as the creative constitution. The settled,
de-risked outline flows on to Scripting, and Fabio judges it at **Gate 2 (exit Scripting)**.

## How it runs

LLM agent. The Showrunner (Vitória) invokes `CriticAgent.run(ctx)` when the episode reaches its
status; there is no standalone CLI entry point. End-to-end via mock adapters:

```
python cli.py run <slug>      # Showrunner drives Tainara as part of the run
```

## Files

- [`agent.py`](agent.py) — `CriticAgent` (key `critic`); validates the four critique keys and
  writes the artifact.
- [`prompt.md`](prompt.md) — the shared brain for the Python agent and the Claude skill.
- Claude skill **`tainara-critic`** — thin interactive wrapper around the same `prompt.md`.

---

*British English throughout. Soul first: a dramatic arc to an emotional, theatrical climax —
Tainara exists to defend it.*
