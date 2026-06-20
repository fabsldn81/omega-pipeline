"""The sub-agent registry — David's crew, keyed by function.

Agents are imported lazily so importing the package stays cheap and free of cycles.
"""

from __future__ import annotations

import importlib

from .base import Agent, AgentContext
from .crew import CREW, FUNCTION, badge, name_of

_AGENT_MODULES: dict[str, str] = {
    "researcher": "agents.researcher.agent",
    "concept": "agents.concept.agent",
    "critic": "agents.critic.agent",
    "scriptwriter": "agents.scriptwriter.agent",
    "director": "agents.director.agent",
    "prompt_engineer": "agents.prompt_engineer.agent",
    "render": "agents.render.agent",
    "editor": "agents.editor.agent",
    "shorts": "agents.shorts.agent",
}


def get_agent(key: str) -> Agent:
    if key not in _AGENT_MODULES:
        raise KeyError(f"Unknown agent '{key}'. Known: {list(_AGENT_MODULES)}")
    module = importlib.import_module(_AGENT_MODULES[key])
    return module.AGENT


def all_agent_keys() -> list[str]:
    return list(_AGENT_MODULES)


__all__ = [
    "Agent",
    "AgentContext",
    "CREW",
    "FUNCTION",
    "badge",
    "name_of",
    "get_agent",
    "all_agent_keys",
]
