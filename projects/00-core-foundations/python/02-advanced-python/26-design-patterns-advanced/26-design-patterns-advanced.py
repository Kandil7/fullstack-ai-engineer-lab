"""
Advanced Python - 26: Advanced Design Patterns
===============================================
Topics: Dependency Injection; Repository; Unit of Work; Strategy vs
        singledispatch; Adapter; Chain of Responsibility; Command with
        undo; Builder; Registry via __init_subclass__; composition over
        inheritance; when a pattern is over-engineering.

Why this matters for AI/backend engineering:
    A `VectorStore` interface with Qdrant/Chroma/FAISS adapters is the
    canonical Adapter story. Dependency Injection is how tests run
    against a FakeLLM instead of paying for real API calls. A plugin
    registry (__init_subclass__) is how agent tool frameworks auto-
    discover tools. Patterns here are not decoration: they are the
    seams that make an AI system testable and swappable.

Run:      python 26-design-patterns-advanced.py
Verify:   python 26-design-patterns-advanced.py --verify
Reference: https://docs.python.org/3/library/abc.html
           https://docs.python.org/3/library/functools.html#functools.singledispatch
"""

from __future__ import annotations

import functools
import os
import random
import sys
from abc import ABC, abstractmethod
from typing import Protocol

random.seed(42)
os.environ.setdefault("MPLBACKEND", "Agg")   # never open a GUI window

# ============================================================
# 1. Dependency Injection: Testability First
# ============================================================
# Instead of the service creating its own LLM client, the client is
# *injected*. Production passes the real one; tests pass a fake. The
# service never knows the difference -- and never makes network calls
# in a test.

class LLMClient(Protocol):
    """The contract every LLM client (real or fake) must satisfy."""

    def complete(self, prompt: str) -> str: ...


class RealOpenAIClient:
    """The production client. Never instantiated in tests."""

    def complete(self, prompt: str) -> str:
        raise NotImplementedError("would call the API here")


