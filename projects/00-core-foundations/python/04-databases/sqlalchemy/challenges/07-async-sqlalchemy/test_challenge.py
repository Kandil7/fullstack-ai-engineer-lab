"""
Challenge 07: Async SQLAlchemy — Hidden Tests
===============================================
Async semantics: await boundaries, session lifecycle, the greenlet
bridge, and engine reusability after an IntegrityError.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import StaticPool

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


def _load(name: str):
    """Load a sibling module under a UNIQUE name registered in sys.modules.

    Registration matters: SQLAlchemy resolves Mapped[...] annotations
    through the module's globals when a mapped class is configured.
    The unique name (challenge dir embedded) prevents collisions
    between the 10 challenge suites in one pytest process.
    """
    parent = Path(__file__).parent.name.replace("-", "_")
    modname = f"{name}_{parent}"
    spec = importlib.util.spec_from_file_location(
        modname, Path(__file__).parent / f"{name}.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[modname] = module
    spec.loader.exec_module(module)
    return module


starter = _load("starter")
solution = _load("solution")


@pytest.fixture()
async def engine():
    """Fresh async engine + schema per test.

    dispose() in teardown is CRITICAL: without it the aiosqlite worker
    threads keep the process alive and pytest hangs.
    """
    eng = create_async_engine("sqlite+aiosqlite://", poolclass=StaticPool)
    async with eng.begin() as conn:
        await conn.run_sync(solution.Base.metadata.create_all)
    yield eng
    await eng.dispose()


ROWS = [
    {"model": "bert", "input_hash": "h-0001", "latency_ms": 42},
    {"model": "gpt2", "input_hash": "h-0002", "latency_ms": 88},
    {"model": "bert", "input_hash": "h-0003", "latency_ms": 15},
]


class TestStarterRaises:
    async def test_count_starter_raises(self, engine):
        with pytest.raises(NotImplementedError):
            await starter.count_models(engine)

    async def test_ingest_starter_raises(self, engine):
        with pytest.raises(NotImplementedError):
            await starter.ingest_batch(engine, [])

    async def test_request_starter_raises(self, engine):
        with pytest.raises(NotImplementedError):
            await starter.simulate_async_request(engine, "bert", "h-0001")

    async def test_run_sync_starter_raises(self, engine):
        with pytest.raises(NotImplementedError):
            await starter.run_sync_count(engine)


class TestCountModels:
    async def test_empty_table(self, engine):
        assert await solution.count_models(engine) == []

    async def test_distinct_sorted(self, engine):
        await solution.ingest_batch(engine, ROWS)
        assert await solution.count_models(engine) == ["bert", "gpt2"]


class TestIngestBatch:
    async def test_returns_row_count(self, engine):
        assert await solution.ingest_batch(engine, ROWS) == 3

    async def test_rows_persist(self, engine):
        await solution.ingest_batch(engine, ROWS)
        assert await solution.run_sync_count(engine) == 3

    async def test_empty_batch_returns_zero(self, engine):
        assert await solution.ingest_batch(engine, []) == 0

    async def test_duplicate_hash_raises_and_engine_stays_usable(self, engine):
        await solution.ingest_batch(engine, ROWS)
        with pytest.raises(IntegrityError):
            await solution.ingest_batch(engine, [ROWS[0]])
        # after the failed commit the engine must still accept work
        assert await solution.run_sync_count(engine) == 3


class TestRequestAndBridge:
    async def test_request_returns_confirmation(self, engine):
        assert (
            await solution.simulate_async_request(engine, "bert", "h-0100")
            == "stored h-0100"
        )

    async def test_request_persists_row(self, engine):
        await solution.simulate_async_request(engine, "bert", "h-0100")
        assert await solution.count_models(engine) == ["bert"]

    async def test_run_sync_counts(self, engine):
        await solution.simulate_async_request(engine, "bert", "h-0100")
        await solution.simulate_async_request(engine, "gpt2", "h-0101")
        assert await solution.run_sync_count(engine) == 2

    async def test_request_after_failure_works(self, engine):
        await solution.simulate_async_request(engine, "bert", "h-0200")
        with pytest.raises(IntegrityError):
            await solution.simulate_async_request(engine, "bert", "h-0200")
        assert (
            await solution.simulate_async_request(engine, "gpt2", "h-0201")
            == "stored h-0201"
        )
