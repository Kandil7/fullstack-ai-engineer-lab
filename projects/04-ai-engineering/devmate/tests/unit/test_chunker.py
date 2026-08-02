"""Unit tests for devmate.ingest.chunker."""

import textwrap

import pytest

from devmate.ingest.chunker import (
    ASTAwareChunker,
    DocumentLoader,
    FixedSizeChunker,
    RecursiveChunker,
    get_chunker,
)


def test_fixed_size_chunker_creates_chunks_with_metadata() -> None:
    content = "word " * 200  # 200 words
    chunker = FixedSizeChunker(chunk_size=100, overlap=10)
    docs = chunker.chunk(content, {"source": "test.md"})

    assert len(docs) > 1
    for doc in docs:
        assert doc.metadata["source"] == "test.md"
        assert doc.metadata["chunker"] == "fixed_size"
        assert doc.metadata["chunk_index"] >= 0
        assert len(doc.id) == 16
        assert len(doc.content) <= 100


def test_fixed_size_chunker_small_content_single_chunk() -> None:
    chunker = FixedSizeChunker(chunk_size=512, overlap=50)
    docs = chunker.chunk("tiny", {"source": "a.txt"})
    assert len(docs) == 1
    assert docs[0].content == "tiny"


def test_recursive_chunker_splits_on_paragraphs() -> None:
    content = textwrap.dedent(
        """\
        Paragraph one with enough words to be its own chunk.

        Paragraph two, also long enough to stand alone.

        Paragraph three, short.
        """
    )
    chunker = RecursiveChunker(chunk_size=64, overlap=0)
    docs = chunker.chunk(content, {"source": "doc.md"})
    assert len(docs) >= 2
    assert all(d.metadata["chunker"] == "recursive" for d in docs)


def test_ast_aware_chunker_extracts_python_functions() -> None:
    content = textwrap.dedent(
        """\
        import os


        def first():
            return 1


        def second():
            return 2


        class Thing:
            def method(self):
                return 3
        """
    )
    chunker = ASTAwareChunker(chunk_size=4096, overlap=0)
    docs = chunker.chunk(content, {"source": "x.py", "language": "python"})

    names = {d.metadata.get("name") for d in docs}
    assert "first" in names
    assert "second" in names
    assert "Thing" in names
    assert all(d.metadata["chunker"] == "ast_aware" for d in docs)


def test_ast_aware_chunker_falls_back_on_syntax_error() -> None:
    chunker = ASTAwareChunker(chunk_size=128, overlap=0)
    docs = chunker.chunk("def broken(:\n", {"source": "bad.py", "language": "python"})
    assert docs  # falls back to recursive, never raises


def test_get_chunker_registry() -> None:
    assert isinstance(get_chunker("fixed"), FixedSizeChunker)
    assert isinstance(get_chunker("recursive"), RecursiveChunker)
    assert isinstance(get_chunker("ast_aware"), ASTAwareChunker)
    with pytest.raises(ValueError):
        get_chunker("nope")


def test_document_loader_skips_binary_and_unsupported(tmp_path) -> None:
    loader = DocumentLoader()
    (tmp_path / "readme.md").write_text("# hi\n", encoding="utf-8")
    (tmp_path / "blob.bin").write_bytes(b"\x00\x01")
    (tmp_path / "weird.xyz").write_text("nope\n", encoding="utf-8")

    docs = list(loader.load_directory(tmp_path, recursive=False))
    assert len(docs) == 1
    assert docs[0].metadata["filename"] == "readme.md"