class FakeLLMClient:
    """A deterministic stand-in: no network, fixed output, call log."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def complete(self, prompt: str) -> str:
        self.calls.append(prompt)
        return f"FAKE:{prompt[:5]}"


class Summarizer:
    """Summarizes text using whatever LLM client it was given."""

    def __init__(self, client: LLMClient) -> None:
        self._client = client

    def summarize(self, text: str) -> str:
        return self._client.complete(f"summarize: {text}")


def demo_di() -> FakeLLMClient:
    """Inject a fake client and observe it being used."""
    fake = FakeLLMClient()
    svc = Summarizer(fake)
    out = svc.summarize("long article")
    print(f"  summary via injected fake: {out!r}")
    print(f"  fake recorded {len(fake.calls)} call(s)")
    return fake
    # Output:
    #   summary via injected fake: 'FAKE:summa'
    #   fake recorded 1 call(s)


# ============================================================
# 2. Repository: Data Access Behind an Interface
# ============================================================
# The service talks to a Repository protocol; swap SQLite for Postgres
# or for an in-memory fake without touching the service.

class UserRecord:
    """A plain data record."""

    def __init__(self, user_id: int, name: str) -> None:
        self.user_id = user_id
        self.name = name


class UserRepository(Protocol):
    """Data-access contract for user storage."""

    def get(self, user_id: int) -> UserRecord | None: ...

    def save(self, record: UserRecord) -> None: ...


class InMemoryUserRepository:
    """A real (test-friendly) implementation: no database at all."""

    def __init__(self) -> None:
        self._store: dict[int, UserRecord] = {}

    def get(self, user_id: int) -> UserRecord | None:
        return self._store.get(user_id)

    def save(self, record: UserRecord) -> None:
        self._store[record.user_id] = record


class UserService:
    """Uses the repository; never touches storage details."""

    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    def rename(self, user_id: int, new_name: str) -> str:
        record = self._repo.get(user_id)
        if record is None:
            raise KeyError(f"no user {user_id}")
        record.name = new_name
        self._repo.save(record)
        return record.name


def demo_repository() -> UserService:
    """CRUD through an interface, backed by memory."""
    repo = InMemoryUserRepository()
    repo.save(UserRecord(1, "ada"))
    svc = UserService(repo)
    svc.rename(1, "ada lovelace")
    print(f"  renamed via repository: {repo.get(1).name!r}")
    return svc
    # Output:
    #   renamed via repository: 'ada lovelace'


# ============================================================
# 3. Unit of Work: Commit or Roll Back as a Group
# ============================================================
# A context manager wraps a batch of repository operations. If any step
# raises, the whole batch rolls back. This is the shape of a DB
# transaction -- and of a batch job that must be all-or-nothing.

class UnitOfWork:
    """Track writes; commit() persists, rollback() discards."""

    def __init__(self, repo: InMemoryUserRepository) -> None:
        self._repo = repo
        self._pending: dict[int, UserRecord] = {}
        self._deleted: list[int] = []

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> bool:
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        return False

    def mark_saved(self, record: UserRecord) -> None:
        self._pending[record.user_id] = record

    def mark_deleted(self, user_id: int) -> None:
        self._deleted.append(user_id)

    def commit(self) -> None:
        for record in self._pending.values():
            self._repo.save(record)
        self._pending.clear()

    def rollback(self) -> None:
        self._pending.clear()
        self._deleted.clear()


def demo_unit_of_work() -> None:
    """A failing batch leaves the repository untouched."""
    repo = InMemoryUserRepository()
    repo.save(UserRecord(1, "ada"))
    try:
        with UnitOfWork(repo) as uow:
            uow.mark_saved(UserRecord(2, "grace"))
            raise RuntimeError("mid-batch failure")
    except RuntimeError:
        pass
    print(f"  repo size after rollback: {len(repo._store)}")
    print(f"  user 1 still present: {repo.get(1) is not None}")
    # Output:
    #   repo size after rollback: 1
    #   user 1 still present: True


# ============================================================
# 4. Strategy vs singledispatch
# ============================================================
# Strategy: interchangeable objects chosen by the caller. singledispatch:
# dispatch on the *type* of the first argument -- a runtime registry of
# functions. Choose Strategy when the variant carries state or behavior
# beyond one function; choose singledispatch for stateless one-liners.

class SummarizeStrategy(ABC):
    """Strategy: a family of interchangeable summarizers."""

    @abstractmethod
    def summarize(self, text: str, max_len: int) -> str: ...


class ExtractStrategy(SummarizeStrategy):
    """Keep the first sentence."""

    def summarize(self, text: str, max_len: int) -> str:
        return text.split(".")[0] + "."


class TruncateStrategy(SummarizeStrategy):
    """Cut to max_len characters."""

    def summarize(self, text: str, max_len: int) -> str:
        return text[:max_len] + "..."


@functools.singledispatch
def score(value: object) -> str:
    """Score an embedding artifact by its type (dispatch registry)."""
    return f"generic:{value}"


@score.register
def _score_list(value: list) -> str:
    return f"list:{len(value)}"


@score.register
def _score_dict(value: dict) -> str:
    return f"dict:{len(value)}"


def demo_strategy_vs_dispatch() -> None:
    """Two strategy objects; one dispatch registry."""
    text = "The quick brown fox jumps over the lazy dog. More text here."
    print(f"  extract strategy: {ExtractStrategy().summarize(text, 10)!r}")
    print(f"  truncate strategy: {TruncateStrategy().summarize(text, 10)!r}")
    print(f"  dispatch on list : {score([1, 2, 3])}")
    print(f"  dispatch on dict : {score({'a': 1})}")
    print(f"  dispatch on str  : {score('hi')}")
    # Output:
    #   extract strategy: 'The quick brown fox jumps over the lazy dog.'
    #   truncate strategy: 'The quick ...'
    #   dispatch on list : list:3
    #   dispatch on dict : dict:1
    #   dispatch on str  : generic:hi


# ============================================================
# 5. Adapter: Incompatible APIs, One Interface
# ============================================================
# Qdrant and Chroma expose different method names and shapes. An Adapter
# per vendor makes both satisfy the VectorStore protocol, so the pipeline
# code is vendor-agnostic. Complexity: O(1) per call, thin wrapper.

class VectorStore(Protocol):
    """The interface the application actually uses."""

    def search(self, query: str, top_k: int) -> list[float]: ...


class QdrantStore:
    """Vendor A: qdrant-style API (search_vector)."""

    def search_vector(self, text: str, limit: int) -> list[float]:
        return [float(len(text) + i) for i in range(limit)]


class ChromaStore:
    """Vendor B: chroma-style API (query_collection, returns tuples)."""

    def query_collection(self, text: str, n_results: int) -> list[tuple[str, float]]:
        return [(f"doc-{i}", float(len(text) + i)) for i in range(n_results)]


class QdrantAdapter:
    """Makes QdrantStore speak VectorStore."""

    def __init__(self, vendor: QdrantStore) -> None:
        self._vendor = vendor

    def search(self, query: str, top_k: int) -> list[float]:
        return self._vendor.search_vector(query, top_k)


class ChromaAdapter:
    """Makes ChromaStore speak VectorStore (drops its tuple shape)."""

    def __init__(self, vendor: ChromaStore) -> None:
        self._vendor = vendor

    def search(self, query: str, top_k: int) -> list[float]:
        return [score for _, score in self._vendor.query_collection(query, top_k)]


def run_pipeline(store: VectorStore, query: str) -> list[float]:
    """Application code: works with ANY VectorStore."""
    return store.search(query, 2)


def demo_adapter() -> None:
    """Both vendors behind one protocol; results have the same shape."""
    qdrant_out = run_pipeline(QdrantAdapter(QdrantStore()), "cat")
    chroma_out = run_pipeline(ChromaAdapter(ChromaStore()), "cat")
    print(f"  qdrant via adapter: {qdrant_out}")
    print(f"  chroma via adapter: {chroma_out}")
    print(f"  same shape: {len(qdrant_out) == len(chroma_out)}")
    # Output:
    #   qdrant via adapter: [3.0, 4.0]
    #   chroma via adapter: [3.0, 4.0]
    #   same shape: True


# ============================================================
# 6. Chain of Responsibility: Middleware
# ============================================================
# Each handler either handles the request or passes it on. This is the
# shape of middleware stacks: auth -> rate limit -> logging -> the call.

class Handler(ABC):
    """A middleware link."""

    def __init__(self) -> None:
        self._next: Handler | None = None

    def set_next(self, nxt: "Handler") -> "Handler":
        self._next = nxt
        return nxt

    def handle(self, request: str) -> str:
        if self._next is not None:
            return self._next.handle(request)
        return "processed"


class AuthHandler(Handler):
    """Rejects requests without a token."""

    def handle(self, request: str) -> str:
        if "token=" not in request:      # "no-token" contains 'token'!
            return "DENIED:missing-token"
        return super().handle(request)


class RateLimitHandler(Handler):
    """Enforces a trivial max-calls budget."""

    def __init__(self, budget: int) -> None:
        super().__init__()
        self._budget = budget

    def handle(self, request: str) -> str:
        if self._budget <= 0:
            return "DENIED:rate-limited"
        self._budget -= 1
        return super().handle(request)


class LoggingHandler(Handler):
    """Records every request that reaches it."""

    def __init__(self) -> None:
        super().__init__()
        self.seen: list[str] = []

    def handle(self, request: str) -> str:
        self.seen.append(request)
        return super().handle(request)


def demo_chain() -> None:
    """auth -> rate limit -> logging -> processor, in order."""
    logger = LoggingHandler()
    chain = AuthHandler()
    chain.set_next(RateLimitHandler(2)).set_next(logger)
    print(f"  no token : {chain.handle('ask')}")
    print(f"  with token: {chain.handle('ask token=abc')}")
    print(f"  logged requests: {len(logger.seen)}")
    # Output:
    #   no token : DENIED:missing-token
    #   with token: processed
    #   logged requests: 1


# ============================================================
# 7. Command with Undo
# ============================================================
# Operations become objects that know how to do AND undo themselves.
# The editor keeps a history; Ctrl+Z pops the last command and undoes it.

class TextBuffer:
    """A tiny mutable document."""

    def __init__(self, text: str = "") -> None:
        self.text = text


class Command(ABC):
    """A reversible operation."""

    @abstractmethod
    def execute(self, buf: TextBuffer) -> None: ...

    @abstractmethod
    def undo(self, buf: TextBuffer) -> None: ...


class InsertCommand(Command):
    """Insert text at a position (undo: remove it)."""

    def __init__(self, pos: int, text: str) -> None:
        self._pos = pos
        self._text = text

    def execute(self, buf: TextBuffer) -> None:
        buf.text = buf.text[: self._pos] + self._text + buf.text[self._pos:]

    def undo(self, buf: TextBuffer) -> None:
        end = self._pos + len(self._text)
        buf.text = buf.text[: self._pos] + buf.text[end:]


class DeleteCommand(Command):
    """Delete a range (undo: re-insert what was removed)."""

    def __init__(self, pos: int, length: int) -> None:
        self._pos = pos
        self._length = length
        self._removed = ""

    def execute(self, buf: TextBuffer) -> None:
        self._removed = buf.text[self._pos: self._pos + self._length]
        buf.text = buf.text[: self._pos] + buf.text[self._pos + self._length:]

    def undo(self, buf: TextBuffer) -> None:
        buf.text = buf.text[: self._pos] + self._removed + buf.text[self._pos:]


class Editor:
    """Applies commands and keeps an undo stack."""

    def __init__(self) -> None:
        self._history: list[Command] = []

    def apply(self, cmd: Command, buf: TextBuffer) -> None:
        cmd.execute(buf)
        self._history.append(cmd)

    def undo(self, buf: TextBuffer) -> None:
        if self._history:
            self._history.pop().undo(buf)


def demo_command() -> TextBuffer:
    """Insert, delete, then undo both operations."""
    buf = TextBuffer("hello world")
    editor = Editor()
    editor.apply(InsertCommand(0, "say "), buf)   # "say hello world"
    editor.apply(DeleteCommand(4, 6), buf)        # delete "hello " -> "say world"
    print(f"  after commands: {buf.text!r}")
    editor.undo(buf)
    print(f"  after one undo: {buf.text!r}")
    editor.undo(buf)
    print(f"  after two undos: {buf.text!r}")
    return buf
    # Output:
    #   after commands: 'say world'
    #   after one undo: 'say hello world'
    #   after two undos: 'hello world'


# ============================================================
# 8. Builder: Complex Configurations Step by Step
# ============================================================
# A Builder separates *how* a complex object is assembled from the object
# itself. Fluent methods make the assembly read like a sentence.

class InferenceConfig:
    """An immutable-ish configuration assembled by its Builder."""

    def __init__(self, model: str, temperature: float, max_tokens: int,
                 timeout: float) -> None:
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout


class InferenceConfigBuilder:
    """Fluent builder with defaults and validation."""

    def __init__(self) -> None:
        self._model = "default-model"
        self._temperature = 0.7
        self._max_tokens = 256
        self._timeout = 30.0

    def with_model(self, model: str) -> "InferenceConfigBuilder":
        self._model = model
        return self

    def with_temperature(self, value: float) -> "InferenceConfigBuilder":
        if not 0.0 <= value <= 2.0:
            raise ValueError("temperature must be in [0, 2]")
        self._temperature = value
        return self

    def with_max_tokens(self, value: int) -> "InferenceConfigBuilder":
        self._max_tokens = value
        return self

    def build(self) -> InferenceConfig:
        return InferenceConfig(self._model, self._temperature,
                               self._max_tokens, self._timeout)


def demo_builder() -> InferenceConfig:
    """Assemble a config without a 4-argument constructor call."""
    cfg = (InferenceConfigBuilder()
           .with_model("llama-3.1-70b")
           .with_temperature(0.2)
           .with_max_tokens(1024)
           .build())
    print(f"  built config: model={cfg.model}, temp={cfg.temperature}, "
          f"max={cfg.max_tokens}")
    return cfg
    # Output:
    #   built config: model=llama-3.1-70b, temp=0.2, max=1024


# ============================================================
# 9. Registry via __init_subclass__
# ============================================================
# Every subclass is auto-registered at class creation time -- no manual
# list, no decorator bookkeeping. Agent tool frameworks use exactly this
# to discover tools. Complexity: O(1) per registration.

class Tool(ABC):
    """Base tool: subclasses register themselves by name."""

    _registry: dict[str, type["Tool"]] = {}

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        name = getattr(cls, "name", None)
        if name is not None:
            Tool._registry[name] = cls

    @classmethod
    def create(cls, name: str) -> "Tool":
        """Factory: instantiate the registered tool by name."""
        return cls._registry[name]()

    @abstractmethod
    def run(self, query: str) -> str: ...


class SearchTool(Tool):
    """Tool 1: registered the moment the class is defined."""

    name = "search"

    def run(self, query: str) -> str:
        return f"search({query})"


class EmbedTool(Tool):
    """Tool 2: registration requires zero extra code."""

    name = "embed"

    def run(self, query: str) -> str:
        return f"embed({query})"


def demo_registry() -> None:
    """Subclasses auto-register; the factory finds them by name."""
    print(f"  discovered tools: {sorted(Tool._registry)}")
    search = Tool.create("search")
    print(f"  factory built: {search.run('cat')}")
    # Output:
    #   discovered tools: ['embed', 'search']
    #   factory built: search(cat)


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: applying a pattern to make code "professional" when a plain
#   function would do. If there is exactly one implementation and no
#   plan to swap it, the interface is decoration.
# CORRECT: add the seam (protocol, injected dependency) when the second
#   implementation appears -- or when tests need a fake.
# MISTAKE: deep inheritance hierarchies when composition + injection
#   express the same design with less coupling.
# MISTAKE: registries that require manual bookkeeping (forgot to add the
#   new tool to the list).
# CORRECT: __init_subclass__ / entry points -- discovery, not lists.


# ============================================================
# Self-Verification  (MANDATORY -- every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # 1. DI: a fake client is used; the real one is never touched.
    fake = FakeLLMClient()
    svc = Summarizer(fake)
    assert svc.summarize("article") == "FAKE:summa", \
        "DI must route calls through the injected client"
    assert len(fake.calls) == 1, "injected fake must record the call"
    assert fake.calls[0] == "summarize: article", \
        "fake must receive the exact prompt"

    # 2. Repository: interface-backed storage works without a database.
    repo = InMemoryUserRepository()
    repo.save(UserRecord(1, "ada"))
    svc = UserService(repo)
    assert svc.rename(1, "ada lovelace") == "ada lovelace", \
        "service must rename through the repository"
    assert repo.get(1).name == "ada lovelace", \
        "rename must persist in the repository"

    # 3. Unit of Work: a failing batch rolls back everything.
    repo = InMemoryUserRepository()
    repo.save(UserRecord(1, "ada"))
    try:
        with UnitOfWork(repo) as uow:
            uow.mark_saved(UserRecord(2, "grace"))
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    assert repo.get(2) is None, \
        "unit of work must roll back writes on failure"
    assert repo.get(1) is not None, "rollback must keep prior committed state"

    # 4. Adapter: two incompatible vendor APIs become interchangeable.
    qdrant_out = run_pipeline(QdrantAdapter(QdrantStore()), "cat")
    chroma_out = run_pipeline(ChromaAdapter(ChromaStore()), "cat")
    assert qdrant_out == chroma_out, \
        "adapters must make both vendors produce identical results"
    assert len(qdrant_out) == 2 and len(chroma_out) == 2, \
        "adapter output must respect top_k"

    # 5. Chain of Responsibility: each link runs in order, gates work.
    logger = LoggingHandler()
    chain = AuthHandler()
    chain.set_next(RateLimitHandler(2)).set_next(logger)
    assert chain.handle("no-token") == "DENIED:missing-token", \
        "auth must reject requests without a token"
    assert chain.handle("ok token=1") == "processed", \
        "authorized request must reach the processor"
    assert logger.seen == ["ok token=1"], \
        "logging handler must see only requests that passed auth"

    # 6. Command: undo restores the exact previous state.
    buf = TextBuffer("hello world")
    editor = Editor()
    editor.apply(InsertCommand(0, "say "), buf)
    editor.apply(DeleteCommand(4, 6), buf)
    assert buf.text == "say world", "commands must transform the buffer"
    editor.undo(buf)
    assert buf.text == "say hello world", "first undo must restore the insert"
    editor.undo(buf)
    assert buf.text == "hello world", "second undo must restore the original"

    # 7. Builder: fluent assembly + validation.
    cfg = (InferenceConfigBuilder()
           .with_model("llama-3.1-70b")
           .with_temperature(0.2)
           .with_max_tokens(1024)
           .build())
    assert cfg.model == "llama-3.1-70b" and cfg.max_tokens == 1024, \
        "builder must carry every fluent step into the config"
    try:
        InferenceConfigBuilder().with_temperature(3.0)
        bad_temp = False
    except ValueError:
        bad_temp = True
    assert bad_temp, "builder must reject out-of-range temperatures"

    # 8. Strategy and singledispatch both dispatch correctly.
    assert ExtractStrategy().summarize("A. B.", 5) == "A.", \
        "extract strategy must keep the first sentence"
    assert TruncateStrategy().summarize("hello world", 5) == "hello...", \
        "truncate strategy must cut to max_len"
    assert score([1, 2]) == "list:2", "singledispatch must route lists"
    assert score({"a": 1}) == "dict:1", "singledispatch must route dicts"
    assert score("hi") == "generic:hi", "singledispatch must use the default"

    # 9. Registry: subclasses are discovered, factory constructs by name.
    assert "search" in Tool._registry and "embed" in Tool._registry, \
        "__init_subclass__ must auto-register both tools"
    assert isinstance(Tool.create("search"), SearchTool), \
        "factory must build the right subclass by name"

    print("\n[OK] 26-design-patterns-advanced: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("=" * 60)
        print("ADVANCED DESIGN PATTERNS: SEAMS FOR TESTABLE AI SYSTEMS")
        print("=" * 60)
        print("\n--- 1. Dependency Injection ---")
        demo_di()
        print("\n--- 2. Repository ---")
        demo_repository()
        print("\n--- 3. Unit of Work ---")
        demo_unit_of_work()
        print("\n--- 4. Strategy vs singledispatch ---")
        demo_strategy_vs_dispatch()
        print("\n--- 5. Adapter (VectorStore) ---")
        demo_adapter()
        print("\n--- 6. Chain of Responsibility ---")
        demo_chain()
        print("\n--- 7. Command with undo ---")
        demo_command()
        print("\n--- 8. Builder ---")
        demo_builder()
        print("\n--- 9. Registry via __init_subclass__ ---")
        demo_registry()
        print("\n--- Summary ---")
        print("1. DI + Repository + Unit of Work = testable data layer.")
        print("2. Adapter makes providers swappable; CoR = middleware.")
        print("3. Command gives undo; registry gives auto-discovery.")
        _verify()
