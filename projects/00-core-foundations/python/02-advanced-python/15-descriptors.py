"""
Descriptors - Advanced Python Exercises
========================================
Descriptors allow you to customize attribute access on classes.
They are the mechanism behind properties, methods, and classmethods.
"""

from typing import Any, Optional


# =============================================================================
# 1. Basic Descriptor
# =============================================================================

class Property:
    """Simple property descriptor."""

    def __init__(self, fget=None, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)


# =============================================================================
# 2. Validation Descriptor
# =============================================================================

class Validated:
    """Descriptor that validates values."""

    def __init__(self, validator, error_msg="Invalid value"):
        self.validator = validator
        self.error_msg = error_msg
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"{self.name}: {self.error_msg}")
        obj.__dict__[self.name] = value


class PositiveNumber(Validated):
    """Descriptor for positive numbers."""

    def __init__(self):
        super().__init__(
            lambda x: isinstance(x, (int, float)) and x > 0,
            "must be a positive number"
        )


class NonEmptyString(Validated):
    """Descriptor for non-empty strings."""

    def __init__(self):
        super().__init__(
            lambda x: isinstance(x, str) and len(x) > 0,
            "must be a non-empty string"
        )


# =============================================================================
# 3. Computed Attribute Descriptor
# =============================================================================

class ComputedAttribute:
    """Descriptor that computes value from other attributes."""

    def __init__(self, func):
        self.func = func
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.func(obj)


# =============================================================================
# 4. Type-Checked Descriptor
# =============================================================================

class Typed:
    """Descriptor that enforces type checking."""

    def __init__(self, expected_type):
        self.expected_type = expected_type
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        obj.__dict__[self.name] = value


# =============================================================================
# 5. Caching Descriptor
# =============================================================================

class CachedResult:
    """Descriptor that caches computed results."""

    def __init__(self, func):
        self.func = func
        self.name = None
        self.cache_attr = None

    def __set_name__(self, owner, name):
        self.name = name
        self.cache_attr = f"_cached_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if not hasattr(obj, self.cache_attr):
            setattr(obj, self.cache_attr, self.func(obj))
        return getattr(obj, self.cache_attr)

    def __delete__(self, obj):
        if hasattr(obj, self.cache_attr):
            delattr(obj, self.cache_attr)


# =============================================================================
# 6. Practical Example Classes
# =============================================================================

class Product:
    """Product with validated attributes."""

    name = NonEmptyString()
    price = PositiveNumber()
    quantity = PositiveNumber()

    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity

    @CachedResult
    def total_value(self) -> float:
        """Expensive computation - cached."""
        print(f"  Computing total value for {self.name}...")
        return self.price * self.quantity

    def __repr__(self) -> str:
        return f"Product({self.name!r}, ${self.price}, qty={self.quantity})"


class Employee:
    """Employee with typed and computed attributes."""

    name = Typed(str)
    age = Typed(int)
    salary = Typed(float)

    def __init__(self, name: str, age: int, salary: float):
        self.name = name
        self.age = age
        self.salary = salary

    @ComputedAttribute
    def tax_rate(self) -> float:
        if self.salary > 100000:
            return 0.35
        elif self.salary > 50000:
            return 0.25
        return 0.15

    @ComputedAttribute
    def annual_tax(self) -> float:
        return self.salary * self.tax_rate


# =============================================================================
# 7. Data Descriptor vs Non-Data Descriptor
# =============================================================================

class DataDescriptor:
    """Data descriptor (has __set__ or __delete__)."""

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(f"_{self.name}", "from data descriptor")

    def __set__(self, obj, value):
        obj.__dict__[f"_{self.name}"] = value


class NonDataDescriptor:
    """Non-data descriptor (only __get__)."""

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return f"from non-data descriptor: {self.name}"


class DescriptorDemo:
    data = DataDescriptor()
    non_data = NonDataDescriptor()


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DESCRIPTORS DEMO")
    print("=" * 60)

    # 1. Validation descriptor
    print("\n--- Validation Descriptors ---")
    product = Product("Laptop", 999.99, 10)
    print(f"  {product}")
    print(f"  Total value: ${product.total_value:,.2f}")
    print(f"  Total value (cached): ${product.total_value:,.2f}")

    try:
        bad_product = Product("", -100, 5)
    except ValueError as e:
        print(f"  Validation error: {e}")

    # 2. Type-checked descriptor
    print("\n--- Type-Checked Descriptors ---")
    emp = Employee("Alice", 30, 75000.0)  # float, as Typed(float) requires
    print(f"  Employee: {emp.name}, age {emp.age}")
    print(f"  Tax rate: {emp.tax_rate:.0%}")
    print(f"  Annual tax: ${emp.annual_tax:,.2f}")

    try:
        emp.age = "thirty"
    except TypeError as e:
        print(f"  Type error: {e}")

    # 3. Computed attribute
    print("\n--- Computed Attributes ---")
    print(f"  {emp.name}'s tax rate: {emp.tax_rate}")
    print(f"  {emp.name}'s annual tax: ${emp.annual_tax:,.2f}")

    # 4. Data vs Non-Data descriptor
    print("\n--- Data vs Non-Data Descriptor ---")
    demo = DescriptorDemo()
    print(f"  Data: {demo.data}")
    print(f"  Non-data: {demo.non_data}")

    # Instance attribute overrides non-data descriptor
    demo.non_data = "instance value"
    print(f"  After instance set: {demo.non_data}")

    # 5. Caching behavior
    print("\n--- Caching Behavior ---")
    product2 = Product("Phone", 699.99, 5)
    print(f"  First access (computes):")
    val1 = product2.total_value
    print(f"  Result: ${val1:,.2f}")
    print(f"  Second access (cached):")
    val2 = product2.total_value
    print(f"  Result: ${val2:,.2f}")

    print("\n" + "=" * 60)
    print("All descriptor demos complete!")
    print("=" * 60)
