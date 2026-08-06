"""
04-databases/sqlalchemy — 05: Querying with select() (2.0 style)
=================================================================
Topics: select(); filters; joins; aliased; scalars;
        execute vs scalars; pagination.

Why this matters for AI/backend engineering:
    Every read path in an AI service — "show me the best experiment
    for model X", "which eval runs failed last week", "paginate the
    model registry" — is a SELECT shaped by the 2.0 select() API.
    Knowing execute() vs scalars(), when a join is needed, and how
    to paginate (offset vs keyset) decides whether the endpoint is
    five lines or a database-wide scan. Filtering and pagination are
    also exactly what a feature-store or registry API does all day.

Run:      python 05-querying-2.0.py
Verify:   python 05-querying-2.0.py --verify
Reference: https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html
"""

from __future__ import annotations

import sys

from sqlalchemy import ForeignKey, String, and_, func, or_, select, tuple_
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, aliased, mapped_column
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine

# ============================================================
# 0. Shared in-memory database + models
# ============================================================
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


class Base(DeclarativeBase):
    pass


class Experiment(Base):
    """One ML training/eval run in a registry."""

    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    model: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(12), default="running")


class EvalMetric(Base):
    """One scalar metric recorded for an experiment."""

    __tablename__ = "eval_metrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    experiment_id: Mapped[int] = mapped_column(
        ForeignKey("experiments.id"), nullable=False
    )
    metric: Mapped[str] = mapped_column(String(30), nullable=False)
    value: Mapped[float] = mapped_column(nullable=False)


class PromptTemplate(Base):
    """Self-referential template tree: a child inherits from a parent."""

    __tablename__ = "prompt_templates"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("prompt_templates.id")
    )


Base.metadata.create_all(engine)

with Session(bind=engine) as session:
    exp_bert = Experiment(name="bert-finetune-1", model="bert", status="done")
    exp_gpt = Experiment(name="gpt-finetune-1", model="gpt2", status="done")
    exp_running = Experiment(name="bert-finetune-2", model="bert", status="running")
    session.add_all([exp_bert, exp_gpt, exp_running])
    session.commit()
    session.add_all(
        [
            EvalMetric(experiment_id=exp_bert.id, metric="f1", value=0.89),
            EvalMetric(experiment_id=exp_bert.id, metric="latency", value=12.5),
            EvalMetric(experiment_id=exp_gpt.id, metric="f1", value=0.93),
            EvalMetric(experiment_id=exp_gpt.id, metric="latency", value=21.0),
            EvalMetric(experiment_id=exp_running.id, metric="f1", value=0.81),
        ]
    )
    session.commit()

    base = PromptTemplate(name="base-rag")
    session.add(base)
    session.flush()  # base.id is now assigned — needed for parent_id
    en = PromptTemplate(name="en-rag", parent_id=base.id)
    de = PromptTemplate(name="de-rag", parent_id=base.id)
    session.add_all([en, de])
    session.commit()

print(f"dialect: {engine.dialect.name}")


def new_session() -> Session:
    """Fresh session bound to the shared engine."""
    return Session(bind=engine)


# ============================================================
# 1. select() and scalars(): the 2.0 way to read rows
# ============================================================
# select(Experiment) builds a SELECT statement; session.scalars()
# returns the ORM objects directly. This is the bread-and-butter
# read: one statement, typed objects, zero string SQL.
# Complexity: result iteration O(rows).

# Example 1: all experiments, ordered
with new_session() as session:
    stmt = select(Experiment).order_by(Experiment.name)
    experiments = session.scalars(stmt).all()
    for exp in experiments:
        print(f"{exp.name}: {exp.model} [{exp.status}]")

# Output:
# bert-finetune-1: bert [done]
# bert-finetune-2: bert [running]
# gpt-finetune-1: gpt2 [done]


# ============================================================
# 2. Filters: where(), in_, like, and_/or_
# ============================================================
# .where() composes with AND automatically; combine alternatives
# explicitly with or_(); negate with ~ or .not_(). All of these
# compile to WHERE clauses with bound parameters — never f-strings.

