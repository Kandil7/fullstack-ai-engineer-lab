"""
Calculator — Mini Project
==========================
Combines: functions, control flow, user input, error handling, string formatting

A CLI calculator with memory operations and history.

Run: python projects/01-calculator/main.py
"""

import math
import sys


class Calculator:
    """A CLI calculator with memory, history, and multiple operations."""

    def __init__(self):
        self.history = []
        self.memory = 0.0
        self.angle_mode = "DEG"  # DEG, RAD, GRAD

    # ── Basic Operations ──────────────────────────────────────────────────

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero!")
        return a / b

    def power(self, base: float, exp: float) -> float:
        return base ** exp

    def root(self, a: float, n: float = 2) -> float:
        if a < 0 and n % 2 == 0:
            raise ValueError("Cannot compute even root of negative number!")
        return a ** (1 / n)

    def modulo(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot modulo by zero!")
        return a % b

    # ── Scientific Operations ─────────────────────────────────────────────

    def _to_radians(self, angle: float) -> float:
        if self.angle_mode == "DEG":
            return math.radians(angle)
        elif self.angle_mode == "GRAD":
            return angle * math.pi / 200
        return angle  # Already in radians

    def sin(self, x: float) -> float:
        return math.sin(self._to_radians(x))

    def cos(self, x: float) -> float:
        return math.cos(self._to_radians(x))

    def tan(self, x: float) -> float:
        rad = self._to_radians(x)
        if abs(math.cos(rad)) < 1e-15:
            raise ValueError("Undefined: tan at this angle")
        return math.tan(rad)

    def log(self, x: float, base: float = math.e) -> float:
        if x <= 0:
            raise ValueError("Logarithm of non-positive number!")
        return math.log(x, base)

    def ln(self, x: float) -> float:
        return self.log(x, math.e)

    def factorial(self, n: int) -> int:
        if n < 0:
            raise ValueError("Factorial of negative number!")
        if n > 170:
            raise ValueError("Result too large!")
        return math.factorial(n)

    # ── Memory Operations ─────────────────────────────────────────────────

    def memory_store(self, value: float):
        self.memory = value

    def memory_recall(self) -> float:
        return self.memory

    def memory_add(self, value: float):
        self.memory += value

    def memory_clear(self):
        self.memory = 0.0

    # ── History ───────────────────────────────────────────────────────────

    def add_to_history(self, expression: str, result: float):
        self.history.append((expression, result))

    def show_history(self) -> str:
        if not self.history:
            return "No history."
        lines = []
        for i, (expr, result) in enumerate(self.history[-10:], 1):
            lines.append(f"  {i:2d}. {expr} = {result}")
        return "\n".join(lines)

    def clear_history(self):
        self.history.clear()


def main():
    calc = Calculator()
    print("=" * 50)
    print("  🧮 Python Calculator")
    print("=" * 50)
    print("  Type 'help' for commands, 'quit' to exit.")
    print()

    while True:
        try:
            expr = input(">> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not expr:
            continue

        if expr.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if expr.lower() == "help":
            print("""
  Commands:
    a + b          Add
    a - b          Subtract
    a * b          Multiply
    a / b          Divide
    a ^ b          Power
    sqrt(a)        Square root
    root(a, n)     Nth root
    sin(x)         Sine (use: angle_mode first)
    cos(x)         Cosine
    tan(x)         Tangent
    log(x)         Natural log
    log10(x)       Base-10 log
    n!             Factorial
    a % b          Modulo
    pi             π constant
    e              Euler's number

    memory         Show stored value
    mstore [val]   Store value in memory
    mrecall        Recall from memory
    madd [val]     Add to memory
    mclear         Clear memory

    history        Show recent results
    clearh         Clear history
    deg            Set angle mode to degrees
    rad            Set angle mode to radians
    help           Show this help
    quit           Exit
            """)
            continue

        if expr.lower() == "history":
            print(calc.show_history())
            continue

        if expr.lower() == "clearh":
            calc.clear_history()
            print("History cleared.")
            continue

        if expr.lower() == "memory":
            print(f"Memory: {calc.memory}")
            continue

        if expr.lower() == "mclear":
            calc.memory_clear()
            print("Memory cleared.")
            continue

        if expr.lower() == "mrecall":
            print(f"Memory: {calc.memory_recall()}")
            continue

        if expr.lower().startswith("mstore"):
            val = float(expr.split(maxsplit=1)[1])
            calc.memory_store(val)
            print(f"Stored {val} in memory.")
            continue

        if expr.lower().startswith("madd"):
            val = float(expr.split(maxsplit=1)[1])
            calc.memory_add(val)
            print(f"Memory: {calc.memory}")
            continue

        if expr.lower() in ("deg", "rad"):
            calc.angle_mode = expr.upper()
            print(f"Angle mode set to {calc.angle_mode}")
            continue

        # Parse and evaluate expression
        try:
            result = evaluate_expression(expr, calc)
            if result is not None:
                # Format result
                if isinstance(result, float):
                    if result == int(result) and abs(result) < 1e15:
                        display = str(int(result))
                    else:
                        display = f"{result:.10f}".rstrip("0").rstrip(".")
                else:
                    display = str(result)
                
                print(f"  = {display}")
                calc.add_to_history(expr.replace(" ", ""), result)
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            print(f"  ⚠️  Error: {e}")


def evaluate_expression(expr: str, calc: Calculator) -> float | None:
    """Parse and evaluate a simple calculator expression."""
    expr = expr.strip()

    # Constants
    if expr.lower() == "pi":
        return math.pi
    if expr.lower() == "e":
        return math.e

    # Functions: sin(x), cos(x), tan(x), log(x), log10(x), sqrt(x), n!
    import re

    # Factorial (trailing !)
    fact_match = re.match(r"^(-?\d+)!$", expr)
    if fact_match:
        return calc.factorial(int(fact_match.group(1)))

    # Single-argument functions
    func_map = {
        "sin": calc.sin,
        "cos": calc.cos,
        "tan": calc.tan,
        "log": lambda x: calc.ln(x),
        "ln": calc.ln,
        "log10": lambda x: calc.log(x, 10),
        "sqrt": lambda x: calc.root(x, 2),
        "abs": abs,
        "floor": math.floor,
        "ceil": math.ceil,
    }

    for name, func in func_map.items():
        pattern = rf"^{name}\((.+)\)$"
        match = re.match(pattern, expr, re.IGNORECASE)
        if match:
            arg = float(match.group(1))
            return func(arg)

    # Binary operations (simple parse: left op right)
    ops = [
        ("+", calc.add),
        ("-", calc.subtract),
        ("*", calc.multiply),
        ("/", calc.divide),
        ("^", calc.power),
        ("%", calc.modulo),
    ]

    for symbol, func in ops:
        parts = expr.rsplit(symbol, 1)
        if len(parts) == 2:
            left = float(parts[0].strip())
            right = float(parts[1].strip())
            return func(left, right)

    # Try as single number
    try:
        return float(expr)
    except ValueError:
        raise ValueError(f"Cannot parse: '{expr}'")


if __name__ == "__main__":
    main()
