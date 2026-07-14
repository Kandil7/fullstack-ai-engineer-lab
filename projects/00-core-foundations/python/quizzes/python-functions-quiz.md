# Python Functions Quiz

## Topic Overview
This quiz covers Python functions including function definition, arguments and parameters, return values, scope, and lambda functions. Test your understanding of how functions work in Python and their various use cases.

## Instructions
- Each question has 4 options (A, B, C, D)
- Select the best answer for each question
- Check your answers using the Answer Key at the end
- Track your score: 1 point per correct answer

---

## Questions

### Question 1
**Which keyword is used to define a function in Python?**

A) function  
B) func  
C) def  
D) define  

**Difficulty:** Easy  

---

### Question 2
**What is the output of this code?**
```python
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))
```

A) Hello, Alice!  
B) name  
C) Error  
D) None  

**Difficulty:** Easy  

---

### Question 3
**What is the difference between a parameter and an argument?**

A) They are the same thing  
B) Parameters are variables in function definition, arguments are values passed to functions  
C) Arguments are variables in function definition, parameters are values passed to functions  
D) Parameters are only used in classes, arguments in functions  

**Difficulty:** Medium  

---

### Question 4
**What is the output of this code?**
```python
def add(a, b=5):
    return a + b

print(add(3))
```

A) 3  
B) 5  
C) 8  
D) Error  

**Difficulty:** Easy  

---

### Question 5
**What is the output of this code?**
```python
def modify_list(lst):
    lst.append(4)
    return lst

my_list = [1, 2, 3]
result = modify_list(my_list)
print(my_list)
```

A) [1, 2, 3]  
B) [1, 2, 3, 4]  
C) Error  
D) [4, 1, 2, 3]  

**Difficulty:** Medium  

---

### Question 6
**What is a lambda function?**

A) A function that runs asynchronously  
B) An anonymous, single-line function  
C) A function that can only be called once  
D) A function that returns a lambda  

**Difficulty:** Easy  

---

### Question 7
**What is the output of this code?**
```python
square = lambda x: x ** 2
print(square(5))
```

A) 5  
B) 10  
C) 25  
D) Error  

**Difficulty:** Easy  

---

### Question 8
**What is the scope of a variable defined inside a function?**

A) Global  
B) Local to the function  
C) Module scope  
D) Class scope  

**Difficulty:** Easy  

---

### Question 9
**What is the output of this code?**
```python
def func(x):
    global y
    y = x * 2
    return y

result = func(5)
print(y)
```

A) 5  
B) 10  
C) Error  
D) None  

**Difficulty:** Medium  

---

### Question 10
**What is the output of this code?**
```python
def func(*args):
    return sum(args)

print(func(1, 2, 3, 4))
```

A) 1  
B) 10  
C) (1, 2, 3, 4)  
D) Error  

**Difficulty:** Medium  

---

### Question 11
**What is the output of this code?**
```python
def func(**kwargs):
    return kwargs

result = func(a=1, b=2)
print(result)
```

A) (1, 2)  
B) {"a": 1, "b": 2}  
C) Error  
D) None  

**Difficulty:** Medium  

---

### Question 12
**What is the output of this code?**
```python
def outer():
    x = 10
    def inner():
        return x
    return inner()

print(outer())
```

A) 10  
B) Error  
C) None  
D) inner  

**Difficulty:** Medium  

---

### Question 13
**What is a decorator in Python?**

A) A function that adds functionality to another function  
B) A comment that explains the code  
C) A type of loop  
D) A class method  

**Difficulty:** Medium  

---

### Question 14
**What is the output of this code?**
```python
def apply(func, x):
    return func(x)

def double(x):
    return x * 2

print(apply(double, 5))
```

A) 5  
B) 10  
C) Error  
D) double  

**Difficulty:** Medium  

---

### Question 15
**What is the output of this code?**
```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

print(factorial(5))
```

A) 5  
B) 25  
C) 120  
D) Error  

**Difficulty:** Medium  

---

### Question 16
**What is the difference between `return` and `print` in a function?**

A) They are the same  
B) `return` sends a value back to the caller, `print` displays output  
C) `print` sends a value back, `return` displays output  
D) `return` can only be used once, `print` can be used multiple times  

**Difficulty:** Medium  

---

### Question 17
**What is the output of this code?**
```python
def func(a, b, c):
    return a + b + c

result = func(1, c=3, b=2)
print(result)
```

A) 6  
B) Error  
C) 1  
D) (1, 2, 3)  

**Difficulty:** Medium  

---

### Question 18
**What is the output of this code?**
```python
def func():
    pass

print(func())
```

A) None  
B) Error  
C) pass  
D) 0  

**Difficulty:** Easy  

---

### Question 19
**What is the purpose of the `*args` parameter?**

A) To accept a fixed number of arguments  
B) To accept any number of positional arguments  
C) To accept keyword arguments only  
D) To accept no arguments  

**Difficulty:** Medium  

---

### Question 20
**What is the output of this code?**
```python
def func(x):
    return lambda y: x + y

add5 = func(5)
print(add5(3))
```

A) 5  
B) 3  
C) 8  
D) Error  

**Difficulty:** Hard  

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! You have a strong grasp of Python functions.
- 14-17: Good job! Review the concepts you missed.
- 10-13: Fair. Consider revisiting function fundamentals.
- Below 10: Keep practicing! Review the functions material.

---

## Answer Key

1. **C) def** - The `def` keyword is used to define functions in Python.

2. **A) Hello, Alice!** - The function returns a formatted string with the provided name.

3. **B) Parameters are variables in function definition, arguments are values passed to functions** - Parameters are placeholders in the function definition, arguments are the actual values passed.

4. **C) 8** - The default value for `b` is 5, so `add(3)` returns `3 + 5 = 8`.

5. **B) [1, 2, 3, 4]** - Lists are mutable, so changes inside the function affect the original list.

6. **B) An anonymous, single-line function** - Lambda functions are small, anonymous functions defined with the `lambda` keyword.

7. **C) 25** - The lambda function squares its input: `5 ** 2 = 25`.

8. **B) Local to the function** - Variables defined inside a function have local scope.

9. **B) 10** - The `global` keyword makes `y` accessible outside the function.

10. **B) 10** - `*args` collects all positional arguments into a tuple, and `sum()` adds them.

11. **B) {"a": 1, "b": 2}** - `**kwargs` collects keyword arguments into a dictionary.

12. **A) 10** - The inner function can access variables from the outer function's scope (closure).

13. **A) A function that adds functionality to another function** - Decorators modify or enhance other functions.

14. **B) 10** - Functions can be passed as arguments to other functions. `apply(double, 5)` calls `double(5)`.

15. **C) 120** - Factorial of 5 is `5 × 4 × 3 × 2 × 1 = 120`.

16. **B) `return` sends a value back to the caller, `print` displays output** - `return` exits the function and sends a value back, `print` just displays to console.

17. **A) 6** - Keyword arguments can be passed in any order, so `func(1, c=3, b=2)` is equivalent to `func(1, 2, 3)`.

18. **A) None** - Functions without an explicit `return` statement return `None`.

19. **B) To accept any number of positional arguments** - `*args` allows a function to accept any number of positional arguments.

20. **C) 8** - The function returns a lambda that adds 5 to its argument: `5 + 3 = 8`.

---

*Quiz completed! How did you score?* 🎯