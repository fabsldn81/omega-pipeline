"""Canned, deterministic creative content for the mock LLM.

Themed around one sample episode — *The Library of Alexandria* — so a fresh
checkout dry-runs into a coherent, inspectable first episode, and the test suite
has stable fixtures. This is NOT production copy; it demonstrates shape and arc.
"""

from __future__ import annotations

from typing import Any

SAMPLE_SLUG = "library-of-alexandria"
SAMPLE_TITLE = "The Library of Alexandria"
SAMPLE_TOPIC = "The Library of Alexandria"
SAMPLE_ANGLE = "Not one fire but a slow forgetting — how the world's memory was really lost."


DOSSIER: dict[str, Any] = {
    "facts": [
        "Founded under the Ptolemies in the 3rd century BCE, attached to the Mouseion.",
        "Aimed to collect a copy of every known scroll; estimates range from 40,000 to 400,000.",
        "Ships entering the harbour were searched for books to copy.",
        "Eratosthenes, a chief librarian, measured the Earth's circumference there.",
        "Its decline was gradual — caesarean fire, edicts, funding loss — not a single blaze.",
    ],
    "timeline": [
        "c.295 BCE — Mouseion and Library established at Alexandria.",
        "3rd c. BCE — Golden age of cataloguing under Zenodotus and Callimachus.",
        "48 BCE — Caesar's fire in the harbour damages stored scrolls.",
        "3rd c. CE — Aurelian's campaigns ravage the royal quarter.",
        "391 CE — Edicts close pagan temples; the Serapeum is destroyed.",
    ],
    "key_figures": [
        "Ptolemy I Soter — founder-patron.",
        "Callimachus — compiler of the Pinakes catalogue.",
        "Eratosthenes — measured the Earth.",
        "Hypatia — later symbol of Alexandrian learning's end.",
    ],
    "hooks": [
        "What if the great loss was not a fire, but neglect?",
        "Every ship searched, every scroll copied — the first total archive.",
        "We measured the planet here, then forgot how.",
    ],
    "controversies": [
        "The 'single catastrophic fire' is a popular myth; sources conflict.",
        "Numbers of scrolls are ancient estimates, wildly inconsistent.",
        "Hypatia's death is often mis-dated and mis-attributed to the Library's fall.",
    ],
    "sources": [
        {"claim": "Founded under the Ptolemies, attached to the Mouseion.",
         "url": "https://www.britannica.com/topic/Library-of-Alexandria"},
        {"claim": "Caesar's 48 BCE fire damaged scrolls in the harbour.",
         "url": "https://www.worldhistory.org/Library_of_Alexandria/"},
        {"claim": "Eratosthenes measured the Earth's circumference at Alexandria.",
         "url": "https://www.britannica.com/biography/Eratosthenes"},
        {"claim": "The Serapeum was destroyed following 391 CE edicts.",
         "url": "https://www.worldhistory.org/Serapeum/"},
    ],
    "demand_signal": (
        "YouTube autocomplete: 'library of alexandria what happened', 'who burned the "
        "library of alexandria'. Google Trends: steady evergreen interest, spikes around "
        "documentary releases. Comparable channels' top videos on the topic clear 1M+ "
        "views. Directional, not precise — fine for a new channel."
    ),
}


PACKAGING: dict[str, Any] = {
    "title_variants": [
        "The Library of Alexandria: The Truth About How It Was Lost",
        "How the World Forgot Everything (The Library of Alexandria)",
        "It Wasn't a Fire — The Real Fall of the Library of Alexandria",
    ],
    "thumbnail_concepts": [
        "A single burning scroll dissolving into drifting ash against a dark harbour — "
        "Chronos Compass glinting faintly in the corner. Big, simple, emotive.",
    ],
    "hook": "Everyone tells you it burned. The truth is stranger — and sadder.",
    "description": (
        "The Library of Alexandria did not die in one night of flame. It died slowly, "
        "in edicts and indifference. David Hattenborg follows the world's first total "
        "archive from its golden age to its long forgetting."
    ),
    "tags": ["library of alexandria", "ancient history", "ancient egypt",
             "history documentary", "lost knowledge"],
    "chapters": [
        "00:00 The promise",
        "01:30 A city that wanted every book",
        "05:00 Measuring the Earth",
        "09:00 The slow forgetting",
        "13:00 What we would save now",
    ],
    "end_screen": "Tease next episode + subscribe; pin the 'real story' Short.",
}


OUTLINE: dict[str, Any] = {
    "logline": "The world built a machine to remember everything — and then forgot how to keep it.",
    "beats": [
        {"name": "Origins", "description": "A dynasty's dream: collect all knowledge in one place."},
        {"name": "Rise", "description": "The Library at its height — Eratosthenes measures the planet."},
        {"name": "The crack", "description": "Fire, war and edicts chip away; no single catastrophe."},
        {"name": "The slow forgetting", "description": "Funding, attention and copyists fade. The real death."},
    ],
    "climax": (
        "The emotional peak: not the flames, but the last scholar who finds the shelves "
        "emptying and realises no one is coming to refill them."
    ),
    "what_next": (
        "Speculative coda: what a 'Library of Alexandria' looks like in 2060 — and what "
        "we would choose to save if we knew it could all be forgotten again."
    ),
    "structure_notes": "Four movements serving the arc; the climax is the realisation, not the fire.",
}


