"""FFmpeg/Whisper command builders — exact argv, no binaries required."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import ffmpeg_ops as ff
from scripts.tooling import run
from scripts.whisper_ops import synthesize_srt_from_text, transcribe_srt_cmd


class FfmpegBuilderTests(unittest.TestCase):
    def test_assembly_concat_count(self):
        argv = ff.assembly_cmd([Path("a.mp4"), Path("b.mp4"), Path("c.mp4")], Path("out.mp4"))
        joined = " ".join(argv)
        self.assertIn("concat=n=3:v=1:a=0[v]", joined)
        self.assertIn("[v]", argv)
        self.assertEqual(argv[0], "ffmpeg")

    def test_assembly_requires_clips(self):
        with self.assertRaises(ValueError):
            ff.assembly_cmd([], Path("out.mp4"))

    def test_loudnorm_targets_minus_14(self):
        argv = ff.loudnorm_apply_cmd(Path("v.wav"), Path("v.norm.wav"))
        af = argv[argv.index("-af") + 1]
        self.assertIn("loudnorm=I=-14.0", af)
        self.assertIn("TP=-1.5", af)

    def test_loudnorm_measure_is_json(self):
        argv = ff.loudnorm_measure_cmd(Path("v.wav"))
        self.assertIn("print_format=json", " ".join(argv))

    def test_duck_uses_sidechain(self):
        argv = ff.duck_cmd(Path("voice.wav"), Path("music.wav"), Path("mix.wav"), duration=100.0)
        fg = argv[argv.index("-filter_complex") + 1]
        self.assertIn("sidechaincompress", fg)
        self.assertIn("afade=t=in", fg)
        self.assertIn("afade=t=out", fg)

    def test_reframe_is_vertical_9x16(self):
        argv = ff.reframe_vertical_cmd(Path("in.mp4"), Path("out.mp4"))
        vf = argv[argv.index("-vf") + 1]
        self.assertIn("crop=1080:1920", vf)

    def test_burn_captions_uses_subtitles_filter(self):
        argv = ff.burn_captions_cmd(Path("cut.mp4"), Path("c.srt"), Path("o.mp4"))
        self.assertIn("subtitles=", argv[argv.index("-vf") + 1])


class WhisperTests(unittest.TestCase):
    def test_transcribe_cmd_emits_srt(self):
        argv = transcribe_srt_cmd(Path("a.wav"), Path("out"))
        self.assertEqual(argv[0], "whisper")
        self.assertIn("--output_format", argv)
        self.assertEqual(argv[argv.index("--output_format") + 1], "srt")

    def test_synthesize_srt_format(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "c.srt"
            synthesize_srt_from_text("One sentence. Two sentence! Three?", out, total_seconds=30)
            text = out.read_text(encoding="utf-8")
        self.assertIn("-->", text)
        self.assertIn("00:00:00,000", text)
        self.assertTrue(text.lstrip().startswith("1"))


class ToolingTests(unittest.TestCase):
    def test_dry_run_plans_only(self):
        res = run(["ffmpeg", "-version"], dry_run=True)
        self.assertFalse(res.executed)
        self.assertEqual(res.argv[0], "ffmpeg")

    def test_missing_binary_plans_only(self):
        res = run(["definitely-not-a-real-binary-xyz", "--help"])
        self.assertFalse(res.executed)
        self.assertIn("not on PATH", res.note)


if __name__ == "__main__":
    unittest.main()
