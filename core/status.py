"""The Episodes.Status enum — the phase pointer for every episode.

Reproduced exactly from the build plan Section 5 (twelve values, in order). Notion
is the source of truth for this field at run time; this enum is the canonical
in-code representation.
"""

from __future__ import annotations

from enum import Enum


class Status(str, Enum):
    IDEA = "Idea"
    RESEARCHING = "Researching"
    PACKAGING_LOCKED = "Packaging-locked"
    SCRIPTING = "Scripting"
    SCRIPT_LOCKED = "Script-locked"
    DIRECTION = "Direction"
    DIRECTION_LOCKED = "Direction-locked"
    GENERATING = "Generating"
    EDITING = "Editing"
    FINAL_REVIEW = "Final-review"
    SCHEDULED = "Scheduled"
    PUBLISHED = "Published"

    def __str__(self) -> str:  # so f"{status}" prints the Notion label
        return self.value


# Canonical ordering. Index in this list == position on the long-form's main track.
STATUS_ORDER: list[Status] = [
    Status.IDEA,
    Status.RESEARCHING,
    Status.PACKAGING_LOCKED,
    Status.SCRIPTING,
    Status.SCRIPT_LOCKED,
    Status.DIRECTION,
    Status.DIRECTION_LOCKED,
    Status.GENERATING,
    Status.EDITING,
    Status.FINAL_REVIEW,
    Status.SCHEDULED,
    Status.PUBLISHED,
]

TERMINAL: Status = Status.PUBLISHED


def status_index(status: Status) -> int:
    return STATUS_ORDER.index(status)


def next_in_order(status: Status) -> Status | None:
    """The status immediately after `status`, or None if terminal."""
    i = status_index(status)
    if i + 1 >= len(STATUS_ORDER):
        return None
    return STATUS_ORDER[i + 1]
