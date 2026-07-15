"""
W3Schools Python Practice Problems — Complete Solutions
=======================================================
All problems from https://www.w3schools.com/practice/practice_python.php

Run: python practice_all.py
Select a problem number to solve.

Categories:
  EASY (20 XP): Problems 1-41
  MEDIUM (50 XP): Problems 42-81
  HARD (100 XP): Problems 82-99
"""

import math
from collections import Counter


# ============================================================
# EASY PROBLEMS (20 XP)
# ============================================================

# Problem 1: Say Hello
def problem_01():
    """Read a name from input and print a greeting."""
    name = input("Enter your name: ")
    print(f"Hello, {name}!")


# Problem 2: Celsius to Fahrenheit
def problem_02():
    """Convert a temperature from Celsius to Fahrenheit."""
    celsius = float(input("Enter temperature in Celsius: "))
    fahrenheit = (celsius * 9/5) + 32
    print(f"{celsius}°C = {fahrenheit}°F")


# Problem 3: Even or Odd
def problem_03():
    """Check if a number is even or odd."""
    num = int(input("Enter a number: "))
    if num % 2 == 0:
        print(f"{num} is even")
    else:
        print(f"{num} is odd")


# Problem 4: Make a Username
def problem_04():
    """Create a username and initials from a first and last name."""
    first = input("Enter first name: ")
    last = input("Enter last name: ")
    username = f"{first.lower()}.{last.lower()}"
    initials = f"{first[0].upper()}.{last[0].upper()}."
    print(f"Username: {username}")
    print(f"Initials: {initials}")


# Problem 5: Voting Age
def problem_05():
    """Determine if a person is old enough to vote."""
    age = int(input("Enter your age: "))
    if age >= 18:
        print("You are old enough to vote!")
    else:
        print(f"You need to wait {18 - age} more years to vote.")


# Problem 6: Grade Calculator
def problem_06():
    """Convert a score into a letter grade."""
    score = int(input("Enter your score (0-100): "))
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"
    print(f"Score: {score} → Grade: {grade}")


# Problem 7: Multiplication Table
def problem_07():
    """Print the multiplication table for a given number."""
    num = int(input("Enter a number: "))
    print(f"Multiplication table for {num}:")
    for i in range(1, 11):
        print(f"{num} x {i} = {num * i}")


# Problem 8: Factorial
def problem_08():
    """Calculate the factorial of a number."""
    num = int(input("Enter a number: "))
    factorial = 1
    for i in range(1, num + 1):
        factorial *= i
    print(f"{num}! = {factorial}")


# Problem 9: Sum of Numbers
def problem_09():
    """Read a list of numbers and calculate their sum."""
    nums = input("Enter numbers separated by spaces: ")
    numbers = [int(x) for x in nums.split()]
    print(f"Sum: {sum(numbers)}")


# Problem 10: Area Calculator
def problem_10():
    """Calculate the area of a rectangle, triangle, or circle."""
    shape = input("Enter shape (rectangle/triangle/circle): ").lower()
    if shape == "rectangle":
        w = float(input("Width: "))
        h = float(input("Height: "))
        print(f"Area: {w * h}")
    elif shape == "triangle":
        b = float(input("Base: "))
        h = float(input("Height: "))
        print(f"Area: {0.5 * b * h}")
    elif shape == "circle":
        r = float(input("Radius: "))
        print(f"Area: {math.pi * r ** 2:.2f}")


# Problem 11: Shopping Receipt
def problem_11():
    """Read item details and print a short receipt."""
    items = []
    while True:
        name = input("Item name (or 'done'): ")
        if name.lower() == "done":
            break
        price = float(input("Price: "))
        qty = int(input("Quantity: "))
        items.append((name, price, qty))

    print("\n--- Receipt ---")
    total = 0
    for name, price, qty in items:
        subtotal = price * qty
        total += subtotal
        print(f"{name}: ${price:.2f} x {qty} = ${subtotal:.2f}")
    print(f"Total: ${total:.2f}")


# Problem 12: Personal Info
def problem_12():
    """Read personal details and display them."""
    name = input("Name: ")
    age = input("Age: ")
    city = input("City: ")
    print(f"\nName: {name}")
    print(f"Age: {age}")
    print(f"City: {city}")


# Problem 13: Swap Values
def problem_13():
    """Read two values and print them in swapped order."""
    a = input("First value: ")
    b = input("Second value: ")
    print(f"Before: a={a}, b={b}")
    a, b = b, a
    print(f"After: a={a}, b={b}")


