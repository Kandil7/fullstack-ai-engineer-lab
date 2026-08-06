"""
04-databases/sqlalchemy — 10: Repository Pattern
==================================================
Topics: Repository abstraction; Unit of Work; keeping domain logic
        out of the ORM; testability tradeoffs.

Why this matters for AI/backend engineering:
    A model registry, an eval store, a feature store: every one of
    them has business rules (promotion thresholds, version rules,
    dedupe policies) that must be testable WITHOUT a database. The
    repository pattern draws a line: the ORM owns SQL, the service
    owns rules, and tests swap the real repository for a dict-based
    fake. The result is a test suite that runs in milliseconds and
    a codebase where "how we store runs" can change (sqlite -> PG
    -> API) without touching a single business rule.

Run:      python 10-repository-pattern.py
Verify:   python 10-repository-pattern.py --verify
Reference: https://docs.sqlalchemy.org/en/20/orm/session_basics.html
"""

from __future__ import annotations

import sys
from typing import Protocol, runtime_checkable

from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.pool import StaticPool

# ============================================================
# 0. ORM model (the only place SQLAlchemy knows about storage)
# ============================================================
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


class Base(DeclarativeBase):
    pass


class Experiment(Base):
    """A training/eval run. Pure persistence shape — NO business logic."""

    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    model: Mapped[str] = mapped_column(String(40), nullable=False)
    score: Mapped[float] = mapped_column(default=0.0)


Base.metadata.create_all(engine)


# ============================================================
# 1. Domain rules, kept OUT of the ORM
# ============================================================
# Business rules are pure functions over plain data. No session, no
# SQL — trivially unit-testable and reusable by any caller.

PROMOTE_THRESHOLD = 0.9


def should_promote(score: float) -> bool:
    """Pure domain rule: is this run good enough to promote?"""
    return score >= PROMOTE_THRESHOLD


def best_model_name(experiments: list[Experiment]) -> str | None:
    """Pure domain query: name of the highest-scoring run, or None."""
    if not experiments:
        return None
    return max(experiments, key=lambda e: e.score).model


# ============================================================
# 2. The Repository interface
# ============================================================
# The contract every storage backend must honor. Domain code depends
# on THIS, never on Session or Experiment. runtime_checkable lets
# isinstance() work on structural typing.
# Complexity: all operations O(1) amortized on PK lookups.

@runtime_checkable
class ExperimentRepository(Protocol):
    """Storage contract: how experiments are stored is an implementation detail."""

    def add(self, experiment: Experiment) -> int:
        """Persist an experiment; return its id."""
        ...

    def get(self, name: str) -> Experiment | None:
        """Fetch one experiment by name, or None."""
        ...

    def list_all(self) -> list[Experiment]:
        """Return every stored experiment."""
        ...

    def count(self) -> int:
        """Number of stored experiments."""
        ...

    def delete(self, name: str) -> bool:
        """Remove an experiment; True if it existed."""
        ...


# ============================================================
# 3. SQLAlchemy implementation (Unit of Work injected)
# ============================================================
# The repository takes a Session — it does NOT create or commit one.
# The caller (a service, a request handler) owns the transaction:
# this is the Unit of Work pattern. Repos stay composable: several
# repositories can share one session/transaction.

