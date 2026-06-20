"""LLM adapter: the brain behind the writing agents (Deborah, Katusha, Tainara, Glesy, Brenda).

Two implementations:
  * MockLLM       — deterministic canned content (default; no keys, no network).
  * AnthropicLLM  — real Claude calls (opt-in via HT_LLM=anthropic + ANTHROPIC_API_KEY).

Agents ask for structured JSON via `complete_json(..., tag=..., required_keys=...)`.
The `tag` selects canned content for the mock; the real adapter ignores it and uses
the system/user prompts the agent supplies.
"""

from __future__ import annotations

import copy
import json
from abc import ABC, abstractmethod
from typing import Any

from core.errors import AdapterNotConfigured, ValidationError
from core.jsonio import require_keys

from ._mock_content import CONTENT


class LLMAdapter(ABC):
    name = "llm"

    @abstractmethod
    def complete_json(
        self,
        system: str,
        user: str,
        *,
        tag: str,
        required_keys: list[str],
        json_schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        ...

    @abstractmethod
    def complete_text(self, system: str, user: str) -> str:
        ...


class MockLLM(LLMAdapter):
    """Returns deterministic canned artifacts keyed by agent tag."""

    name = "mock"

    def __init__(self, content: dict[str, Any] | None = None) -> None:
        self._content = content if content is not None else CONTENT

    def complete_json(
        self,
        system: str,
        user: str,
        *,
        tag: str,
        required_keys: list[str],
        json_schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        data = self._content.get(tag)
        if data is None:
            raise ValidationError(f"MockLLM has no canned content for tag '{tag}'.")
        data = copy.deepcopy(data)
        require_keys(data, required_keys, context=f"MockLLM[{tag}]")
        return data

    def complete_text(self, system: str, user: str) -> str:
        return f"(mock completion)\n{user[:200]}"


class AnthropicLLM(LLMAdapter):
    """Real Claude calls. Optional — only used when HT_LLM=anthropic.

    Forces JSON-only output and validates the required keys, retrying once on a
    parse/validation miss. Kept deliberately small; swap in the SDK's structured
    output / tool-use if you want stricter guarantees.
    """

    name = "anthropic"

    def __init__(self, model: str = "claude-opus-4-8", api_key: str | None = None) -> None:
        self.model = model
        try:
            import anthropic  # noqa: F401
        except ImportError as exc:  # pragma: no cover - exercised only on real runs
            raise AdapterNotConfigured(
                "The 'anthropic' package is not installed. `pip install anthropic` "
                "or set HT_LLM=mock."
            ) from exc
        import os

        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise AdapterNotConfigured(
                "ANTHROPIC_API_KEY is not set. Export it or set HT_LLM=mock."
            )
        from anthropic import Anthropic

        self._client = Anthropic(api_key=key)

    def _call(self, system: str, user: str) -> str:  # pragma: no cover - network
        msg = self._client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(block.text for block in msg.content if block.type == "text")

    def complete_json(
        self,
        system: str,
        user: str,
        *,
        tag: str,
        required_keys: list[str],
        json_schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]:  # pragma: no cover - network
        instruction = (
            "\n\nReturn ONLY a single JSON object, no prose, no code fences. "
            f"It must contain these top-level keys: {required_keys}."
        )
        for attempt in range(2):
            raw = self._call(system, user + instruction)
            raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            try:
                data = json.loads(raw)
                require_keys(data, required_keys, context=f"AnthropicLLM[{tag}]")
                return data
            except (json.JSONDecodeError, ValidationError):
                if attempt == 1:
                    raise
        raise ValidationError(f"AnthropicLLM[{tag}] failed to produce valid JSON.")

    def complete_text(self, system: str, user: str) -> str:  # pragma: no cover - network
        return self._call(system, user)
