# Challenge 04: Relationships — Book/Author/Tag Graph

## 🥉 Bronze — One Graph Write (~20 min)

**Task:** Implement `create_review_graph(title, tags, author_name)` which persists
an author, a book, and its tags in **one** `add()` — the unit of work writes the
whole graph in the correct dependency order.

**Signature:**
```python
def create_review_graph(title: str, tags: list[str], author_name: str = "Review Bot") -> tuple[int, list[int]]
```

**Requirements:**
- Reuse the author when `author_name` already exists; otherwise create it
- Reuse existing tags by `label`; create only missing ones
- Return `(book_id, [tag_ids])`
- Book `author_id` is NOT NULL — the graph write must always satisfy it

| Input | Expected |
|---|---|
| `create_review_graph("Hobbit", ["fantasy"])` | `(book_id, [tag_id])`, author "Review Bot" |
| second call, same author | same author id, no duplicate author row |

---

## 🥈 Silver — Navigate Many-to-Many (~35 min)

**Task:** Implement `find_books_by_tag(session, tag_label)` which returns the
titles of every book carrying that tag, sorted ascending.

**Signature:**
```python
def find_books_by_tag(session: Session, tag_label: str) -> list[str]:
```

**Requirements:**
- Traverse `tag -> books` (the many-to-many relationship)
- Return `[]` for a tag that does not exist or has no books

| Input | Expected |
|---|---|
| tag "fantasy" on books "Hobbit", "Silmarillion" | `["Hobbit", "Silmarillion"]` |
| unknown tag | `[]` |

---

## 🥇 Gold — Cascade Delete (~75 min)

**Task:** Implement `delete_author_cascade(session, author_name)` which deletes
an author **and** all their books, and returns how many books were removed.

**Signature:**
```python
def delete_author_cascade(session: Session, author_name: str) -> int:
```

**Requirements:**
- The delete must clean up books (cascade `all, delete-orphan` on `Author.books`)
- Association rows (`book_tag`) must vanish with the books
- Authors/books owned by OTHER authors stay untouched
- Missing author → `0`

| Input | Expected |
|---|---|
| author with 2 books | `2`, books gone, other authors intact |
| unknown author | `0` |

**Follow-up:** what would happen without the cascade? (Answer: `DELETE` of the
author succeeds but `books.author_id` dangles — a broken graph and, with FK
enforcement, an `IntegrityError`.)

---

## Running

```bash
pytest challenges/04-relationships/test_challenge.py -v
```

## Test File Structure

```
challenges/04-relationships/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
