"""Challenge 30 solution — reference implementation with reasoning comments.

The trick of the whole challenge: __getitem__ + __len__ + __iter__ on a
Mapping base, and the ABC supplies get/keys/values/items/eq. Snapshot
precomputes its hash once (O(n) construction, O(1) hashes later) so the
hash/eq contract holds forever — the object is immutable.
"""
from __future__ import annotations

from collections.abc import Iterator, Mapping


class SnapshotDict(Mapping):
    """Immutable, hashable snapshot of a KeyValueStore.

    Why precompute the hash: the object never changes, so hashing the
    full contents once at construction makes every later hash O(1) and
    guarantees the hash/eq contract (equal snapshots hash equally,
    and the hash never changes while the object is alive).
    """

    def __init__(self, data: dict[str, int]) -> None:
        # Immutable by construction: private dict, never exposed as mutable.
        self._data = dict(data)
        # One pass over items; tuple-hash is deterministic and order-stable.
        self._hash = hash(tuple(sorted(self._data.items())))

    def __hash__(self) -> int:
        """O(1): the value was computed once at construction."""
        return self._hash

    def __eq__(self, other: object) -> bool:
        """Value equality: equal contents, regardless of class."""
        if isinstance(other, SnapshotDict):
            return self._data == other._data
        if isinstance(other, Mapping):
            return dict(self.items()) == dict(other.items())
        return False

    def __getitem__(self, key: str) -> int:
        """O(1) average; KeyError on missing key, like a dict."""
        return self._data[key]

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)


class KeyValueStore(Mapping):
    """A dict-like store growing into full Mapping semantics.

    The ABC provides get/keys/values/items/__contains__/__eq__ from the
    three dunders we implement — that is the whole point of the
    collections.abc hierarchy: implement the minimal core, inherit the
    full interface.
    """

    def __init__(self, data: dict[str, int] | None = None) -> None:
        self._data = dict(data) if data else {}

    def __getitem__(self, key: str) -> int:
        """O(1) average; KeyError for missing keys (dict semantics)."""
        return self._data[key]

    def __setitem__(self, key: str, value: int) -> None:
        """O(1) average insert/update."""
        self._data[key] = value

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: object) -> bool:
        """Exact-key membership, like dict."""
        return key in self._data

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def snapshot(self) -> SnapshotDict:
        """O(n) copy into an immutable, hashable SnapshotDict."""
        return SnapshotDict(self._data)
