# Python Error Handling Quiz

## Topic Overview
This quiz covers Python error handling including exception types, try/except/else/finally blocks, custom exceptions, and context managers. Test your understanding of how to handle errors gracefully in Python.

## Instructions
- Each question has 4 options (A, B, C, D)
- Select the best answer for each question
- Check your answers using the Answer Key at the end
- Track your score: 1 point per correct answer

---

## Questions

### Question 1
**What is a syntax error?**

A) An error that occurs at runtime  
B) An error in the structure of the code that prevents it from running  
C) An error that occurs when a function is called incorrectly  
D) An error that occurs when a variable is not defined  

**Difficulty:** Easy  

---

### Question 2
**What is the output of this code?**
```python
try:
    x = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
```

A) 10  
B) Error  
C) Cannot divide by zero  
D) None  

**Difficulty:** Easy  

---

### Question 3
**What is the purpose of the `finally` block?**

A) It runs only if an exception occurs  
B) It runs only if no exception occurs  
C) It always runs, whether or not an exception occurs  
D) It runs only if the `else` block is executed  

**Difficulty:** Easy  

---

### Question 4
**What is the output of this code?**
```python
try:
    x = int("abc")
except ValueError as e:
    print(f"Error: {e}")
```

A) Error: invalid literal for int() with base 10: 'abc'  
B) abc  
C) Error  
D) None  

**Difficulty:** Easy  

---

### Question 5
**What is the difference between `except` and `except Exception as e`?**

A) They are the same  
B) `except` catches all exceptions, `except Exception as e` catches specific exceptions  
C) `except Exception as e` catches all exceptions, `except` catches specific exceptions  
D) `except` is deprecated, `except Exception as e` is the modern way  

**Difficulty:** Medium  

---

### Question 6
**What is the output of this code?**
```python
try:
    x = 10 / 0
except ZeroDivisionError:
    print("Caught exception")
else:
    print("No exception")
finally:
    print("Finally block")
```

A) Caught exception Finally block  
B) No exception Finally block  
C) Caught exception No exception Finally block  
D) Error  

**Difficulty:** Medium  

---

### Question 7
**What is a custom exception?**

A) An exception defined by the Python interpreter  
B) An exception created by the user to handle specific error conditions  
C) An exception that cannot be caught  
D) An exception that only works in certain Python versions  

**Difficulty:** Easy  

---

### Question 8
**What is the output of this code?**
```python
class CustomError(Exception):
    pass

try:
    raise CustomError("Custom error occurred")
except CustomError as e:
    print(e)
```

A) CustomError  
B) Custom error occurred  
C) Error  
D) None  

**Difficulty:** Medium  

---

### Question 9
**What is a context manager?**

A) A way to manage database connections  
B) An object that defines methods for `with` statement (enter and exit)  
C) A type of exception  
D) A way to manage global variables  

**Difficulty:** Medium  

---

### Question 10
**What is the output of this code?**
```python
with open("nonexistent.txt", "r") as file:
    content = file.read()
```

A) FileNotFoundError  
B) The file is read successfully  
C) Error but no exception is raised  
D) None  

**Difficulty:** Easy  

---

### Question 11
**What is the purpose of the `else` block in try/except?**

A) It runs if an exception occurs  
B) It runs if no exception occurs in the try block  
C) It runs after the finally block  
D) It runs before the try block  

**Difficulty:** Medium  

---

### Question 12
**What is the output of this code?**
```python
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
    else:
        return result

print(divide(10, 2))
```

A) 5  
B) Cannot divide by zero  
C) Error  
D) None  

**Difficulty:** Medium  

---

### Question 13
**What is the hierarchy of exceptions in Python?**

A) All exceptions inherit from `Exception`  
B) All exceptions inherit from `BaseException`  
C) Only some exceptions inherit from `Exception`  
D) There is no hierarchy  

**Difficulty:** Medium  

---

### Question 14
**What is the output of this code?**
```python
try:
    x = [1, 2, 3]
    print(x[5])
except IndexError as e:
    print(f"Index error: {e}")
except Exception as e:
    print(f"Other error: {e}")
```

