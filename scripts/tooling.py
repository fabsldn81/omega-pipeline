"""Cross-platform helpers for invoking external CLIs (ffmpeg / ffprobe / whisper).

OS-AGNOSTIC MANDATE: no shell strings, no osascript, no POSIX-isms. Commands are
argv lists run without a shell; binaries are located with shutil.which so the same
code works on macOS (dev) and Windows (Fabio).
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from core.errors import ToolNotFound


def find_tool(name: str) -> str | None:
    """Absolute path to a binary on PATH, or None if absent (Windows .exe aware)."""
    return shutil.which(name)


def require_tool(name: str) -> str:
    path = find_tool(name)
    if path is None:
        raise ToolNotFound(
            f"'{name}' was not found on PATH. Install it (Windows: winget/choco) and "
            f"confirm `{name}` runs from a terminal."
        )
    return path


@dataclass
class ToolResult:
    argv: list[str]
    executed: bool
    returncode: int | None = None
    stdout: str = ""
    stderr: str = ""
    note: str = ""

    @property
    def ok(self) -> bool:
        return self.executed and self.returncode == 0


def run(argv: list[str], *, dry_run: bool = False, timeout: int | None = None) -> ToolResult:
    """Run an argv command, or plan it.

    If `dry_run` is set, or the binary is missing, the command is returned as a plan
    (executed=False) instead of being run — so callers degrade gracefully on a
    machine without ffmpeg/whisper, and tests stay hermetic.
    """
    argv = [str(a) for a in argv]
    tool = argv[0] if argv else ""
    if dry_run:
        return ToolResult(argv=argv, executed=False, note="dry-run: not executed")
    if find_tool(tool) is None and not Path(tool).exists():
        return ToolResult(argv=argv, executed=False, note=f"'{tool}' not on PATH: planned only")
    proc = subprocess.run(  # noqa: S603 - argv list, no shell
        argv, capture_output=True, text=True, timeout=timeout
    )
    return ToolResult(
        argv=argv,
        executed=True,
        returncode=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )
