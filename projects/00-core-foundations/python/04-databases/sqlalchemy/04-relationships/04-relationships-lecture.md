# Databases (SQLAlchemy) — 04: Relationships

## Topic Overview

Real metadata is a graph: experiment -> runs -> metrics, model -> deployments
-> evaluations, dataset -> samples -> labels. `relationship()` is the ORM's
way of navigating that graph in Python: `author.books`, `book.author`,
`book.tags`. It is a *virtual* attribute — no column, no storage — that tells
the ORM how to find related rows and how to keep both directions in sync via
`back_populates`.

For AI/backend engineers, relationships decide whether service code walks a
metadata graph in one line or one hundred, and cascades decide whether
deleting an experiment cleans up its rows or orphans them. This lecture covers
the three relationship shapes — one-to-many, many-to-many (association table),
and self-referential (trees) — plus cascade semantics and the graph-write
production pattern.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Declare a one-to-many relationship with `back_populates` on both sides
2. Navigate relationships from parent to children and child to parent
3. Explain what `relationship()` is *not*: a column, a join, or storage
4. Build a many-to-many with an association `Table` and `secondary=`
5. Order table/class declarations to keep mapper configuration happy
6. Use `cascade="all, delete-orphan"` and predict delete behavior
7. Build a self-referential tree with `remote_side` on the many-to-one side
8. Persist a whole object graph with one `session.add()`
9. Avoid the post-class-body `relationship()` crash
10. Choose cascade settings per relationship shape (one-to-many vs many-to-many)

---

## Prerequisites

| Need | Where |
|---|---|
| Mapped models and FKs | `02-declarative-models-lecture.md` |
| Session lifecycle | `03-session-lifecycle-lecture.md` |
| flush() for graph ids | `03-session-lifecycle-lecture.md` |

---

## 1. One-to-Many with back_populates

`relationship()` is a virtual attribute: it is not a column. `back_populates`
wires two sides of the *same* relationship so both stay in sync — append on
one side and the other side sees it immediately, even before flush.

```python
from sqlalchemy import Column, ForeignKey, String, Table, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from sqlalchemy.pool import StaticPool

engine = create_engine("sqlite://", connect_args={"check_same_thread": False},
                       poolclass=StaticPool)

class Base(DeclarativeBase):
    pass

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

Base.metadata.create_all(engine)

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
```

The FK lives only in `Book.author_id`; `relationship()` on both classes just
exposes the same edge from both directions.

## 2. Cascade: Deleting a Parent Cleans Its Children

`cascade="all, delete-orphan"` means: when the author row is deleted,
SQLAlchemy also deletes the book rows in the same transaction. Without it, the
DB would be left with books pointing at a missing author.

```python
with Session(bind=engine) as session:
    lewis = Author(name="C.S. Lewis")
    lewis.books.append(Book(title="The Lion, the Witch and the Wardrobe"))
    session.add(lewis)
    session.commit()
    session.delete(lewis)
    session.commit()
    print(f"books left: {len(session.scalars(select(Book)).all())}")
# Output:
# books left: 2
```

Cascade is a **unit-of-work** behavior: the ORM emits the child DELETEs; the
database has no `ON DELETE CASCADE` clause. Both approaches exist, and you
should know which one you are relying on.

## 3. Many-to-Many with an Association Table

Many-to-many needs a third table holding the pair of FKs. When that table has
no extra columns, a plain Core `Table` is enough; both mapped sides use
`secondary=book_tag` and the same `back_populates` pair.

```python
book_tag = Table(
    "book_tag",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    books: Mapped[list["Book"]] = relationship(
        secondary=book_tag, back_populates="tags"
    )
```

The `Book` class gains `tags: Mapped[list["Tag"]] = relationship(
secondary=book_tag, back_populates="books")`. Appending tags writes the
association rows automatically:

```python
with Session(bind=engine) as session:
    hobbit = session.scalars(select(Book).where(Book.title == "The Hobbit")).one()
    hobbit.tags.extend([Tag(label="fantasy"), Tag(label="classic")])
    session.add_all(hobbit.tags)
    session.commit()
    print(f"hobbit tags: {[t.label for t in hobbit.tags]}")
# Output:
# hobbit tags: ['fantasy', 'classic']
```

The association rows physically exist in `book_tag` — two rows after this
write.

## 4. Self-Referential: Trees (Prompt Templates, Datasets)

