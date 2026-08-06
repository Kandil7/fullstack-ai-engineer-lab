"""
W3Schools Python Tutorial - 24: Python Iterators
=================================================
Topics: Iterator concept, iter(), next(), custom iterators

Run: python 24-iterators.py
Reference: https://www.w3schools.com/python/python_iterators.asp
"""

# ============================================================
# What is an Iterator?
# ============================================================
# An iterator is an object that contains a countable number of values.
# An iterator is an object that implements the iterator protocol:
#   - __iter__() method returns the iterator object itself
#   - __next__() method returns the next value

# ============================================================
# Example 1: Iterating with a for loop
# ============================================================
print("--- For Loop Iteration ---")
mytuple = ("apple", "banana", "cherry")
for x in mytuple:
    print(x)

# Output:
# apple
# banana
# cherry

# ============================================================
# iter() and next()
# ============================================================
# Example 2: Manual iteration
print("\n--- Manual Iteration ---")
mytuple = ("apple", "banana", "cherry")

# Get iterator from tuple
myiter = iter(mytuple)

# Get first item
print(next(myiter))  # apple
print(next(myiter))  # banana
print(next(myiter))  # cherry

# Uncomment to see StopIteration error:
# print(next(myiter))  # StopIteration

# Example 3: Iterating through a string
print("\n--- String Iterator ---")
mystring = "Hello"
myiter = iter(mystring)

print(next(myiter))  # H
print(next(myiter))  # e
print(next(myiter))  # l
print(next(myiter))  # l
print(next(myiter))  # o

# ============================================================
# For Loop Iteration (Under the Hood)
# ============================================================
# Example 4: What a for loop actually does
print("\n--- Under the Hood ---")
mytuple = ("apple", "banana", "cherry")

# A for loop is equivalent to:
myiter = iter(mytuple)
while True:
    try:
        x = next(myiter)
        print(x)
    except StopIteration:
        break

# ============================================================
# Creating Custom Iterators
# ============================================================
# Example 5: Custom iterator class
class Counter:
    """A custom iterator that counts from 1 to a given number."""
    
    def __init__(self, start, end):
        self.current = start
        self.end = end
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

print("\n--- Custom Iterator: Counter ---")
counter = Counter(1, 5)
for num in counter:
    print(num, end=" ")
print()

# Output: 1 2 3 4 5

# ============================================================
# Example 6: Custom iterator for powers of 2
# ============================================================
class PowerOfTwo:
    """Iterator that yields powers of 2."""
    
    def __init__(self, max_power):
        self.max_power = max_power
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current > self.max_power:
            raise StopIteration
        result = 2 ** self.current
        self.current += 1
        return result

print("\n--- Powers of 2 ---")
for power in PowerOfTwo(5):
    print(f"2^{power.bit_length()-1} = {power}")

# Output:
# 2^0 = 1
# 2^1 = 2
# 2^2 = 4
# 2^3 = 8
# 2^4 = 16
# 2^5 = 32

# ============================================================
# Example 7: Custom iterator for Fibonacci sequence
# ============================================================
class Fibonacci:
    """Iterator that yields Fibonacci numbers."""
    
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
        self.a, self.b = 0, 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.count >= self.max_count:
            raise StopIteration
        value = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return value

print("\n--- Fibonacci Iterator ---")
fib = Fibonacci(10)
for num in fib:
    print(num, end=" ")
print()

# Output: 0 1 1 2 3 5 8 13 21 34

# ============================================================
# Generator Functions (Simpler Iterators)
# ============================================================
# Example 8: Using yield to create iterators
def countdown(n):
    """Generator that counts down from n to 1."""
    while n > 0:
        yield n
        n -= 1

print("\n--- Generator: Countdown ---")
for i in countdown(5):
    print(i, end=" ")
print()

# Output: 5 4 3 2 1

# Example 9: Generator for even numbers
def even_numbers(limit):
    """Generator that yields even numbers up to limit."""
    for i in range(0, limit + 1, 2):
        yield i

print("\n--- Even Numbers Generator ---")
for num in even_numbers(10):
    print(num, end=" ")
print()

# Output: 0 2 4 6 8 10

# ============================================================
# Generator Expressions
# ============================================================
# Example 10: Generator expression (like list comprehension but lazy)
print("\n--- Generator Expression ---")

# List comprehension (creates entire list in memory)
squares_list = [x ** 2 for x in range(10)]
print(f"List: {squares_list}")

# Generator expression (yields one at a time)
squares_gen = (x ** 2 for x in range(10))
print(f"Generator: {squares_gen}")

# Convert to list to see values
print(f"As list: {list(squares_gen)}")

# Memory efficient for large sequences
import sys
list_size = sys.getsizeof([x ** 2 for x in range(1000)])
gen_size = sys.getsizeof(x ** 2 for x in range(1000))
print(f"\nList size: {list_size} bytes")
print(f"Generator size: {gen_size} bytes")

# ============================================================
# Practical Example
# ============================================================
# Example 11: File line iterator (simulated)
class LineReader:
    """Simulated file line iterator."""
    
    def __init__(self, lines):
        self.lines = iter(lines)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        line = next(self.lines)
        return line.strip()

print("\n--- Line Reader Iterator ---")
lines = [
    "  Hello, World!  ",
    "  Python is great  ",
    "  Iterators are useful  "
]

reader = LineReader(lines)
for line in reader:
    print(f"'{line}'")

# Output:
# 'Hello, World!'
# 'Python is great'
# 'Iterators are useful'

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. Iterator: object with __iter__() and __next__() methods")
print("2. iter(): get an iterator from an iterable")
print("3. next(): get the next value from an iterator")
print("4. StopIteration: raised when iterator is exhausted")
print("5. Custom iterators: implement __iter__ and __next__")
print("6. Generators: simpler way to create iterators with yield")
print("7. Generator expressions: (x for x in range(n))")
