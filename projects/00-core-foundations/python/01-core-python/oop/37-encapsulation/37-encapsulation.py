"""
W3Schools Python Tutorial - 37: Python Encapsulation
=====================================================
Topics: Private variables, getter/setter, name mangling

Run: python 37-encapsulation.py
Reference: https://www.w3schools.com/python/python_encapsulation.asp
"""

# ============================================================
# What is Encapsulation?
# ============================================================
# Encapsulation is the bundling of data (attributes) and methods
# that operate on that data within a single unit (class).
# It restricts direct access to some components.

# ============================================================
# Access Modifiers
# ============================================================
# Python uses naming conventions for access control:
# - public:     attribute (no underscore)
# - protected:  _attribute (single underscore) - convention only
# - private:    __attribute (double underscore) - name mangling

# Example 1: Public, Protected, Private
print("--- Access Modifiers ---")

class Person:
    def __init__(self, name, age, ssn):
        self.name = name          # Public
        self._age = age           # Protected (convention)
        self.__ssn = ssn          # Private (name mangling)
    
    def get_info(self):
        return f"{self.name}, Age: {self._age}"

person = Person("Alice", 30, "123-45-6789")

# Public - accessible
print(f"Name: {person.name}")

# Protected - accessible but "don't touch"
print(f"Age: {person._age}")

# Private - not directly accessible!
try:
    print(f"SSN: {person.__ssn}")
except AttributeError as e:
    print(f"Private access error: {e}")

# Name mangling - Python changes __attribute to _ClassName__attribute
print(f"SSN (mangled): {person._Person__ssn}")

# Output:
# Name: Alice
# Age: 30
# Private access error: 'Person' object has no attribute '__ssn'
# SSN (mangled): 123-45-6789

# ============================================================
# Getter and Setter Methods
# ============================================================
# Example 2: Traditional getter/setter
print("\n--- Getter and Setter ---")

class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    # Getter
    def get_celsius(self):
        return self._celsius
    
    # Setter with validation
    def set_celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value
    
    # Property (Pythonic way)
    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5/9

temp = Temperature(25)
print(f"Celsius: {temp.get_celsius()}")
print(f"Fahrenheit: {temp.fahrenheit}")

temp.set_celsius(100)
print(f"\nAfter set_celsius(100):")
print(f"Celsius: {temp.get_celsius()}")
print(f"Fahrenheit: {temp.fahrenheit}")

temp.fahrenheit = 32
print(f"\nAfter fahrenheit = 32:")
print(f"Celsius: {temp.get_celsius()}")

# Output:
# Celsius: 25
# Fahrenheit: 77.0
#
# After set_celsius(100):
# Celsius: 100
# Fahrenheit: 212.0
#
# After fahrenheit = 32:
# Celsius: 0.0

# ============================================================
# @property Decorator (Pythonic Way)
# ============================================================
# Example 3: Properties with validation
print("\n--- @property Decorator ---")

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance  # Private
        self.__transaction_log = []
    
    @property
    def balance(self):
        """Getter: read-only access to balance."""
        return self.__balance
    
    @balance.setter
    def balance(self, value):
        """Setter: validate before setting."""
        if value < 0:
            raise ValueError("Balance cannot be negative!")
        self.__balance = value
    
    @property
    def transaction_count(self):
        return len(self.__transaction_log)
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive!")
        self.__balance += amount
        self.__transaction_log.append(f"Deposit: +${amount:.2f}")
        return self.__balance
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive!")
        if amount > self.__balance:
            raise ValueError("Insufficient funds!")
        self.__balance -= amount
        self.__transaction_log.append(f"Withdrawal: -${amount:.2f}")
        return self.__balance
    
    def get_statement(self):
        return "\n".join(self.__transaction_log)

account = BankAccount("Alice", 1000)
print(f"Initial balance: ${account.balance}")

account.deposit(500)
account.withdraw(200)
print(f"After transactions: ${account.balance}")
print(f"Transactions: {account.transaction_count}")
print(f"\nStatement:\n{account.get_statement()}")

# Can't access private directly
try:
    print(account.__balance)
except AttributeError:
    print("\nCannot access __balance directly!")

# Output:
# Initial balance: $1000
# After transactions: $1300
# Transactions: 2
#
# Statement:
# Deposit: +$500.00
# Withdrawal: -$200.00
#
# Cannot access __balance directly!

# ============================================================
# Name Mangling
# ============================================================
# Example 4: How name mangling works
print("\n--- Name Mangling ---")

class MyClass:
    def __init__(self):
        self.public = "public"
        self._protected = "protected"
        self.__private = "private"
    
    def get_private(self):
        return self.__private

obj = MyClass()

# Name mangling transforms __private to _MyClass__private
print(f"Public: {obj.public}")
print(f"Protected: {obj._protected}")
print(f"Private (via method): {obj.get_private()}")
print(f"Private (mangled): {obj._MyClass__private}")

# Subclass can't access parent's private
class ChildClass(MyClass):
    def try_access(self):
        try:
            return self.__private  # Fails!
        except AttributeError:
            return "Cannot access parent's private"

child = ChildClass()
print(f"\nChild accessing parent private: {child.try_access()}")

# Output:
# Public: public
# Protected: protected
# Private (via method): private
# Private (mangled): private
#
# Child accessing parent private: Cannot access parent's private

# ============================================================
# Practical Example
# ============================================================
# Example 5: Real-world encapsulation
print("\n--- Practical Example: User Account ---")

class UserAccount:
    def __init__(self, username, email, password):
        self.username = username
        self._email = email  # Protected
        self.__password = self._hash_password(password)  # Private
        self.__failed_attempts = 0
        self.__is_locked = False
    
    @staticmethod
    def _hash_password(password):
        """Simple hash for demo (use proper hashing in production!)."""
        return hash(password)
    
    @property
    def email(self):
        """Getter with masking."""
        return self._email
    
    @email.setter
    def email(self, value):
        """Setter with validation."""
        if "@" not in value:
            raise ValueError("Invalid email format!")
        self._email = value
    
    @property
    def is_locked(self):
        return self.__is_locked
    
    def authenticate(self, password):
        """Try to authenticate."""
        if self.__is_locked:
            return "Account is locked!"
        
        if self._hash_password(password) == self.__password:
            self.__failed_attempts = 0
            return "Authentication successful!"
        
        self.__failed_attempts += 1
        if self.__failed_attempts >= 3:
            self.__is_locked = True
            return "Account locked due to too many failed attempts!"
        
        return f"Wrong password! {3 - self.__failed_attempts} attempts remaining."
    
    def reset_password(self, old_password, new_password):
        """Reset password."""
        if self._hash_password(old_password) != self.__password:
            return "Current password incorrect!"
        self.__password = self._hash_password(new_password)
        return "Password updated!"

# Usage
user = UserAccount("alice", "alice@example.com", "secret123")
print(f"Username: {user.username}")
print(f"Email: {user.email}")

print(f"\nWrong password: {user.authenticate('wrong')}")
print(f"Wrong password: {user.authenticate('wrong')}")
print(f"Wrong password: {user.authenticate('wrong')}")  # Locks account!
print(f"Account locked: {user.is_locked}")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. Public: attribute (no underscore) - fully accessible")
print("2. Protected: _attribute (single underscore) - convention")
print("3. Private: __attribute (double underscore) - name mangling")
print("4. @property: Pythonic getter/setter with validation")
print("5. Name mangling: __attr becomes _Class__attr")
print("6. Encapsulation protects internal state")
print("7. Use methods to control access to private data")