A) Index error: list index out of range  
B) Other error: list index out of range  
C) Error  
D) None  

**Difficulty:** Medium  

---

### Question 15
**What is the purpose of `raise` keyword?**

A) To catch exceptions  
B) To manually trigger an exception  
C) To define custom exceptions  
D) To ignore exceptions  

**Difficulty:** Easy  

---

### Question 16
**What is the output of this code?**
```python
class MyContextManager:
    def __enter__(self):
        print("Entering context")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting context")
        return False

with MyContextManager() as cm:
    print("Inside context")
```

A) Entering context Inside context Exiting context  
B) Inside context Entering context Exiting context  
C) Error  
D) None  

**Difficulty:** Hard  

---

### Question 17
**What is the output of this code?**
```python
try:
    x = 10
    y = 0
    result = x / y
finally:
    print("Finally executed")
```

A) Finally executed  
B) Error  
C) Finally executed after error  
D) None  

**Difficulty:** Medium  

---

### Question 18
**What is the purpose of `__exit__` method in context managers?**

A) To initialize the context  
B) To clean up resources when exiting the context  
C) To handle exceptions  
D) To create the context  

**Difficulty:** Medium  

---

### Question 19
**What is the output of this code?**
```python
def risky_operation():
    raise ValueError("Operation failed")

try:
    risky_operation()
except ValueError as e:
    print(f"Caught: {e}")
else:
    print("No exception")
```

A) Caught: Operation failed  
B) No exception  
C) Error  
D) None  

**Difficulty:** Easy  

---

### Question 20
**What is the benefit of using context managers?**

A) They make code run faster  
B) They ensure resources are properly cleaned up  
C) They prevent all exceptions  
D) They simplify syntax  

**Difficulty:** Easy  

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! You have a strong grasp of error handling.
- 14-17: Good job! Review the concepts you missed.
- 10-13: Fair. Consider revisiting error handling fundamentals.
- Below 10: Keep practicing! Review the error handling material.

---

## Answer Key

1. **B) An error in the structure of the code that prevents it from running** - Syntax errors are detected before the code runs and must be fixed.

2. **C) Cannot divide by zero** - The `except ZeroDivisionError` catches the division by zero error.

3. **C) It always runs, whether or not an exception occurs** - The `finally` block is always executed, even if an exception occurs.

4. **A) Error: invalid literal for int() with base 10: 'abc'** - The `ValueError` is caught and the error message is printed.

5. **B) `except` catches all exceptions, `except Exception as e` catches specific exceptions** - Both can catch exceptions, but `as e` gives access to the exception object.

6. **A) Caught exception Finally block** - The exception occurs, so `except` runs, `else` is skipped, and `finally` runs.

7. **B) An exception created by the user to handle specific error conditions** - Custom exceptions let you define error types specific to your application.

8. **B) Custom error occurred** - The custom exception is raised and caught, printing its message.

9. **B) An object that defines methods for `with` statement (enter and exit)** - Context managers define `__enter__` and `__exit__` methods.

10. **A) FileNotFoundError** - The file doesn't exist, so a `FileNotFoundError` is raised.

11. **B) It runs if no exception occurs in the try block** - The `else` block is for code that should run only if no exception occurred.

12. **A) 5** - No exception occurs, so the `else` block runs and returns the result.

13. **B) All exceptions inherit from `BaseException`** - `BaseException` is the root of the exception hierarchy.

14. **A) Index error: list index out of range** - The more specific `IndexError` is caught first.

15. **B) To manually trigger an exception** - `raise` lets you explicitly throw an exception.

16. **A) Entering context Inside context Exiting context** - The `__enter__` method runs first, then the code inside `with`, then `__exit__`.

17. **A) Finally executed** - The `finally` block runs even when an exception occurs.

18. **B) To clean up resources when exiting the context** - `__exit__` handles cleanup (closing files, connections, etc.).

19. **A) Caught: Operation failed** - The exception is raised and caught, printing the error message.

20. **B) They ensure resources are properly cleaned up** - Context managers guarantee that resources like files and connections are closed.

---

*Quiz completed! How did you score?* 🎯