class SqlExperimentRepository:
    """Repository backed by SQLAlchemy. Session = injected Unit of Work."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, experiment: Experiment) -> int:
        self.session.add(experiment)
        self.session.flush()  # assign the PK; commit stays with the caller
        return experiment.id

    def get(self, name: str) -> Experiment | None:
        return self.session.scalars(
            select(Experiment).where(Experiment.name == name)
        ).first()

    def list_all(self) -> list[Experiment]:
        return list(self.session.scalars(select(Experiment).order_by(Experiment.id)))

    def count(self) -> int:
        return len(self.session.scalars(select(Experiment.id)).all())

    def delete(self, name: str) -> bool:
        exp = self.get(name)
        if exp is None:
            return False
        self.session.delete(exp)
        self.session.flush()
        return True


# ============================================================
# 4. In-memory fake (the test double that needs no database)
# ============================================================
# Same interface, dict storage. Services and domain rules are now
# testable at full speed with zero setup. The tradeoff: the fake
# does not model constraints, transactions, or SQL quirks — real
# integration tests still run against sqlite/Postgres.

class InMemoryExperimentRepository:
    """Dict-backed repository; behavior-compatible for tests."""

    def __init__(self) -> None:
        self._store: dict[str, Experiment] = {}
        self._next_id = 1

    def add(self, experiment: Experiment) -> int:
        if experiment.name in self._store:
            raise ValueError(f"duplicate name: {experiment.name}")
        experiment.id = self._next_id
        self._next_id += 1
        self._store[experiment.name] = experiment
        return experiment.id

    def get(self, name: str) -> Experiment | None:
        return self._store.get(name)

    def list_all(self) -> list[Experiment]:
        return list(self._store.values())

    def count(self) -> int:
        return len(self._store)

    def delete(self, name: str) -> bool:
        return self._store.pop(name, None) is not None


# ============================================================
# 5. The service: rules + repository, no Session in sight
# ============================================================
# The service is the application's use-case layer. It depends only
# on the Protocol — so it runs against sqlite, Postgres, or the
# dict fake without modification.

class RegistryService:
    """Model-registry use cases: register, promote, rank."""

    def __init__(self, repo: ExperimentRepository) -> None:
        self.repo = repo

    def register(self, name: str, model: str, score: float) -> int:
        """Register a run; refuses duplicate names (domain rule)."""
        if self.repo.get(name) is not None:
            raise ValueError(f"experiment already registered: {name}")
        return self.repo.add(Experiment(name=name, model=model, score=score))

    def promote(self, name: str) -> bool:
        """Promote a run to production if it beats the threshold."""
        exp = self.repo.get(name)
        if exp is None:
            return False
        return should_promote(exp.score)

    def leaderboard(self, limit: int = 10) -> list[tuple[str, str, float]]:
        """Best runs first; ranking is a DOMAIN rule, not SQL."""
        runs = self.repo.list_all()
        ranked = sorted(runs, key=lambda e: e.score, reverse=True)[:limit]
        return [(e.name, e.model, e.score) for e in ranked]

    def champion(self) -> str | None:
        """Best-performing model family overall."""
        return best_model_name(self.repo.list_all())


# ============================================================
# 6. Production Pattern: repo + service + explicit transaction
# ============================================================
# One session = one transaction = one unit of work. The request
# handler opens the session, builds repos on it, runs the service,
# and commits ONCE. If any step fails, nothing is half-written.

def register_batch_with_transaction(
    session: Session, entries: list[tuple[str, str, float]]
) -> int:
    """Register several runs atomically; roll back all on any failure."""
    repo = SqlExperimentRepository(session)
    service = RegistryService(repo)
    count = 0
    try:
        for name, model, score in entries:
            service.register(name, model, score)
        session.commit()  # the ONE commit for the whole unit of work
        count = repo.count()
    except Exception:
        session.rollback()  # atomic: nothing persists on failure
        raise
    return count


# ============================================================
# 7. Demo: the SAME service against both repositories
# ============================================================
def run_service_demo(repo: ExperimentRepository) -> list[str]:
    """Drive the service through any repository; returns log lines."""
    service = RegistryService(repo)
    out: list[str] = []
    service.register("bert-1", "bert", 0.91)
    service.register("bert-2", "bert", 0.72)
    service.register("gpt-1", "gpt2", 0.88)
    out.append(f"count={service.repo.count()}")
    out.append(f"promote bert-1 -> {service.promote('bert-1')}")
    out.append(f"promote gpt-1  -> {service.promote('gpt-1')}")
    out.append(f"champion model  -> {service.champion()}")
    out.append(f"leaderboard     -> {service.leaderboard(2)}")
    return out


print("--- sqlite repository ---")
with Session(bind=engine) as demo_session:
    for line in run_service_demo(SqlExperimentRepository(demo_session)):
        print(line)

# Output:
# --- sqlite repository ---
# count=3
# promote bert-1 -> True
# promote gpt-1  -> False
# champion model  -> bert
# leaderboard     -> [('bert-1', 'bert', 0.91), ('gpt-1', 'gpt2', 0.88)]

print("--- in-memory fake repository ---")
for line in run_service_demo(InMemoryExperimentRepository()):
    print(line)

# Output:
# --- in-memory fake repository ---
# count=3
# promote bert-1 -> True
# promote gpt-1  -> False
# champion model  -> bert
# leaderboard     -> [('bert-1', 'bert', 0.91), ('gpt-1', 'gpt2', 0.88)]


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: repository methods that commit.
#   def add(self, exp): session.add(exp); session.commit()
# CORRECT: flush() only — the caller owns the transaction (UoW),
#   otherwise partial workflows cannot be rolled back atomically.
#
# MISTAKE: business rules inside the model or the repository.
#   class Experiment: def should_promote(self): ...   # model is now
#                                                     # not purely storage
# CORRECT: pure functions (should_promote) or a service layer.
#
# MISTAKE: faking the database with a fake that doesn't match the
#   interface's semantics (duplicate handling, id assignment).
# CORRECT: the fake honors the same contract the real repo does —
#   see the duplicate-name ValueError above.


# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # 1. Pure domain rules need no database
    assert should_promote(0.95) is True, "0.95 must clear the bar"
    assert should_promote(0.5) is False, "0.5 must not clear the bar"
    runs = [
        Experiment(name="a", model="bert", score=0.7),
        Experiment(name="b", model="gpt2", score=0.9),
    ]
    assert best_model_name(runs) == "gpt2", "pure ranking must pick the max"

    # 2. The SQL repository implements the protocol (structural typing)
    with Session(bind=engine) as verify_session:
        sql_repo = SqlExperimentRepository(verify_session)
        assert isinstance(sql_repo, ExperimentRepository), \
            "SqlExperimentRepository must satisfy the repository protocol"

    # 3. Service behaves identically on sqlite and the fake
    with Session(bind=engine) as verify_session:
        sql_log = run_service_demo(SqlExperimentRepository(verify_session))
    fake_log = run_service_demo(InMemoryExperimentRepository())
    assert sql_log == fake_log, \
        "service must produce identical results on both repositories"
    assert "promote bert-1 -> True" in sql_log, "threshold promotion must work"
    assert "champion model  -> bert" in sql_log, "champion rule must rank models"

    # 4. Duplicate registration is refused by BOTH backends
    fake = InMemoryExperimentRepository()
    svc = RegistryService(fake)
    svc.register("dup", "bert", 0.5)
    try:
        svc.register("dup", "gpt2", 0.6)
        raise AssertionError("duplicate register must raise ValueError")
    except ValueError:
        pass

    # 5. Unit of Work: session rollback undoes a failed batch
    with Session(bind=engine) as verify_session:
        before = SqlExperimentRepository(verify_session).count()
        try:
            register_batch_with_transaction(
                verify_session,
                [("uow-1", "bert", 0.5), ("uow-1", "bert", 0.6)],  # dup -> fails
            )
            raise AssertionError("duplicate batch must fail")
        except ValueError:
            verify_session.rollback()
    with Session(bind=engine) as verify_session:
        after = SqlExperimentRepository(verify_session).count()
    assert before == after, "failed batch must leave zero rows behind"

    # 6. Atomic batch succeeds and commits exactly once
    with Session(bind=engine) as verify_session:
        n = register_batch_with_transaction(
            verify_session,
            [("atom-1", "bert", 0.5), ("atom-2", "gpt2", 0.6)],
        )
    assert n >= 2, "committed batch must persist every entry"

    # 7. delete() reports existence truthfully
    repo = InMemoryExperimentRepository()
    svc2 = RegistryService(repo)
    svc2.register("gone", "bert", 0.1)
    assert repo.delete("gone") is True, "delete must report existing rows"
    assert repo.delete("gone") is False, "delete must report missing rows"

    print("[OK] 10-repository-pattern: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Protocol + two implementations: swap storage, keep the rules")
        print("2. Unit of Work: repos flush, services commit, sessions roll back")
        print("3. Domain rules as pure functions -> millisecond tests")
        _verify()  # always runs, so plain execution is also a test
