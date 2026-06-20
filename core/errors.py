"""Exception hierarchy for the pipeline."""

from __future__ import annotations


class HistoryTubeError(Exception):
    """Base class for every pipeline-specific error."""


class InvalidTransition(HistoryTubeError):
    """Raised when an episode is asked to move to a status it cannot reach."""


class GateNotApproved(HistoryTubeError):
    """Raised when advancing past a gate that Fabio has not approved."""


class AdapterNotConfigured(HistoryTubeError):
    """Raised when a real adapter (LLM / Higgsfield / Notion) lacks its credentials.

    The mock adapters never raise this; it exists so the live adapters fail loudly
    and early on Fabio's machine instead of silently producing nothing.
    """


class ArtifactMissing(HistoryTubeError):
    """Raised when a phase needs an upstream artifact that does not exist yet."""


class ValidationError(HistoryTubeError):
    """Raised when an LLM artifact fails its lightweight schema check."""


class ToolNotFound(HistoryTubeError):
    """Raised when an external binary (ffmpeg/ffprobe/whisper) is required but absent."""
