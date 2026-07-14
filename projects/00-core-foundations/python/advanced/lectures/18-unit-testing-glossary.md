# Glossary: Unit Testing

## Quick Reference Table

| Term | Definition | Key Methods | Purpose |
|------|------------|-------------|---------|
| Test Case | Class containing test methods | `test_*()` | Test isolation |
| Assertion | Verify expected behavior | `assertEqual()`, `assertTrue()` | Validation |
| Fixture | Test setup/teardown | `setUp()`, `tearDown()` | Test preparation |
| Mock | Simulate external dependencies | `Mock()`, `patch()` | Isolation |
| Test Suite | Collection of tests | `TestSuite()` | Organization |
| Parameterized | Multiple inputs test | `subTest()` | Test coverage |
| TDD | Test-Driven Development | Red-Green-Refactor | Development process |
| Coverage | Code tested percentage | `coverage` module | Quality metric |

---

## Alphabetical Definitions

### assertion

**Definition**: A statement that verifies a condition is true. If false, the test fails. Unittest provides many assertion methods for different comparisons.

**Example**:
```python
import unittest

class TestAssertions(unittest.TestCase):
    def test_equality(self):
        self.assertEqual(2 + 2, 4)
        self.assertNotEqual(2 + 2, 5)
    
    def test_boolean(self):
        self.assertTrue(True)
        self.assertFalse(False)
    
    def test_membership(self):
        self.assertIn(1, [1, 2, 3])
        self.assertNotIn(4, [1, 2, 3])

if __name__ == "__main__":
    unittest.main()
```

**Related Terms**: assertEqual, assertTrue, assertRaises

**Common Assertions**:
- `assertEqual(a, b)`: a == b
- `assertNotEqual(a, b)`: a != b
- `assertTrue(x)`: bool(x) is True
- `assertFalse(x)`: bool(x) is False
- `assertIn(a, b)`: a in b
- `assertRaises(E)`: E is raised

---

### coverage

**Definition**: A metric measuring the percentage of code executed during testing. Higher coverage generally indicates better test completeness.

**Example**:
```python
# Install coverage: pip install coverage
# Run with coverage: coverage run -m pytest
# Generate report: coverage report

# Example coverage report
# Name                    Stmts   Miss  Cover
# -------------------------------------------
# calculator.py              20      2    90%
# -------------------------------------------
# TOTAL                      20      2    90%
```

**Related Terms**: test coverage, code quality, metrics

---

### mock

**Definition**: A simulated object that replaces real dependencies during testing. Allows testing code in isolation without external calls.

**Example**:
```python
import unittest
from unittest.mock import Mock, patch

class EmailService:
    def send_email(self, to, subject, body):
        return True

class UserService:
    def __init__(self, email_service):
        self.email_service = email_service
    
    def register(self, name, email):
        self.email_service.send_email(email, "Welcome", f"Hello {name}")
        return {"name": name, "email": email}

class TestUserService(unittest.TestCase):
    def test_register(self):
        mock_email = Mock(spec=EmailService)
        mock_email.send_email.return_value = True
        
        service = UserService(mock_email)
        user = service.register("Alice", "alice@example.com")
        
        self.assertEqual(user["name"], "Alice")
        mock_email.send_email.assert_called_once()

if __name__ == "__main__":
    unittest.main()
```

**Related Terms**: Mock, patch, MagicMock

**Key Methods**:
- `Mock()`: Create mock object
- `patch()`: Replace object temporarily
- `assert_called()`: Verify method called
- `assert_called_once()`: Verify called exactly once
- `assert_called_with()`: Verify called with args

---

### patch

**Definition**: A context manager or decorator that temporarily replaces an object with a mock during testing.