CRITIQUE: dict[str, Any] = {
    "issues": [
        {"area": "accuracy", "severity": "medium",
         "note": "Avoid asserting a single fire; foreground the 'slow forgetting' framing throughout."},
        {"area": "retention", "severity": "low",
         "note": "Cold open must promise the myth-busting payoff in the first 15 seconds."},
        {"area": "climax", "severity": "low",
         "note": "The 'last scholar' beat lands — keep it as the emotional peak, do not bury it."},
        {"area": "advertiser-safety", "severity": "low",
         "note": "Topic is safe; keep Hypatia's death factual and non-sensational."},
    ],
    "verdict": "Strong. Arc builds to a genuine emotional climax. Proceed after minor accuracy framing.",
    "advertiser_safe": True,
    "revisions": [
        "Re-frame any 'the fire' language as 'the fires, and the silence between them'.",
        "Tighten the cold open to a single promise.",
    ],
}


SCRIPT: dict[str, Any] = {
    "hook": (
        "They'll tell you it burned in a single night. That a careless flame swallowed the "
        "greatest library the world had ever known. But that is not what happened. The truth "
        "is quieter — and so much worse."
    ),
    "open_bookend": "David activates the Chronos Compass. \"Sit down. Here comes the story.\"",
    "body": (
        "Picture a city that wanted every book ever written. Not some of them — all of them. "
        "In Alexandria, ships that entered the harbour were searched, their scrolls carried "
        "ashore, copied by hand, the copies returned and the originals kept. This was the "
        "first time humanity tried to hold its entire memory in one room.\n\n"
        "And for a while, it worked. Here a man named Eratosthenes looked at a shadow in a "
        "well and measured the size of the Earth — and got it very nearly right. This was not "
        "a storehouse. It was a machine for understanding the world.\n\n"
        "So how do you lose a thing like that? Not all at once. A fire in the harbour takes "
        "some. A war takes a quarter of the city. An edict closes a temple. And between each "
        "blow — silence. Fewer copyists. Less money. Fewer people who remembered why it "
        "mattered. The scrolls did not all burn. Many simply crumbled, unread, while the "
        "world looked away.\n\n"
        "Imagine the last scholar walking those shelves, finding the gaps widening, and "
        "understanding — slowly, terribly — that no one was coming to fill them again."
    ),
    "close_bookend": (
        "\"The past is fixed. The future is not.\" The Chronos Compass turns. "
        "\"I'll see you in the next story.\""
    ),
    "estimated_seconds": 720,
}


SHOTLIST: dict[str, Any] = {
    "shots": [
        {"id": "S01", "scene": "Open", "beat": "Bookend",
         "visual_subject": "David in his study activating the Chronos Compass",
         "composition": "Medium, slightly low angle", "camera_move": "Slow push-in",
         "lighting": "Warm key, deep shadow", "mood": "Intimate, conspiratorial",
         "transition": "Compass flare to white"},
        {"id": "S02", "scene": "Origins", "beat": "The dream",
         "visual_subject": "Alexandria harbour at dawn, scrolls carried ashore",
         "composition": "Wide establishing", "camera_move": "Drifting crane down",
         "lighting": "Golden hour, long shadows", "mood": "Awe",
         "transition": "Match-cut on a scroll"},
        {"id": "S03", "scene": "Rise", "beat": "Measuring the Earth",
         "visual_subject": "Eratosthenes and a shadow in a well; lines arcing over a globe",
         "composition": "Close on instrument, then wide", "camera_move": "Static then tilt up",
         "lighting": "Hard noon sun", "mood": "Wonder",
         "transition": "Dissolve"},
        {"id": "S04", "scene": "Decline", "beat": "The slow forgetting",
         "visual_subject": "Empty shelves, dust in shafts of light, a single guttering lamp",
         "composition": "Slow track past shelving", "camera_move": "Lateral dolly",
         "lighting": "Cold, low key, single source", "mood": "Grief",
         "transition": "Fade to black"},
        {"id": "S05", "scene": "Close", "beat": "Bookend",
         "visual_subject": "David, Chronos Compass turning, addressing camera",
         "composition": "Medium close", "camera_move": "Slow push-in",
         "lighting": "Warm key returning", "mood": "Resolve, hope",
         "transition": "Compass flare to end card"},
    ],
}


CONTENT: dict[str, Any] = {
    "researcher": {"dossier": DOSSIER, "packaging": PACKAGING},
    "concept": OUTLINE,
    "critic": CRITIQUE,
    "scriptwriter": SCRIPT,
    "director": SHOTLIST,
}
