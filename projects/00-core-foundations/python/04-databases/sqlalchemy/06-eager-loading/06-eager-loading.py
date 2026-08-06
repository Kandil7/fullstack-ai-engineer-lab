"""
04-databases/sqlalchemy — 06: Eager Loading and the N+1 Problem (STAR)
======================================================================
Topics: the N+1 problem, demonstrated with query counts;
        selectinload vs joinedload vs subqueryload; lazy= strategies.

Why this matters for AI/backend engineering:
    N+1 is the single most common performance defect in ORM-backed
    services: listing 100 model versions lazily fires 101 queries.
    In an ML platform (registry listing, run explorer, eval matrix)
    the "one extra query per row" pattern turns a 5 ms endpoint into
    a 500 ms one and the database into a bottleneck. This exercise
    measures query counts directly with a SQLAlchemy event listener,
    then fixes the problem with eager loading — and asserts the fix
    in code so it cannot silently regress.

Run:      python 06-eager-loading.py
Verify:   python 06-eager-loading.py --verify
Reference: https://docs.sqlalchemy.org/en/20/orm/loading_relationships.html
"""

from __future__ import annotations

import sys

from sqlalchemy import ForeignKey, String, create_engine, event, select
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    joinedload,
    mapped_column,
    relationship,
    selectinload,
    subqueryload,
)
from sqlalchemy.pool import StaticPool

# ============================================================
# 0. Models: Project -> Experiment (one-to-many, the classic N+1)
# ============================================================
# A project (a tuning campaign) owns many experiments (runs).
# Default loading is LAZY: .experiments fires a query every time
# it is accessed on an unloaded instance.
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)

    experiments: Mapped[list["Experiment"]] = relationship(
        back_populates="project"
    )


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"), nullable=False
    )

    project: Mapped[Project] = relationship(back_populates="experiments")


Base.metadata.create_all(engine)

N_PROJECTS = 4
K_EXPERIMENTS = 3

with Session(bind=engine) as session:
    for p in range(N_PROJECTS):
        project = Project(name=f"campaign-{p}")
        project.experiments.extend(
            [Experiment(name=f"{project.name}-run-{k}") for k in range(K_EXPERIMENTS)]
        )
        session.add(project)
    session.commit()
    session.expunge_all()  # drop identity map so every load hits the DB


def new_session() -> Session:
    return Session(bind=engine)


# ============================================================
# 1. The N+1 problem, made visible: count every SQL statement
# ============================================================
# The measurement technique: SQLAlchemy fires an event before every
# cursor execute. A listener counts statements — the honest way to
# see how many queries your ORM code really sends. No guessing.
# Complexity: 1 + N queries for N parents (lazy); O(1) counting.

class QueryCounter:
    """Counts SQL statements executed on a given engine."""

    def __init__(self, engine) -> None:
        self.queries: list[str] = []
        event.listen(engine, "before_cursor_execute", self._on_execute)

    def _on_execute(self, conn, cursor, statement, parameters, context, executemany):
        self.queries.append(statement)

    def count(self) -> int:
        return len(self.queries)

    def reset(self) -> None:
        self.queries = []


counter = QueryCounter(engine)

# Example 1: lazy traversal — load all projects, then touch children
with new_session() as session:
    counter.reset()
    projects = session.scalars(select(Project).order_by(Project.id)).all()
    total_runs = 0
    for project in projects:
        total_runs += len(project.experiments)  # ONE query per project
    lazy_count = counter.count()

print(f"lazy: {lazy_count} queries for {N_PROJECTS} projects ({total_runs} runs)")
print(f"  -> N+1: {lazy_count} = 1 (projects) + {N_PROJECTS} (children)")

# Output:
# lazy: 5 queries for 4 projects (12 runs)
#   -> N+1: 5 = 1 (projects) + 4 (children)


# ============================================================
# 2. selectinload: fetch children in ONE extra query
# ============================================================
# selectinload turns the per-child queries into a single
# "WHERE project_id IN (...)" query: 1 + 1 = 2 total.
# It is the default recommendation: simple, no row duplication,
# works with pagination.

# Example 2: same traversal, eager children
with new_session() as session:
    stmt = select(Project).options(selectinload(Project.experiments)).order_by(Project.id)
    projects = session.scalars(stmt).all()
    counter.reset()
    total_runs = sum(len(p.experiments) for p in projects)  # no SQL fired
    selectin_count = counter.count()

print(f"selectinload: {selectin_count} queries ({total_runs} runs loaded)")
print(f"  -> 1 (projects) + 1 (children IN ...)")

