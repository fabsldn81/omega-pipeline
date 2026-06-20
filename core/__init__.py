"""Core domain layer for the History Tube pipeline.

Pure standard-library code: status enum, gate definitions, the per-episode phase
map, the state machine, domain models, configuration loading and errors. Nothing
here touches the network, the filesystem (beyond config reads), or any external
binary — that lives in `adapters/` and `scripts/`.
"""

from .status import Status, STATUS_ORDER
from .gates import Gate, GATE_EXIT, STATUS_GATE
from .phases import Phase, PHASES, phase_for
from .state_machine import StateMachine

__all__ = [
    "Status",
    "STATUS_ORDER",
    "Gate",
    "GATE_EXIT",
    "STATUS_GATE",
    "Phase",
    "PHASES",
    "phase_for",
    "StateMachine",
]
