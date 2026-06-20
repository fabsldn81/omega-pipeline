"""Showrunner orchestration: gates pause, approvals advance, no autonomous publish."""

from __future__ import annotations

from core.errors import GateNotApproved
from core.status import Status
from orchestrator.showrunner import READY_TO_PUBLISH, TERMINAL, WAITING_GATE

from .base import HistoryTubeTestCase


class ManualSteppingTests(HistoryTubeTestCase):
    def test_first_gate_pauses_at_gate_1(self):
        self.make_episode("rome")
        self.sr.step("rome")  # Idea -> Researching
        r = self.sr.step("rome")  # runs Deborah, pauses at Gate 1
        self.assertEqual(r.action, WAITING_GATE)
        self.assertIn("Gate 1", r.gate)
        self.assertEqual(self.sr.get("rome").status, Status.RESEARCHING)

    def test_cannot_step_past_pending_gate(self):
        self.make_episode("rome")
        self.sr.step("rome")
        self.sr.step("rome")  # now waiting at Gate 1
        r = self.sr.step("rome")  # still waiting, no re-run
        self.assertEqual(r.action, WAITING_GATE)

    def test_approve_advances(self):
        self.make_episode("rome")
        self.sr.step("rome")
        self.sr.step("rome")
        r = self.sr.approve("rome")
        self.assertEqual(self.sr.get("rome").status, Status.PACKAGING_LOCKED)
        self.assertIsNone(self.sr.get("rome").pending_gate)

    def test_approve_without_pending_raises(self):
        self.make_episode("rome")
        with self.assertRaises(GateNotApproved):
            self.sr.approve("rome")

    def test_run_stops_at_first_gate_in_manual_mode(self):
        self.make_episode("rome")
        results = self.sr.run("rome", with_shorts=False)
        self.assertEqual(results[-1].action, WAITING_GATE)
        self.assertEqual(self.sr.get("rome").status, Status.RESEARCHING)


class PublishGuardTests(HistoryTubeTestCase):
    def test_manual_step_at_scheduled_refuses_to_publish(self):
        ep = self.make_episode("rome")
        ep.status = Status.SCHEDULED  # jump straight to the publish boundary
        self.sr.store.save(ep)
        r = self.sr.step("rome")  # manual mode
        self.assertEqual(r.action, READY_TO_PUBLISH)
        self.assertEqual(self.sr.get("rome").status, Status.SCHEDULED)  # did NOT advance

    def test_manual_run_reaches_ready_to_publish(self):
        self.make_episode("rome")
        # Approve each gate by hand until we hit the publish boundary.
        guard = 0
        while guard < 40:
            guard += 1
            r = self.sr.step("rome")
            if r.action == WAITING_GATE:
                self.sr.approve("rome")
            elif r.action in (READY_TO_PUBLISH, TERMINAL):
                break
        self.assertEqual(self.sr.get("rome").status, Status.SCHEDULED)
        self.assertEqual(r.action, READY_TO_PUBLISH)
        # Only an explicit publish moves it to Published.
        self.sr.publish("rome")
        self.assertEqual(self.sr.get("rome").status, Status.PUBLISHED)


class AutoRunTests(HistoryTubeTestCase):
    def test_auto_run_reaches_published(self):
        self.make_episode("rome")
        results = self.sr.run("rome", auto_approve=True, with_shorts=True)
        self.assertEqual(self.sr.get("rome").status, Status.PUBLISHED)
        # Every gated transition shows as advanced (auto-approved), none left waiting.
        self.assertFalse(any(r.action == WAITING_GATE for r in results))
