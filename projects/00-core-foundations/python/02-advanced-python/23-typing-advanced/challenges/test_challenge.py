"""
Challenge 23: Typing Advanced — Hidden Tests
============================================
Runs against starter.py by default; set CHALLENGE_MODULE=solution to
verify the reference implementation.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


target = _load(os.environ.get("CHALLENGE_MODULE", "starter"))


def sample(a: int, b: str = "x") -> bool:
    return a > 0


class TestBuildSchema:
    def test_name(self):
        assert target.build_schema(sample)["name"] == "sample"

    def test_params_in_order(self):
        assert target.build_schema(sample)["params"] == [("a", None), ("b", "x")]

    def test_return_stringified(self):
        assert target.build_schema(sample)["return"] == "bool"

    def test_no_default_is_none(self):
        assert target.build_schema(sample)["params"][0][1] is None


class TestSignatureMatches:
    def test_exact_match(self):
        assert target.signature_matches(sample, ["a", "b"]) is True

    def test_order_matters(self):
        assert target.signature_matches(sample, ["b", "a"]) is False

    def test_missing_param(self):
        assert target.signature_matches(sample, ["a"]) is False

    def test_extra_param(self):
        assert target.signature_matches(sample, ["a", "b", "c"]) is False

    def test_empty_against_empty(self):
        def no_args() -> None:
            pass

        assert target.signature_matches(no_args, []) is True


class TestVerifyRetriever:
    def test_qdrant_passes(self):
        assert target.verify_retriever(target.QdrantRetriever()) is True

    def test_chroma_passes(self):
        assert target.verify_retriever(target.ChromaRetriever()) is True

    def test_wrong_shape_rejected(self):
        wrong = target.WrongSignatureRetriever()
        assert isinstance(wrong, target.Retriever), "isinstance is shallow: it must pass"
        assert target.verify_retriever(wrong) is False, (
            "verify must reject the wrong signature even though isinstance passed"
        )

    def test_non_retriever_rejected(self):
        assert target.verify_retriever(42) is False


class TestSafeSearch:
    def test_success_carries_values(self):
        result = target.safe_search(target.QdrantRetriever(), "hello", k=3)
        assert result.ok is True
        assert result.error is None
        assert result.value == ["qdrant:hello-0", "qdrant:hello-1", "qdrant:hello-2"]

    def test_chroma_success(self):
        result = target.safe_search(target.ChromaRetriever(), "hi", k=1)
        assert result.ok is True
        assert result.value == ["chroma:hi-0"]

    def test_wrong_shape_fails_gracefully(self):
        result = target.safe_search(target.WrongSignatureRetriever(), "hi")
        assert result.ok is False
        assert result.value is None
        assert isinstance(result.error, str)

    def test_garbage_fails_gracefully(self):
        result = target.safe_search("not a retriever", "hi")
        assert result.ok is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