A node pointing at a parent node of the same type: prompt-template inheritance,
dataset hierarchies, org charts. The trick is `remote_side`: it names the
column the FK points *to* and belongs on the **many-to-one** side (`parent`),
so SQLAlchemy can tell which end of the self-reference is which.

```python
class PromptTemplate(Base):
    __tablename__ = "prompt_templates"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("prompt_templates.id"))
    children: Mapped[list["PromptTemplate"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )
    parent: Mapped["PromptTemplate | None"] = relationship(
        back_populates="children", remote_side="PromptTemplate.id"
    )

Base.metadata.create_all(engine)

with Session(bind=engine) as session:
    base = PromptTemplate(name="base-rag")
    en = PromptTemplate(name="en-rag", parent=base)
    de = PromptTemplate(name="de-rag", parent=base)
    session.add_all([base, en, de])
    session.commit()
    root = session.scalars(select(PromptTemplate).where(PromptTemplate.name == "base-rag")).one()
    print(f"root '{root.name}' children: {sorted(c.name for c in root.children)}")
# Output:
# root 'base-rag' children: ['de-rag', 'en-rag']
```

If `remote_side` goes on the wrong side, SQLAlchemy raises
`ArgumentError: could not determine relationship direction` — the error that
tells you the self-reference is ambiguous.

## 5. Production Pattern: One Graph Write

One `add()` persists the whole graph — author, books, tags — in dependency
order, thanks to the Unit of Work. The only hard requirement: satisfy every
FK the schema declares (here, `Book.author_id` is NOT NULL, so the author must
exist).

```python
def create_review_graph(session: Session, title: str, tags: list[str],
                        author_name: str = "Review Bot") -> tuple[int, list[int]]:
    author = session.scalars(select(Author).where(Author.name == author_name)).first()
    if author is None:
        author = Author(name=author_name)
        session.add(author)          # persistent BEFORE backref wiring
    book = Book(title=title)
    session.add(book)                # avoids "not in session" SAWarning
    book.author = author
    for label in tags:
        existing = session.scalars(select(Tag).where(Tag.label == label)).first()
        tag = existing if existing else Tag(label=label)
        session.add(tag)
        book.tags.append(tag)
    session.commit()
    return book.id, [t.id for t in book.tags]
```

Adding each object to the session *before* wiring relationships is the
discipline that keeps backref cascades warning-free.

---

## Common Mistakes to Avoid

### Mistake 1: Bolting a relationship onto a class after its body
```
# WRONG — ArgumentError: relationship 'tags' expects a class or a mapper argument
class Book(Base): ...
Book.tags = relationship("Tag", secondary=book_tag)
# CORRECT — declare inside the class body; string annotation for forward refs
class Book(Base):
    tags: Mapped[list["Tag"]] = relationship(secondary=book_tag, back_populates="books")
```

### Mistake 2: `remote_side` on the children side of a self-reference
```
# WRONG — "could not determine relationship direction"
parent: Mapped[...] = relationship(back_populates="children", remote_side="PromptTemplate.parent_id")
# CORRECT — remote_side names the FK TARGET; belongs on the many-to-one side
parent: Mapped["PromptTemplate | None"] = relationship(
    back_populates="children", remote_side="PromptTemplate.id")
```

### Mistake 3: delete-orphan on a many-to-many relationship
```
# WRONG — deleting a tag would delete the books attached to it
class Tag(Base):
    books = relationship(secondary=book_tag, cascade="all, delete-orphan")
# CORRECT — default cascade on many-to-many; delete-orphan only on one-to-many
books = relationship(secondary=book_tag, back_populates="tags")
```

### Mistake 4: Expecting relationship() to create a column
```
# WRONG — no 'books' column exists in the DB; it is virtual
# CORRECT — the FK column lives in the child table; relationship navigates it
```

### Mistake 5: Wiring relationships before objects are in the session
```
# WRONG — SAWarning: Object of type <Book> not in session, add operation will not proceed
book = Book(title=title, author=author)   # author persistent, book transient
# CORRECT — session.add(book) first, then book.author = author
```

---

## Best Practices

1. Always pair both sides with `back_populates` (or one side with backref)
2. Declare association tables before the mapped classes that use them
3. Put both `relationship()` sides inside class bodies; use string annotations
4. Use `cascade="all, delete-orphan"` only on the ONE side of a one-to-many
5. Put `remote_side` on the many-to-one side of self-references
6. Add objects to the session before wiring relationship attributes
7. Let one `add()` persist a whole graph; never hand-build INSERT order
8. Count children before `session.delete()` when you need the number
9. Remember mapper configuration is lazy: errors surface at first use
10. Keep FK columns NOT NULL where the graph requires them

