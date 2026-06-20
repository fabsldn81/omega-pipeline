"""Shared test scaffolding: an isolated temp repo with real config, mock adapters."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from core.config import load_config
from core.paths import repo_root
from orchestrator.showrunner import Showrunner

_MOCK_OVERRIDES = {"llm": "mock", "store": "local", "higgsfield": "mock", "dry_run": "0"}


class HistoryTubeTestCase(unittest.TestCase):
    """Builds a throwaway repo so tests never touch the real episodes/ or state/."""

    def setUp(self) -> None:
        self._tmp = tempfile.mkdtemp(prefix="ht-test-")
        self.repo = Path(self._tmp)
        # Copy the real config (channel-dna, models, voice-recipe) into the temp repo.
        shutil.copytree(repo_root() / "config", self.repo / "config")
        (self.repo / "episodes").mkdir()
        (self.repo / "state").mkdir()
        self.config = load_config(self.repo, overrides=_MOCK_OVERRIDES)
        self.sr = Showrunner(self.config)

    def tearDown(self) -> None:
        shutil.rmtree(self._tmp, ignore_errors=True)

    def make_episode(self, slug: str = "test-ep", **kwargs):
        kwargs.setdefault("title", "Test Episode")
        kwargs.setdefault("angle", "A test angle.")
        return self.sr.create_episode(slug, **kwargs)
