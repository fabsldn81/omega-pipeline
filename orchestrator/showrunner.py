"""Vitória — the Showrunner. Reads pipeline state, runs the right agent, pauses at gates.

She proposes; Fabio disposes. She advances an episode's status only after the relevant
gate is approved, and she NEVER publishes on her own — the Scheduled -> Published step
is an explicit Fabio action (or auto-approved only in a dry-run).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from adapters.factory import Adapters, build_adapters
from agents import get_agent
from agents.base import AgentContext
from agents.crew import name_of
from core.config import Config, load_config
from core.errors import GateNotApproved, HistoryTubeError
from core.models import Episode
from core.state_machine import StateMachine
from core.status import Status

# Actions a step can report.
ADVANCED = "advanced"
WAITING_GATE = "waiting_gate"
READY_TO_PUBLISH = "ready_to_publish"
TERMINAL = "terminal"


@dataclass
class StepResult:
    slug: str
    action: str
    from_status: Status | None = None
    to_status: Status | None = None
    ran: list[dict[str, Any]] = field(default_factory=list)
    gate: str | None = None
    message: str = ""

    @property
    def stopped(self) -> bool:
        return self.action in (WAITING_GATE, READY_TO_PUBLISH, TERMINAL)


class Showrunner:
    def __init__(self, config: Config | None = None) -> None:
        self.config = config or load_config()
        self.adapters: Adapters = build_adapters(self.config)
        self.store = self.adapters.store
        self.sm = StateMachine()
        self.name = name_of("showrunner")

    # --- episode lifecycle -------------------------------------------------

    def create_episode(
        self,
        slug: str,
        *,
        title: str = "",
        topic: str = "",
        angle: str = "",
        target_length_min: int = 12,
    ) -> Episode:
        ep = Episode(
            slug=slug,
            title=title or slug.replace("-", " ").title(),
            topic=topic or title,
            angle=angle,
            target_length_min=target_length_min,
            status=Status.IDEA,
        )
        self.config.paths.ensure_episode_dirs(slug)
        ep.log(f"{self.name}: episode created at {Status.IDEA}.")
        self.store.create(ep)
        return ep

    def get(self, slug: str) -> Episode:
        return self.store.get(slug)

    def list(self) -> list[Episode]:
        return self.store.list()

    # --- the engine --------------------------------------------------------

    def _run_agents(self, ep: Episode, agent_keys: tuple[str, ...]) -> list[dict[str, Any]]:
        ran: list[dict[str, Any]] = []
        for key in agent_keys:
            agent = get_agent(key)
            ctx = AgentContext(episode=ep, config=self.config, adapters=self.adapters)
            ran.append(agent.run(ctx))
        return ran

    def step(self, slug: str, *, auto_approve: bool = False) -> StepResult:
        """Advance one phase. Pauses (does not advance) at gates and at publish."""
        ep = self.store.get(slug)
        status = ep.status

        if self.sm.is_terminal(status):
            return StepResult(slug, TERMINAL, from_status=status, message="Already published.")

        # A gate is already pending from a previous step.
        if ep.pending_gate:
            if not auto_approve:
                return StepResult(
                    slug, WAITING_GATE, from_status=status, gate=ep.pending_gate,
                    message=f"Waiting on {ep.pending_gate}. Approve to continue.",
                )
            return self._approve_and_advance(ep)

        phase = self.sm.phase(status)

        # The Showrunner never publishes on her own.
        if status == Status.SCHEDULED and not auto_approve:
            return StepResult(
                slug, READY_TO_PUBLISH, from_status=status,
                message="Approved and scheduled. Fabio publishes (run `publish`).",
            )

        ran = self._run_agents(ep, phase.agents)
        gate = phase.gate

        if gate is None:
            nxt = self.sm.advance(status, gate_approved=True)
            ep.status = nxt
            ep.log(f"{self.name}: {status} -> {nxt}.")
            self.store.save(ep)
            return StepResult(slug, ADVANCED, from_status=status, to_status=nxt, ran=ran)

        if auto_approve:
            nxt = self.sm.advance(status, gate_approved=True)
            ep.status = nxt
            ep.log(f"{self.name}: {gate} auto-approved (dry-run); {status} -> {nxt}.")
            self.store.save(ep)
            return StepResult(slug, ADVANCED, from_status=status, to_status=nxt, ran=ran, gate=gate.value)

        ep.pending_gate = gate.value
        ep.log(f"{self.name}: paused at {gate} — awaiting Fabio.")
        self.store.save(ep)
        return StepResult(
            slug, WAITING_GATE, from_status=status, gate=gate.value, ran=ran,
            message=f"Artifacts ready. Awaiting {gate.value}.",
        )

    def _approve_and_advance(self, ep: Episode) -> StepResult:
        status = ep.status
        gate = ep.pending_gate
        ep.pending_gate = None
        nxt = self.sm.advance(status, gate_approved=True)
        ep.status = nxt
        ep.log(f"{self.name}: {gate} approved; {status} -> {nxt}.")
        self.store.save(ep)
        return StepResult(ep.slug, ADVANCED, from_status=status, to_status=nxt, gate=gate)

    def approve(self, slug: str, gate: str | None = None) -> StepResult:
        ep = self.store.get(slug)
        if not ep.pending_gate:
            raise GateNotApproved(f"Episode '{slug}' has no gate pending approval.")
        if gate is not None and gate not in (ep.pending_gate, ep.pending_gate.split(" — ")[0]):
            raise GateNotApproved(
                f"Pending gate is '{ep.pending_gate}', not '{gate}'."
            )
        return self._approve_and_advance(ep)

    def publish(self, slug: str) -> StepResult:
        """Explicit Fabio action: Scheduled -> Published."""
        ep = self.store.get(slug)
        if ep.status != Status.SCHEDULED:
            raise HistoryTubeError(f"Episode '{slug}' is {ep.status}, not Scheduled.")
        ep.status = Status.PUBLISHED
        ep.log(f"{self.name}: published (Fabio's action).")
        self.store.save(ep)
        return StepResult(slug, ADVANCED, from_status=Status.SCHEDULED, to_status=Status.PUBLISHED)

    def spin_off_shorts(self, slug: str) -> dict[str, Any]:
        """Phase 9 — run Jucilene off the finished long-form."""
        ep = self.store.get(slug)
        ctx = AgentContext(episode=ep, config=self.config, adapters=self.adapters)
        summary = get_agent("shorts").run(ctx)
        self.store.save(ep)
        return summary

    def run(
        self,
        slug: str,
        *,
        auto_approve: bool = False,
        with_shorts: bool = True,
        max_steps: int = 50,
    ) -> list[StepResult]:
        """Step until a stop (a gate / ready-to-publish in manual mode) or terminal."""
        results: list[StepResult] = []
        for _ in range(max_steps):
            r = self.step(slug, auto_approve=auto_approve)
            results.append(r)
            if r.action == TERMINAL:
                break
            if r.stopped and not auto_approve:
                break
        if with_shorts and self.get(slug).status == Status.PUBLISHED:
            self.spin_off_shorts(slug)
        return results
