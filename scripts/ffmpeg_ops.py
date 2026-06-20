"""FFmpeg command builders + runners for the editor (Cleidiane) and shorts (Jucilene).

Each `*_cmd` function is PURE — it returns an argv list and runs nothing, so the test
suite verifies the exact ffmpeg invocation without needing ffmpeg installed. The
`run_*` wrappers execute the command when ffmpeg is present (else they plan it).

Audio rule (Section 6): voice and music are SEPARATE stems. Assembly handles picture;
`duck_cmd` mixes the stems with music ducked under the narration.
Loudness target: -14 LUFS (YouTube reference).
"""

from __future__ import annotations

from pathlib import Path

from .tooling import ToolResult, run

FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"

TARGET_LUFS = -14.0
TARGET_TP = -1.5  # true peak ceiling
TARGET_LRA = 11.0

SHORTS_W = 1080
SHORTS_H = 1920  # 9:16


def probe_cmd(media: Path) -> list[str]:
    return [
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration:stream=width,height,codec_type",
        "-of", "json", str(media),
    ]


def assembly_cmd(clips: list[Path], out: Path) -> list[str]:
    """Concatenate picture clips in order to a single silent video track.

    Uses the concat filter (re-encode) so heterogeneous AI clips join cleanly.
    """
    if not clips:
        raise ValueError("assembly_cmd needs at least one clip.")
    argv: list[str] = [FFMPEG, "-y"]
    for clip in clips:
        argv += ["-i", str(clip)]
    n = len(clips)
    streams = "".join(f"[{i}:v:0]" for i in range(n))
    filtergraph = f"{streams}concat=n={n}:v=1:a=0[v]"
    argv += [
        "-filter_complex", filtergraph,
        "-map", "[v]",
        "-pix_fmt", "yuv420p",
        str(out),
    ]
    return argv


def loudnorm_measure_cmd(audio: Path) -> list[str]:
    """First pass: measure loudness, print JSON (parse for the second pass)."""
    return [
        FFMPEG, "-y", "-i", str(audio),
        "-af",
        f"loudnorm=I={TARGET_LUFS}:TP={TARGET_TP}:LRA={TARGET_LRA}:print_format=json",
        "-f", "null", "-",
    ]


def loudnorm_apply_cmd(audio: Path, out: Path, measured: dict | None = None) -> list[str]:
    """Second pass: apply normalisation to -14 LUFS, optionally with measured values."""
    af = f"loudnorm=I={TARGET_LUFS}:TP={TARGET_TP}:LRA={TARGET_LRA}"
    if measured:
        af += (
            f":measured_I={measured.get('input_i')}"
            f":measured_TP={measured.get('input_tp')}"
            f":measured_LRA={measured.get('input_lra')}"
            f":measured_thresh={measured.get('input_thresh')}"
            ":linear=true"
        )
    return [FFMPEG, "-y", "-i", str(audio), "-af", af, str(out)]


def duck_cmd(
    voice: Path,
    music: Path,
    out: Path,
    *,
    fade_in: float = 1.0,
    fade_out: float = 2.0,
    duration: float | None = None,
) -> list[str]:
    """Mix voice + music with the music ducked under the narration (sidechain).

    Music is side-chain compressed by the voice, then both are summed; fades top and
    tail the music bed.
    """
    fade = f"afade=t=in:st=0:d={fade_in}"
    if duration is not None:
        fade += f",afade=t=out:st={max(0.0, duration - fade_out)}:d={fade_out}"
    filtergraph = (
        "[1:a]" + fade + "[bed];"
        "[bed][0:a]sidechaincompress=threshold=0.05:ratio=8:attack=5:release=250[ducked];"
        "[0:a][ducked]amix=inputs=2:duration=longest:normalize=0[mix]"
    )
    return [
        FFMPEG, "-y",
        "-i", str(voice),
        "-i", str(music),
        "-filter_complex", filtergraph,
        "-map", "[mix]",
        str(out),
    ]


def mux_cmd(video: Path, audio: Path, out: Path) -> list[str]:
    """Combine the assembled picture with the final mixed audio."""
    return [
        FFMPEG, "-y",
        "-i", str(video),
        "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-shortest",
        str(out),
    ]


def bookend_concat_cmd(open_clip: Path, body: Path, close_clip: Path, out: Path) -> list[str]:
    """Wrap the body with David's open/close bookend clips."""
    return assembly_cmd([open_clip, body, close_clip], out)


def burn_captions_cmd(video: Path, srt: Path, out: Path) -> list[str]:
    """Burn an SRT subtitle track into the picture."""
    # ffmpeg subtitles filter takes a path; forward slashes are safest cross-platform.
    srt_path = str(srt).replace("\\", "/")
    return [
        FFMPEG, "-y", "-i", str(video),
        "-vf", f"subtitles='{srt_path}'",
        str(out),
    ]


def reframe_vertical_cmd(video: Path, out: Path, *, width: int = SHORTS_W, height: int = SHORTS_H) -> list[str]:
    """Re-frame a landscape long-form clip to vertical 9:16 for a Short."""
    vf = (
        f"scale={width}:-2:force_original_aspect_ratio=increase,"
        f"crop={width}:{height}"
    )
    return [FFMPEG, "-y", "-i", str(video), "-vf", vf, str(out)]


# --- runners -------------------------------------------------------------------

def run_cmd(argv: list[str], *, dry_run: bool = False) -> ToolResult:
    return run(argv, dry_run=dry_run)
