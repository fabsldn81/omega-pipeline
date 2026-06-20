"""State machine + gate wiring."""

from __future__ import annotations

import unittest

from core.errors import GateNotApproved, InvalidTransition
from core.gates import GATE_EXIT, STATUS_GATE, Gate, gate_for_status
from core.state_machine import StateMachine
from core.status import STATUS_ORDER, Status


class StatusOrderTests(unittest.TestCase):
    def test_twelve_statuses_in_plan_order(self):
        self.assertEqual(len(STATUS_ORDER), 12)
        self.assertEqual(STATUS_ORDER[0], Status.IDEA)
        self.assertEqual(STATUS_ORDER[-1], Status.PUBLISHED)
        # Final-review sits between Editing and Scheduled (the reconciled mapping).
        self.assertEqual(
            STATUS_ORDER[STATUS_ORDER.index(Status.EDITING) + 1], Status.FINAL_REVIEW
        )
        self.assertEqual(
            STATUS_ORDER[STATUS_ORDER.index(Status.FINAL_REVIEW) + 1], Status.SCHEDULED
        )


class GateMappingTests(unittest.TestCase):
    def test_gate_exit_targets(self):
        self.assertEqual(GATE_EXIT[Gate.GATE_1], Status.RESEARCHING)
        self.assertEqual(GATE_EXIT[Gate.GATE_2], Status.SCRIPTING)
        self.assertEqual(GATE_EXIT[Gate.GATE_3], Status.DIRECTION)
        self.assertEqual(GATE_EXIT[Gate.LIGHT_REVIEW], Status.GENERATING)
        # Gate 4 gates exit from Final-review, not Editing.
        self.assertEqual(GATE_EXIT[Gate.GATE_4], Status.FINAL_REVIEW)

    def test_status_gate_is_reverse_of_gate_exit(self):
        for gate, status in GATE_EXIT.items():
            self.assertEqual(STATUS_GATE[status], gate)
            self.assertEqual(gate_for_status(status), gate)

    def test_ungated_statuses_have_no_gate(self):
        for status in (Status.IDEA, Status.PACKAGING_LOCKED, Status.SCRIPT_LOCKED,
                       Status.DIRECTION_LOCKED, Status.EDITING, Status.SCHEDULED):
            self.assertIsNone(gate_for_status(status))


class TransitionTests(unittest.TestCase):
    def setUp(self):
        self.sm = StateMachine()

    def test_advance_ungated(self):
        self.assertEqual(self.sm.advance(Status.IDEA, gate_approved=False), Status.RESEARCHING)

    def test_gated_blocks_without_approval(self):
        with self.assertRaises(GateNotApproved):
            self.sm.advance(Status.RESEARCHING, gate_approved=False)

    def test_gated_passes_with_approval(self):
        self.assertEqual(
            self.sm.advance(Status.RESEARCHING, gate_approved=True), Status.PACKAGING_LOCKED
        )

    def test_terminal_cannot_advance(self):
        self.assertTrue(self.sm.is_terminal(Status.PUBLISHED))
        with self.assertRaises(InvalidTransition):
            self.sm.advance(Status.PUBLISHED, gate_approved=True)

    def test_full_forward_path_with_approvals(self):
        status = Status.IDEA
        seen = [status]
        while not self.sm.is_terminal(status):
            status = self.sm.advance(status, gate_approved=True)
            seen.append(status)
        self.assertEqual(seen, STATUS_ORDER)


if __name__ == "__main__":
    unittest.main()
