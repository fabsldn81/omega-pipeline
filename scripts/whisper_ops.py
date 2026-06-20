"""Whisper caption builders + a dependency-free SRT synthesiser.

`transcribe_srt_cmd` builds the real Whisper CLI invocation (tested without Whisper
installed). `synthesize_srt_from_text` writes a naive, evenly-timed SRT from the
script so the dry-run still produces captions with no Whisper and no audio.
"""

from __future__ import annotations

from pathlib import Path

WHISPER = "whisper"


def transcribe_srt_cmd(
    audio: Path,
    out_dir: Path,
    *,
    model: str = "small",
    language: str = "en",
) -> list[str]:
    """Build the Whisper CLI command to emit an .srt next to the audio."""
    return [
        WHISPER, str(audio),
        "--model", model,
        "--language", language,
        "--output_format", "srt",
        "--output_dir", str(out_dir),
    ]


def _fmt_ts(seconds: float) -> str:
    if seconds < 0:
        seconds = 0.0
    ms = int(round((seconds - int(seconds)) * 1000))
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def synthesize_srt_from_text(text: str, out_path: Path, *, total_seconds: float = 720.0) -> Path:
    """Write a simple SRT by splitting text into sentence-ish cues, evenly timed.

    A stand-in for Whisper on a machine with no audio/Whisper — enough to prove the
    caption path end-to-end. Replace with real Whisper output in production.
    """
    import re

    chunks = [c.strip() for c in re.split(r"(?<=[.!?])\s+", text.replace("\n", " ")) if c.strip()]
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if not chunks:
        out_path.write_text("", encoding="utf-8")
        return out_path
    per = total_seconds / len(chunks)
    lines: list[str] = []
    for i, chunk in enumerate(chunks):
        start = i * per
        end = (i + 1) * per
        lines.append(str(i + 1))
        lines.append(f"{_fmt_ts(start)} --> {_fmt_ts(end)}")
        lines.append(chunk)
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path
