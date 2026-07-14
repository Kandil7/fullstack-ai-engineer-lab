# Lecture 18: Unit Testing

## Topic Overview

Unit testing is a software testing technique where individual units of code are tested in isolation. Python's `unittest` module provides a framework for writing and running tests with assertions, fixtures, and test organization. Good testing practices ensure code reliability, facilitate refactoring, and serve as documentation.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Write unit tests** using the unittest framework
2. **Use assertions** to verify expected behavior
3. **Set up test fixtures** with setUp and tearDown
4. **Mock external dependencies** using unittest.mock
5. **Write parameterized tests** for multiple inputs
6. **Organize tests** into test suites
7. **Apply TDD principles** for test-driven development

---

## Key Concepts

### 1. Basic Test Case

Test cases are classes that inherit from `unittest.TestCase`.

#### Simple Test

```python
import unittest

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(2 + 3, 5)
    
    def test_subtract(self):
        self.assertEqual(5 - 3, 2)
    
    def test_multiply(self):
        self.assertEqual(2 * 3, 6)
    
    def test_divide(self):
        self.assertEqual(10 / 2, 5)

if __name__ == "__main__":
    unittest.main()
```

#### Testing a Class

```python
import unittest

class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

class TestCalculator(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.calc = Calculator()
    
    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)
    
    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(0, 5), -5)
    
    def test_multiply(self):
        self.assertEqual(self.calc.multiply(3, 4), 12)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(0, 5), 0)
    
    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertAlmostEqual(self.calc.divide(1, 3), 0.3333, places=3)
    
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError) as context:
            self.calc.divide(10, 0)
        self.assertEqual(str(context.exception), "Cannot divide by zero")

if __name__ == "__main__":
    unittest.main()
```

---

### 2. Common Assertions

`unittest` provides many assertion methods for different comparisons.

```python
import unittest

class TestAssertions(unittest.TestCase):
    def test_equality(self):
        self.assertEqual(2 + 2, 4)
        self.assertNotEqual(2 + 2, 5)
    
    def test_boolean(self):
        self.assertTrue(True)
        self.assertFalse(False)
    
    def test_identity(self):
        self.assertIs(None, None)
        self.assertIsNot(1, 2)
    
    def test_membership(self):
        self.assertIn(1, [1, 2, 3])
        self.assertNotIn(4, [1, 2, 3])
    
    def test_exceptions(self):
        with self.assertRaises(ZeroDivisionError):
            1 / 0
        
        with self.assertRaises(ValueError) as context:
            int("abc")
        self.assertEqual(str(context.exception), "invalid literal for int() with base 10: 'abc'")
    
    def test_float_comparison(self):
        self.assertAlmostEqual(0.1 + 0.2, 0.3, places=7)
        self.assertNotAlmostEqual(0.1 + 0.2, 0.4)
    
    def test_type_checking(self):
        self.assertIsInstance(42, int)
        self.assertNotIsInstance("hello", int)

if __name__ == "__main__":
    unittest.main()
```

---

### 3. setUp and tearDown

Fixtures run before and after each test method.

```python
import unittest

class TestWithFixtures(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures - runs before each test."""
        self.data = [3, 1, 4, 1, 5, 9, 2, 6]
        self.sorted_data = sorted(self.data)
        print(f"setUp: {self.data}")
    
    def tearDown(self):
        """Clean up after tests - runs after each test."""
        self.data = None
        self.sorted_data = None
        print("tearDown: cleaned up")
    
    def test_sorted(self):
        self.assertEqual(sorted(self.data), self.sorted_data)
    
    def test_min(self):
        self.assertEqual(min(self.data), 1)
    
    def test_max(self):
        self.assertEqual(max(self.data), 9)
    
    def test_length(self):
        self.assertEqual(len(self.data), 8)

if __name__ == "__main__":
    unittest.main()
```

#### Class-Level Fixtures

```python
import unittest

class TestWithClassFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up class-level fixtures - runs once for all tests."""
        print("Setting up class fixtures")
        cls.shared_resource = {"key": "value"}
    
    @classmethod
    def tearDownClass(cls):
        """Clean up class-level fixtures - runs once after all tests."""
        print("Cleaning up class fixtures")
        cls.shared_resource = None
    
    def test_shared_resource(self):
        self.assertIsNotNone(self.shared_resource)
        self.assertEqual(self.shared_resource["key"], "value")

if __name__ == "__main__":
    unittest.main()
```

---

### 4. Mock Objects

Mock objects simulate external dependencies for isolated testing.

#### Basic Mock