# Output:
# selectinload: 0 queries (12 runs loaded)
#   -> 1 (projects) + 1 (children IN ...)


# ============================================================
# 3. joinedload: ONE query with a JOIN
# ============================================================
# joinedload emits a single SELECT with LEFT OUTER JOIN; children
# come back in the same result set. The cost: the parent row is
# repeated per child, so the ORM must de-duplicate (unique()) —
# and the JOIN can be slow when the one side is large.
# Session.scalars() applies unique() automatically in 2.0.

# Example 3: joinedload — one SQL statement for the whole graph.
# NOTE: with a collection, the parent row repeats once per child, so
# the result must be de-duplicated with .unique() — SQLAlchemy raises
# InvalidRequestError if you forget (2.0 does not auto-apply it).
with new_session() as session:
    stmt = select(Project).options(joinedload(Project.experiments)).order_by(Project.id)
    projects = session.scalars(stmt).unique().all()
    counter.reset()
    total_runs = sum(len(p.experiments) for p in projects)
    joined_count = counter.count()

print(f"joinedload: {joined_count} query, {len(projects)} projects deduped")
print(f"  -> 1 (single JOIN) vs {N_PROJECTS + 1} (lazy)")

# Output:
# joinedload: 0 query, 4 projects deduped
#   -> 1 (single JOIN) vs 5 (lazy)


# ============================================================
# 4. subqueryload: children via a derived-table JOIN
# ============================================================
# subqueryload wraps the parent query in a subquery and joins the
# children against THAT — 2 queries, but the JOIN is against a
# small derived set instead of the full parent table. Rarely
# needed; selectinload is the modern default.

# Example 4: subqueryload — 2 queries, children joined to a subquery
with new_session() as session:
    stmt = select(Project).options(subqueryload(Project.experiments)).order_by(Project.id)
    projects = session.scalars(stmt).all()
    counter.reset()
    total_runs = sum(len(p.experiments) for p in projects)
    subquery_count = counter.count()

print(f"subqueryload: {subquery_count} queries ({total_runs} runs loaded)")

# Output:
# subqueryload: 0 queries (12 runs loaded)


# ============================================================
# 5. lazy= strategies and raiseload: fail loudly, not slowly
# ============================================================
# The relationship() default is lazy="select" (one query per access).
# lazy="raise" turns accidental lazy loading into an exception —
# the standard trick to catch N+1 in tests. Joined and selectin
# can also be set as relationship DEFAULTS, not just per-query.

class StrictProject(Base):
    """Same shape as Project, but lazy access is a hard error."""

    __tablename__ = "strict_projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)

    experiments: Mapped[list["StrictExperiment"]] = relationship(
        back_populates="project", lazy="raise"
    )


class StrictExperiment(Base):
    __tablename__ = "strict_experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("strict_projects.id"), nullable=False
    )

    project: Mapped[StrictProject] = relationship(back_populates="experiments")


Base.metadata.create_all(engine)
with Session(bind=engine) as session:
    p = StrictProject(name="strict-0")
    p.experiments.append(StrictExperiment(name="strict-0-run-0"))
    session.add(p)
    session.commit()


# Example 5: touching a lazy="raise" collection raises
def touch_lazy(engine) -> str:
    """Try to read an unloaded 'raise' collection; return exception name."""
    with Session(bind=engine) as session:
        project = session.scalars(select(StrictProject)).first()
        try:
            _ = len(project.experiments)  # would fire SQL if lazy="select"
        except InvalidRequestError as exc:
            return type(exc).__name__
        return "no error"


print(f"lazy='raise' access -> {touch_lazy(engine)}")

# Output:
# lazy='raise' access -> InvalidRequestError


# ============================================================
# 6. Production Pattern: one loader with a strategy switch
# ============================================================
# The production shape: a function that owns the loading strategy,
# callers get projects with children WITHOUT knowing how the SQL is
# shaped. The verify block below asserts the query counts, so any
# future edit that reintroduces N+1 fails the exercise.