# Problem 14: Rectangle Border
def problem_14():
    """Print a rectangle border made of stars."""
    width = int(input("Width: "))
    height = int(input("Height: "))
    for i in range(height):
        if i == 0 or i == height - 1:
            print("*" * width)
        else:
            print("*" + " " * (width - 2) + "*")


# Problem 15: Repeat Message
def problem_15():
    """Read a message and a number, then print the message that many times."""
    msg = input("Message: ")
    times = int(input("How many times? "))
    for _ in range(times):
        print(msg)


# Problem 16: Currency Exchange
def problem_16():
    """Calculate a currency exchange from an amount and rate."""
    amount = float(input("Amount: "))
    rate = float(input("Exchange rate: "))
    result = amount * rate
    print(f"${amount:.2f} × {rate} = ${result:.2f}")


# Problem 17: BMI Calculator
def problem_17():
    """Calculate Body Mass Index from weight and height."""
    weight = float(input("Weight (kg): "))
    height = float(input("Height (m): "))
    bmi = weight / (height ** 2)
    print(f"BMI: {bmi:.1f}")
    if bmi < 18.5:
        print("Category: Underweight")
    elif bmi < 25:
        print("Category: Normal weight")
    elif bmi < 30:
        print("Category: Overweight")
    else:
        print("Category: Obese")


# Problem 18: Circle Properties
def problem_18():
    """Calculate the circumference and area of a circle."""
    r = float(input("Radius: "))
    circumference = 2 * math.pi * r
    area = math.pi * r ** 2
    print(f"Circumference: {circumference:.2f}")
    print(f"Area: {area:.2f}")


# Problem 19: Simple Calculator
def problem_19():
    """Perform basic arithmetic on two numbers."""
    a = float(input("First number: "))
    op = input("Operator (+, -, *, /): ")
    b = float(input("Second number: "))
    if op == "+":
        print(f"Result: {a + b}")
    elif op == "-":
        print(f"Result: {a - b}")
    elif op == "*":
        print(f"Result: {a * b}")
    elif op == "/":
        print(f"Result: {a / b}" if b != 0 else "Error: Division by zero")


# Problem 20: Discount Price
def problem_20():
    """Calculate a discounted price from a price and discount percentage."""
    price = float(input("Original price: "))
    discount = float(input("Discount percentage: "))
    final = price * (1 - discount / 100)
    print(f"Final price: ${final:.2f}")


# Problem 21: Split the Bill
def problem_21():
    """Split a total amount equally among a group of people."""
    total = float(input("Total bill: "))
    people = int(input("Number of people: "))
    per_person = total / people
    print(f"Each person pays: ${per_person:.2f}")


# Problem 22: Digit Extractor
def problem_22():
    """Extract the individual digits of a 3-digit number."""
    num = int(input("Enter a 3-digit number: "))
    hundreds = num // 100
    tens = (num // 10) % 10
    ones = num % 10
    print(f"Hundreds: {hundreds}")
    print(f"Tens: {tens}")
    print(f"Ones: {ones}")


# Problem 23: Word Counter
def problem_23():
    """Count the number of words in a sentence."""
    sentence = input("Enter a sentence: ")
    words = sentence.split()
    print(f"Word count: {len(words)}")


# Problem 24: Shout It Out
def problem_24():
    """Convert a string to uppercase and print its length."""
    text = input("Enter text: ")
    print(f"Uppercase: {text.upper()}")
    print(f"Length: {len(text)}")


# Problem 25: First and Last
def problem_25():
    """Print the first and last character of a word."""
    word = input("Enter a word: ")
    print(f"First: {word[0]}")
    print(f"Last: {word[-1]}")


# Problem 26: Repeat String
def problem_26():
    """Read a string and a number, then print the string repeated that many times."""
    text = input("Enter text: ")
    times = int(input("How many times? "))
    print(text * times)


# Problem 27: Range Checker
def problem_27():
    """Check if a number falls within a given range."""
    num = float(input("Enter a number: "))
    low = float(input("Range start: "))
    high = float(input("Range end: "))
    if low <= num <= high:
        print(f"{num} is in the range [{low}, {high}]")
    else:
        print(f"{num} is NOT in the range [{low}, {high}]")


# Problem 28: Password Check
def problem_28():
    """Check if a password is long enough."""
    password = input("Enter password: ")
    min_length = 8
    if len(password) >= min_length:
        print("Password is strong enough!")
    else:
        print(f"Password too short. Need {min_length - len(password)} more characters.")


# Problem 29: Ticket Price
def problem_29():
    """Determine the ticket type and price based on age."""
    age = int(input("Enter age: "))
    if age < 5:
        print("Free entry!")
    elif age < 12:
        print("Child ticket: $5")
    elif age < 60:
        print("Adult ticket: $10")
    else:
        print("Senior ticket: $7")


# Problem 30: Positive Negative Zero
def problem_30():
    """Check if a number is positive, negative, or zero."""
    num = float(input("Enter a number: "))
    if num > 0:
        print("Positive")
    elif num < 0:
        print("Negative")
    else:
        print("Zero")


# Problem 31: Smallest of Three
def problem_31():
    """Find the smallest of three numbers."""
    a = float(input("First number: "))
    b = float(input("Second number: "))
    c = float(input("Third number: "))
    print(f"Smallest: {min(a, b, c)}")


# Problem 32: Countdown
def problem_32():
    """Count down from a number to 1 and print Go!"""
    num = int(input("Start countdown from: "))
    for i in range(num, 0, -1):
        print(i)
    print("Go!")


# Problem 33: FizzBuzz
def problem_33():
    """Implement the classic FizzBuzz challenge."""
    n = int(input("Enter a number: "))
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)


