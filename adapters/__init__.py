"""External-world adapters: LLM, Higgsfield, Suno, and the episode store.

Every adapter has a mock/local default so the pipeline runs end-to-end with no
keys, no network and no external binaries. Real backends are opt-in via Config.
"""

from .factory import Adapters, build_adapters, build_higgsfield, build_llm, build_store

__all__ = [
    "Adapters",
    "build_adapters",
    "build_llm",
    "build_higgsfield",
    "build_store",
]
