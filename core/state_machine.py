"""The status state machine: the rules for moving an episode forward.

Pure logic, no I/O. The Showrunner uses this to decide what may happen next; it
never lets an episode skip a status or cross a gate without approval.
"""

from __future__ import annotations

from .errors import GateNotApproved, InvalidTransition
from .gates import Gate, gate_for_status
from .phases import Phase, phase_for
from .status import Status, next_in_order, status_index


class StateMachine:
    """Stateless helper that enforces the ordered, gated status progression."""

    # --- queries -----------------------------------------------------------

    def phase(self, status: Status) -> Phase:
        return phase_for(status)

    def next_status(self, status: Status) -> Status | None:
        return next_in_order(status)

    def gate(self, status: Status) -> Gate | None:
        """The gate that must be approved to exit `status` (None if ungated)."""
        return gate_for_status(status)

    def is_gated(self, status: Status) -> bool:
        return gate_for_status(status) is not None

    def is_terminal(self, status: Status) -> bool:
        return next_in_order(status) is None

    def is_fabio_owned(self, status: Status) -> bool:
        return phase_for(status).fabio_owned

    # --- transitions -------------------------------------------------------

    def can_advance(self, status: Status, *, gate_approved: bool) -> bool:
        if self.is_terminal(status):
            return False
        if self.is_gated(status) and not gate_approved:
            return False
        return True

    def advance(self, status: Status, *, gate_approved: bool) -> Status:
        """Return the next status, enforcing the gate.

        Raises InvalidTransition at the terminal status and GateNotApproved when a
        gate guards the exit and has not been approved.
        """
        nxt = next_in_order(status)
        if nxt is None:
            raise InvalidTransition(f"{status} is terminal; nothing to advance to.")
        gate = gate_for_status(status)
        if gate is not None and not gate_approved:
            raise GateNotApproved(
                f"Cannot leave {status}: {gate} must be approved first."
            )
        return nxt

    def assert_valid_order(self, src: Status, dst: Status) -> None:
        """Guard against out-of-order writes (e.g. a buggy adapter)."""
        if status_index(dst) != status_index(src) + 1:
            raise InvalidTransition(
                f"{src} -> {dst} is not a single forward step."
            )
