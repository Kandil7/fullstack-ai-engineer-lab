"""
Challenge 04: Relationships — Reference Solution
==================================================
Why this approach: relationships make graph persistence declarative.
One add() writes author -> books -> tags in dependency order; the
cascade makes delete clean up children in the same transaction.
"""

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, String, Table, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


class Base(DeclarativeBase):
    pass


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
    One add() persists the whole graph in dependency order.
    """
    author = session.scalars(
        select(Author).where(Author.name == author_name)
    ).first()
    if author is None:
        author = Author(name=author_name)
        session.add(author)          # persistent BEFORE backref wiring

    book = Book(title=title)
    session.add(book)                # avoids the "not in session" SAWarning
    book.author = author

    for label in tags:
        existing = session.scalars(
            select(Tag).where(Tag.label == label)
        ).first()
        tag = existing if existing else Tag(label=label)
        session.add(tag)             # persistent before append
        book.tags.append(tag)

    session.add(book)
    session.commit()
    return book.id, [t.id for t in book.tags]


def find_books_by_tag(session: Session, tag_label: str) -> list[str]:
    """Return book titles (sorted) carrying the given tag, or []."""
    tag = session.scalars(
        select(Tag).where(Tag.label == tag_label)
    ).first()
    if tag is None:
        return []
    return sorted(b.title for b in tag.books)


def delete_author_cascade(session: Session, author_name: str) -> int:
    """Delete an author and their books (cascade); return books removed."""
    author = session.scalars(
        select(Author).where(Author.name == author_name)
    ).first()
    if author is None:
        return 0
    removed = len(author.books)   # count BEFORE the delete
    session.delete(author)        # cascade removes books + book_tag rows
    session.commit()
    return removed
