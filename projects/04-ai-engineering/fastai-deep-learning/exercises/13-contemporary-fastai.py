"""
13 - Contemporary fast.ai: The 2026 Ecosystem
===============================================
Goal: Explore the tools and philosophy of the fast.ai ecosystem in 2026.
You will implement simplified versions of Solveit's context management,
a reversible data pipeline (fasttransform-style), a FastHTML-inspired
routing system, and a productivity-paradox simulation.

You will:
  1. Build a Solveit-inspired context manager with pin/hide/summarize.
  2. Implement a reversible transformation pipeline (fasttransform-style).
  3. Build a minimal FastHTML-style routing decorator.
  4. Simulate the agentic productivity paradox (METR-style).

Prerequisites:
  Python 3.10+ (stdlib only — no external dependencies)

Run:
  python 13-contemporary-fastai.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable


# ============================================================
# 1. Solveit-Inspired Context Manager
# ============================================================
class MessageState(Enum):
    ACTIVE = auto()     # visible to AI
    HIDDEN = auto()     # invisible to AI
    PINNED = auto()     # always visible, cannot be evicted


@dataclass
class ContextMessage:
    role: str
    content: str
    state: MessageState = MessageState.ACTIVE


class ManagedContext:
    """A Solveit-inspired context manager with granular control.

    Supports pinning (always visible), hiding (remove from AI view),
    and truncation (manage token budget).
    """

    def __init__(self, max_tokens: int = 4096):
        self._messages: list[ContextMessage] = []
        self.max_tokens = max_tokens

    def add(self, role: str, content: str, state: MessageState = MessageState.ACTIVE) -> None:
        self._messages.append(ContextMessage(role=role, content=content, state=state))

    def hide(self, index: int) -> None:
        """Hide a message from the AI (e.g., a previous wrong answer)."""
        if 0 <= index < len(self._messages):
            self._messages[index].state = MessageState.HIDDEN

    def pin(self, index: int) -> None:
        """Pin a message so it is always included (e.g., system prompt)."""
        if 0 <= index < len(self._messages):
            self._messages[index].state = MessageState.PINNED

    def get_active_context(self) -> list[dict]:
        """Return only messages visible to the AI, with pinned ones first."""
        pinned = [m for m in self._messages if m.state == MessageState.PINNED]
        active = [m for m in self._messages if m.state == MessageState.ACTIVE]

        context = pinned + active
        # Truncate to max_tokens approximately
        total = 0
        for i, m in enumerate(context):
            total += len(m.content.split())
            if total > self.max_tokens:
                context = context[:i]
                break
        return [{"role": m.role, "content": m.content} for m in context]

    def summarize(self) -> str:
        """Return a human-readable summary of the context state."""
        total = len(self._messages)
        active = sum(1 for m in self._messages if m.state == MessageState.ACTIVE)
        hidden = sum(1 for m in self._messages if m.state == MessageState.HIDDEN)
        pinned = sum(1 for m in self._messages if m.state == MessageState.PINNED)
        return f"Context: {total} msgs ({active} active, {hidden} hidden, {pinned} pinned)"


# ============================================================
# 2. Reversible Transformation Pipeline (fasttransform-style)
# ============================================================
class Transform:
    """A single reversible transformation."""

    def encode(self, x: Any) -> Any:
        raise NotImplementedError

    def decode(self, x: Any) -> Any:
        raise NotImplementedError


@dataclass
class Normalize(Transform):
    """Normalize values to [0, 1] using min-max scaling."""

    min_val: float = 0.0
    max_val: float = 255.0

    def encode(self, x: float | list) -> float | list:
        if isinstance(x, (list, tuple)):
            return [(v - self.min_val) / (self.max_val - self.min_val) for v in x]
        return (x - self.min_val) / (self.max_val - self.min_val)

    def decode(self, x: float | list) -> float | list:
        if isinstance(x, (list, tuple)):
            return [v * (self.max_val - self.min_val) + self.min_val for v in x]
        return x * (self.max_val - self.min_val) + self.min_val


@dataclass
class Clip(Transform):
    """Clip values to a range. NOTE: clipping is lossy — decode() cannot
    restore clipped values. This demonstrates a limitation of "reversible"
    pipelines: some transformations inherently destroy information.
    """

    min_val: float = 0.0
    max_val: float = 1.0

    def encode(self, x: float) -> float:
        return max(self.min_val, min(self.max_val, x))

    def decode(self, x: float) -> float:
        # Clipping is lossy: values outside [min, max] cannot be restored.
        # This is a design trade-off — not all transforms can be perfectly inverted.
        return x


@dataclass
class Pipeline:
    """A sequence of reversible transformations."""

    transforms: list[Transform] = field(default_factory=list)

    def encode(self, x: Any) -> Any:
        for t in self.transforms:
            x = t.encode(x)
        return x

    def decode(self, x: Any) -> Any:
        for t in reversed(self.transforms):
            x = t.decode(x)
        return x

    def decode_at(self, step: int, x: Any) -> Any:
        """Reverse only from the end back to a specific step."""
        for t in reversed(self.transforms[step:]):
            x = t.decode(x)
        return x


# ============================================================
# 3. FastHTML-Inspired Routing
# ============================================================
class RouteApp:
    """A minimal FastHTML-style routing system.

    Routes are defined with decorators. HTMX attributes are supported
    via keyword arguments. Responses are HTML strings.
    """

    def __init__(self):
        self._routes: dict[tuple[str, str], Callable] = {}

    def route(self, path: str, methods: list[str] | None = None):
        """Decorator to register a route."""
        if methods is None:
            methods = ["GET"]

        def decorator(func: Callable) -> Callable:
            for method in methods:
                self._routes[(method.upper(), path)] = func
            return func
        return decorator

    def dispatch(self, method: str, path: str, **kwargs) -> str:
        """Dispatch a request to the matching route handler."""
        handler = self._routes.get((method.upper(), path))
        if handler is None:
            return f"<h1>404 Not Found</h1><p>{method} {path}</p>"
        return handler(**kwargs)

    def htmx_button(self, label: str, hx_get: str, hx_swap: str = "outerHTML") -> str:
        """Generate an HTML button with htmx attributes (note: htmx, not HTMX)."""
        return f'<button hx-get="{hx_get}" hx-swap="{hx_swap}">{label}</button>'


# ============================================================
# 4. Productivity Paradox Simulation (METR-style)
# ============================================================
@dataclass
class ProductivityMetrics:
    mode: str
    perceived_productivity: float = 0.0
    actual_output_quality: float = 0.0
    code_maintainability: float = 0.0
    understanding_retention: float = 0.0

    def gap(self) -> float:
        return self.perceived_productivity - self.actual_output_quality


def simulate_productivity_paradox() -> list[ProductivityMetrics]:
    """Simulate the METR finding across three development modes."""
    return [
        ProductivityMetrics(
            mode="solo (no AI)",
            perceived_productivity=4.0,
            actual_output_quality=6.0,
            code_maintainability=8.0,
            understanding_retention=9.0,
        ),
        ProductivityMetrics(
            mode="AI-assisted (Solveit-style)",
            perceived_productivity=7.0,
            actual_output_quality=8.0,
            code_maintainability=7.0,
            understanding_retention=7.0,
        ),
        ProductivityMetrics(
            mode="agentic (full automation)",
            perceived_productivity=9.0,
            actual_output_quality=5.0,
            code_maintainability=3.0,
            understanding_retention=2.0,
        ),
    ]


def print_productivity_table(metrics: list[ProductivityMetrics]) -> None:
    """Print a formatted productivity comparison table."""
    header = f"{'Mode':<35s} {'Perceived':>10s} {'Actual':>8s} {'Gap':>6s} {'Maint.':>7s} {'Underst.':>10s}"
    print(header)
    print("-" * len(header))
    for s in metrics:
        gap_str = f"{s.gap():+.1f}"
        print(f"{s.mode:<35s} {s.perceived_productivity:>6.1f}/10"
              f" {s.actual_output_quality:>6.1f}/10 {gap_str:>6s}"
              f" {s.code_maintainability:>5.1f}/10"
              f" {s.understanding_retention:>8.1f}/10")


# ============================================================
# 5. Main Demonstration
# ============================================================
def main() -> None:
    print("=" * 60)
    print("1. Solveit-Inspired Context Manager")
    print("=" * 60)

    ctx = ManagedContext(max_tokens=100)
    ctx.add("system", "You are a helpful coding assistant.", state=MessageState.PINNED)
    ctx.add("human", "How do I parse JSON in Python?")
    ctx.add("ai", "Use json.loads() with a try/except block.")
    print(ctx.summarize())

    # Hide a wrong answer
    ctx.add("human", "Actually, that doesn't handle nested JSON.")
    ctx.add("ai", "Let me correct that...")
    ctx.hide(3)  # hide the wrong first answer (index 3)
    print(f"After hiding: {ctx.summarize()}")
    print(f"Active context has {len(ctx.get_active_context())} messages")
    print()

    print("=" * 60)
    print("2. Reversible Pipeline (fasttransform-style)")
    print("=" * 60)

    pipe = Pipeline([
        Normalize(min_val=0, max_val=255),
    ])

    test_values = [0, 128, 255, 64.0]
    for v in test_values:
        enc = pipe.encode(v)
        dec = pipe.decode(enc)
        ok = "OK" if abs(dec - v) < 0.001 else "MISMATCH"
        print(f"  {v:>6.1f} -> {enc:>8.4f} -> {dec:>6.1f} [{ok}]")

    # Demonstrating a lossy transform: clipping cannot be perfectly reversed
    clip_pipe = Pipeline([Clip(0.0, 1.0)])
    for v in [0.5, 1.5, -0.5]:
        enc = clip_pipe.encode(v)
        dec = clip_pipe.decode(enc)
        lossy = "lossy" if abs(dec - v) > 0.001 else "OK"
        print(f"  Clip: {v:>5.1f} -> {enc:>4.1f} -> {dec:>4.1f} [{lossy}]")
    print()

    print("=" * 60)
    print("3. FastHTML-Style Routing")
    print("=" * 60)

    app = RouteApp()

    @app.route("/")
    def home():
        return "<h1>Welcome</h1><p>FastHTML-style routing works!</p>" + \
               app.htmx_button("Click me", "/click")

    @app.route("/click")
    def click():
        return '<p style="color: green">Button clicked! No JS needed.</p>'

    print("GET /  -> " + app.dispatch("GET", "/")[:60] + "...")
    print("GET /click -> " + app.dispatch("GET", "/click")[:60] + "...")
    print("GET /nonexistent -> " + app.dispatch("GET", "/nonexistent"))
    print()

    print("=" * 60)
    print("4. Productivity Paradox (METR-Style)")
    print("=" * 60)

    metrics = simulate_productivity_paradox()
    print_productivity_table(metrics)
    print()

    # Highlight the key finding
    agentic = [m for m in metrics if m.mode == "agentic (full automation)"][0]
    print(f"Key insight: '{agentic.mode}' has perception={agentic.perceived_productivity:.0f}/10")
    print(f"  but actual quality={agentic.actual_output_quality:.0f}/10, "
          f"maintainability={agentic.code_maintainability:.0f}/10")
    print(f"  Gap: {agentic.gap():+.1f} — the productivity paradox.")
    print()

    # EXERCISE 1: Add a `collapse(heading)` method to ManagedContext that
    # hides all messages under a given markdown heading.
    # This simulates Solveit's collapsible sections feature.

    # EXERCISE 2: Extend the Pipeline with an AddGaussianNoise transform:
    #   encode: x += noise (store noise for decoding)
    #   decode: x -= noise (reconstruct original)
    # Measure the reconstruction error for different noise levels.

    # EXERCISE 3: Add POST and PUT method support to RouteApp.
    # Create a route that accepts form data via POST and returns a response.

    # EXERCISE 4: Add a `with_understanding_decay(weeks)` method to
    # ProductivityMetrics that reduces understanding_retention over time
    # at different rates for each mode. Simulate a 12-week project.

    # EXERCISE 5: Write an /llms-ctx.txt-style string for the RouteApp class.
    # Document its API, key conventions, and example patterns so an AI
    # assistant could generate code using it.


if __name__ == "__main__":
    main()
