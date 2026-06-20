"""Each agent produces a valid artifact when driven through the pipeline (mock)."""

from __future__ import annotations

from agents import all_agent_keys, get_agent
from agents.base import AgentContext
from agents.crew import CREW
from core.jsonio import load_json
from core.models import (
    ART_CRITIQUE,
    ART_DOSSIER,
    ART_EDIT_PLAN,
    ART_OUTLINE,
    ART_PACKAGING,
    ART_PROMPTS,
    ART_SCRIPT,
    ART_SHORTS,
    ART_SHOTLIST,
)

from .base import HistoryTubeTestCase


class WritingAgentTests(HistoryTubeTestCase):
    def _ctx(self, ep) -> AgentContext:
        return AgentContext(episode=ep, config=self.config, adapters=self.sr.adapters)

    def test_researcher_writes_dossier_and_packaging(self):
        ep = self.make_episode()
        get_agent("researcher").run(self._ctx(ep))
        self.assertIn(ART_DOSSIER, ep.artifacts)
        self.assertIn(ART_PACKAGING, ep.artifacts)
        dossier = load_json(self.repo / ep.artifacts[ART_DOSSIER])
        self.assertTrue(dossier["sources"])
        # Every source is a claim->url pair.
        for src in dossier["sources"]:
            self.assertIn("claim", src)
            self.assertIn("url", src)

    def test_pipeline_artifacts_chain(self):
        ep = self.make_episode()
        for key in ("researcher", "concept", "critic", "scriptwriter", "director", "prompt_engineer"):
            get_agent(key).run(self._ctx(ep))
        for art in (ART_DOSSIER, ART_PACKAGING, ART_OUTLINE, ART_CRITIQUE, ART_SCRIPT, ART_SHOTLIST, ART_PROMPTS):
            self.assertIn(art, ep.artifacts, f"missing {art}")
        shots = load_json(self.repo / ep.artifacts[ART_SHOTLIST])["shots"]
        self.assertTrue(shots)
        # Bookend shots exist (David only at open + close).
        bookends = [s for s in shots if s["beat"] == "Bookend"]
        self.assertGreaterEqual(len(bookends), 2)
        # Prompt engineer attached prompts to every shot.
        for s in shots:
            self.assertTrue(s["prompts"])

    def test_critic_reports_advertiser_safety(self):
        ep = self.make_episode()
        get_agent("researcher").run(self._ctx(ep))
        get_agent("concept").run(self._ctx(ep))
        get_agent("critic").run(self._ctx(ep))
        critique = load_json(self.repo / ep.artifacts[ART_CRITIQUE])
        self.assertIn("advertiser_safe", critique)
        self.assertIsInstance(critique["advertiser_safe"], bool)


class RenderEditShortsTests(HistoryTubeTestCase):
    def _full(self, ep):
        ctx = AgentContext(episode=ep, config=self.config, adapters=self.sr.adapters)
        for key in ("researcher", "concept", "critic", "scriptwriter", "director",
                    "prompt_engineer", "render", "editor", "shorts"):
            get_agent(key).run(ctx)
        return ep

    def test_render_creates_separate_stems(self):
        ep = self._full(self.make_episode())
        types = {a.type for a in ep.assets}
        self.assertIn("clip", types)
        self.assertIn("voice", types)
        self.assertIn("music", types)  # voice and music are SEPARATE assets

    def test_editor_plan_targets_minus_14_and_writes_captions(self):
        ep = self._full(self.make_episode())
        plan = load_json(self.repo / ep.artifacts[ART_EDIT_PLAN])
        self.assertEqual(plan["target_lufs"], -14.0)
        self.assertTrue((self.repo / plan["captions"]).exists())

    def test_shorts_plan_is_vertical(self):
        ep = self._full(self.make_episode())
        shorts = load_json(self.repo / ep.artifacts[ART_SHORTS])["shorts"]
        self.assertTrue(shorts)
        for s in shorts:
            self.assertIn("crop=1080:1920", " ".join(s["reframe_cmd"]))


class RegistryTests(HistoryTubeTestCase):
    def test_every_agent_has_a_crew_name(self):
        for key in all_agent_keys():
            self.assertIn(key, CREW)
            self.assertEqual(get_agent(key).key, key)
            self.assertTrue(get_agent(key).name)
