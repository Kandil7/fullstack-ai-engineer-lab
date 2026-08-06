"""
Challenge 04: Relationships — Starter Code
============================================
Fill in the function bodies. Do not modify signatures.
Topic: one-to-many, many-to-many, cascades, graph writes.
"""

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# The association table is declared BEFORE the mapped classes that
# reference it, so every ForeignKey resolves when create_all runs.
book_tag = Table(
    "book_tag",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)

    books: Mapped[list["Book"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    author: Mapped["Author"] = relationship(back_populates="books")
    tags: Mapped[list["Tag"]] = relationship(
        secondary=book_tag, back_populates="books"
    )


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

    books: Mapped[list["Book"]] = relationship(
        secondary=book_tag, back_populates="tags"
    )


def create_review_graph(
    session: Session,
    title: str,
    tags: list[str],
    author_name: str = "Review Bot",
) -> tuple[int, list[int]]:
    """Create author+book+tags in ONE graph write; return (book_id, [tag_ids]).

    Reuse the author and existing tags; create only what is missing.
    """
    raise NotImplementedError


def find_books_by_tag(session: Session, tag_label: str) -> list[str]:
    """Return book titles (sorted) carrying the given tag, or []."""
    raise NotImplementedError


def delete_author_cascade(session: Session, author_name: str) -> int:
    """Delete an author and their books (cascade); return books removed."""
    raise NotImplementedError
