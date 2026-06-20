"""OS-agnostic media tooling: FFmpeg + Whisper wrappers.

Pure command-builders (testable without the binaries) plus runners that execute when
ffmpeg/whisper are on PATH and otherwise return the planned command. No osascript, no
shell strings — Windows-safe by construction.
"""

from . import ffmpeg_ops, whisper_ops
from .tooling import ToolResult, find_tool, require_tool, run

__all__ = ["ffmpeg_ops", "whisper_ops", "ToolResult", "find_tool", "require_tool", "run"]
