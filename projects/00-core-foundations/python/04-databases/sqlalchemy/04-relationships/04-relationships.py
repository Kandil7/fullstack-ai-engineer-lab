"""
04-databases/sqlalchemy — 04: Relationships
==============================================
Topics: relationship(); one-to-many, many-to-many, self-referential;
        back_populates; cascades.

Why this matters for AI/backend engineering:
    Real metadata graphs — experiment -> runs -> metrics, model ->
    deployments -> evaluations, dataset -> samples -> labels — are
    relationship graphs. Getting `relationship()` right decides whether
    your service navigates those graphs in one line or one hundred.
    Cascades decide whether deleting an experiment cleans up its rows
    or orphans them (and possibly corrupts reports).

Run:      python 04-relationships.py
Verify:   python 04-relationships.py --verify
Reference: https://docs.sqlalchemy.org/en/20/orm/relationships.html
"""

from __future__ import annotations

import sys

from sqlalchemy import Column, ForeignKey, String, Table, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from sqlalchemy.pool import StaticPool

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


class Base(DeclarativeBase):
    pass


# ============================================================
# 1. One-to-many with back_populates
# ============================================================
# relationship() is a *virtual* attribute: it is not a column. It tells
# the ORM how to find related rows. back_populates wires the two sides
# of the same relationship so both directions stay in sync.

# The many-to-many association table is declared BEFORE the mapped
# classes that reference it (its ForeignKey strings resolve lazily at
# create_all time). Defining it late and then bolting a relationship
# onto an already-mapped class is a classic "relationship expects a
# class or mapper argument" crash — see Common Mistakes.
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

    author: Mapped[Author | None] = relationship(back_populates="books")
    # String annotation "Tag" resolves when the mapper is configured,
    # by which time Tag below already exists.
    tags: Mapped[list["Tag"]] = relationship(
        secondary=book_tag, back_populates="books"
    )


# Tag is declared HERE (before the first create_all) because the
# association table's foreign key must resolve to a real table when
# create_all runs. Its relationship is explained in section 3.
class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

    books: Mapped[list[Book]] = relationship(
        secondary=book_tag, back_populates="tags"
    )


Base.metadata.create_all(engine)


# Example 1: navigating the relationship from both directions
with Session(bind=engine) as session:
    tolkien = Author(name="J.R.R. Tolkien")
    tolkien.books.append(Book(title="The Hobbit"))
    tolkien.books.append(Book(title="The Lord of the Rings"))
    session.add(tolkien)
    session.commit()
    for b in tolkien.books:
        print(f"{b.title} by {b.author.name}")

# Output:
# The Hobbit by J.R.R. Tolkien
# The Lord of the Rings by J.R.R. Tolkien

# ============================================================
# 2. Cascade: deleting a parent deletes its children
# ============================================================
# cascade="all, delete-orphan" means: when the author row is deleted,
# SQLAlchemy also deletes the book rows. Without it, the DB would leave
# books pointing at a missing author (unless the FK has ON DELETE
# CASCADE at the DB level).

# Example 2: delete-orphan cascade removes children in the same tx
with Session(bind=engine) as session:
    lewis = Author(name="C.S. Lewis")
    lewis.books.append(Book(title="The Lion, the Witch and the Wardrobe"))
    session.add(lewis)
    session.commit()
    print(f"before delete: {len(session.scalars(select(Book)).all())} books")

    session.delete(lewis)
    session.commit()
    print(f"after delete:  {len(session.scalars(select(Book)).all())} books")

# Output:
# before delete: 3 books
# after delete:  2 books

# ============================================================
# 3. Many-to-many with an association table
# ============================================================
# Many-to-many needs a THIRD table holding the pair of foreign keys.
# The association table is plain Core (no mapped class needed when it
# has no extra columns). Both sides use secondary=book_tag and the
# same back_populates pair. The table and the Tag class were declared
# in section 1 (mapper configuration is lazy, so the relationship was
# fully wired only now, at first use) — that keeps every ForeignKey
# resolvable when create_all runs.

# Example 3: tag two books; association rows are written automatically
with Session(bind=engine) as session:
    fantasy = Tag(label="fantasy")
    classic = Tag(label="classic")
    hobbit = session.scalars(
        select(Book).where(Book.title == "The Hobbit")
    ).one()
    hobbit.tags.extend([fantasy, classic])
    session.add_all([fantasy, classic])
    session.commit()
    print(f"hobbit tags: {[t.label for t in hobbit.tags]}")

# Output:
# hobbit tags: ['fantasy', 'classic']

# Example 4: association rows physically exist in the join table
with Session(bind=engine) as session:
    assoc = session.execute(select(book_tag.c.book_id, book_tag.c.tag_id)).all()
    print(f"association rows: {len(assoc)}")

# Output:
# association rows: 2

# ============================================================
# 4. Self-referential: a tree (prompt templates or datasets)
# ============================================================
# A node pointing at a parent node of the same type. Used for prompt
# template inheritance, dataset hierarchies, org charts.

