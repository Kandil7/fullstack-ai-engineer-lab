# Relationships — Glossary 04

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| association table | Relationship | A third table holding the FK pair of a many-to-many |
| back_populates | Relationship | Wires two sides of one relationship so both stay in sync |
| cascade | Relationship | Unit-of-work behaviors propagated along a relationship |
| delete-orphan | Cascade | Deleting a parent also deletes its children |
| ForeignKey | Schema | A column referencing another table's column |
| lazy | Loading | Default loading: children fetched on first access |
| many-to-many | Relationship | Both sides hold collections via `secondary=` |
| one-to-many | Relationship | Parent holds a collection; child holds the FK |
| remote_side | Relationship | Names the FK target; lives on the many-to-one side |
| relationship() | Relationship | Virtual navigation attribute between mapped classes |
| save-update | Cascade | Adds related objects to the session automatically |
| secondary | Relationship | The association table used by a many-to-many |
| self-referential | Relationship | A class related to itself (trees) |
| virtual attribute | Relationship | A relationship is NOT a column and stores nothing |
| backref | Relationship | One-sided shorthand that creates the other side |
| graph write | Pattern | One add() persists a whole object graph |

## Detailed Definitions

### association table
**Definition**: The third table holding the two FKs of a many-to-many. A plain
Core `Table` suffices when it has no extra columns.
**Example**:
```python
from sqlalchemy import Column, ForeignKey, Table
book_tag = Table(
    "book_tag", Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)
```
**Related**: many-to-many, secondary

### back_populates
**Definition**: Declares the counterpart attribute name on the other class,
keeping both directions of ONE relationship in sync — append on one side and
the other sees it immediately.
**Example**:
```python
class Author(Base):
    books: Mapped[list["Book"]] = relationship(back_populates="author")

class Book(Base):
    author: Mapped["Author"] = relationship(back_populates="books")
```
**Related**: backref, relationship()

### cascade
**Definition**: Unit-of-work behaviors propagated along a relationship —
what happens to children when the parent is saved or deleted. `all,
delete-orphan` is the one-to-many standard.
**Example**:
```python
books: Mapped[list["Book"]] = relationship(
    back_populates="author", cascade="all, delete-orphan"
)
```
**Related**: delete-orphan, save-update

### delete-orphan
**Definition**: Cascade behavior: when a parent is deleted (or a child is
removed from its collection), the child rows are deleted too. Only for
one-to-many; never for many-to-many.
**Related**: cascade, one-to-many

### ForeignKey
**Definition**: A column referencing another table's column — the schema edge
the relationship navigates. Declared as a string so order does not matter.
**Related**: one-to-many, self-referential

### lazy
**Definition**: The default loading strategy: related rows are fetched with a
query on first attribute access. Correctness-friendly; the seed of N+1
(topic 06).
**Example**:
```python
print(len(author.books))   # fires a SELECT the first time
```
**Related**: relationship(), one-to-many

### many-to-many
**Definition**: Both sides hold collections of the other. Needs an
association table and `secondary=` on both `relationship()`s.
**Example**:
```python
tags: Mapped[list["Tag"]] = relationship(
    secondary=book_tag, back_populates="books"
)
```
**Related**: association table, secondary

### one-to-many
**Definition**: A parent holds a collection of children; the FK lives in the
child table. The parent side carries the cascade.
**Related**: ForeignKey, cascade

### remote_side
**Definition**: Names the column the FK points TO. Belongs on the many-to-one
side of a self-reference, or SQLAlchemy cannot determine the direction.
**Example**:
```python
parent: Mapped["PromptTemplate | None"] = relationship(
    back_populates="children", remote_side="PromptTemplate.id"
)
```
**Related**: self-referential

### relationship()
**Definition**: The virtual navigation attribute between mapped classes. Not
a column: no storage, just the instructions for finding related rows.
**Example**:
```python
books: Mapped[list["Book"]] = relationship(back_populates="author")
```
**Related**: virtual attribute, back_populates

### save-update
**Definition**: The default cascade: related objects are saved (added to the
session) automatically when their parent is saved. Safe for many-to-many.
**Related**: cascade, delete-orphan

### secondary
**Definition**: The association table named in a many-to-many
`relationship(secondary=book_tag, ...)`; SQLAlchemy writes/removes the pair
rows automatically.
**Related**: many-to-many, association table

### self-referential
**Definition**: A class related to itself — prompt template inheritance,
dataset hierarchies. Needs `remote_side` on the parent side.
**Related**: remote_side, relationship()

### virtual attribute
**Definition**: What a relationship is: navigation metadata, not a column.
There is no `books` column in the DB; the FK lives in the child.
**Related**: relationship(), ForeignKey

### backref
**Definition**: One-sided shorthand: `relationship("Child", backref="parent")`
creates the reverse attribute automatically. Explicit `back_populates` is
preferred for clarity.
**Related**: back_populates, relationship()

### graph write
**Definition**: The unit-of-work pattern where one `session.add(parent)`
persists the whole graph — author, books, tags — in dependency order.
**Example**:
```python
session.add(book)      # persists book + author + tags
session.commit()
```
**Related**: cascade, save-update

## Key Concepts Summary

### The Three Shapes
- one-to-many: FK in the child; cascade on the parent
- many-to-many: association table + `secondary=` on both sides
- self-referential: `remote_side` on the many-to-one side

### Cascade Discipline
- `all, delete-orphan` only on one-to-many
- default (save-update, merge) on many-to-many
- cascade is ORM behavior; the DB knows nothing unless ON DELETE is set

### Declaration Order
- association tables before the mapped classes that use them
- relationships inside class bodies with string annotations
- mapper configuration is lazy: errors surface at first use

## Practice Terms

Match each term to its definition (answers at the bottom).

1. association table — ___
2. delete-orphan — ___
3. remote_side — ___
4. virtual attribute — ___
5. save-update — ___
6. secondary — ___

A) Deletes children when the parent is deleted
B) Third table holding the FK pair
C) Names the FK target on the many-to-one side
D) The association table named in a many-to-many
E) Navigation metadata, not a column
F) Default cascade that saves related objects

**Answers:** 1-B, 2-A, 3-C, 4-E, 5-F, 6-D
