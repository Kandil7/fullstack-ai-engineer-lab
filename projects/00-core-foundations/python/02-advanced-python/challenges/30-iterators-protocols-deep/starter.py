"""Challenge 30 starter — fill in the bodies (never return working code)."""
from __future__ import annotations

from collections.abc import Iterator, Mapping


class KeyValueStore(Mapping):
    """A dict-like store growing into full Mapping semantics."""

    def __init__(self, data: dict[str, int] | None = None) -> None:
        raise NotImplementedError

    def __getitem__(self, key: str) -> int:
        raise NotImplementedError

    def __setitem__(self, key: str, value: int) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __contains__(self, key: object) -> bool:
        raise NotImplementedError

    def __iter__(self) -> Iterator[str]:
        raise NotImplementedError

    def snapshot(self) -> "SnapshotDict":
        raise NotImplementedError


class SnapshotDict(Mapping):
    """Immutable, hashable snapshot of a KeyValueStore."""

    def __init__(self, data: dict[str, int]) -> None:
        raise NotImplementedError

    def __hash__(self) -> int:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    def __getitem__(self, key: str) -> int:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __iter__(self) -> Iterator[str]:
        raise NotImplementedError