# Example 2: where + in_
with new_session() as session:
    stmt = select(Experiment).where(Experiment.status.in_(["done", "archived"]))
    done = session.scalars(stmt).all()
    print(f"done/archived experiments: {len(done)}")

# Output:
# done/archived experiments: 2

# Example 3: like + and_
with new_session() as session:
    stmt = select(Experiment).where(
        and_(Experiment.model == "bert", Experiment.name.like("bert-%"))
    )
    bert_runs = session.scalars(stmt).all()
    print(f"bert runs: {[e.name for e in bert_runs]}")

# Output:
# bert runs: ['bert-finetune-1', 'bert-finetune-2']

# Example 4: or_ combines alternatives in one predicate
with new_session() as session:
    stmt = select(Experiment).where(
        or_(Experiment.status == "running", Experiment.model == "gpt2")
    )
    matches = session.scalars(stmt).all()
    print(f"running or gpt2: {[e.name for e in matches]}")

# Output:
# running or gpt2: ['bert-finetune-2', 'gpt-finetune-1']


# ============================================================
# 3. execute() vs scalars(): Row vs object
# ============================================================
# session.execute(stmt) returns Row objects: useful for projections
# (a subset of columns) and aggregates, where no ORM object exists.
# session.scalars(stmt) unwraps single-column results into plain
# values or ORM objects. Reach for execute() when you need columns
# from several tables or func() aggregates.

# Example 5: execute() gives Rows; index by position or name
with new_session() as session:
    stmt = select(Experiment.name, Experiment.status).order_by(Experiment.name)
    rows = session.execute(stmt).all()
    first = rows[0]
    print(f"row type: {type(first).__name__}; name via key: {first.name}")

# Output:
# row type: Row; name via key: bert-finetune-1

# Example 6: aggregates via func() — metric rows and average per model.
# Note the join multiplies rows (one per metric), so count(Experiment.id)
# counts METRIC rows, not experiments — filter to one metric to make
# both numbers meaningful.
with new_session() as session:
    stmt = (
        select(
            Experiment.model,
            func.count(Experiment.id),
            func.avg(EvalMetric.value),
        )
        .join(EvalMetric, EvalMetric.experiment_id == Experiment.id)
        .where(EvalMetric.metric == "f1")
        .group_by(Experiment.model)
        .order_by(Experiment.model)
    )
    for model, f1_rows, avg_f1 in session.execute(stmt):
        print(f"{model}: {f1_rows} f1 rows, avg f1 = {avg_f1:.3f}")

# Output:
# bert: 2 f1 rows, avg f1 = 0.850
# gpt2: 1 f1 rows, avg f1 = 0.930


# ============================================================
# 4. Joins: join() and outerjoin()
# ============================================================
# .join(Target) infers the ON clause from the foreign key;
# .outerjoin() keeps rows that have no match on the other side.
# The result of a join is still ORM objects when you select them.

# Example 7: inner join — experiments that HAVE at least one metric
with new_session() as session:
    stmt = (
        select(Experiment)
        .join(EvalMetric)
        .distinct()
        .order_by(Experiment.name)
    )
    with_metrics = session.scalars(stmt).all()
    print(f"experiments with metrics: {[e.name for e in with_metrics]}")

# Output:
# experiments with metrics: ['bert-finetune-1', 'bert-finetune-2', 'gpt-finetune-1']

# Example 8: outer join — every experiment, metric or not
with new_session() as session:
    stmt = (
        select(Experiment.name, func.count(EvalMetric.id))
        .outerjoin(EvalMetric)
        .group_by(Experiment.id)
        .order_by(Experiment.name)
    )
    for name, metric_count in session.execute(stmt):
        print(f"{name}: {metric_count} metrics")

# Output:
# bert-finetune-1: 2 metrics
# bert-finetune-2: 1 metrics
# gpt-finetune-1: 2 metrics


