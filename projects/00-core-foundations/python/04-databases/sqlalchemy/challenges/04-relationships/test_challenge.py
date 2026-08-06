"""
Challenge 04: Relationships — Hidden Tests
============================================
Graph writes, many-to-many navigation, and cascade cleanup.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


def _load(name: str):
    """Load a sibling module under a UNIQUE name registered in sys.modules.

    Registration matters: SQLAlchemy resolves Mapped[...] annotations
    through the module's globals when a mapped class is configured.
    The unique name (challenge dir embedded) prevents collisions
    between the 10 challenge suites in one pytest process.
    """
    parent = Path(__file__).parent.name.replace("-", "_")
    modname = f"{name}_{parent}"
    spec = importlib.util.spec_from_file_location(
        modname, Path(__file__).parent / f"{name}.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[modname] = module
    spec.loader.exec_module(module)
    return module


starter = _load("starter")
solution = _load("solution")


@pytest.fixture()
def session():
    """Fresh engine + schema + session per test: no cross-test pollution."""
    engine = create_engine("sqlite://", poolclass=StaticPool)
    solution.Base.metadata.create_all(engine)
    with Session(bind=engine) as s:
        yield s
    engine.dispose()


class TestStarterRaises:
    def test_create_graph_starter_raises(self, session):
        with pytest.raises(NotImplementedError):
            starter.create_review_graph(session, "Hobbit", ["fantasy"])

    def test_find_by_tag_starter_raises(self, session):
        with pytest.raises(NotImplementedError):
            starter.find_books_by_tag(session, "fantasy")

    def test_delete_cascade_starter_raises(self, session):
        with pytest.raises(NotImplementedError):
            starter.delete_author_cascade(session, "Tolkien")


class TestCreateReviewGraph:
    def test_returns_book_and_tag_ids(self, session):
        book_id, tag_ids = solution.create_review_graph(session, "Hobbit", ["fantasy"])
        assert isinstance(book_id, int) and book_id > 0
        assert len(tag_ids) == 1 and isinstance(tag_ids[0], int)

    def test_creates_default_author(self, session):
        solution.create_review_graph(session, "Hobbit", [])
        authors = session.scalars(select(solution.Author.name)).all()
        assert authors == ["Review Bot"]

    def test_reuses_existing_author(self, session):
        solution.create_review_graph(session, "Hobbit", [])
        book_id, _ = solution.create_review_graph(session, "Silmarillion", [])
        authors = session.scalars(select(solution.Author)).all()
        assert len(authors) == 1, "the second graph write must reuse the author"
        assert session.get(solution.Book, book_id).author_id == authors[0].id

    def test_reuses_existing_tags(self, session):
        _, first_tags = solution.create_review_graph(session, "Hobbit", ["fantasy"])
        _, second_tags = solution.create_review_graph(session, "LOTR", ["fantasy"])
        assert first_tags == second_tags, "existing tag must be reused, not duplicated"
        assert len(session.scalars(select(solution.Tag)).all()) == 1

    def test_persists_graph_in_db(self, session):
        book_id, _ = solution.create_review_graph(
            session, "Hobbit", ["fantasy", "classic"]
        )
        book = session.get(solution.Book, book_id)
        assert book.title == "Hobbit"
        assert sorted(t.label for t in book.tags) == ["classic", "fantasy"]


class TestFindBooksByTag:
    def test_returns_sorted_titles(self, session):
        solution.create_review_graph(session, "Hobbit", ["fantasy"])
        solution.create_review_graph(session, "Silmarillion", ["fantasy"])
        assert solution.find_books_by_tag(session, "fantasy") == [
            "Hobbit",
            "Silmarillion",
        ]

    def test_unknown_tag_is_empty(self, session):
        assert solution.find_books_by_tag(session, "nope") == []

    def test_tag_without_books_is_empty(self, session):
        session.add(solution.Tag(label="lonely"))
        session.commit()
        assert solution.find_books_by_tag(session, "lonely") == []


class TestDeleteAuthorCascade:
    def _seed(self, session) -> None:
        solution.create_review_graph(
            session, "Hobbit", ["fantasy"], author_name="Tolkien"
        )
        solution.create_review_graph(
            session, "LOTR", ["fantasy"], author_name="Tolkien"
        )
        solution.create_review_graph(session, "Narnia", [], author_name="Lewis")

    def test_returns_removed_book_count(self, session):
        self._seed(session)
        assert solution.delete_author_cascade(session, "Tolkien") == 2

    def test_books_are_deleted(self, session):
        self._seed(session)
        solution.delete_author_cascade(session, "Tolkien")
        titles = session.scalars(select(solution.Book.title)).all()
        assert titles == ["Narnia"], "only the deleted author's books may go"

    def test_other_authors_untouched(self, session):
        self._seed(session)
        solution.delete_author_cascade(session, "Tolkien")
        remaining = session.scalars(select(solution.Author.name)).all()
        assert remaining == ["Lewis"]

    def test_association_rows_cleaned(self, session):
        self._seed(session)
        solution.delete_author_cascade(session, "Tolkien")
        assoc = session.execute(select(solution.book_tag)).all()
        assert assoc == [], "book_tag rows of deleted books must vanish"

    def test_missing_author_returns_zero(self, session):
        self._seed(session)
        assert solution.delete_author_cascade(session, "Nobody") == 0
        assert len(session.scalars(select(solution.Book)).all()) == 3
