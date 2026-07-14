# Python Basics Quiz

## Topic Overview
This quiz covers fundamental Python concepts including variables and data types, operators, control flow, input/output operations, and basic syntax rules. Test your understanding of Python's core building blocks.

## Instructions
- Each question has 4 options (A, B, C, D)
- Select the best answer for each question
- Check your answers using the Answer Key at the end
- Track your score: 1 point per correct answer

---

## Questions

### Question 1
**What is the output of the following code?**
```python
x = 5
y = 2
print(x // y)
```

A) 2.5  
B) 2  
C) 3  
D) 2.0  

**Difficulty:** Easy  

---

### Question 2
**Which of the following is a valid variable name in Python?**

A) 2name  
B) my-var  
C) _private_var  
D) class  

**Difficulty:** Easy  

---

### Question 3
**What data type is the result of: `type(3.14)`?**

A) int  
B) float  
C) decimal  
D) double  

**Difficulty:** Easy  

---

### Question 4
**What is the output of: `print("Hello" * 3)`?**

A) HelloHelloHello  
B) Hello Hello Hello  
C) 3Hello  
D) Error  

**Difficulty:** Easy  

---

### Question 5
**Which operator is used for exponentiation in Python?**

A) ^  
B) **  
C) //  
D) %%  

**Difficulty:** Medium  

---

### Question 6
**What is the output of this code?**
```python
x = [1, 2, 3]
y = x
y.append(4)
print(x)
```

A) [1, 2, 3]  
B) [1, 2, 3, 4]  
C) Error  
D) [4, 1, 2, 3]  

**Difficulty:** Medium  

---

### Question 7
**Which of the following is NOT a valid Boolean value in Python?**

A) True  
B) False  
C) true  
D) None  

**Difficulty:** Easy  

---

### Question 8
**What is the output of: `print(type(True))`?**

A) bool  
B) int  
C) str  
D) boolean  

**Difficulty:** Easy  

---

### Question 9
**What will be the output of:**
```python
for i in range(5):
    if i == 3:
        break
    print(i, end=" ")
```

A) 0 1 2 3  
B) 0 1 2  
C) 0 1 2 3 4  
D) 3  

**Difficulty:** Medium  

---

### Question 10
**What is the output of:**
```python
x = "10"
y = 20
print(x + str(y))
```

A) 30  
B) 1020  
C) Error  
D) 10 20  

**Difficulty:** Medium  

---

### Question 11
**Which of the following is an immutable data type?**

A) list  
B) dictionary  
C) set  
D) tuple  

**Difficulty:** Medium  

---

### Question 12
**What is the output of: `print(0.1 + 0.2 == 0.3)`?**

A) True  
B) False  
C) Error  
D) 0.3  

**Difficulty:** Hard  

---

### Question 13
**What does the `is` operator check?**

A) Value equality  
B) Identity (same object in memory)  
C) Type equality  
D) Both value and type  

**Difficulty:** Medium  

---

### Question 14
**What is the output of:**
```python
x = None
print(type(x))
```

A) null  
B) NoneType  
C) void  
D) object  

**Difficulty:** Easy  

---

### Question 15
**Which statement is used to skip the current iteration in a loop?**

A) skip  
B) continue  
C) pass  
D) next  

**Difficulty:** Easy  

---

### Question 16
**What is the output of: `print(10 % 3)`?**

A) 3  
B) 1  
C) 3.33  
D) 0  

**Difficulty:** Easy  

---

### Question 17
**What is the correct way to take integer input from the user?**

A) `x = input("Enter: ")`  
B) `x = int(input("Enter: "))`  
C) `x = integer(input("Enter: "))`  
D) `x = input(int("Enter: "))`  

**Difficulty:** Easy  

---

### Question 18
**What is the output of:**
```python
x = [1, 2, 3, 4, 5]
print(x[1:4])
```

A) [1, 2, 3, 4]  
B) [2, 3, 4]  
C) [2, 3, 4, 5]  
D) [1, 2, 3]  

**Difficulty:** Medium  

---

### Question 19
**Which keyword is used to define a function in Python?**

A) function  
B) func  
C) def  
D) define  

**Difficulty:** Easy  

---

### Question 20
**What is the output of:**
```python
x = "Python"
print(x[-1])
```

A) P  
B) n  
C) nohtyP  
D) Error  

**Difficulty:** Easy  

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! You have a strong grasp of Python basics.
- 14-17: Good job! Review the concepts you missed.
- 10-13: Fair. Consider revisiting the fundamentals.
- Below 10: Keep practicing! Review the Python basics material.

---

## Answer Key

1. **B) 2** - The `//` operator performs floor division, which returns the largest integer less than or equal to the division result.

2. **C) _private_var** - Variable names can start with letters or underscores, but not numbers or special characters like hyphens. `class` is a reserved keyword.

3. **B) float** - Decimal numbers with a point are of type `float` in Python.

4. **A) HelloHelloHello** - The `*` operator with strings performs repetition.

5. **B) ** - Python uses `**` for exponentiation. `^` is the XOR operator.

6. **B) [1, 2, 3, 4]** - Lists are mutable, and `y = x` creates a reference to the same list object.

7. **C) true** - Python is case-sensitive. The Boolean values are `True` and `False` (capitalized).

8. **A) bool** - `True` is a Boolean value, so `type(True)` returns `<class 'bool'>`.

9. **B) 0 1 2** - The loop prints 0, 1, 2, then when `i == 3`, the `break` statement exits the loop.

10. **B) 1020** - String concatenation converts the integer to a string and joins them.

11. **D) tuple** - Tuples are immutable. Lists, dictionaries, and sets are mutable.

12. **B) False** - Due to floating-point precision issues, `0.1 + 0.2` doesn't exactly equal `0.3`.

13. **B) Identity (same object in memory)** - `is` checks if two variables point to the same object, while `==` checks value equality.

14. **B) NoneType** - `None` is of type `NoneType`.

15. **B) continue** - The `continue` statement skips the rest of the current loop iteration and moves to the next iteration.

16. **B) 1** - The `%` operator returns the remainder of division. 10 divided by 3 is 3 with remainder 1.

17. **B) `x = int(input("Enter: "))`** - `input()` returns a string, which must be converted to an integer using `int()`.

18. **B) [2, 3, 4]** - Slicing `x[1:4]` returns elements from index 1 to 3 (inclusive).

19. **C) def** - The `def` keyword is used to define functions in Python.

20. **B) n** - Negative indexing counts from the end. `x[-1]` returns the last character.

---

*Quiz completed! How did you score?* 🎯