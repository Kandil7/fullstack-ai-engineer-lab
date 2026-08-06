"""
Challenge 46: CLI & Configuration — Hidden Tests
=================================================
"""

from __future__ import annotations

import importlib.util
import io
import sys
from pathlib import Path

HERE = Path(__file__).parent

def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

solution = _load("solution")
import pytest


class TestParseKeyValue:
    def test_equals_form(self):
        assert solution.parse_key_value(["--lr=1e-3"]) == {"lr": "1e-3"}

    def test_space_form(self):
        assert solution.parse_key_value(["--epochs", "10"]) == {"epochs": "10"}

    def test_mixed(self):
        assert solution.parse_key_value(["--data", "x", "--seed=42"]) == {
            "data": "x", "seed": "42"
        }

    def test_empty(self):
        assert solution.parse_key_value([]) == {}

    def test_missing_value_raises(self):
        with pytest.raises(ValueError):
            solution.parse_key_value(["--key"])

    def test_bare_token_raises(self):
        with pytest.raises(ValueError):
            solution.parse_key_value(["plain"])


class TestResolve:
    def test_earlier_wins(self):
        assert solution.resolve([{"lr": "1e-4"}, {"lr": "1e-3", "seed": "0"}]) == {
            "lr": "1e-4", "seed": "0"
        }

    def test_none_layers_skipped(self):
        assert solution.resolve([None, {"a": "1"}]) == {"a": "1"}

    def test_empty(self):
        assert solution.resolve([{}]) == {}
        assert solution.resolve([]) == {}

    def test_does_not_mutate_inputs(self):
        a = {"x": "1"}
        b = {"x": "2", "y": "3"}
        solution.resolve([a, b])
        assert a == {"x": "1"} and b == {"x": "2", "y": "3"}

    def test_three_layers(self):
        layers = [{"lr": "a"}, None, {"lr": "b", "bs": "32"}, {"bs": "64", "seed": "1"}]
        assert solution.resolve(layers) == {"lr": "a", "bs": "32", "seed": "1"}


class TestMain:
    def _run(self, argv):
        out, err = io.StringIO(), io.StringIO()
        code = solution.main(argv, out, err)
        return code, out.getvalue(), err.getvalue()

    def test_train_success(self):
        code, out, err = self._run(["train", "--epochs", "10"])
        assert code == 0 and "training 10 epochs" in out and err == ""

    def test_eval_success(self):
        code, out, _ = self._run(["eval", "--checkpoint", "best.pt", "--data", "d"])
        assert code == 0 and "eval best.pt" in out

    def test_train_missing_epochs(self):
        code, _, err = self._run(["train"])
        assert code == 2 and "epochs" in err

    def test_eval_missing_args(self):
        code, _, err = self._run(["eval", "--checkpoint", "best.pt"])
        assert code == 2 and "checkpoint" in err and "data" in err

    def test_unknown_command(self):
        code, _, err = self._run(["deploy"])
        assert code == 2 and "unknown command" in err

    def test_no_args(self):
        code, _, err = self._run([])
        assert code == 2 and "usage" in err

    def test_non_int_epochs(self):
        code, _, err = self._run(["train", "--epochs", "many"])
        assert code == 2 and "epochs" in err

    def test_none_argv_defaults_to_empty(self):
        code, _, err = self._run(None)
        assert code == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
