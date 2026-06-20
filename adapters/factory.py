"""Build the adapter set from a Config (selects mock vs real backends)."""

from __future__ import annotations

from dataclasses import dataclass

from core.config import Config

from .higgsfield import HiggsfieldAdapter, HiggsfieldAPI, MockHiggsfield
from .llm import AnthropicLLM, LLMAdapter, MockLLM
from .store import LocalStore, NotionStore, Store


@dataclass
class Adapters:
    llm: LLMAdapter
    higgsfield: HiggsfieldAdapter
    store: Store


def build_llm(config: Config) -> LLMAdapter:
    if config.llm_backend == "anthropic":
        return AnthropicLLM(model=config.llm_model)
    return MockLLM()


def build_higgsfield(config: Config) -> HiggsfieldAdapter:
    if config.higgsfield_backend == "api":
        return HiggsfieldAPI()
    return MockHiggsfield()


def build_store(config: Config) -> Store:
    if config.store_backend == "notion":
        return NotionStore()
    return LocalStore(paths=config.paths)


def build_adapters(config: Config) -> Adapters:
    return Adapters(
        llm=build_llm(config),
        higgsfield=build_higgsfield(config),
        store=build_store(config),
    )