# ============================================================
# 5. aliased(): join a table to itself
# ============================================================
# To join a table to itself (parent/child, duplicate detection),
# you need TWO distinct references to the same mapped class.
# aliased() creates the second one; the SELECT gets an alias
# in SQL (SQLite: "SELECT ... FROM prompt_templates AS pt_1").

# Example 9: child templates with their parent name (self-join)
with new_session() as session:
    parent = aliased(PromptTemplate)
    stmt = (
        select(PromptTemplate.name, parent.name)
        .join(parent, PromptTemplate.parent_id == parent.id)
        .order_by(PromptTemplate.name)
    )
    for child_name, parent_name in session.execute(stmt):
        print(f"{child_name} inherits from {parent_name}")

# Output:
# de-rag inherits from base-rag
# en-rag inherits from base-rag


# ============================================================
# 6. Pagination: LIMIT/OFFSET and the keyset pattern
# ============================================================
# .limit(n).offset(m) is the simple pager. It degrades at scale:
# OFFSET 100000 means the database reads and discards 100000 rows.
# Keyset pagination filters on the last seen row instead — each
# page costs O(page_size) — and is stable when new rows arrive.

# Example 10: offset pagination, page 2 of size 1
with new_session() as session:
    page2 = (
        session.scalars(
            select(Experiment).order_by(Experiment.id).limit(1).offset(1)
        )
        .all()
    )
    print(f"offset page 2: {[e.name for e in page2]}")

# Output:
# offset page 2: ['gpt-finetune-1']


# ============================================================
# 7. Production Pattern: keyset-paginated registry listing
# ============================================================
# Real model registries paginate with keyset (also called
# "seek pagination") so deep pages stay O(page_size), not O(offset).
# The cursor is the last (id) seen; the next query is
# WHERE id > :last_id ORDER BY id LIMIT :size.

def keyset_page(session: Session, after_id: int | None, size: int) -> list[Experiment]:
    """Return the next page of experiments strictly after after_id.

    after_id=None means the first page. Uses the primary key as the
    cursor because it is unique, immutable, and indexed — the same
    reason streaming APIs use it instead of offset.
    """
    stmt = select(Experiment).order_by(Experiment.id).limit(size)
    if after_id is not None:
        stmt = stmt.where(Experiment.id > after_id)
    return list(session.scalars(stmt).all())


def metric_leaders(
    session: Session, metric: str, min_value: float, limit: int
) -> list[tuple[str, float]]:
    """Return (experiment_name, value) for experiments beating a bar.

    Uses an explicit join + filter so the caller never sees a row
    without its metric — the classic "join then filter" shape of a
    leaderboard query.
    """
    stmt = (
        select(Experiment.name, EvalMetric.value)
        .join(EvalMetric, EvalMetric.experiment_id == Experiment.id)
        .where(and_(EvalMetric.metric == metric, EvalMetric.value >= min_value))
        .order_by(EvalMetric.value.desc())
        .limit(limit)
    )
    return [(name, value) for name, value in session.execute(stmt)]


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: forgetting .scalars() and getting Row objects.
#   rows = session.execute(select(Experiment)).all()   # Rows, not Experiment
#   exp = rows[0].Experiment                            # awkward
# CORRECT:
#   exps = session.scalars(select(Experiment)).all()    # Experiment objects
#
# MISTAKE: OFFSET pagination on a big registry.
#   page = select(...).limit(20).offset(200_000)        # reads 200k rows
# CORRECT: keyset cursor (see section 7) — O(page_size) per page.
#
# MISTAKE: f-string values into .where().
#   stmt = select(Exp).where(Exp.name == f"{user}")     # injection risk
# CORRECT: bound parameters are automatic — just pass the value.


# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    with new_session() as session:
        # 1. scalars() returns ORM objects, not Rows
        first = session.scalars(select(Experiment).order_by(Experiment.id)).first()
        assert isinstance(first, Experiment), "scalars() must unwrap ORM objects"

        # 2. Filters: in_ and like compose with and_
        names = session.scalars(
            select(Experiment.name)
            .where(
                and_(
                    Experiment.model == "bert",
                    Experiment.name.like("bert-%"),
                    Experiment.status.in_(["done", "running"]),
                )
            )
            .order_by(Experiment.name)
        ).all()
        assert names == ["bert-finetune-1", "bert-finetune-2"], \
            "where/and_/in_/like must compose"

        # 3. or_ alternatives work
        names = session.scalars(
            select(Experiment.name)
            .where(or_(Experiment.status == "running", Experiment.model == "gpt2"))
            .order_by(Experiment.name)
        ).all()
        assert names == ["bert-finetune-2", "gpt-finetune-1"], \
            "or_ must combine alternatives"

        # 4. execute() rows support attribute access
        row = session.execute(
            select(Experiment.name, Experiment.status)
            .where(Experiment.name == "bert-finetune-1")
        ).one()
        assert row.name == "bert-finetune-1" and row.status == "done", \
            "execute() Rows must expose columns as attributes"

        # 5. Aggregates: one f1 value per experiment with metrics
        pairs = session.execute(
            select(EvalMetric.experiment_id, func.count(EvalMetric.id))
            .group_by(EvalMetric.experiment_id)
            .order_by(EvalMetric.experiment_id)
        ).all()
        assert [(p[0], p[1]) for p in pairs] == [(1, 2), (2, 2), (3, 1)], \
            "group_by + count must match the seeded data"

        # 6. Outer join keeps experiments without metrics (none seeded, so
        #    the LEFT side count equals the total experiment count)
        total = len(session.scalars(select(Experiment.id)).all())
        outer = session.execute(
            select(func.count(Experiment.id))
            .outerjoin(EvalMetric, EvalMetric.experiment_id == Experiment.id)
            .group_by(Experiment.id)
        ).all()
        assert len(outer) == total, "outerjoin must keep every left row"

        # 7. aliased self-join resolves parent names
        parent = aliased(PromptTemplate)
        children = session.execute(
            select(PromptTemplate.name, parent.name)
            .join(parent, PromptTemplate.parent_id == parent.id)
            .order_by(PromptTemplate.name)
        ).all()
        assert [(c[0], c[1]) for c in children] == [
            ("de-rag", "base-rag"),
            ("en-rag", "base-rag"),
        ], "aliased self-join must pair children with parents"

        # 8. Keyset pagination: two pages, no overlap, no gaps
        page1 = keyset_page(session, None, 2)
        page2 = keyset_page(session, page1[-1].id, 2)
        ids1 = {e.id for e in page1}
        ids2 = {e.id for e in page2}
        assert len(page1) == 2 and len(page2) == 1, "keyset pages sized correctly"
        assert ids1.isdisjoint(ids2), "keyset pages must not overlap"
        assert max(ids1) < min(ids2), "keyset page 2 must start after page 1"

        # 9. Leaderboard: join-then-filter returns only qualifying rows
        leaders = metric_leaders(session, "f1", 0.90, 5)
        assert leaders == [("gpt-finetune-1", 0.93)], \
            "metric_leaders must filter by value and metric"

        # 10. tuple_ row-value comparison is supported (SQLite >= 3.15);
        #     the cursor is DERIVED from the last row of the first page
        page1 = keyset_page(session, None, 2)
        cursor = (page1[-1].id, page1[-1].name)
        after = session.scalars(
            select(Experiment.name)
            .where(tuple_(Experiment.id, Experiment.name) > cursor)
            .order_by(Experiment.id, Experiment.name)
        ).all()
        assert after == ["bert-finetune-2"], \
            "row-value comparison must page forward from the cursor"

    print("[OK] 05-querying-2.0: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. scalars() for objects, execute() for Rows and aggregates")
        print("2. join()/outerjoin() + aliased() cover every join shape")
        print("3. Keyset pagination beats OFFSET as rows grow")
        _verify()  # always runs, so plain execution is also a test
