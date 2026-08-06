"""
Challenge 06: Eager Loading and the N+1 Problem — Reference Solution
=====================================================================
Why this approach: eager loading converts 1 + N queries into a bounded
number (2 for selectin, 1 for joined). lazy="raise" turns accidental
lazy loads into exceptions so N+1 cannot silently regress.
"""

from __future__ import annotations

from sqlalchemy import ForeignKey, String, select
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    joinedload,
    mapped_column,
    relationship,
    selectinload,
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


class StrictProject(Base):
    """Same shape as Project, but lazy collection access is a hard error."""

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


def load_projects(session: Session) -> list[tuple[str, list[str]]]:
    """(project_name, [run_names]) for all projects — EXACTLY 2 queries."""
    stmt = (
        select(Project)
        .options(selectinload(Project.experiments))
        .order_by(Project.id)
    )
    projects = session.scalars(stmt).all()
    return [
        (p.name, sorted(e.name for e in p.experiments)) for p in projects
    ]


def load_projects_joined(session: Session) -> list[tuple[str, list[str]]]:
    """Same shape via joinedload — EXACTLY 1 query, no duplicate projects."""
    stmt = (
        select(Project)
        .options(joinedload(Project.experiments))
        .order_by(Project.id)
    )
    projects = session.scalars(stmt).unique().all()   # dedupe parent rows
    return [
        (p.name, sorted(e.name for e in p.experiments)) for p in projects
    ]


def fetch_projects_with_runs(session: Session) -> list[tuple[str, list[str]]]:
    """Production listing — at most 2 queries, same shape."""
    return load_projects(session)


def lazy_access_raises(session: Session) -> str:
    """Return 'InvalidRequestError' when touching StrictProject.experiments
    without eager loading (lazy='raise' must make it a loud failure)."""
    project = session.scalars(
        select(StrictProject).order_by(StrictProject.id)
    ).first()
    try:
        _ = project.experiments   # lazy="raise" -> InvalidRequestError
    except InvalidRequestError:
        return "InvalidRequestError"
    return "no error"