```python
import unittest
from unittest.mock import Mock

class EmailService:
    def send_email(self, to, subject, body):
        # Simulate sending email
        return True

class UserService:
    def __init__(self, email_service):
        self.email_service = email_service
    
    def register(self, name, email):
        if not self.email_service.validate_email(email):
            raise ValueError("Invalid email")
        user = {"name": name, "email": email}
        self.email_service.send_email(email, "Welcome!", f"Hello {name}!")
        return user

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.mock_email = Mock(spec=EmailService)
        self.service = UserService(self.mock_email)
    
    def test_register_success(self):
        self.mock_email.validate_email.return_value = True
        self.mock_email.send_email.return_value = True
        
        user = self.service.register("Bob", "bob@example.com")
        
        self.assertEqual(user["name"], "Bob")
        self.mock_email.validate_email.assert_called_once_with("bob@example.com")
        self.mock_email.send_email.assert_called_once()
    
    def test_register_invalid_email(self):
        self.mock_email.validate_email.return_value = False
        
        with self.assertRaises(ValueError):
            self.service.register("Bob", "invalid-email")
        
        self.mock_email.send_email.assert_not_called()

if __name__ == "__main__":
    unittest.main()
```

#### Patching

```python
import unittest
from unittest.mock import patch, MagicMock

class ExternalAPI:
    def fetch_data(self, url):
        # Simulate API call
        return {"data": "value"}

class DataService:
    def __init__(self):
        self.api = ExternalAPI()
    
    def get_processed_data(self, url):
        raw = self.api.fetch_data(url)
        return raw["data"].upper()

class TestDataService(unittest.TestCase):
    @patch.object(ExternalAPI, 'fetch_data')
    def test_get_processed_data(self, mock_fetch):
        mock_fetch.return_value = {"data": "hello"}
        
        service = DataService()
        result = service.get_processed_data("http://api.example.com")
        
        self.assertEqual(result, "HELLO")
        mock_fetch.assert_called_once_with("http://api.example.com")

if __name__ == "__main__":
    unittest.main()
```

---

### 5. Parameterized Tests

Test multiple inputs with the same test logic.

```python
import unittest

class Calculator:
    def add(self, a, b):
        return a + b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

class TestParameterized(unittest.TestCase):
    def test_add_parameterized(self):
        calc = Calculator()
        test_cases = [
            (1, 2, 3),
            (0, 0, 0),
            (-1, 1, 0),
            (100, 200, 300),
        ]
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(calc.add(a, b), expected)
    
    def test_division_parameterized(self):
        calc = Calculator()
        test_cases = [
            (10, 2, 5),
            (9, 3, 3),
            (7, 2, 3.5),
        ]
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(calc.divide(a, b), expected)

if __name__ == "__main__":
    unittest.main()
```

---

### 6. Test Organization

Organize tests into logical groups.

```python
import unittest

class TestStringOperations(unittest.TestCase):
    """String operation tests."""
    
    def test_upper(self):
        self.assertEqual("hello".upper(), "HELLO")
    
    def test_lower(self):
        self.assertEqual("HELLO".lower(), "hello")
    
    def test_split(self):
        self.assertEqual("a b c".split(), ["a", "b", "c"])
    
    def test_join(self):
        self.assertEqual("-".join(["a", "b", "c"]), "a-b-c")

class TestListOperations(unittest.TestCase):
    """List operation tests."""
    
    def test_append(self):
        lst = [1, 2, 3]
        lst.append(4)
        self.assertEqual(lst, [1, 2, 3, 4])
    
    def test_extend(self):
        lst = [1, 2]
        lst.extend([3, 4])
        self.assertEqual(lst, [1, 2, 3, 4])
    
    def test_remove(self):
        lst = [1, 2, 3, 2]
        lst.remove(2)
        self.assertEqual(lst, [1, 3, 2])

if __name__ == "__main__":
    unittest.main()
```

---

### 7. Testing Exceptions

Properly test exception handling.

```python
import unittest

class BankAccount:
    def __init__(self, balance=0):
        self._balance = balance
    
    @property
    def balance(self):
        return self._balance
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

class TestBankAccount(unittest.TestCase):
    def test_deposit_positive(self):
        account = BankAccount(100)
        account.deposit(50)
        self.assertEqual(account.balance, 150)
    
    def test_deposit_negative(self):
        account = BankAccount(100)
        with self.assertRaises(ValueError) as context:
            account.deposit(-50)
        self.assertEqual(str(context.exception), "Deposit amount must be positive")
    
    def test_withdraw_insufficient(self):
        account = BankAccount(100)
        with self.assertRaises(ValueError) as context:
            account.withdraw(200)
        self.assertEqual(str(context.exception), "Insufficient funds")
    
    def test_withdraw_success(self):
        account = BankAccount(100)
        account.withdraw(30)
        self.assertEqual(account.balance, 70)

if __name__ == "__main__":
    unittest.main()
```

---

## Common Mistakes to Avoid

### 1. Not Testing Edge Cases