# Problem 34: Sum 1 to N
def problem_34():
    """Calculate the sum of all numbers from 1 to N."""
    n = int(input("Enter N: "))
    total = sum(range(1, n + 1))
    print(f"Sum from 1 to {n}: {total}")


# Problem 35: Star Triangle
def problem_35():
    """Print a right triangle made of stars."""
    n = int(input("Height: "))
    for i in range(1, n + 1):
        print("*" * i)


# Problem 36: Tip Calculator
def problem_36():
    """Create a tip calculator function for a restaurant bill."""
    bill = float(input("Bill amount: "))
    tip_percent = float(input("Tip percentage: "))
    tip = bill * tip_percent / 100
    total = bill + tip
    print(f"Tip: ${tip:.2f}")
    print(f"Total: ${total:.2f}")


# Problem 37: Power Function
def problem_37():
    """Write a function that calculates the power of a number."""
    base = float(input("Base: "))
    exp = int(input("Exponent: "))
    result = base ** exp
    print(f"{base}^{exp} = {result}")


# Problem 38: Average Score
def problem_38():
    """Read a list of scores and calculate their average."""
    scores = input("Enter scores separated by spaces: ")
    scores = [float(x) for x in scores.split()]
    average = sum(scores) / len(scores)
    print(f"Average: {average:.2f}")


# Problem 39: Count Matches
def problem_39():
    """Count how many numbers in a list match a target value."""
    nums = input("Enter numbers: ")
    numbers = [int(x) for x in nums.split()]
    target = int(input("Target value: "))
    count = numbers.count(target)
    print(f"{target} appears {count} time(s)")


# Problem 40: Min and Max
def problem_40():
    """Find the smallest and largest numbers in a list."""
    nums = input("Enter numbers: ")
    numbers = [int(x) for x in nums.split()]
    print(f"Smallest: {min(numbers)}")
    print(f"Largest: {max(numbers)}")


# Problem 41: Absolute Difference
def problem_41():
    """Calculate the absolute difference between two numbers."""
    a = float(input("First number: "))
    b = float(input("Second number: "))
    diff = abs(a - b)
    print(f"Absolute difference: {diff}")


# ============================================================
# MEDIUM PROBLEMS (50 XP)
# ============================================================

# Problem 42: Leap Year
def problem_42():
    """Determine if a given year is a leap year."""
    year = int(input("Enter a year: "))
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        print(f"{year} is a leap year")
    else:
        print(f"{year} is not a leap year")


# Problem 43: Day of Week
def problem_43():
    """Convert a day number to a day name."""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    num = int(input("Enter day number (1-7): "))
    if 1 <= num <= 7:
        print(f"Day {num}: {days[num - 1]}")
    else:
        print("Invalid number")


# Problem 44: Triangle Classifier
def problem_44():
    """Classify a triangle based on its side lengths."""
    a = float(input("Side A: "))
    b = float(input("Side B: "))
    c = float(input("Side C: "))
    if a + b <= c or a + c <= b or b + c <= a:
        print("Not a valid triangle")
    elif a == b == c:
        print("Equilateral")
    elif a == b or b == c or a == c:
        print("Isosceles")
    else:
        print("Scalene")


# Problem 45: Time Converter
def problem_45():
    """Convert a number of seconds into hours, minutes, and seconds."""
    total = int(input("Enter seconds: "))
    hours = total // 3600
    minutes = (total % 3600) // 60
    seconds = total % 60
    print(f"{hours}h {minutes}m {seconds}s")


# Problem 46: Reverse Words
def problem_46():
    """Reverse the order of words in a sentence."""
    sentence = input("Enter a sentence: ")
    words = sentence.split()
    reversed_words = words[::-1]
    print(" ".join(reversed_words))


# Problem 47: Palindrome Check
def problem_47():
    """Check if a word reads the same forwards and backwards."""
    word = input("Enter a word: ").lower()
    if word == word[::-1]:
        print(f"'{word}' is a palindrome!")
    else:
        print(f"'{word}' is not a palindrome.")


# Problem 48: Count Vowels
def problem_48():
    """Count the number of vowels in a string."""
    text = input("Enter text: ").lower()
    vowels = "aeiou"
    count = sum(1 for char in text if char in vowels)
    print(f"Vowel count: {count}")


# Problem 49: Title Case
def problem_49():
    """Capitalize the first letter of each word in a sentence."""
    sentence = input("Enter a sentence: ")
    print(sentence.title())


# Problem 50: Remove Duplicates
def problem_50():
    """Remove consecutive duplicate characters from a string."""
    text = input("Enter text: ")
    if not text:
        print("Result: (empty)")
        return
    result = text[0]
    for char in text[1:]:
        if char != result[-1]:
            result += char
    print(f"Result: {result}")


# Problem 51: Longest Word
def problem_51():
    """Find the longest word in a sentence."""
    sentence = input("Enter a sentence: ")
    words = sentence.split()
    longest = max(words, key=len)
    print(f"Longest word: '{longest}' ({len(longest)} characters)")


# Problem 52: Access Control
def problem_52():
    """Determine if a person gets access based on role, age, and membership."""
    role = input("Role (admin/user/guest): ").lower()
    age = int(input("Age: "))
    member = input("Is member? (yes/no): ").lower() == "yes"

    if role == "admin":
        print("Access granted (admin)")
    elif role == "user" and age >= 18 and member:
        print("Access granted (member)")
    elif role == "user" and age >= 21:
        print("Access granted (age)")
    else:
        print("Access denied")


# Problem 53: Digit Sum
def problem_53():
    """Calculate the sum of all digits in a number."""
    num = abs(int(input("Enter a number: ")))
    digit_sum = sum(int(d) for d in str(num))
    print(f"Digit sum: {digit_sum}")


# Problem 54: Number Pyramid
def problem_54():
    """Print a pyramid of numbers."""
    n = int(input("Height: "))
    for i in range(1, n + 1):
        spaces = " " * (n - i)
        nums = " ".join(str(j) for j in range(1, i + 1))
        print(spaces + nums)


# Problem 55: Collatz Steps
def problem_55():
    """Count the steps to reach 1 using the Collatz sequence."""
    n = int(input("Enter a number: "))
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    print(f"Steps to reach 1: {steps}")


# Problem 56: Prime Check
def problem_56():
    """Check if a number is a prime number."""
    num = int(input("Enter a number: "))
    if num < 2:
        print(f"{num} is not prime")
        return
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            print(f"{num} is not prime (divisible by {i})")
            return
    print(f"{num} is prime!")


# Problem 57: Reverse Number
def problem_57():
    """Reverse the digits of a number."""
    num = int(input("Enter a number: "))
    reversed_num = int(str(num)[::-1])
    print(f"Reversed: {reversed_num}")


# Problem 58: Is Palindrome Function
def problem_58():
    """Write a function that checks if a word is a palindrome."""
    word = input("Enter a word: ").lower()
    is_palindrome = word == word[::-1]
    print(f"Is palindrome: {is_palindrome}")


# Problem 59: Min of Three
def problem_59():
    """Write a function that returns the smallest of three numbers."""
    a = float(input("First: "))
    b = float(input("Second: "))
    c = float(input("Third: "))
    print(f"Smallest: {min(a, b, c)}")


# Problem 60: Count Digits
def problem_60():
    """Write a function that counts the number of digits in a number."""
    num = abs(int(input("Enter a number: ")))
    count = len(str(num))
    print(f"Digit count: {count}")


