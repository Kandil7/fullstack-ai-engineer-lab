"""Challenge 26: Design Patterns Advanced — starter (signatures only)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


class Tool:
    registry: dict[str, type["Tool"]] = {}

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        pass  # TODO: register cls in cls.registry under its lowercase name

    def run(self, args: dict) -> str:
        raise NotImplementedError


class Calculator(Tool):
    def run(self, args: dict) -> str:
        raise NotImplementedError


class Search(Tool):
    def run(self, args: dict) -> str:
        raise NotImplementedError


def registry_dispatch(name: str, args: dict) -> str:
    raise NotImplementedError


class Editor:
    def insert(self, offset: int, text: str) -> None:
        raise NotImplementedError

    def delete(self, offset: int, count: int) -> None:
        raise NotImplementedError

    def undo(self) -> None:
        raise NotImplementedError

    def redo(self) -> None:
        raise NotImplementedError

    def text(self) -> str:
        raise NotImplementedError


@runtime_checkable
class LLMClient(Protocol):
    def complete(self, prompt: str, temperature: float = 0.0) -> str:
        ...


class RealLLMClient:
    def complete(self, prompt: str, temperature: float = 0.0) -> str:
        raise NotImplementedError


class FakeLLMClient:
    def complete(self, prompt: str, temperature: float = 0.0) -> str:
        raise NotImplementedError


class Summarizer:
    def __init__(self, llm: LLMClient) -> None:
        raise NotImplementedError

    def summarize(self, text: str) -> str:
        raise NotImplementedError
