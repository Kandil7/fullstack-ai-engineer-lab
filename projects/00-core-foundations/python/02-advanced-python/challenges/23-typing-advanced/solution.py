"""Challenge 23: Typing Advanced — reference solution.

Why these approaches:
- Bronze: inspect.signature is the runtime window into a callable;
  annotations are strings, so we stringify them honestly.
- Silver: parameter NAMES are the robust runtime signal — this is what
  runtime_checkable cannot verify.
- Gold: the protocol is the structural contract; the explicit signature
  check closes the shallow-isinstance gap; Result[T] carries typed
  success/failure through the seam.
"""

from __future__ import annotations

import inspect
from typing import Generic, Protocol, TypeVar, runtime_checkable

T = TypeVar("T")


def build_schema(func) -> dict:
    """Introspect a callable into {name, params, return}."""
    sig = inspect.signature(func)
    params = [(p.name, p.default if p.default is not inspect.Parameter.empty else None)
              for p in sig.parameters.values()]
    return {
        "name": func.__name__,
        "params": params,
        "return": str(sig.return_annotation),
    }


def signature_matches(func, expected: list[str]) -> bool:
    """Exact, ordered parameter-name match."""
    actual = [p.name for p in inspect.signature(func).parameters.values()]
    return actual == expected


@runtime_checkable
class Retriever(Protocol):
    def retrieve(self, query: str, k: int = 5) -> list[str]:
        ...


class QdrantRetriever:
    def retrieve(self, query: str, k: int = 5) -> list[str]:
        return [f"qdrant:{query[:8]}-{i}" for i in range(k)]


class ChromaRetriever:
    def retrieve(self, query: str, k: int = 5) -> list[str]:
        return [f"chroma:{query[:8]}-{i}" for i in range(k)]


class WrongSignatureRetriever:
    def retrieve(self, top_k: int) -> list[str]:
        return ["x"] * top_k


class Result(Generic[T]):
    """Typed success/failure carrier."""

    def __init__(self, ok: bool, value: T | None, error: str | None = None) -> None:
        self.ok = ok
        self.value = value
        self.error = error

    @classmethod
    def success(cls, value: T) -> "Result[T]":
        return cls(True, value)

    @classmethod
    def failure(cls, error: str) -> "Result[T]":
        return cls(False, None, error)


def verify_retriever(obj) -> bool:
    """isinstance is shallow; the signature check is the real gate."""
    if not isinstance(obj, Retriever):
        return False
    return signature_matches(obj.retrieve, ["query", "k"])


def safe_search(retriever, query: str, k: int = 5) -> Result[list[str]]:
    if not verify_retriever(retriever):
        return Result.failure("not a valid retriever")
    return Result.success(retriever.retrieve(query, k))
