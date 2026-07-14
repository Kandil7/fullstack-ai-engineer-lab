"""
Unit Testing - Advanced Python Exercises
=========================================
unittest provides a framework for writing and running tests
with assertions, fixtures, and test organization.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Optional
import math


# =============================================================================
# 1. Classes to Test
# =============================================================================

class Calculator:
    """Simple calculator for testing."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def power(self, a: float, b: float) -> float:
        return a ** b


class BankAccount:
    """Bank account for testing."""

    def __init__(self, owner: str, balance: float = 0):
        self.owner = owner
        self._balance = balance
        self._transactions: List[dict] = []

    @property
    def balance(self) -> float:
        return self._balance

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

    def get_transactions(self) -> List[dict]:
        return self._transactions.copy()


class EmailService:
    """Email service for mocking."""

    def send_email(self, to: str, subject: str, body: str) -> bool:
        # Simulate sending email
        return True

    def validate_email(self, email: str) -> bool:
        return "@" in email and "." in email


class UserService:
    """User service depending on EmailService."""

    def __init__(self, email_service: EmailService):
        self.email_service = email_service
        self.users = []

    def register(self, name: str, email: str) -> dict:
        if not self.email_service.validate_email(email):
            raise ValueError("Invalid email")
        user = {"name": name, "email": email}
        self.users.append(user)
        self.email_service.send_email(email, "Welcome!", f"Hello {name}!")
        return user


# =============================================================================
# 2. Test Cases
# =============================================================================

class TestCalculator(unittest.TestCase):
    """Test Calculator class."""

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

    def test_power(self):
        self.assertEqual(self.calc.power(2, 3), 8)
        self.assertEqual(self.calc.power(5, 0), 1)


class TestBankAccount(unittest.TestCase):
    """Test BankAccount class."""

    def setUp(self):
        self.account = BankAccount("Alice", 1000)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 1000)
        self.assertEqual(self.account.owner, "Alice")

    def test_deposit(self):
        self.account.deposit(500)
        self.assertEqual(self.account.balance, 1500)

    def test_deposit_negative(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100)

    def test_withdraw(self):
        self.account.withdraw(300)
        self.assertEqual(self.account.balance, 700)

    def test_withdraw_insufficient(self):
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(2000)
        self.assertEqual(str(context.exception), "Insufficient funds")

    def test_transactions(self):
        self.account.deposit(100)
        self.account.withdraw(50)
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]["type"], "deposit")
        self.assertEqual(transactions[1]["type"], "withdrawal")


# =============================================================================
# 3. Mock Objects
# =============================================================================

class TestUserService(unittest.TestCase):
    """Test UserService with mocked EmailService."""

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


# =============================================================================
# 4. Patching
# =============================================================================

class TestWithPatch(unittest.TestCase):
    """Test using patch decorator."""

    @patch('builtins.print')
    def test_print_called(self, mock_print):
        print("Hello, World!")
        mock_print.assert_called_once_with("Hello, World!")

    @patch.object(EmailService, 'send_email', return_value=True)
    def test_email_send(self, mock_send):
        service = EmailService()
        result = service.send_email("test@example.com", "Hi", "Hello")
        self.assertTrue(result)
        mock_send.assert_called_once()


# =============================================================================
# 5. Parameterized Tests
# =============================================================================

class TestParameterized(unittest.TestCase):
    """Demonstrate parameterized testing."""

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


# =============================================================================
# 6. setUp and tearDown
# =============================================================================

class TestWithFixtures(unittest.TestCase):
    """Test with setup and teardown."""

    def setUp(self):
        """Set up test fixtures."""
        self.data = [3, 1, 4, 1, 5, 9, 2, 6]
        self.sorted_data = sorted(self.data)

    def tearDown(self):
        """Clean up after tests."""
        self.data = None
        self.sorted_data = None

    def test_sorted(self):
        self.assertEqual(sorted(self.data), self.sorted_data)

    def test_min(self):
        self.assertEqual(min(self.data), 1)

    def test_max(self):
        self.assertEqual(max(self.data), 9)


# =============================================================================
# 7. Test Organization
# =============================================================================

class TestStringOperations(unittest.TestCase):
    """Organized string tests."""

    def test_upper(self):
        self.assertEqual("hello".upper(), "HELLO")

    def test_lower(self):
        self.assertEqual("HELLO".lower(), "hello")

    def test_split(self):
        self.assertEqual("a b c".split(), ["a", "b", "c"])

    def test_join(self):
        self.assertEqual("-".join(["a", "b", "c"]), "a-b-c")

    def test_replace(self):
        self.assertEqual("hello world".replace("world", "Python"), "hello Python")


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("UNIT TESTING DEMO")
    print("=" * 60)
    print("\nRunning all tests...")
    print("-" * 60)

    # Run tests
    unittest.main(verbosity=2)
