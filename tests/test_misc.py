"""Config loading, crew roster, and the full end-to-end dry run on disk."""

from __future__ import annotations

from agents import all_agent_keys
from agents.crew import CREW, FUNCTION, badge, name_of
from core.config import load_config
from core.models import ART_EDIT_PLAN, ART_SHORTS
from core.status import STATUS_ORDER, Status

from .base import HistoryTubeTestCase


class ConfigTests(HistoryTubeTestCase):
    def test_loads_channel_dna_and_configs(self):
        cfg = load_config(self.repo, overrides={"llm": "mock", "store": "local", "higgsfield": "mock"})
        self.assertIn("David Hattenborg", cfg.channel_dna)
        self.assertIn("dramatic arc", cfg.channel_dna)
        self.assertIn("voice_tts", cfg.models)
        self.assertEqual(cfg.voice_recipe.get("character"), "David Hattenborg")

    def test_default_backends_are_mock(self):
        cfg = load_config(self.repo)
        self.assertTrue(cfg.is_fully_mocked)


class CrewTests(HistoryTubeTestCase):
    def test_roster_covers_every_agent_plus_showrunner(self):
        for key in all_agent_keys():
            self.assertIn(key, CREW)
            self.assertIn(key, FUNCTION)
        self.assertIn("showrunner", CREW)

    def test_requested_names_present(self):
        names = set(CREW.values())
        for n in ("Deborah", "Katusha", "Tainara", "Glesy", "Brenda", "Vitória"):
            self.assertIn(n, names)

    def test_badge_format(self):
        self.assertEqual(name_of("researcher"), "Deborah")
        self.assertEqual(badge("researcher"), "Deborah (Researcher)")


class EndToEndTests(HistoryTubeTestCase):
    def test_full_dry_run_to_published(self):
        self.make_episode("e2e", title="E2E", angle="x")
        results = self.sr.run("e2e", auto_approve=True, with_shorts=True)
        ep = self.sr.get("e2e")

        # Reached the terminal status.
        self.assertEqual(ep.status, Status.PUBLISHED)

        # Visited every status on the way (advanced steps record from->to).
        visited = [r.from_status for r in results if r.from_status] + [Status.PUBLISHED]
        for status in STATUS_ORDER:
            self.assertIn(status, visited, f"never visited {status}")

        # Tangible deliverables exist on disk.
        self.assertIn(ART_EDIT_PLAN, ep.artifacts)
        self.assertIn(ART_SHORTS, ep.artifacts)
        self.assertTrue((self.repo / "episodes" / "e2e" / "final" / "captions.srt").exists())
        self.assertGreaterEqual(len(ep.assets), 8)
        # An audit trail was kept.
        self.assertTrue(ep.history)