**Example**:
```python
import unittest
from unittest.mock import patch

class ExternalAPI:
    def fetch(self, url):
        return {"data": "value"}

class DataService:
    def get_data(self, url):
        api = ExternalAPI()
        return api.fetch(url)

class TestDataService(unittest.TestCase):
    @patch.object(ExternalAPI, 'fetch')
    def test_get_data(self, mock_fetch):
        mock_fetch.return_value = {"data": "test"}
        
        service = DataService()
        result = service.get_data("http://api.example.com")
        
        self.assertEqual(result, {"data": "test"})
        mock_fetch.assert_called_once_with("http://api.example.com")

if __name__ == "__main__":
    unittest.main()
```

**Related Terms**: mock, decorator, context manager

---

### parameterized

**Definition**: A technique for running the same test with multiple input sets, improving test coverage without duplicating code.

**Example**:
```python
import unittest

class Calculator:
    def add(self, a, b):
        return a + b

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

if __name__ == "__main__":
    unittest.main()
```

**Related Terms**: subTest, test cases, efficiency

---

### setUp

**Definition**: A method that runs before each test method, used to initialize test fixtures and prepare the test environment.

**Example**:
```python
import unittest

class TestWithSetUp(unittest.TestCase):
    def setUp(self):
        """Runs before each test."""
        self.data = [3, 1, 4, 1, 5, 9, 2, 6]
        self.sorted_data = sorted(self.data)
    
    def test_sorted(self):
        self.assertEqual(sorted(self.data), self.sorted_data)
    
    def test_min(self):
        self.assertEqual(min(self.data), 1)
    
    def test_max(self):
        self.assertEqual(max(self.data), 9)

if __name__ == "__main__":
    unittest.main()
```

**Related Terms**: tearDown, fixture, test lifecycle

---

### subTest

**Definition**: A context manager that allows multiple test cases within a single test method, reporting failures for each case separately.

**Example**:
```python
import unittest

class TestWithSubTest(unittest.TestCase):
    def test_evens(self):
        test_cases = [
            (2, True),
            (4, True),
            (3, False),
            (6, True),
            (7, False),
        ]
        for number, expected in test_cases:
            with self.subTest(number=number):
                self.assertEqual(number % 2 == 0, expected)

if __name__ == "__main__":
    unittest.main()
```

**Related Terms**: parameterized, test cases

---

### TDD (Test-Driven Development)

**Definition**: A development methodology where tests are written before the implementation code. Follows the Red-Green-Refactor cycle.

**Example**:
```python
# Step 1: RED - Write failing test
def test_add(self):
    calc = Calculator()
    self.assertEqual(calc.add(2, 3), 5)

# Step 2: GREEN - Write minimal implementation
class Calculator:
    def add(self, a, b):
        return a + b

# Step 3: REFACTOR - Improve code
class Calculator:
    def add(self, a, b):
        """Add two numbers."""
        return a + b
```

**Related Terms**: Red-Green-Refactor, unit testing

**Cycle**:
1. **Red**: Write a failing test
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve code while tests pass

---

### tearDown

**Definition**: A method that runs after each test method, used to clean up resources and reset state.

**Example**:
```python
import unittest
import tempfile
import os

class TestWithFile(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.mktemp(suffix=".txt")
    
    def tearDown(self):
        """Clean up temp file."""
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
    
    def test_write_and_read(self):
        with open(self.temp_file, 'w') as f:
            f.write("test data")
        
        with open(self.temp_file, 'r') as f:
            content = f.read()
        
        self.assertEqual(content, "test data")

if __name__ == "__main__":
    unittest.main()
```

**Related Terms**: setUp, fixture, cleanup

---

### test case

**Definition**: A class containing test methods that verify specific behavior. Inherits from `unittest.TestCase`.

**Example**:
```python
import unittest

class TestCalculator(unittest.TestCase):
    """Test case for Calculator class."""
    
    def test_add(self):
        self.assertEqual(2 + 2, 4)
    
    def test_subtract(self):
        self.assertEqual(5 - 3, 2)
    
    def test_multiply(self):
        self.assertEqual(2 * 3, 6)

if __name__ == "__main__":
    unittest.main()
```