# Problem 61: Recursive Sum
def problem_61():
    """Write a recursive function to sum numbers from 1 to N."""
    def recursive_sum(n):
        if n == 0:
            return 0
        return n + recursive_sum(n - 1)

    n = int(input("Enter N: "))
    print(f"Sum from 1 to {n}: {recursive_sum(n)}")


# Problem 62: Array Map Function
def problem_62():
    """Write a function that doubles every number in a list."""
    nums = input("Enter numbers: ")
    numbers = [int(x) for x in nums.split()]
    doubled = [x * 2 for x in numbers]
    print(f"Doubled: {doubled}")


# Problem 63: Find the Largest
def problem_63():
    """Read a list of numbers and find the largest one."""
    nums = input("Enter numbers: ")
    numbers = [int(x) for x in nums.split()]
    print(f"Largest: {max(numbers)}")


# Problem 64: Reverse a List
def problem_64():
    """Read a list of numbers and print them in reverse order."""
    nums = input("Enter numbers: ")
    numbers = [int(x) for x in nums.split()]
    print(f"Reversed: {numbers[::-1]}")


# Problem 65: Second Largest
def problem_65():
    """Find the second largest number in a list."""
    nums = input("Enter numbers: ")
    numbers = list(set(int(x) for x in nums.split()))
    numbers.sort(reverse=True)
    if len(numbers) >= 2:
        print(f"Second largest: {numbers[1]}")
    else:
        print("Not enough unique numbers")


# Problem 66: Running Sum
def problem_66():
    """Print the running (cumulative) sum of a list of numbers."""
    nums = input("Enter numbers: ")
    numbers = [int(x) for x in nums.split()]
    running = []
    total = 0
    for n in numbers:
        total += n
        running.append(total)
    print(f"Running sum: {running}")


# Problem 67: Count Above Average
def problem_67():
    """Count how many numbers are above the average."""
    nums = input("Enter numbers: ")
    numbers = [int(x) for x in nums.split()]
    avg = sum(numbers) / len(numbers)
    count = sum(1 for n in numbers if n > avg)
    print(f"Average: {avg:.2f}")
    print(f"Above average: {count}")


# Problem 68: Longest Streak
def problem_68():
    """Find the longest consecutive streak of the same number."""
    nums = input("Enter numbers: ")
    numbers = [int(x) for x in nums.split()]
    max_streak = 1
    current_streak = 1
    for i in range(1, len(numbers)):
        if numbers[i] == numbers[i - 1]:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1
    print(f"Longest streak: {max_streak}")


# Problem 69: Greatest Common Divisor
def problem_69():
    """Find the greatest common divisor (GCD) of two numbers."""
    a = int(input("First number: "))
    b = int(input("Second number: "))
    print(f"GCD: {math.gcd(a, b)}")


# Problem 70: Fibonacci
def problem_70():
    """Print the first N numbers of the Fibonacci sequence."""
    n = int(input("How many Fibonacci numbers? "))
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    print(f"Fibonacci: {fib[:n]}")


# Problem 71: Prime Factors
def problem_71():
    """Find all prime factors of a number."""
    n = int(input("Enter a number: "))
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    print(f"Prime factors: {factors}")


# Problem 72: Power of Two
def problem_72():
    """Check if a number is a power of 2."""
    num = int(input("Enter a number: "))
    if num > 0 and (num & (num - 1)) == 0:
        print(f"{num} is a power of 2")
    else:
        print(f"{num} is NOT a power of 2")


# Problem 73: Sum of Squares
def problem_73():
    """Calculate the sum of squares from 1 to N."""
    n = int(input("Enter N: "))
    total = sum(i ** 2 for i in range(1, n + 1))
    print(f"Sum of squares 1² to {n}²: {total}")


# Problem 74: LCM Calculator
def problem_74():
    """Calculate the least common multiple of two numbers."""
    a = int(input("First number: "))
    b = int(input("Second number: "))
    lcm = abs(a * b) // math.gcd(a, b)
    print(f"LCM: {lcm}")


# Problem 75: Perfect Number
def problem_75():
    """Check if a number is a perfect number."""
    num = int(input("Enter a number: "))
    divisors = [i for i in range(1, num) if num % i == 0]
    if sum(divisors) == num:
        print(f"{num} is a perfect number!")
    else:
        print(f"{num} is NOT a perfect number")


# Problem 76: Sort Three Numbers
def problem_76():
    """Read three numbers and print them in ascending order."""
    a = float(input("First: "))
    b = float(input("Second: "))
    c = float(input("Third: "))
    print(f"Sorted: {sorted([a, b, c])}")