def fetch_projects_with_runs(
    session: Session, eager: bool = True
) -> tuple[list[Project], int]:
    """Return (projects, queries_fired) — eager loads by default.

    Chosen over a fixed lazy="" strategy because the loading policy
    is a PER-QUERY decision: list endpoints want selectinload, a
    single-project detail page may prefer joinedload, and bulk
    analytics often want Core, not the ORM at all.
    """
    counter.reset()
    stmt = select(Project).order_by(Project.id)
    if eager:
        stmt = stmt.options(selectinload(Project.experiments))
    projects = list(session.scalars(stmt).all())
    for project in projects:
        _ = len(project.experiments)  # touch children exactly like a view does
    return projects, counter.count()


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: "I only added selectinload to the first query."
#   projects = session.scalars(select(Project)).all()      # no options!
#   runs = [e for p in projects for e in p.experiments]    # N+1 again
# CORRECT: put options() on EVERY query that loads the graph.
#
# MISTAKE: using joinedload on a one-to-many for a huge parent set.
#   The JOIN materializes one parent row per child in the result set;
#   for 100k experiments that is 100k-row result for 10 projects.
# CORRECT: selectinload for big collections, joinedload for
#   many-to-one / small collections.
#
# MISTAKE: disabling lazy loading by hand-poking relationships.
# CORRECT: lazy="raise" (or raiseload()) so the ORM fails loudly
#   in tests instead of silently degrading production.


# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    with new_session() as session:
        # 1. Lazy traversal fires exactly 1 + N queries (the N+1 bug)
        counter.reset()
        projects = session.scalars(select(Project).order_by(Project.id)).all()
        run_count = sum(len(p.experiments) for p in projects)
        lazy_queries = counter.count()
        assert run_count == N_PROJECTS * K_EXPERIMENTS, "seed data must be intact"
        assert lazy_queries == 1 + N_PROJECTS, \
            f"lazy must be N+1 queries, got {lazy_queries}"

        # 2. selectinload: exactly 2 queries (parents + children IN ...)
        counter.reset()
        stmt = (
            select(Project)
            .options(selectinload(Project.experiments))
            .order_by(Project.id)
        )
        eager_projects = session.scalars(stmt).all()
        eager_runs = sum(len(p.experiments) for p in eager_projects)
        assert counter.count() == 2, \
            f"selectinload must be 2 queries, got {counter.count()}"
        assert eager_runs == N_PROJECTS * K_EXPERIMENTS, \
            "selectinload must load every child"

        # 3. joinedload: exactly 1 query, parents de-duplicated
        counter.reset()
        stmt = (
            select(Project)
            .options(joinedload(Project.experiments))
            .order_by(Project.id)
        )
        joined_projects = session.scalars(stmt).unique().all()
        assert counter.count() == 1, \
            f"joinedload must be 1 query, got {counter.count()}"
        assert len(joined_projects) == N_PROJECTS, \
            "joinedload must de-duplicate parent rows"

        # 4. subqueryload: exactly 2 queries
        counter.reset()
        stmt = (
            select(Project)
            .options(subqueryload(Project.experiments))
            .order_by(Project.id)
        )
        sub_projects = session.scalars(stmt).all()
        assert counter.count() == 2, \
            f"subqueryload must be 2 queries, got {counter.count()}"
        assert sum(len(p.experiments) for p in sub_projects) == N_PROJECTS * K_EXPERIMENTS, \
            "subqueryload must load every child"

        # 5. All strategies return identical data (correctness parity)
        eager_names = {
            p.name: sorted(e.name for e in p.experiments)
            for p in session.scalars(
                select(Project).options(selectinload(Project.experiments))
            ).all()
        }
        assert len(eager_names) == N_PROJECTS and all(
            len(v) == K_EXPERIMENTS for v in eager_names.values()
        ), "loaded graphs must match the seed"

        # 6. lazy='raise' turns accidental N+1 into an exception
        assert touch_lazy(engine) == "InvalidRequestError", \
            "lazy='raise' must raise on unloaded access"

        # 7. Production loader: eager by default -> 2 queries
        #    (fresh sessions so the identity map never hides queries)
        loaded, queries = fetch_projects_with_runs(new_session(), eager=True)
        assert queries == 2, f"production loader must be eager, got {queries}"
        assert len(loaded) == N_PROJECTS, "loader must return all projects"

        # 8. Production loader with eager=False reproduces N+1 (visible, not silent)
        loaded, queries = fetch_projects_with_runs(new_session(), eager=False)
        assert queries == 1 + N_PROJECTS, \
            "non-eager loader must show the N+1 cost explicitly"

    print("[OK] 06-eager-loading: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. N+1 is real and measurable: 1 + N queries via event listener")
        print("2. selectinload: 2 queries; joinedload: 1; subqueryload: 2")
        print("3. lazy='raise' fails loud in tests; choose strategy per query")
        _verify()  # always runs, so plain execution is also a test
