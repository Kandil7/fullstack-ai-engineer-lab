"""
Challenge 30: Iterators and Protocols Deep — Hidden Tests
=========================================================
Dict semantics, ABC mixin behavior, hash/eq contract, one-pass hash
guard, and memory guard for the snapshot.
"""
from __future__ import annotations

import importlib.util
import sys
import tracemalloc
from collections.abc import Mapping
from pathlib import Path

import pytest

HERE = Path(__file__).parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


solution = _load("solution")
starter = _load("starter")


# --- Bronze: KeyValueStore core ---------------------------------------------

def test_bronze_getitem():
    s = solution.KeyValueStore({"a": 1})
    assert s["a"] == 1


def test_bronze_setitem_and_len():
    s = solution.KeyValueStore()
    s["b"] = 2
    assert len(s) == 1, "one set item means length 1"
    s["c"] = 3
    assert len(s) == 2
    assert len(solution.KeyValueStore({"a": 1, "b": 2})) == 2


def test_bronze_contains():
    s = solution.KeyValueStore({"a": 1})
    assert "a" in s
    assert "z" not in s


def test_bronze_keyerror_on_missing():
    s = solution.KeyValueStore({"a": 1})
    with pytest.raises(KeyError):
        _ = s["missing"]


# --- Silver: Mapping ABC semantics ------------------------------------------

def test_silver_is_mapping():
    assert issubclass(solution.KeyValueStore, Mapping)
    assert isinstance(solution.KeyValueStore({"a": 1}), Mapping)


def test_silver_get_default():
    s = solution.KeyValueStore({"a": 1})
    assert s.get("nope", 99) == 99
    assert s.get("a") == 1


def test_silver_keys_values_items():
    s = solution.KeyValueStore({"a": 1, "b": 2})
    assert sorted(s.keys()) == ["a", "b"]
    assert sorted(s.values()) == [1, 2]
    assert dict(s.items()) == {"a": 1, "b": 2}


def test_silver_equality_with_dict():
    s = solution.KeyValueStore({"a": 1, "b": 2})
    assert s == {"a": 1, "b": 2}
    assert s != {"a": 1}


def test_silver_iteration():
    s = solution.KeyValueStore({"a": 1, "b": 2})
    assert sorted(iter(s)) == ["a", "b"]


# --- Gold: SnapshotDict -----------------------------------------------------

def _store():
    return solution.KeyValueStore({"a": 1, "b": 2})


def test_gold_snapshot_reads():
    snap = _store().snapshot()
    assert snap["a"] == 1
    assert len(snap) == 2
    assert dict(snap.items()) == {"a": 1, "b": 2}


def test_gold_snapshot_immutable_after_source_mutation():
    s = _store()
    snap = s.snapshot()
    s["a"] = 999
    assert snap["a"] == 1, "snapshot must not change when the store mutates"


def test_gold_snapshot_hash_consistent():
    a = _store().snapshot()
    b = _store().snapshot()
    assert a == b
    assert hash(a) == hash(b), "equal snapshots must hash equally"


def test_gold_snapshot_usable_as_dict_key():
    snap = _store().snapshot()
    table = {snap: "value"}
    assert table[_store().snapshot()] == "value"


def test_gold_snapshot_hash_precomputed_once():
    # One pass over items: the item-counting iterator proves each key
    # visited exactly once at construction (O(n) once, O(1) after).
    visits = {"n": 0}
    data = {str(i): i for i in range(1000)}

    class CountingIter:
        def __iter__(self):
            for k in data:
                visits["n"] += 1
                yield k

    snap = solution.SnapshotDict(dict(zip(CountingIter(), data.values())))
    assert hash(snap) == hash(snap)
    assert visits["n"] == 1000, "hash must visit each key exactly once"


def test_gold_snapshot_memory_guard():
    big = {str(i): i for i in range(50_000)}
    tracemalloc.start()
    solution.SnapshotDict(big)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert peak < 8_000_000, f"peak {peak} bytes exceeds 8 MB budget"


# --- Starter must be unimplemented -----------------------------------------

def test_starter_not_implemented():
    with pytest.raises(NotImplementedError):
        starter.KeyValueStore({"a": 1})["a"]
    with pytest.raises(NotImplementedError):
        s = starter.KeyValueStore()
        s["b"] = 2
    with pytest.raises(NotImplementedError):
        len(starter.KeyValueStore({"a": 1}))
    with pytest.raises(NotImplementedError):
        "a" in starter.KeyValueStore({"a": 1})
    with pytest.raises(NotImplementedError):
        iter(starter.KeyValueStore({"a": 1}))
    with pytest.raises(NotImplementedError):
        starter.KeyValueStore({"a": 1}).snapshot()
    with pytest.raises(NotImplementedError):
        starter.SnapshotDict({"a": 1})


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
