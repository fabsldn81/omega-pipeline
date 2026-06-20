"""Tiny JSON helpers shared across the pipeline (stdlib only)."""

from __future__ import annotations

import json
from dataclasses import is_dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Any


def to_jsonable(value: Any) -> Any:
    """Convert dataclasses / enums / nested containers into JSON-safe primitives."""
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return {k: to_jsonable(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {k: to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(v) for v in value]
    if isinstance(value, Path):
        return str(value)
    return value


def dumps(value: Any) -> str:
    return json.dumps(to_jsonable(value), indent=2, ensure_ascii=False)


def save_json(path: Path, value: Any) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dumps(value) + "\n", encoding="utf-8")
    return path


def load_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def require_keys(obj: Any, keys: list[str], *, context: str) -> None:
    """Lightweight schema check for LLM-produced dicts.

    Raises core.errors.ValidationError if `obj` is not a dict or misses a key.
    """
    from .errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError(f"{context}: expected an object, got {type(obj).__name__}")
    missing = [k for k in keys if k not in obj]
    if missing:
        raise ValidationError(f"{context}: missing keys {missing}")
