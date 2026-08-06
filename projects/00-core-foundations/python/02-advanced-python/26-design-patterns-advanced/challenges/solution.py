"""Challenge 26: Design Patterns Advanced — reference solution.

Why these approaches:
- Bronze: __init_subclass__ makes the registry self-maintaining — new
  tools join by declaring a class, with zero registration code.
- Silver: each command captures the state needed to reverse itself at
  CONSTRUCTION time (delete saves the removed text), so undo is exact;
  a history stack + redo stack implements undo/redo; new edits clear
  the redo stack.
- Gold: the dependency arrives through the constructor — production
  and tests use the same Summarizer class with different clients, and
  the llm parameter is the seam the tests verify.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


class Tool:
    registry: dict[str, type["Tool"]] = {}

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.registry[cls.__name__.lower()] = cls

    def run(self, args: dict) -> str:
        raise NotImplementedError


class Calculator(Tool):
    def run(self, args: dict) -> str:
        return str(args.get("a", 0) + args.get("b", 0))


class Search(Tool):
    def run(self, args: dict) -> str:
        return f"results-for:{args.get('q', '')}"


def registry_dispatch(name: str, args: dict) -> str:
    if name not in Tool.registry:
        raise ValueError(f"unknown tool: {name}")
    return Tool.registry[name]().run(args)


class _Insert:
    def __init__(self, buf: list[str], offset: int, text: str) -> None:
        self._buf, self._offset, self._text = buf, offset, text

    def apply(self) -> None:
        self._buf[self._offset:self._offset] = list(self._text)

    def revert(self) -> None:
        del self._buf[self._offset:self._offset + len(self._text)]


class _Delete:
    def __init__(self, buf: list[str], offset: int, count: int) -> None:
        self._buf, self._offset = buf, offset
        self._removed = buf[offset:offset + count]   # captured at construction

    def apply(self) -> None:
        del self._buf[self._offset:self._offset + len(self._removed)]

    def revert(self) -> None:
        self._buf[self._offset:self._offset] = list(self._removed)


class Editor:
    def __init__(self) -> None:
        self._buf: list[str] = []
        self._undo: list = []
        self._redo: list = []

    def insert(self, offset: int, text: str) -> None:
        cmd = _Insert(self._buf, offset, text)
        cmd.apply()
        self._undo.append(cmd)
        self._redo.clear()

    def delete(self, offset: int, count: int) -> None:
        cmd = _Delete(self._buf, offset, count)
        cmd.apply()
        self._undo.append(cmd)
        self._redo.clear()

    def undo(self) -> None:
        if self._undo:
            cmd = self._undo.pop()
            cmd.revert()
            self._redo.append(cmd)

    def redo(self) -> None:
        if self._redo:
            cmd = self._redo.pop()
            cmd.apply()
            self._undo.append(cmd)

    def text(self) -> str:
        return "".join(self._buf)


@runtime_checkable
class LLMClient(Protocol):
    def complete(self, prompt: str, temperature: float = 0.0) -> str:
        ...


class RealLLMClient:
    def complete(self, prompt: str, temperature: float = 0.0) -> str:
        return f"REAL:{prompt[:5]}:{temperature}"


class FakeLLMClient:
    def complete(self, prompt: str, temperature: float = 0.0) -> str:
        return f"FAKE:{prompt[:5]}:{temperature}"


class Summarizer:
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm                 # injected, never constructed here

    def summarize(self, text: str) -> str:
        return self._llm.complete(f"summarize: {text}")
