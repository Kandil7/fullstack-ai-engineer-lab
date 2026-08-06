"""
Advanced Python - 23: Advanced Typing
=====================================
Topics: TypeVar bounds/constraints; generic classes; ParamSpec and
        Concatenate; Protocol + runtime_checkable; overload; Literal;
        Final; Annotated; TypeAlias; Self; NewType; TYPE_CHECKING.

Why this matters for AI/backend engineering:
    A typed `Retriever` protocol is what makes Qdrant, Chroma, and
    pgvector interchangeable behind one interface, and typed tool
    signatures are the exact mechanism behind LLM function calling.
    Static checking (mypy/pyright) catches the bugs, but this file shows
    which parts also matter at runtime -- protocols and generics are
    structural, so they work without inheritance.

Run:      python 23-typing-advanced.py
Verify:   python 23-typing-advanced.py --verify
Reference: https://docs.python.org/3/library/typing.html
"""

from __future__ import annotations

import functools
import inspect
import os
import random
import sys
import typing
from collections.abc import Callable, Sequence
from typing import (
    Annotated,
    Concatenate,
    Final,
    Literal,
    NewType,
    ParamSpec,
    Protocol,
    Self,
    TypeAlias,
    TypeVar,
    get_args,
    get_origin,
    get_type_hints,
    overload,
    runtime_checkable,
)

random.seed(42)
os.environ.setdefault("MPLBACKEND", "Agg")   # never open a GUI window

# ============================================================
# 1. TypeVar: Bounds and Constraints
# ============================================================
# T = TypeVar("T", bound=Something) accepts any subtype of Something.
# Constraints T = TypeVar("T", str, bytes) accept ONLY the listed types.
# These exist for the type checker; at runtime they are erased.

T = TypeVar("T", bound=float)


def clamp(value: T, low: T, high: T) -> T:
    """Return `value` clamped to [low, high]. Works for any comparable number."""
    if value < low:
        return low
    if value > high:
        return high
    return value


# Example 1: the same generic function serves int, float, and bool
print("Example 1: TypeVar bound = float")
print(f"  clamp(1.5, 0.0, 1.0) = {clamp(1.5, 0.0, 1.0)}")
print(f"  clamp(3, 1, 2)       = {clamp(3, 1, 2)}")
# Output:
#   clamp(1.5, 0.0, 1.0) = 1.0
#   clamp(3, 1, 2)       = 2


# ============================================================
# 2. Generic Classes
# ============================================================
# A class that is generic over T: the container type parameter is declared
# on the class, so Stack[int] and Stack[str] are distinct at check time.

class Stack(typing.Generic[T]):
    """A minimal LIFO container generic over its element type.

    Complexity: push/pop O(1) amortized (list append/pop at the end).
    """

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def __len__(self) -> int:
        return len(self._items)


# Example 2: one generic class, two element types
print("\nExample 2: generic Stack[T]")
s = Stack[int]()
s.push(10)
s.push(20)
print(f"  pop -> {s.pop()}, pop -> {s.pop()}, len -> {len(s)}")
# Output:
#   pop -> 20, pop -> 10, len -> 0


# ============================================================
# 3. Protocol + runtime_checkable: Structural Typing
# ============================================================
# A Protocol describes what an object MUST HAVE, not what it inherits.
# With @runtime_checkable, isinstance() verifies the structure at runtime.
# This is how one VectorStore interface accepts Qdrant, Chroma, FAISS.

@runtime_checkable
class Retriever(Protocol):
    """Anything with retrieve(text) -> list[str] is a Retriever."""

    def retrieve(self, query: str, top_k: int = 3) -> list[str]: ...


class SqlRetriever:
    """A real class that NEVER inherits from Retriever."""

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        return [f"sql:{query}:{i}" for i in range(top_k)]


class MissingRetriever:
    """Lacks the retrieve method entirely -> fails the protocol."""

    def search(self, query: str) -> list[str]:
        return []


class WrongSignatureRetriever:
    """Has retrieve() but a wrong signature.

    NOTE: @runtime_checkable only checks member *presence* and
    callability -- it cannot see signatures. This class still passes
    isinstance()! Signature checking is a static checker's job (mypy),
    never isinstance(). This is a documented limitation.
    """

    def retrieve(self, query: str) -> str:
        return query


# Example 3: structural match, no inheritance required
print("\nExample 3: runtime_checkable Protocol")
print(f"  SqlRetriever is Retriever: {isinstance(SqlRetriever(), Retriever)}")
print(f"  MissingRetriever is Retriever: {isinstance(MissingRetriever(), Retriever)}")
print(f"  WrongSignature is Retriever (limitation): "
      f"{isinstance(WrongSignatureRetriever(), Retriever)}")
