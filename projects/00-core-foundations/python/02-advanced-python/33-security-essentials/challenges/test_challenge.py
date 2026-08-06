"""
Challenge 33: Security Essentials — Hidden Tests
================================================
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


solution = _load("solution")
import pytest  # noqa: E402
import yaml  # noqa: E402


# ============================================================
# Bronze: Password Store
# ============================================================

def test_hash_lengths():
    digest, salt = solution.hash_password("p@ss")
    assert len(digest) == 32, "SHA-256 digest is 32 bytes"
    assert len(salt) == 16, "fresh salt is 16 bytes"


def test_verify_correct_and_wrong():
    digest, salt = solution.hash_password("p@ss")
    assert solution.verify_password("p@ss", digest, salt) is True
    assert solution.verify_password("p@ss2", digest, salt) is False


def test_random_salts():
    d1, s1 = solution.hash_password("same")
    d2, s2 = solution.hash_password("same")
    assert d1 != d2, "same password, different salts -> different hashes"
    assert s1 != s2


def test_supplied_salt_deterministic():
    salt = b"\x01" * 16
    d1, _ = solution.hash_password("x", salt=salt)
    d2, _ = solution.hash_password("x", salt=salt)
    assert d1 == d2, "same salt + same password -> same hash"


def test_verify_uses_compare_digest():
    source = (HERE / "solution.py").read_text(encoding="utf-8")
    assert "compare_digest" in source, "verify must use compare_digest"
    assert "== " not in source.replace("!=", ""), "no plain == in verify"


# ============================================================
# Silver: Safe Query Layer
# ============================================================

def test_add_and_find():
    store = solution.SafeStore()
    store.add("1", "alice")
    assert store.find("1") == [("alice",)]


def test_find_missing_returns_empty():
    store = solution.SafeStore()
    assert store.find("nope") == []


def test_injection_payload_blocked():
    store = solution.SafeStore()
    store.add("1", "alice")
    store.add("2", "bob")
    payload = "1' OR '1'='1"
    assert store.find(payload) == [], \
        "parameterized query must treat the payload as a literal"


def test_injection_variant_blocked():
    store = solution.SafeStore()
    store.add("1", "alice")
    payload = "1'; DROP TABLE users; --"
    assert store.find(payload) == [], \
        "multi-statement injection must not execute"


def test_no_fstring_sql():
    source = (HERE / "solution.py").read_text(encoding="utf-8")
    # f-strings are fine for messages; SQL must never be built from them
    assert "f\"SELECT" not in source and "f'SELECT" not in source
    assert "f\"INSERT" not in source and "f'INSERT" not in source
    assert "f\"WHERE" not in source and "f'WHERE" not in source
    assert "? " in source or "?," in source, "placeholders must be used"


# ============================================================
# Gold: Safe Config Loader
# ============================================================

def _write_config(text: str) -> Path:
    tmp = tempfile.TemporaryDirectory()
    path = Path(tmp.name) / "config.yaml"
    path.write_text(text, encoding="utf-8")
    return path, tmp


def test_load_valid_config():
    path, tmp = _write_config("model: base\nbatch_size: 8\n")
    try:
        cfg = solution.load_config(path)
        assert cfg == {"model": "base", "batch_size": 8}
    finally:
        tmp.cleanup()


def test_load_rejects_unknown_key():
    path, tmp = _write_config("model: base\nevil_key: 1\n")
    try:
        with pytest.raises(ValueError):
            solution.load_config(path)
    finally:
        tmp.cleanup()


def test_load_rejects_wrong_type():
    path, tmp = _write_config("model: base\nbatch_size: many\n")
    try:
        with pytest.raises(ValueError):
            solution.load_config(path)
    finally:
        tmp.cleanup()


def test_load_rejects_non_mapping():
    path, tmp = _write_config("- a\n- b\n")
    try:
        with pytest.raises(ValueError):
            solution.load_config(path)
    finally:
        tmp.cleanup()


def test_load_rejects_python_tag():
    path, tmp = _write_config(
        "model: !!python/object/apply:os.system ['echo x']\n"
    )
    try:
        with pytest.raises(yaml.YAMLError):
            solution.load_config(path)
    finally:
        tmp.cleanup()


def test_is_safe_path_inside_root():
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    try:
        result = solution.is_safe_path(root, "config.yaml")
        assert result == (root / "config.yaml").resolve()
        assert result.is_relative_to(root.resolve())
    finally:
        tmp.cleanup()


def test_is_safe_path_blocks_traversal():
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    try:
        for evil in ("../outside.txt", "sub/../../outside.txt"):
            with pytest.raises(ValueError):
                solution.is_safe_path(root, evil)
    finally:
        tmp.cleanup()


def test_solution_uses_safe_load():
    source = (HERE / "solution.py").read_text(encoding="utf-8")
    assert "yaml.safe_load" in source, "must use yaml.safe_load"
    for forbidden in ("yaml.load(", "eval(", "exec("):
        assert forbidden not in source, f"forbidden: {forbidden}"


def test_solution_resolves_before_containment():
    source = (HERE / "solution.py").read_text(encoding="utf-8")
    assert "resolve()" in source and "is_relative_to" in source


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