```python
# WRONG - only tests happy path
def test_divide(self):
    self.assertEqual(self.calc.divide(10, 2), 5)

# CORRECT - tests edge cases
def test_divide(self):
    self.assertEqual(self.calc.divide(10, 2), 5)
    self.assertEqual(self.calc.divide(0, 5), 0)
    self.assertEqual(self.calc.divide(-10, 2), -5)
    with self.assertRaises(ValueError):
        self.calc.divide(10, 0)
```

### 2. Testing Implementation Details

```python
# WRONG - tests internal implementation
def test_add(self):
    self.calc._internal_value = 5
    self.assertEqual(self.calc.add(2, 3), 5)

# CORRECT - tests behavior
def test_add(self):
    result = self.calc.add(2, 3)
    self.assertEqual(result, 5)
```

### 3. Not Using setUp/tearDown

```python
# WRONG - creates new instance in each test
def test_add(self):
    calc = Calculator()
    self.assertEqual(calc.add(2, 3), 5)

def test_subtract(self):
    calc = Calculator()  # Duplicate code
    self.assertEqual(calc.subtract(5, 3), 2)

# CORRECT - uses setUp
def setUp(self):
    self.calc = Calculator()

def test_add(self):
    self.assertEqual(self.calc.add(2, 3), 5)

def test_subtract(self):
    self.assertEqual(self.calc.subtract(5, 3), 2)
```

---

## Best Practices

### 1. Follow AAA Pattern

```python
def test_example(self):
    # Arrange
    calculator = Calculator()
    a, b = 2, 3
    
    # Act
    result = calculator.add(a, b)
    
    # Assert
    self.assertEqual(result, 5)
```

### 2. Test One Thing Per Test

```python
# BAD - tests multiple things
def test_calculator(self):
    self.assertEqual(self.calc.add(2, 3), 5)
    self.assertEqual(self.calc.subtract(5, 3), 2)
    self.assertEqual(self.calc.multiply(2, 3), 6)

# GOOD - separate tests
def test_add(self):
    self.assertEqual(self.calc.add(2, 3), 5)

def test_subtract(self):
    self.assertEqual(self.calc.subtract(5, 3), 2)

def test_multiply(self):
    self.assertEqual(self.calc.multiply(2, 3), 6)
```

### 3. Use Descriptive Test Names

```python
# BAD
def test1(self):
    pass

def test2(self):
    pass

# GOOD
def test_add_positive_numbers(self):
    pass

def test_divide_by_zero_raises_error(self):
    pass
```

---

## Practice Exercises

### Exercise 1: Test a String Processor
```python
class StringProcessor:
    def capitalize_words(self, text):
        return text.title()
    
    def count_vowels(self, text):
        return sum(1 for c in text.lower() if c in 'aeiou')
    
    def is_palindrome(self, text):
        cleaned = text.lower().replace(' ', '')
        return cleaned == cleaned[::-1]

# Write tests for StringProcessor
```

### Exercise 2: Test a File Handler
```python
class FileHandler:
    def __init__(self, filename):
        self.filename = filename
    
    def read(self):
        with open(self.filename, 'r') as f:
            return f.read()
    
    def write(self, content):
        with open(self.filename, 'w') as f:
            f.write(content)

# Write tests using mock for file operations
```

### Exercise 3: Test a Cache
```python
class LRUCache:
    def __init__(self, capacity):
        self.cache = {}
        self.capacity = capacity
    
    def get(self, key):
        return self.cache.get(key, -1)
    
    def put(self, key, value):
        if len(self.cache) >= self.capacity:
            # Remove oldest
            oldest = next(iter(self.cache))
            del self.cache[oldest]
        self.cache[key] = value

# Write tests for LRUCache
```

---

## Summary

### Test Case Methods

| Method | Purpose |
|--------|---------|
| `assertEqual(a, b)` | a == b |
| `assertNotEqual(a, b)` | a != b |
| `assertTrue(x)` | bool(x) is True |
| `assertFalse(x)` | bool(x) is False |
| `assertIs(a, b)` | a is b |
| `assertIn(a, b)` | a in b |
| `assertRaises(E)` | E is raised |
| `assertAlmostEqual(a, b)` | round(a-b, N) == 0 |

### Test Fixtures

| Method | When Called |
|--------|------------|
| `setUp()` | Before each test |
| `tearDown()` | After each test |
| `setUpClass()` | Once before all tests |
| `tearDownClass()` | Once after all tests |

### Key Takeaways

1. **Write tests first** (TDD) for better design
2. **Test one thing** per test method
3. **Use setUp/tearDown** for fixtures
4. **Mock external dependencies** for isolation
5. **Test edge cases** and error conditions
6. **Use descriptive names** for test methods

---

## Further Reading

- [Python unittest documentation](https://docs.python.org/3/library/unittest.html)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)
- [pytest documentation](https://docs.pytest.org/)
