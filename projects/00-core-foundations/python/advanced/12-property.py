"""
Property - Advanced Python Exercises
======================================
Properties provide a Pythonic way to manage attribute access
with getters, setters, and computed values.
"""

from typing import Optional
import math


# =============================================================================
# 1. Basic Property
# =============================================================================

class Circle:
    """Circle with property-controlled radius."""

    def __init__(self, radius: float):
        self._radius = radius  # Use setter for validation

    @property
    def radius(self) -> float:
        """Get the radius."""
        return self._radius

    @radius.setter
    def radius(self, value: float):
        """Set the radius with validation."""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def diameter(self) -> float:
        """Computed property - diameter."""
        return self._radius * 2

    @property
    def area(self) -> float:
        """Computed property - area."""
        return math.pi * self._radius ** 2

    @property
    def circumference(self) -> float:
        """Computed property - circumference."""
        return 2 * math.pi * self._radius

    def __repr__(self) -> str:
        return f"Circle(radius={self._radius})"


# =============================================================================
# 2. Property with Caching
# =============================================================================

class ExpensiveCalculation:
    """Demonstrate caching with property."""

    def __init__(self, data: list):
        self._data = data
        self._sorted_cache: Optional[list] = None
        self._stats_cache: Optional[dict] = None

    @property
    def sorted_data(self) -> list:
        """Sort data only once."""
        if self._sorted_cache is None:
            print("  Sorting data (first access)...")
            self._sorted_cache = sorted(self._data)
        return self._sorted_cache

    @property
    def statistics(self) -> dict:
        """Compute statistics only once."""
        if self._stats_cache is None:
            print("  Computing statistics (first access)...")
            self._stats_cache = {
                "count": len(self._data),
                "min": min(self._data),
                "max": max(self._data),
                "mean": sum(self._data) / len(self._data),
            }
        return self._stats_cache

    def invalidate_cache(self) -> None:
        """Clear all cached values."""
        self._sorted_cache = None
        self._stats_cache = None


# =============================================================================
# 3. Property with Validation
# =============================================================================

class Temperature:
    """Temperature with unit conversion and validation."""

    def __init__(self, celsius: float):
        self._celsius = None
        self.celsius = celsius  # Use setter

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float):
        self.celsius = (value - 32) * 5/9

    @property
    def kelvin(self) -> float:
        return self._celsius + 273.15

    @kelvin.setter
    def kelvin(self, value: float):
        self.celsius = value - 273.15

    def __repr__(self) -> str:
        return f"Temperature({self._celsius:.1f}°C)"


# =============================================================================
# 4. Property with Read-Only
# =============================================================================

class BankAccount:
    """Bank account with read-only balance history."""

    def __init__(self, owner: str, initial_balance: float = 0):
        self.owner = owner
        self._balance = initial_balance
        self._transactions: list = []

    @property
    def balance(self) -> float:
        """Current balance (read-only)."""
        return self._balance

    @property
    def transactions(self) -> list:
        """Transaction history (read-only copy)."""
        return self._transactions.copy()

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
        self._transactions.append({"type": "deposit", "amount": amount})

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self._transactions.append({"type": "withdrawal", "amount": amount})

    def __repr__(self) -> str:
        return f"BankAccount({self.owner}, balance={self._balance})"


# =============================================================================
# 5. Property Decorator Pattern
# =============================================================================

def cached_property(func):
    """Decorator to create a cached property."""
    attr_name = f"_cached_{func.__name__}"

    @property
    def property_wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    return property_wrapper


class DataAnalyzer:
    """Using custom cached_property decorator."""

    def __init__(self, numbers: list):
        self.numbers = numbers

    @cached_property
    def mean(self) -> float:
        print("  Calculating mean...")
        return sum(self.numbers) / len(self.numbers)

    @cached_property
    def variance(self) -> float:
        print("  Calculating variance...")
        mean = self.mean  # Uses cached mean
        return sum((x - mean) ** 2 for x in self.numbers) / len(self.numbers)

    @cached_property
    def std_dev(self) -> float:
        return math.sqrt(self.variance)


# =============================================================================
# 6. Property with Deletion
# =============================================================================

class CachedData:
    """Data with deletable cached properties."""

    def __init__(self, data: list):
        self._data = data
        self._cache = {}

    @property
    def processed(self) -> list:
        if "processed" not in self._cache:
            print("  Processing data...")
            self._cache["processed"] = [x * 2 for x in self._data]
        return self._cache["processed"]

    @processed.deleter
    def processed(self):
        print("  Clearing processed cache")
        self._cache.pop("processed", None)


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PROPERTY DEMO")
    print("=" * 60)

    # 1. Basic property
    print("\n--- Basic Property ---")
    c = Circle(5)
    print(f"  {c}")
    print(f"  Radius: {c.radius}")
    print(f"  Diameter: {c.diameter}")
    print(f"  Area: {c.area:.2f}")
    c.radius = 10
    print(f"  After radius=10: area={c.area:.2f}")

    try:
        c.radius = -5
    except ValueError as e:
        print(f"  Validation: {e}")

    # 2. Caching
    print("\n--- Caching Property ---")
    calc = ExpensiveCalculation([3, 1, 4, 1, 5, 9, 2, 6])
    print(f"  First access: {calc.sorted_data}")
    print(f"  Second access: {calc.sorted_data}")
    print(f"  Stats: {calc.statistics}")

    # 3. Validation
    print("\n--- Temperature Validation ---")
    t = Temperature(100)
    print(f"  {t} = {t.fahrenheit}°F = {t.kelvin}K")
    t.fahrenheit = 32
    print(f"  After 32°F: {t.celsius}°C")

    # 4. Read-only
    print("\n--- Bank Account ---")
    account = BankAccount("Alice", 1000)
    account.deposit(500)
    account.withdraw(200)
    print(f"  Balance: {account.balance}")
    print(f"  Transactions: {account.transactions}")

    # 5. Cached property decorator
    print("\n--- Custom Cached Property ---")
    analyzer = DataAnalyzer([1, 2, 3, 4, 5])
    print(f"  Mean: {analyzer.mean}")
    print(f"  Mean (cached): {analyzer.mean}")
    print(f"  Std Dev: {analyzer.std_dev:.4f}")

    # 6. Deletable property
    print("\n--- Deletable Property ---")
    data = CachedData([1, 2, 3])
    print(f"  Processed: {data.processed}")
    del data.processed
    print(f"  After delete, re-access: {data.processed}")

    print("\n" + "=" * 60)
    print("All property demos complete!")
    print("=" * 60)