---

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Navigate a loaded relationship | O(1) | O(1) | — |
| Lazy load a collection | 1 extra SELECT | O(children) | eager loading (topic 06) |
| Graph write (author+books+tags) | O(nodes) SQL | O(nodes) | one `add()`, unit of work handles order |
| Cascade delete | O(children) DELETEs | O(1) | DB-level ON DELETE CASCADE |

**Cost note:** each lazy relationship access is one round trip — the root of
the N+1 problem that topic 06 attacks. Relationships are *correctness*
machinery; eager loading is the *performance* lever.

---

## AI Engineering Relevance

**Where this shows up:** experiment tracking graphs (experiment -> runs ->
metrics), model registries (model -> versions -> eval reports), dataset
manifests (dataset -> splits -> samples), and prompt template trees with
inheritance.

| Concept here | Used for |
|---|---|
| one-to-many | experiment -> its eval metrics |
| many-to-many | models <-> tags, datasets <-> users |
| self-referential | prompt template inheritance, dataset hierarchies |
| cascade delete | removing an experiment cleans its runs and metrics |

**Scale note:** at 1M metrics, the graph still loads fine — but each lazy
`experiment.metrics` access becomes a scan unless eager loading (06) is used.
At 200 concurrent writes, graph writes must be short transactions inside
session-per-request (03).

---

## Practice Exercises

### Exercise 1: One-to-Many Readback (Difficulty: Easy)
Build `Author("Tolkien")` with two books, commit, then print every
`book.title` via `author.books` in a fresh session.

### Exercise 2: Cascade Behavior (Difficulty: Medium)
Create an author with three books and a tag shared with another author's book.
Delete the first author. Verify: its books are gone, the tag and the other
book survive, and `book_tag` has no dangling rows.

### Exercise 3: Many-to-Many Reuse (Difficulty: Medium)
Write `create_review_graph` (section 5) and prove the second call with the
same author/tag reuses rows instead of duplicating them.

### Exercise 4: Template Tree (Difficulty: Medium)
Build a 3-level prompt template tree. Walk it from the root: print each node
with its parent and children. Confirm `remote_side` on `parent`.

### Exercise 5: Graph Write Design (Difficulty: Hard)
Design relationships for `Experiment -> Run -> Metric` plus
`Experiment <-> Tag`. Justify the cascade choice per relationship, then
persist a complete graph with one `add()`. (Challenge 04 tests this shape.)

---

## Summary

| Concept | Description |
|---|---|
| `relationship()` | virtual navigation attribute — not a column |
| `back_populates` | keeps both directions of one relationship in sync |
| one-to-many | FK on the child; cascade on the parent side |
| many-to-many | association `Table` + `secondary=` on both sides |
| self-referential | `remote_side` on the many-to-one (parent) side |
| cascade delete | ORM-level cleanup in the same transaction |

Relationships turn schema edges into object graphs. The same graph powers the
queries of topic 05 and the eager-loading decisions of topic 06 — and the
N+1 problem is born right here, from lazily touching collections.

---

## Quick Reference

| Task | Idiom |
|---|---|
| one-to-many | `children: Mapped[list["Child"]] = relationship(back_populates="parent", cascade="all, delete-orphan")` |
| child side | `parent: Mapped["Parent"] = relationship(back_populates="children")` |
| association table | `Table("a_b", Base.metadata, Column("a_id", FK, primary_key=True), Column("b_id", FK, primary_key=True))` |
| many-to-many side | `bs: Mapped[list["B"]] = relationship(secondary=a_b, back_populates="as")` |
| self-ref parent | `parent: Mapped["T | None"] = relationship(back_populates="children", remote_side="T.id")` |
| cascade delete | `session.delete(parent)` then `session.commit()` |

---

## Next Steps

Next: **[05 — Querying with select()](05-querying-2.0-lecture.md)** — read the
graph back with `select()`, joins, filters, and pagination.

Continues in: **[Phase 05 — Databases](../../05-web-frameworks/fastapi/19-orm.py)** —
relationship graphs served by a FastAPI API.

Official docs:
- Relationships: https://docs.sqlalchemy.org/en/20/orm/relationships.html
- Relationship configuration: https://docs.sqlalchemy.org/en/20/orm/relationship_api.html
- Cascades: https://docs.sqlalchemy.org/en/20/orm/cascades.html