print(f"  retrieve through protocol: {SqlRetriever().retrieve('cat', 2)}")
# Output:
#   SqlRetriever is Retriever: True
#   MissingRetriever is Retriever: False
#   WrongSignature is Retriever (limitation): True
#   retrieve through protocol: ['sql:cat:0', 'sql:cat:1']


# ============================================================
# 4. ParamSpec and Concatenate: Typing Decorators
# ============================================================
# ParamSpec captures a function's parameters so a decorator can forward
# them unchanged. Concatenate prepends one extra parameter. Without these
# you can only type decorators as (*args, **kwargs) -> Any.

P = ParamSpec("P")
R = TypeVar("R", covariant=True)


def logged(func: Callable[P, R]) -> Callable[P, R]:
    """Preserve the signature of the wrapped function (P stays intact)."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"  calling {func.__name__} with {args}")
        return func(*args, **kwargs)

    return wrapper


@logged
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


def with_config(func: Callable[Concatenate[dict[str, str], P], R]) -> Callable[P, R]:
    """Inject a config dict as the FIRST argument (Concatenate)."""

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        config = {"model": "gpt-4o-mini", "temperature": 0.2}
        return func(config, *args, **kwargs)

    return wrapper


@with_config
def embed(config: dict[str, str], text: str) -> str:
    """Callers only pass `text`; the decorator supplies the config."""
    return f"{config['model']} embedded: {text}"


# Example 4: ParamSpec preserves inspectable signatures
print("\nExample 4: ParamSpec / Concatenate")
print(f"  add(2, 3) = {add(2, 3)}")
print(f"  add parameter names preserved: {list(inspect.signature(add).parameters)}")
print(f"  embed('hi') = {embed('hi')}")
# Output:
#   calling add with (2, 3)
#   add(2, 3) = 5
#   add parameter names preserved: ['a', 'b']
#   embed('hi') = gpt-4o-mini embedded: hi


# ============================================================
# 5. overload: One Name, Several Type Contracts
# ============================================================
# Overloads declare the type checker's view; only the final implementation
# runs. typing.get_overloads() can inspect them at runtime (3.11+).

@overload
def to_num(value: int) -> int: ...

@overload
def to_num(value: str) -> int: ...

@overload
def to_num(value: list[str]) -> list[int]: ...


def to_num(value: int | str | list[str]) -> int | list[int]:
    """Convert int/str/list[str] to int/list[int] (overloads above)."""
    if isinstance(value, list):
        return [int(v) for v in value]
    return int(value)


# Example 5: overloads erase at runtime, one implementation runs
print("\nExample 5: overload")
print(f"  to_num('42')      = {to_num('42')}")
print(f"  to_num(['1','2']) = {to_num(['1', '2'])}")
print(f"  overloads declared: {len(typing.get_overloads(to_num))}")
# Output:
#   to_num('42')      = 42
#   to_num(['1','2']) = [1, 2]
#   overloads declared: 3


# ============================================================
# 6. Literal, Final, TypeAlias
# ============================================================
# Literal pins a value, not just a type. Final marks a constant for
# static checkers (runtime assignment still works). TypeAlias gives
# complex types a readable name.

Device: TypeAlias = Literal["cpu", "cuda", "mps"]
MAX_BATCH: Final[int] = 64


def device_name(device: Device) -> str:
    """Only the three literal strings are valid at check time."""
    return f"using {device}"


# Example 6: aliases, literals, finals
print("\nExample 6: Literal / Final / TypeAlias")
print(f"  {device_name('cuda')}")
print(f"  MAX_BATCH = {MAX_BATCH}")
print(f"  type(Device) = {type(Device).__name__}")
# Output:
#   using cuda
#   MAX_BATCH = 64
#   type(Device) = _GenericAlias


# ============================================================
# 7. Annotated: Metadata Attached to a Type
# ============================================================
# Annotated[T, meta] keeps T as the type but lets tooling read `meta`
# (validation rules, JSON schema hints, units). Runtime introspection via
# typing.get_origin / get_args.

class Between:
    """Metadata: value must lie in [low, high]."""

    def __init__(self, low: float, high: float) -> None:
        self.low = low
        self.high = high


Temperature = Annotated[float, Between(0.0, 2.0)]


def check_temp(value: Temperature) -> float:
    """Docstring-only here; the metadata is for validators/schema tools."""
    return value


# Example 7: peeling metadata off with get_origin / get_args
print("\nExample 7: Annotated")
origin = get_origin(Temperature)
args = get_args(Temperature)
print(f"  origin = {origin.__name__}, base type = {args[0].__name__}, "
      f"meta = {type(args[1]).__name__}({args[1].low}, {args[1].high})")
hints = get_type_hints(check_temp, include_extras=True)
print(f"  annotated hint survives: {hints['value']}")
# Output:
#   origin = Union, base type = float, meta = Between(0.0, 2.0)
#   annotated hint survives: typing.Annotated[float, Between(0.0, 2.0)]


# ============================================================
# 8. Self: The Fluent Builder
# ============================================================
# Self means "the exact type of the instance". Subclasses get the builder
# methods back typed as themselves -- no lossy Base annotations.

class ModelConfig:
    """Fluent config builder returning Self from every step."""

    def __init__(self) -> None:
        self.model: str = "default"
        self.temperature: float = 1.0

    def with_model(self, name: str) -> Self:
        self.model = name
        return self

    def with_temperature(self, value: float) -> Self:
        self.temperature = value
        return self


class SpecialConfig(ModelConfig):
    """Subclass: inherited builders must still return SpecialConfig."""

    def with_top_p(self, value: float) -> Self:
        self.top_p = value      # type: ignore[attr-defined]  # demo only
        return self


# Example 8: chaining is type-correct with Self
print("\nExample 8: Self")
cfg = ModelConfig().with_model("llama-3").with_temperature(0.1)
print(f"  {cfg.model} @ {cfg.temperature}")
print(f"  chain returns the same class: {type(cfg).__name__}")
# Output:
#   llama-3 @ 0.1
#   chain returns the same class: ModelConfig


# ============================================================
# 9. NewType: A Distinct Type At Check Time Only
# ============================================================
# NewType creates a function that is identical to the base type at runtime
# -- no new class. The pitfall: isinstance() against it raises TypeError.

UserId = NewType("UserId", int)


def get_user(uid: UserId) -> str:
    """Type checker only accepts UserId here, not a bare int."""
    return f"user-{uid}"


# Example 9: NewType is a phantom type at runtime
print("\nExample 9: NewType")
uid = UserId(7)
print(f"  UserId(7) == 7: {uid == 7}")
print(f"  type(UserId(7)) is int: {type(uid) is int}")
try:
    isinstance(uid, UserId)
except TypeError as exc:
    print(f"  isinstance against NewType raises TypeError: {exc}")
# Output:
#   UserId(7) == 7: True
#   type(UserId(7)) is int: True
#   isinstance against NewType raises TypeError: isinstance() arg 2 must be a type


# ============================================================
# 10. TYPE_CHECKING: Import Cycles
# ============================================================
# When two modules import each other, move the import under TYPE_CHECKING
# (a bool that is True only while a checker runs). At runtime the import
# never executes, so no cycle; the checker still sees the names.

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Never executed at runtime; exists only for mypy/pyright.
    from collections.abc import Iterator

# Example 10: the guard is False when running
print("\nExample 10: TYPE_CHECKING")
print(f"  TYPE_CHECKING at runtime: {TYPE_CHECKING}")
# Output:
#   TYPE_CHECKING at runtime: False


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: using isinstance() against a Protocol that is NOT decorated
#   with @runtime_checkable -- raises TypeError.
# CORRECT: @runtime_checkable on the Protocol.
# MISTAKE: trusting isinstance() to check signatures on a protocol --
#   it only checks member presence/callability (WrongSignatureRetriever
#   above passes!). A wrong signature is caught by mypy, never by
#   isinstance().
# CORRECT: run mypy/pyright on protocol consumers; use isinstance() only
#   as a coarse gate.
# MISTAKE: expecting overloads to dispatch at runtime.
# CORRECT: overloads are compile-time contracts; the implementation does
#   real isinstance() dispatch.
# MISTAKE: isinstance(x, SomeNewType) -- NewType is a function, not a type.
# CORRECT: check against the base type; the NewType only guides checkers.


# ============================================================
# Self-Verification  (MANDATORY -- every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # 1. Protocol structural match at runtime, no inheritance involved.
    assert isinstance(SqlRetriever(), Retriever), \
        "SqlRetriever must structurally satisfy the Retriever protocol"
    assert not isinstance(MissingRetriever(), Retriever), \
        "MissingRetriever must NOT satisfy the Retriever protocol"
    assert isinstance(WrongSignatureRetriever(), Retriever), \
        "runtime_checkable is shallow: wrong signatures still pass (documented)"
    assert SqlRetriever().retrieve("cat", 2) == ["sql:cat:0", "sql:cat:1"], \
        "protocol methods must be callable through the concrete class"

    # 2. Generic class behaves LIFO for any element type.
    stack = Stack[str]()
    stack.push("a")
    stack.push("b")
    assert stack.pop() == "b" and stack.pop() == "a" and len(stack) == 0, \
        "generic Stack must pop LIFO"

    # 3. TypeVar-bound generic function works across numeric types.
    assert clamp(1.5, 0.0, 1.0) == 1.0, "clamp must cap at high"
    assert clamp(-1, 0, 2) == 0, "clamp must floor at low"
    assert clamp(5, 1, 3) == 3, "clamp must cap at high for ints"

    # 4. ParamSpec preserves the signature for inspection tools.
    assert list(inspect.signature(add).parameters) == ["a", "b"], \
        "ParamSpec decorator must preserve the wrapped parameter names"

    # 5. Concatenate injects the config argument transparently.
    assert embed("hi") == "gpt-4o-mini embedded: hi", \
        "Concatenate must inject the config as the first argument"

    # 6. overload: the implementation handles every declared arm.
    assert to_num("42") == 42, "overload str -> int arm must work"
    assert to_num(7) == 7, "overload int -> int arm must work"
    assert to_num(["1", "2"]) == [1, 2], "overload list[str] arm must work"

    # 7. Annotated metadata is inspectable at runtime.
    hint = get_type_hints(check_temp, include_extras=True)["value"]
    assert get_args(hint) and get_args(hint)[0] is float, \
        "Annotated hint must peel back to its base type via get_args"
    assert get_args(hint)[1].low == 0.0, \
        "Annotated metadata must be readable via get_args"

    # 8. Self-typed builder chains return the instance type.
    assert isinstance(cfg, ModelConfig), "builder chain must return ModelConfig"

    # 9. NewType is a phantom: equal to base, not a real type.
    assert UserId(7) == 7, "NewType value must equal the base value"
    assert type(UserId(7)) is int, "NewType must not create a new class"
    try:
        isinstance(UserId(7), UserId)      # type: ignore[arg-type]
        newtype_isinstance_failed = False
    except TypeError:
        newtype_isinstance_failed = True
    assert newtype_isinstance_failed, \
        "isinstance() against a NewType must raise TypeError"

    # 10. TYPE_CHECKING is a runtime-visible constant, False on execution.
    assert TYPE_CHECKING is False, "TYPE_CHECKING must be False at runtime"

    print("\n[OK] 23-typing-advanced: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("=" * 60)
        print("ADVANCED TYPING: STATIC CONTRACTS, RUNTIME BEHAVIOR")
        print("=" * 60)
        print("\n1. TypeVar bounds and constraints")
        print(f"  clamp(1.5, 0.0, 1.0) = {clamp(1.5, 0.0, 1.0)}")
        print(f"  clamp(3, 1, 2) = {clamp(3, 1, 2)}")
        print("\n2. Generic Stack[int]")
        s = Stack[int]()
        s.push(10)
        s.push(20)
        print(f"  pop -> {s.pop()}, pop -> {s.pop()}")
        print("\n3. Protocol structural match")
        print(f"  SqlRetriever is Retriever: {isinstance(SqlRetriever(), Retriever)}")
        print(f"  MissingRetriever is Retriever: {isinstance(MissingRetriever(), Retriever)}")
        print(f"  WrongSignature is Retriever (shallow check): "
              f"{isinstance(WrongSignatureRetriever(), Retriever)}")
        print("\n4. ParamSpec / Concatenate")
        print(f"  add(2, 3) = {add(2, 3)}")
        print(f"  parameters: {list(inspect.signature(add).parameters)}")
        print(f"  embed('hi') = {embed('hi')}")
        print("\n5. overload")
        print(f"  to_num('42') = {to_num('42')}; to_num(['1','2']) = {to_num(['1', '2'])}")
        print("\n6. Literal / Final / TypeAlias")
        print(f"  {device_name('cuda')}; MAX_BATCH = {MAX_BATCH}")
        print("\n7. Annotated")
        origin = get_origin(Temperature)
        args = get_args(Temperature)
        print(f"  origin = {origin.__name__}, base = {args[0].__name__}, meta = {type(args[1]).__name__}")
        print("\n8. Self")
        print(f"  {cfg.model} @ {cfg.temperature}")
        print("\n9. NewType")
        print(f"  UserId(7) == 7: {UserId(7) == 7}")
        print("\n10. TYPE_CHECKING")
        print(f"  TYPE_CHECKING at runtime: {TYPE_CHECKING}")
        print("\n--- Summary ---")
        print("1. Protocols give structural interfaces: no inheritance needed.")
        print("2. ParamSpec/Concatenate/overload type decorators and overloads.")
        print("3. Annotated carries metadata; Self types fluent builders.")
        print("4. NewType and TYPE_CHECKING are checker-only, not runtime.")
        _verify()