# Problem 77: Sort Numbers
def problem_77():
    """Read a list of numbers and print them sorted."""
    nums = input("Enter numbers: ")
    numbers = [int(x) for x in nums.split()]
    print(f"Sorted: {sorted(numbers)}")


# Problem 78: Sort Words
def problem_78():
    """Read a list of words and print them sorted alphabetically."""
    words = input("Enter words: ").split()
    print(f"Sorted: {sorted(words)}")


# Problem 79: Letter Frequency
def problem_79():
    """Count how many times each letter appears in a word."""
    word = input("Enter a word: ").lower()
    freq = Counter(word)
    for letter, count in sorted(freq.items()):
        print(f"'{letter}': {count}")


# Problem 80: Most Common Char
def problem_80():
    """Find the character that appears most often in a string."""
    text = input("Enter text: ").lower()
    freq = Counter(text)
    most_common = freq.most_common(1)[0]
    print(f"Most common: '{most_common[0]}' ({most_common[1]} times)")


# Problem 81: Digit Frequency
def problem_81():
    """Count how many times each digit appears in a number."""
    num = str(abs(int(input("Enter a number: "))))
    freq = Counter(num)
    for digit, count in sorted(freq.items()):
        print(f"Digit {digit}: {count} time(s)")


# ============================================================
# HARD PROBLEMS (100 XP)
# ============================================================

# Problem 82: Caesar Cipher
def problem_82():
    """Encrypt a message by shifting each letter in the alphabet."""
    text = input("Enter text: ")
    shift = int(input("Shift value: "))
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    print(f"Encrypted: {result}")


# Problem 83: Anagram Check
def problem_83():
    """Check if two words are anagrams of each other."""
    word1 = input("First word: ").lower()
    word2 = input("Second word: ").lower()
    if sorted(word1) == sorted(word2):
        print("They are anagrams!")
    else:
        print("They are NOT anagrams.")


# Problem 84: Run Length Encoding
def problem_84():
    """Compress a string using run-length encoding."""
    text = input("Enter text: ")
    if not text:
        return
    result = ""
    count = 1
    for i in range(1, len(text)):
        if text[i] == text[i-1]:
            count += 1
        else:
            result += text[i-1] + str(count)
            count = 1
    result += text[-1] + str(count)
    print(f"Encoded: {result}")


