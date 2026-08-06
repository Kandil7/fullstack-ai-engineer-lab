"""Challenge 03: Polars Lazy Evaluation — tests for all three tiers.

Run from the module root:
    python -m pytest 03-libraries/polars/challenges/03-lazy-evaluation/test_challenge.py -v
"""

from __future__ import annotations

import importlib.util
import os

import polars as pl
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


solution = _load("solution_03", os.path.join(HERE, "solution.py"))
starter = _load("starter_03", os.path.join(HERE, "starter.py"))


@pytest.fixture()
def data_dir(tmp_path):
    """A 4-column csv + matching parquet (1000 rows)."""
    n = 1000
    df = pl.DataFrame({
        "id": range(n),
        "score": [float(i % 97) for i in range(n)],
        "split": ["valid" if i % 4 == 0 else "train" for i in range(n)],
        "weight": [0.5] * n,
    })
    csv_path = tmp_path / "events.csv"
    df.write_csv(csv_path)
    pq_path = tmp_path / "events.parquet"
    df.write_parquet(pq_path)
    return str(csv_path), str(pq_path), df


# ---------------------------------------------------------------- bronze

def test_bronze_count_matches(data_dir):
    csv_path, _, df = data_dir
    assert solution.lazy_count(csv_path) == df.height


def test_bronze_never_read_csv(data_dir):
    csv_path, _, _ = data_dir
    with open(os.path.join(HERE, "solution.py"), encoding="utf-8") as fh:
        source = fh.read()
    assert "read_csv(" not in source, "must stay lazy: no read_csv"


def test_bronze_returns_int(data_dir):
    csv_path, _, _ = data_dir
    assert isinstance(solution.lazy_count(csv_path), int)


def test_bronze_starter_raises(data_dir):
    csv_path, _, _ = data_dir
    with pytest.raises(NotImplementedError):
        starter.lazy_count(csv_path)


# ---------------------------------------------------------------- silver

def test_silver_pushes_predicate(data_dir):
    _, pq_path, df = data_dir
    assert solution.predicate_pushed(pq_path, "split", "valid") is True


def test_silver_does_not_collect(data_dir):
    _, pq_path, _ = data_dir
    with open(os.path.join(HERE, "solution.py"), encoding="utf-8") as fh:
        source = fh.read()
    # predicate_pushed must only explain; count the collect calls per fn
    fn_src = source.split("def _projected_columns")[0]
    assert fn_src.count("collect(") == 1, \
        "predicate_pushed must use explain, not collect"


def test_silver_starter_raises(data_dir):
    _, pq_path, _ = data_dir
    with pytest.raises(NotImplementedError):
        starter.predicate_pushed(pq_path, "split", "valid")


# ---------------------------------------------------------------- gold

def test_gold_result_correct(data_dir):
    _, pq_path, df = data_dir
    result, cols = solution.project_and_filter(pq_path, ["score"], "split", "valid")
    expected = df.filter(pl.col("split") == "valid").select("score")
    assert result.height == expected.height == 250
    assert result.columns == ["score"]
    assert abs(result["score"].sum() - expected["score"].sum()) < 1e-9


def test_gold_projection_reads_only_needed(data_dir):
    _, pq_path, _ = data_dir
    result, cols = solution.project_and_filter(pq_path, ["score"], "split", "valid")
    # keep=1 column but the filter column is also needed: 2 of 4
    assert cols == 2, f"expected PROJECT 2/4 COLUMNS, got {cols}"


def test_gold_keeps_two_columns(data_dir):
    _, pq_path, df = data_dir
    result, cols = solution.project_and_filter(pq_path, ["id", "score"], "split", "train")
    assert cols == 3, "id + score + split (filter) must be read"
    assert result.columns == ["id", "score"]
    assert result.height == df.filter(pl.col("split") == "train").height


def test_gold_starter_raises(data_dir):
    _, pq_path, _ = data_dir
    with pytest.raises(NotImplementedError):
        starter.project_and_filter(pq_path, ["score"], "split", "valid")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