**Related Terms**: test method, test suite, assertion

---

### test method

**Definition**: A method within a test case that tests a specific behavior. Must start with `test_`.

**Example**:
```python
import unittest

class TestString(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("hello".upper(), "HELLO")
    
    def test_lower(self):
        self.assertEqual("HELLO".lower(), "hello")
    
    def test_split(self):
        self.assertEqual("a b c".split(), ["a", "b", "c"])

if __name__ == "__main__":
    unittest.main()
```

**Related Terms**: test case, assertion

---

### test suite

**Definition**: A collection of test cases and test suites, used to organize and run tests together.

**Example**:
```python
import unittest

class TestA(unittest.TestCase):
    def test_a1(self):
        self.assertTrue(True)

class TestB(unittest.TestCase):
    def test_b1(self):
        self.assertTrue(True)

# Create test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromTestCase(TestA))
suite.addTests(loader.loadTestsFromTestCase(TestB))

# Run suite
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
```

**Related Terms**: test case, test runner

---

## Concept Relationships

```
Unit Testing
├── Framework
│   ├── TestCase (base class)
│   ├── TestSuite (collection)
│   └── TestRunner (execution)
│
├── Assertions
│   ├── assertEqual, assertNotEqual
│   ├── assertTrue, assertFalse
│   ├── assertIn, assertNotIn
│   ├── assertRaises
│   └── assertAlmostEqual
│
├── Fixtures
│   ├── setUp() - before each test
│   ├── tearDown() - after each test
│   ├── setUpClass() - before all tests
│   └── tearDownClass() - after all tests
│
├── Mocking
│   ├── Mock - simulated objects
│   ├── patch - temporary replacement
│   └── MagicMock - enhanced mock
│
└── Best Practices
    ├── AAA pattern (Arrange-Act-Assert)
    ├── One assertion per test
    ├── Descriptive test names
    └── Test edge cases
```

---

## Assertion Methods

| Method | Purpose |
|--------|---------|
| `assertEqual(a, b)` | a == b |
| `assertNotEqual(a, b)` | a != b |
| `assertTrue(x)` | bool(x) is True |
| `assertFalse(x)` | bool(x) is False |
| `assertIs(a, b)` | a is b |
| `assertIsNone(x)` | x is None |
| `assertIn(a, b)` | a in b |
| `assertRaises(E)` | E is raised |
| `assertAlmostEqual(a, b)` | round(a-b, N) == 0 |

---

## Test Lifecycle

```
TestCase
├── setUpClass() [once]
│   ├── setUp() [each test]
│   │   ├── test_method_1()
│   │   └── tearDown()
│   ├── setUp()
│   │   ├── test_method_2()
│   │   └── tearDown()
│   └── tearDownClass() [once]
```

---

## Common Patterns

### 1. AAA Pattern
```python
def test_example(self):
    # Arrange
    calc = Calculator()
    
    # Act
    result = calc.add(2, 3)
    
    # Assert
    self.assertEqual(result, 5)
```

### 2. Mock Pattern
```python
def test_with_mock(self):
    mock_service = Mock(spec=EmailService)
    mock_service.send.return_value = True
    
    service = UserService(mock_service)
    result = service.process()
    
    self.assertTrue(result)
    mock_service.send.assert_called_once()
```

### 3. Exception Testing
```python
def test_exception(self):
    with self.assertRaises(ValueError) as context:
        risky_operation()
    self.assertEqual(str(context.exception), "Expected error")
```

### 4. Parameterized Testing
```python
def test_multiple_inputs(self):
    test_cases = [(1, 2, 3), (0, 0, 0), (-1, 1, 0)]
    for a, b, expected in test_cases:
        with self.subTest(a=a, b=b):
            self.assertEqual(calc.add(a, b), expected)
```