# Problem 85: Date Validator
def problem_85():
    """Check if a given date is valid."""
    date = input("Enter date (DD/MM/YYYY): ")
    try:
        day, month, year = map(int, date.split("/"))
        if month < 1 or month > 12:
            print("Invalid month")
            return
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if month == 2 and (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
            days_in_month[1] = 29
        if day < 1 or day > days_in_month[month - 1]:
            print("Invalid day")
            return
        print(f"Date {date} is valid!")
    except ValueError:
        print("Invalid format")


# Problem 86: Diamond Pattern
def problem_86():
    """Print a diamond pattern of stars."""
    n = int(input("Half height: "))
    for i in range(1, n + 1):
        print(" " * (n - i) + "*" * (2 * i - 1))
    for i in range(n - 1, 0, -1):
        print(" " * (n - i) + "*" * (2 * i - 1))


# Problem 87: Number to Binary
def problem_87():
    """Convert a decimal number to binary."""
    num = int(input("Enter a number: "))
    binary = bin(num)[2:]
    print(f"Binary: {binary}")


# Problem 88: Pascal Triangle Row
def problem_88():
    """Print a specific row of Pascal's triangle."""
    row = int(input("Enter row number (0-indexed): "))
    result = [1]
    for i in range(1, row + 1):
        result.append(result[i-1] * (row - i + 1) // i)
    print(f"Row {row}: {result}")


# Problem 89: Remove Duplicates (List)
def problem_89():
    """Remove duplicate numbers from a list while keeping order."""
    nums = input("Enter numbers: ")
    numbers = [int(x) for x in nums.split()]
    seen = set()
    result = []
    for n in numbers:
        if n not in seen:
            seen.add(n)
            result.append(n)
    print(f"Without duplicates: {result}")


# Problem 90: Rotate Left
def problem_90():
    """Rotate a list of numbers to the left by K positions."""
    nums = input("Enter numbers: ")
    numbers = [int(x) for x in nums.split()]
    k = int(input("Rotate by: "))
    k = k % len(numbers)
    rotated = numbers[k:] + numbers[:k]
    print(f"Rotated: {rotated}")


# Problem 91: Merge Sorted
def problem_91():
    """Merge two sorted lists into one sorted list."""
    list1 = [int(x) for x in input("List 1 (sorted): ").split()]
    list2 = [int(x) for x in input("List 2 (sorted): ").split()]
    merged = sorted(list1 + list2)
    print(f"Merged: {merged}")


# Problem 92: Pair Sum
def problem_92():
    """Find the first pair of numbers that add up to a target."""
    nums = [int(x) for x in input("Enter numbers: ").split()]
    target = int(input("Target sum: "))
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            print(f"Pair found: {complement} + {num} = {target}")
            return
        seen[num] = i
    print("No pair found")


# Problem 93: GCD Function (Recursive)
def problem_93():
    """Write a recursive function to find the GCD of two numbers."""
    def gcd(a, b):
        if b == 0:
            return a
        return gcd(b, a % b)

    a = int(input("First: "))
    b = int(input("Second: "))
    print(f"GCD: {gcd(a, b)}")


# Problem 94: Number Base Convert
def problem_94():
    """Convert a number from one base to another."""
    num = input("Number: ")
    from_base = int(input("From base: "))
    to_base = int(input("To base: "))
    decimal = int(num, from_base)
    if to_base == 2:
        result = bin(decimal)[2:]
    elif to_base == 8:
        result = oct(decimal)[2:]
    elif to_base == 16:
        result = hex(decimal)[2:].upper()
    else:
        result = ""
        n = decimal
        while n > 0:
            result = str(n % to_base) + result
            n //= to_base
    print(f"Result: {result}")


# Problem 95: Bubble Sort
def problem_95():
    """Implement bubble sort and count the number of swaps."""
    nums = [int(x) for x in input("Enter numbers: ").split()]
    arr = nums[:]
    swaps = 0
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
    print(f"Sorted: {arr}")
    print(f"Swaps: {swaps}")


# Problem 96: Selection Sort
def problem_96():
    """Implement selection sort and print each step."""
    nums = [int(x) for x in input("Enter numbers: ").split()]
    arr = nums[:]
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        print(f"Step {i + 1}: {arr}")
    print(f"Final: {arr}")


# Problem 97: Insertion Sort
def problem_97():
    """Implement insertion sort and print each step."""
    nums = [int(x) for x in input("Enter numbers: ").split()]
    arr = nums[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        print(f"Step {i}: {arr}")
    print(f"Final: {arr}")


# Problem 98: Word Frequency
def problem_98():
    """Count how many times each word appears in a sentence."""
    sentence = input("Enter a sentence: ").lower()
    words = sentence.split()
    freq = Counter(words)
    for word, count in sorted(freq.items()):
        print(f"'{word}': {count}")


# Problem 99: Unique Elements Count
def problem_99():
    """Count how many unique numbers appear in a list."""
    nums = input("Enter numbers: ")
    numbers = [int(x) for x in nums.split()]
    unique = len(set(numbers))
    print(f"Unique elements: {unique}")


# ============================================================
# MAIN MENU
# ============================================================

def main():
    problems = {
        # Easy
        1: ("Say Hello", problem_01),
        2: ("Celsius to Fahrenheit", problem_02),
        3: ("Even or Odd", problem_03),
        4: ("Make a Username", problem_04),
        5: ("Voting Age", problem_05),
        6: ("Grade Calculator", problem_06),
        7: ("Multiplication Table", problem_07),
        8: ("Factorial", problem_08),
        9: ("Sum of Numbers", problem_09),
        10: ("Area Calculator", problem_10),
        11: ("Shopping Receipt", problem_11),
        12: ("Personal Info", problem_12),
        13: ("Swap Values", problem_13),
        14: ("Rectangle Border", problem_14),
        15: ("Repeat Message", problem_15),
        16: ("Currency Exchange", problem_16),
        17: ("BMI Calculator", problem_17),
        18: ("Circle Properties", problem_18),
        19: ("Simple Calculator", problem_19),
        20: ("Discount Price", problem_20),
        21: ("Split the Bill", problem_21),
        22: ("Digit Extractor", problem_22),
        23: ("Word Counter", problem_23),
        24: ("Shout It Out", problem_24),
        25: ("First and Last", problem_25),
        26: ("Repeat String", problem_26),
        27: ("Range Checker", problem_27),
        28: ("Password Check", problem_28),
        29: ("Ticket Price", problem_29),
        30: ("Positive Negative Zero", problem_30),
        31: ("Smallest of Three", problem_31),
        32: ("Countdown", problem_32),
        33: ("FizzBuzz", problem_33),
        34: ("Sum 1 to N", problem_34),
        35: ("Star Triangle", problem_35),
        36: ("Tip Calculator", problem_36),
        37: ("Power Function", problem_37),
        38: ("Average Score", problem_38),
        39: ("Count Matches", problem_39),
        40: ("Min and Max", problem_40),
        41: ("Absolute Difference", problem_41),
        # Medium
        42: ("Leap Year", problem_42),
        43: ("Day of Week", problem_43),
        44: ("Triangle Classifier", problem_44),
        45: ("Time Converter", problem_45),
        46: ("Reverse Words", problem_46),
        47: ("Palindrome Check", problem_47),
        48: ("Count Vowels", problem_48),
        49: ("Title Case", problem_49),
        50: ("Remove Duplicates", problem_50),
        51: ("Longest Word", problem_51),
        52: ("Access Control", problem_52),
        53: ("Digit Sum", problem_53),
        54: ("Number Pyramid", problem_54),
        55: ("Collatz Steps", problem_55),
        56: ("Prime Check", problem_56),
        57: ("Reverse Number", problem_57),
        58: ("Is Palindrome Function", problem_58),
        59: ("Min of Three", problem_59),
        60: ("Count Digits", problem_60),
        61: ("Recursive Sum", problem_61),
        62: ("Array Map Function", problem_62),
        63: ("Find the Largest", problem_63),
        64: ("Reverse a List", problem_64),
        65: ("Second Largest", problem_65),
        66: ("Running Sum", problem_66),
        67: ("Count Above Average", problem_67),
        68: ("Longest Streak", problem_68),
        69: ("Greatest Common Divisor", problem_69),
        70: ("Fibonacci", problem_70),
        71: ("Prime Factors", problem_71),
        72: ("Power of Two", problem_72),
        73: ("Sum of Squares", problem_73),
        74: ("LCM Calculator", problem_74),
        75: ("Perfect Number", problem_75),
        76: ("Sort Three Numbers", problem_76),
        77: ("Sort Numbers", problem_77),
        78: ("Sort Words", problem_78),
        79: ("Letter Frequency", problem_79),
        80: ("Most Common Char", problem_80),
        81: ("Digit Frequency", problem_81),
        # Hard
        82: ("Caesar Cipher", problem_82),
        83: ("Anagram Check", problem_83),
        84: ("Run Length Encoding", problem_84),
        85: ("Date Validator", problem_85),
        86: ("Diamond Pattern", problem_86),
        87: ("Number to Binary", problem_87),
        88: ("Pascal Triangle Row", problem_88),
        89: ("Remove Duplicates (List)", problem_89),
        90: ("Rotate Left", problem_90),
        91: ("Merge Sorted", problem_91),
        92: ("Pair Sum", problem_92),
        93: ("GCD Function (Recursive)", problem_93),
        94: ("Number Base Convert", problem_94),
        95: ("Bubble Sort", problem_95),
        96: ("Selection Sort", problem_96),
        97: ("Insertion Sort", problem_97),
        98: ("Word Frequency", problem_98),
        99: ("Unique Elements Count", problem_99),
    }

    print("=" * 50)
    print("  W3Schools Python Practice Problems")
    print("=" * 50)
    print("\nCategories:")
    print("  EASY (1-41):    20 XP each")
    print("  MEDIUM (42-81): 50 XP each")
    print("  HARD (82-99):   100 XP each")
    print("\n  Type 'list' to see all problems")
    print("  Type 'quit' to exit")
    print("=" * 50)

    while True:
        choice = input("\nEnter problem number: ").strip().lower()

        if choice == "quit":
            print("Goodbye!")
            break
        elif choice == "list":
            print("\n--- EASY ---")
            for num in range(1, 42):
                print(f"  {num:2d}. {problems[num][0]}")
            print("\n--- MEDIUM ---")
            for num in range(42, 82):
                print(f"  {num:2d}. {problems[num][0]}")
            print("\n--- HARD ---")
            for num in range(82, 100):
                print(f"  {num:2d}. {problems[num][0]}")
            continue

        try:
            num = int(choice)
            if num in problems:
                name, func = problems[num]
                print(f"\n--- Problem {num}: {name} ---")
                func()
            else:
                print("Invalid problem number. Enter 1-99.")
        except ValueError:
            print("Please enter a valid number.")


if __name__ == "__main__":
    main()
