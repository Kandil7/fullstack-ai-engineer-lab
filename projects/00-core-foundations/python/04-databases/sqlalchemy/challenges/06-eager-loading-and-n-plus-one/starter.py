"""
Challenge 06: Eager Loading and the N+1 Problem — Starter Code
================================================================
Fill in the function bodies. Do not modify signatures.
Topic: N+1, selectinload, joinedload, lazy="raise".
"""

from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


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
    raise NotImplementedError


def load_projects_joined(session: Session) -> list[tuple[str, list[str]]]:
    """Same shape via joinedload — EXACTLY 1 query, no duplicate projects."""
    raise NotImplementedError


def fetch_projects_with_runs(session: Session) -> list[tuple[str, list[str]]]:
    """Production listing — at most 2 queries, same shape."""
    raise NotImplementedError


def lazy_access_raises(session: Session) -> str:
    """Return 'InvalidRequestError' when touching StrictProject.experiments
    without eager loading (lazy='raise' must make it a loud failure)."""
    raise NotImplementedError
