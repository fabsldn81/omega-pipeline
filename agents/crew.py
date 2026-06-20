"""David's crew — the personas behind each function (naming is Fabio's creative act).

Function key -> persona name. Renaming here renames the agent everywhere (CLI banners,
logs, skills). Function labels remain the contract; the names are the flavour.
"""

from __future__ import annotations

CREW: dict[str, str] = {
    "showrunner": "Vitória",       # orchestrator
    "researcher": "Deborah",       # Phase 1 — research + demand validation
    "concept": "Katusha",          # Phase 2 — dramatic-arc outline
    "critic": "Tainara",           # Phase 3 — adversarial review
    "scriptwriter": "Glesy",       # Phase 4 — the locked script
    "director": "Brenda",          # Phase 5 — draft shot list
    "prompt_engineer": "Sabrina",  # Phase 6 — model-ready prompts
    "render": "Wanessa",           # Phase 7 — clips + voice + music
    "editor": "Cleidiane",         # Phase 8 — the cut
    "shorts": "Jucilene",          # Phase 9 — vertical Shorts
}

FUNCTION: dict[str, str] = {
    "showrunner": "Showrunner / orchestrator",
    "researcher": "Researcher",
    "concept": "Concept writer",
    "critic": "Adversarial critic",
    "scriptwriter": "Scriptwriter",
    "director": "Director-assistant",
    "prompt_engineer": "Prompt engineer",
    "render": "Render orchestrator",
    "editor": "Editor",
    "shorts": "Shorts cutter",
}


def name_of(key: str) -> str:
    return CREW.get(key, key)


def badge(key: str) -> str:
    """e.g. 'Deborah (Researcher)'."""
    return f"{CREW.get(key, key)} ({FUNCTION.get(key, key)})"
