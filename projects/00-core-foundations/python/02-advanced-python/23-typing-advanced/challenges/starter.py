"""Challenge 23: Typing Advanced — starter (signatures only)."""

from __future__ import annotations

from typing import Generic, Protocol, TypeVar, runtime_checkable

T = TypeVar("T")


def build_schema(func) -> dict:
    """Return {name, params: [(name, default), ...], return} for func."""
    raise NotImplementedError


def signature_matches(func, expected: list[str]) -> bool:
    """True only if func's parameter names match `expected` exactly."""
    raise NotImplementedError


@runtime_checkable
class Retriever(Protocol):
    def retrieve(self, query: str, k: int = 5) -> list[str]:
        ...


class QdrantRetriever:
    def retrieve(self, query: str, k: int = 5) -> list[str]:
        raise NotImplementedError


class ChromaRetriever:
    def retrieve(self, query: str, k: int = 5) -> list[str]:
        raise NotImplementedError


class WrongSignatureRetriever:
    def retrieve(self, top_k: int) -> list[str]:
        raise NotImplementedError


class Result(Generic[T]):
    def __init__(self, ok: bool, value: T | None, error: str | None = None) -> None:
        raise NotImplementedError

    @classmethod
    def success(cls, value: T) -> "Result[T]":
        raise NotImplementedError

    @classmethod
    def failure(cls, error: str) -> "Result[T]":
        raise NotImplementedError


def verify_retriever(obj) -> bool:
    """True only if obj is a Retriever AND its signature is correct."""
    raise NotImplementedError


def safe_search(retriever, query: str, k: int = 5) -> Result[list[str]]:
    """Return Result.success(results) or Result.failure for bad shapes."""
    raise NotImplementedError