class PromptTemplate(Base):
    __tablename__ = "prompt_templates"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("prompt_templates.id")
    )

    children: Mapped[list["PromptTemplate"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )
    # remote_side names the column the FK points TO; it belongs on the
    # MANY-TO-ONE side (parent), otherwise SQLAlchemy cannot tell which
    # end of the self-reference is which.
    parent: Mapped["PromptTemplate | None"] = relationship(
        back_populates="children", remote_side="PromptTemplate.id"
    )


Base.metadata.create_all(engine)

# Example 5: build and walk a two-level template tree
with Session(bind=engine) as session:
    base = PromptTemplate(name="base-rag")
    en = PromptTemplate(name="en-rag", parent=base)
    de = PromptTemplate(name="de-rag", parent=base)
    session.add_all([base, en, de])
    session.commit()

    root = session.scalars(
        select(PromptTemplate).where(PromptTemplate.name == "base-rag")
    ).one()
    print(f"root '{root.name}' children: {sorted(c.name for c in root.children)}")

# Output:
# root 'base-rag' children: ['de-rag', 'en-rag']

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: defining relationship() on only ONE side and expecting the
#          other side to exist.
# CORRECT: back_populates on both sides, or a single relationship on the
#          parent with back_populates creating the child attribute.
#
# MISTAKE: cascade="all, delete-orphan" on a many-to-many relationship
#          (deleting a tag would delete books it is attached to).
# CORRECT: cascade on the many-to-many side belongs on the ONE side of
#          a one-to-many; use "save-update, merge" (the default) or
#          passive_deletes for many-to-many.
#
# MISTAKE: defining a relationship on a class AFTER the class body via
#          MyClass.attr = relationship(...) — SQLAlchemy raises
#          "relationship 'x' expects a class or a mapper argument".
# CORRECT: declare association tables before the mapped classes and put
#          both relationship() sides inside their class bodies, using
#          string annotations ("Tag") for forward references.


# ============================================================
# Production Pattern: full graph persistence
# ============================================================
# One add() persists the whole graph thanks to the unit of work:
# author -> books -> tags all inserted in the correct dependency order.

def create_review_graph(
    title: str, tags: list[str], author_name: str = "Review Bot"
) -> tuple[int, list[int]]:
    """Create an author with a book and tags; return (book_id, [tag_ids]).

    The author is required because Book.author_id is NOT NULL — a graph
    write must always satisfy every FK that the schema declares.
    """
    with Session(bind=engine) as session:
        author = session.scalars(
            select(Author).where(Author.name == author_name)
        ).first()
        if author is None:
            author = Author(name=author_name)
        book = Book(title=title, author=author)
        for label in tags:
            existing = session.scalars(
                select(Tag).where(Tag.label == label)
            ).first()
            book.tags.append(existing if existing else Tag(label=label))
        session.add(book)
        session.commit()
        return book.id, [t.id for t in book.tags]


def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # 1. Relationship navigation works both directions
    with Session(bind=engine) as session:
        hobbit = session.scalars(
            select(Book).where(Book.title == "The Hobbit")
        ).one()
        assert hobbit.author.name == "J.R.R. Tolkien", \
            "child -> parent navigation must work"
        assert "The Hobbit" in [b.title for b in hobbit.author.books], \
            "parent -> children navigation must work"

    # 2. Many-to-many association rows exist after graph insert
    #    (checked BEFORE the cascade delete below removes them)
    with Session(bind=engine) as session:
        assoc = session.execute(select(book_tag.c.book_id)).all()
        assert len(assoc) >= 2, "association rows must be written"

    # 3. Tag navigation back to books works
    with Session(bind=engine) as session:
        fantasy = session.scalars(
            select(Tag).where(Tag.label == "fantasy")
        ).one()
        titles = [b.title for b in fantasy.books]
        assert "The Hobbit" in titles, "many-to-many reverse navigation must work"

    # 4. Cascade delete removes children rows (no orphans left behind)
    with Session(bind=engine) as session:
        tolkien = session.scalars(
            select(Author).where(Author.name == "J.R.R. Tolkien")
        ).one()
        session.delete(tolkien)
        session.commit()
        leftover = session.scalars(
            select(Book).where(Book.author_id.is_(None))
        ).all()
        # books deleted by cascade: ZERO rows may remain orphaned
        assert leftover == [], "delete-orphan must remove every child row"

    # 5. Self-referential tree: parent/child navigation
    with Session(bind=engine) as session:
        root = session.scalars(
            select(PromptTemplate).where(PromptTemplate.name == "base-rag")
        ).one()
        child_names = sorted(c.name for c in root.children)
        assert child_names == ["de-rag", "en-rag"], "tree children must resolve"
        assert root.children[0].parent.name == "base-rag", \
            "child -> parent must resolve"

    # 6. Production pattern writes a full graph in one transaction
    book_id, tag_ids = create_review_graph("Dune", ["sci-fi", "classic"])
    assert book_id is not None and len(tag_ids) == 2, \
        "graph insert must return ids"

    print("[OK] 04-relationships: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. relationship() is virtual navigation; back_populates syncs sides")
        print("2. cascade='all, delete-orphan' cleans children on parent delete")
        print("3. Many-to-many = association table; self-ref = tree")
        _verify()  # always runs, so plain execution is also a test
