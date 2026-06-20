"""Adapters: local store round-trip, mock LLM determinism, Higgsfield + Suno mocks."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from adapters.higgsfield import MockHiggsfield
from adapters.llm import MockLLM
from adapters.store import LocalStore
from adapters.suno import ensure_placeholder, ingest_music
from core.errors import ValidationError
from core.models import Episode
from core.paths import Paths
from core.status import Status


class LocalStoreTests(unittest.TestCase):
    def test_round_trip_and_status(self):
        with tempfile.TemporaryDirectory() as d:
            store = LocalStore(db_path=Path(d) / "db.json")
            ep = Episode(slug="x", title="X", angle="a", status=Status.SCRIPTING)
            store.create(ep)
            self.assertTrue(store.exists("x"))
            got = store.get("x")
            self.assertEqual(got.status, Status.SCRIPTING)
            self.assertEqual(got.title, "X")
            got.status = Status.PUBLISHED
            store.save(got)
            self.assertEqual(store.get("x").status, Status.PUBLISHED)
            self.assertEqual(len(store.list()), 1)

    def test_duplicate_create_raises(self):
        with tempfile.TemporaryDirectory() as d:
            store = LocalStore(db_path=Path(d) / "db.json")
            store.create(Episode(slug="x"))
            with self.assertRaises(ValueError):
                store.create(Episode(slug="x"))


class MockLLMTests(unittest.TestCase):
    def test_returns_canned_for_known_tag(self):
        llm = MockLLM()
        out = llm.complete_json("s", "u", tag="researcher", required_keys=["dossier", "packaging"])
        self.assertIn("dossier", out)
        self.assertIn("sources", out["dossier"])

    def test_deterministic(self):
        llm = MockLLM()
        a = llm.complete_json("s", "u", tag="director", required_keys=["shots"])
        b = llm.complete_json("s", "u", tag="director", required_keys=["shots"])
        self.assertEqual(a, b)

    def test_unknown_tag_raises(self):
        with self.assertRaises(ValidationError):
            MockLLM().complete_json("s", "u", tag="nobody", required_keys=[])

    def test_returns_independent_copies(self):
        llm = MockLLM()
        a = llm.complete_json("s", "u", tag="concept", required_keys=["beats"])
        a["beats"].append("mutation")
        b = llm.complete_json("s", "u", tag="concept", required_keys=["beats"])
        self.assertNotIn("mutation", b["beats"])


class HiggsfieldAndSunoTests(unittest.TestCase):
    def test_mock_clip_and_voice(self):
        with tempfile.TemporaryDirectory() as d:
            hf = MockHiggsfield()
            clip = hf.generate_clip("a prompt", Path(d) / "renders" / "s.txt", shot_id="S1", take=1)
            self.assertTrue(clip.exists())
            self.assertIn("MOCK CLIP", clip.read_text(encoding="utf-8"))
            voice = hf.tts("narration", {"preset": "p"}, Path(d) / "voice.txt")
            self.assertIn("MOCK VOICE", voice.read_text(encoding="utf-8"))

    def test_suno_ingest_and_placeholder(self):
        with tempfile.TemporaryDirectory() as d:
            music = Path(d) / "music"
            self.assertEqual(ingest_music(music), [])
            ph = ensure_placeholder(music)
            self.assertTrue(ph.exists())
            (music / "track.mp3").write_text("x", encoding="utf-8")
            found = ingest_music(music)
            self.assertIn(music / "track.mp3", found)


if __name__ == "__main__":
    unittest.main()
