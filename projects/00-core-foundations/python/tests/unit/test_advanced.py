"""
Unit tests for advanced Python features.
"""

import pytest
from advanced.type_hints import (
    greet,
    calculate,
    process_items,
    merge_dicts,
    find_duplicates,
    flexible_input,
    Stack,
    Pair,
    draw_shape,
    Circle,
    Square,
    set_mode,
    MAX_RETRIES,
    scale_vector,
    apply_operation,
    create_multiplier,
    User,
)
from advanced.decorators import timer, log_calls, retry, cache, singleton, add_repr


class TestTypeHints:
    """Test type hint examples."""

    def test_greet(self):
        assert greet("World") == "Hello, World!"

    def test_calculate(self):
        assert calculate(10, 5, "add") == 15
        assert calculate(10, 5, "sub") == 5
        assert calculate(10, 5, "mul") == 50
        assert calculate(10, 5, "div") == 2.0
        assert calculate(10, 5, "unknown") == 0.0

    def test_process_items(self):
        result = process_items(["apple", "banana"], uppercase=True)
        assert result == {"APPLE": 5, "BANANA": 6}
        result = process_items(["apple", "banana"], uppercase=False)
        assert result == {"apple": 5, "banana": 6}

    def test_merge_dicts(self):
        result = merge_dicts({"a": 1}, {"b": 2})
        assert result == {"a": 1, "b": 2}

    def test_find_duplicates(self):
        result = find_duplicates([1, 2, 3, 2, 4, 3, 5])
        assert result == {2, 3}

    def test_flexible_input(self):
        assert flexible_input("hello") == "String: hello"
        assert flexible_input(42) == "Integer: 42"
        assert flexible_input(3.14) == "Float: 3.14"

    def test_stack(self):
        stack = Stack[int]()
        assert stack.is_empty()
        stack.push(1)
        stack.push(2)
        assert len(stack) == 2
        assert stack.peek() == 2
        assert stack.pop() == 2
        assert stack.pop() == 1
        assert stack.is_empty()

    def test_stack_string(self):
        stack = Stack[str]()
        stack.push("hello")
        stack.push("world")
        assert stack.pop() == "world"

    def test_pair(self):
        pair = Pair("key", 42)
        assert pair.key == "key"
        assert pair.value == 42

    def test_protocol(self):
        circle = Circle()
        square = Square()
        assert draw_shape(circle) == "Drawing a circle"
        assert draw_shape(square) == "Drawing a square"

    def test_literal(self):
        assert set_mode("read") == "Mode set to: read"
        assert set_mode("write") == "Mode set to: write"
        assert set_mode("append") == "Mode set to: append"

    def test_final(self):
        assert MAX_RETRIES == 3

    def test_type_alias(self):
        result = scale_vector([1.0, 2.0, 3.0], 2.5)
        assert result == [2.5, 5.0, 7.5]

    def test_callable(self):
        result = apply_operation([1, 2, 3, 4], lambda x: x * 2)
        assert result == [2, 4, 6, 8]
        triple = create_multiplier(3)
        assert triple(5) == 15

    def test_dataclass(self):
        user = User("Alice", "alice@example.com", 30, tags=["admin", "user"])
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        assert user.age == 30
        assert user.is_active is True
        assert user.tags == ["admin", "user"]
        assert user.to_dict()["name"] == "Alice"


class TestDecorators:
    """Test decorator examples."""

    def test_timer_decorator(self):
        @timer
        def fast_func():
            return "done"

        result = fast_func()
        assert result == "done"

    def test_log_calls_decorator(self):
        @log_calls
        def add(a, b):
            return a + b

        result = add(2, 3)
        assert result == 5

    def test_retry_decorator(self):
        counter = {"value": 0}

        @retry(max_attempts=3, delay=0.01)
        def flaky():
            counter["value"] += 1
            if counter["value"] < 3:
                raise ValueError("Not ready")
            return "success"

        result = flaky()
        assert result == "success"
        assert counter["value"] == 3

    def test_cache_decorator(self):
        call_count = {"n": 0}

        @cache(max_size=10)
        def fibonacci(n):
            call_count["n"] += 1
            if n < 2:
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)

        result = fibonacci(10)
        assert result == 55
        # Should be much fewer calls due to caching
        assert call_count["n"] < 20

    def test_singleton_decorator(self):
        @singleton
        class DatabaseConnection:
            def __init__(self):
                self.id = id(self)

        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
        assert db1 is db2
        assert db1.id == db2.id

    def test_add_repr_decorator(self):
        @add_repr
        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        p = Point(3, 4)
        assert repr(p) == "Point(x=3, y=4)"
