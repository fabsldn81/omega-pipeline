"""The gate system — the explicit human checkpoints where the Showrunner pauses.

Four hard gates plus one light review (build plan Section 4). Each gate authorises
exit from exactly one status. The Showrunner advances a gated status ONLY after the
gate is approved; ungated statuses flow through automatically.
"""

from __future__ import annotations

from enum import Enum

from .status import Status


class Gate(str, Enum):
    GATE_1 = "Gate 1 — Topic + Packaging"
    GATE_2 = "Gate 2 — Script"
    GATE_3 = "Gate 3 — Direction"
    LIGHT_REVIEW = "Light Review — Take selection"
    GATE_4 = "Gate 4 — Final cut + publish"

    def __str__(self) -> str:
        return self.value


# Which status each gate authorises exit FROM.
GATE_EXIT: dict[Gate, Status] = {
    Gate.GATE_1: Status.RESEARCHING,
    Gate.GATE_2: Status.SCRIPTING,
    Gate.GATE_3: Status.DIRECTION,
    Gate.LIGHT_REVIEW: Status.GENERATING,
    Gate.GATE_4: Status.FINAL_REVIEW,
}

# Reverse lookup: the gate (if any) that gates exit from a given status.
STATUS_GATE: dict[Status, Gate] = {status: gate for gate, status in GATE_EXIT.items()}


GATE_APPROVES: dict[Gate, str] = {
    Gate.GATE_1: "Angle, working title(s), thumbnail concept, hook/promise",
    Gate.GATE_2: "The final, frozen script",
    Gate.GATE_3: "Camera move + lighting, shot by shot (Fabio's domain)",
    Gate.LIGHT_REVIEW: "Best take per shot; flag re-rolls",
    Gate.GATE_4: "The assembled video + final packaging",
}

GATE_WHY: dict[Gate, str] = {
    Gate.GATE_1: "Protects against expensive work on a weak idea or weak packaging.",
    Gate.GATE_2: "Freezes the foundation everything downstream is built on.",
    Gate.GATE_3: "Fabio's creative ownership — the one thing he never delegates.",
    Gate.LIGHT_REVIEW: "Quality control without heavy process.",
    Gate.GATE_4: "Nothing reaches the public unapproved.",
}


def gate_for_status(status: Status) -> Gate | None:
    """The gate that must be approved to exit `status`, or None if ungated."""
    return STATUS_GATE.get(status)
