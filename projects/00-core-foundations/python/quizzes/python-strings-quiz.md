# Python Strings Quiz

## Topic Overview
This quiz covers Python string operations including string methods, string formatting, regular expressions, and string manipulation. Test your understanding of how to work with strings effectively in Python.

## Instructions
- Each question has 4 options (A, B, C, D)
- Select the best answer for each question
- Check your answers using the Answer Key at the end
- Track your score: 1 point per correct answer

---

## Questions

### Question 1
**What is the output of this code?**
```python
s = "Hello, World!"
print(s.lower())
```

A) HELLO, WORLD!  
B) hello, world!  
C) Hello, World!  
D) Error  

**Difficulty:** Easy  

---

### Question 2
**How do you create a multi-line string in Python?**

A) Using double quotes  
B) Using triple quotes  
C) Using backslashes  
D) Using parentheses  

**Difficulty:** Easy  

---

### Question 3
**What is the output of this code?**
```python
s = "Python"
print(s[1:4])
```

A) Pyt  
B)ytho  
C)yth  
D) Pyth  

**Difficulty:** Easy  

---

### Question 4
**Which method removes whitespace from both ends of a string?**

A) strip()  
B) trim()  
C) remove()  
D) clean()  

**Difficulty:** Easy  

---

### Question 5
**What is the output of this code?**
```python
name = "Alice"
age = 25
print(f"My name is {name} and I am {age} years old.")
```

A) My name is Alice and I am 25 years old.  
B) My name is {name} and I am {age} years old.  
C) Error  
D) My name is name and I am age years old.  

**Difficulty:** Easy  

---

### Question 6
**What is the output of this code?**
```python
s = "Hello World"
print(s.split())
```

A) ['H', 'e', 'l', 'l', 'o', 'W', 'o', 'r', 'l', 'd']  
B) ['Hello', 'World']  
C) ['Hello World']  
D) Error  

**Difficulty:** Easy  

---

### Question 7
**What is the output of this code?**
```python
s = "Python Programming"
print(s.find("Pro"))
```

A) 7  
B) 0  
C) -1  
D) Error  

**Difficulty:** Easy  

---

### Question 8
**What is the output of this code?**
```python
s = "hello"
print(s.replace("l", "r"))
```

A) herro  
B) helro  
C) herrro  
D) herro  

**Difficulty:** Easy  

---

### Question 9
**What is the difference between `split()` and `split(' ')`?**

A) They are the same  
B) `split()` splits by any whitespace, `split(' ')` splits by single space only  
C) `split(' ')` splits by any whitespace, `split()` splits by single space only  
D) `split()` doesn't exist, only `split(' ')` works  

**Difficulty:** Medium  

---

### Question 10
**What is the output of this code?**
```python
s = "12345"
print(s.isdigit())
```

A) True  
B) False  
C) 12345  
D) Error  

**Difficulty:** Easy  

---

### Question 11
**What is the output of this code?**
```python
s = "Hello"
print(s * 3)
```

A) HelloHelloHello  
B) Hello Hello Hello  
C) 3Hello  
D) Error  

**Difficulty:** Easy  

---

### Question 12
**What is the output of this code?**
```python
import re
text = "Hello 123 World 456"
numbers = re.findall(r'\d+', text)
print(numbers)
```

A) ['123', '456']  
B) [123, 456]  
C) Hello World  
D) Error  

**Difficulty:** Medium  

---

### Question 13
**What is the output of this code?**
```python
s = "Hello, World!"
print(s.count("l"))
```

A) 2  
B) 3  
C) 1  
D) Error  

**Difficulty:** Easy  

---

### Question 14
**What is the purpose of the `join()` method?**

A) To combine multiple strings into one  
B) To split a string into multiple parts  
C) To find a substring  
D) To replace characters  

**Difficulty:** Easy  

---

### Question 15
**What is the output of this code?**
```python
words = ["Hello", "World"]
result = " ".join(words)
print(result)
```

A) ['Hello', 'World']  
B) HelloWorld  
C) Hello World  
D) Error  

**Difficulty:** Easy  

---

### Question 16
**What is the output of this code?**
```python
s = "Python"
print(s[::-1])
```

A) Python  
B) nohtyP  
C) nohtyp  
D) Error  

**Difficulty:** Medium  

---

### Question 17
**What is the output of this code?**
```python
s = "hello world"
print(s.title())
```

A) hello world  
B) HELLO WORLD  
C) Hello World  
D) Error  

**Difficulty:** Easy  

---

### Question 18
**What is the output of this code?**
```python
s = "  Hello  "
print(s.strip())
```

A) Hello  
B)   Hello  
C) Hello   
D) Error  

**Difficulty:** Easy  

---

### Question 19
**What is the output of this code?**
```python
import re
text = "Hello World"
pattern = r"World"
match = re.search(pattern, text)
print(match.start())
```

A) 6  
B) 0  
C) 5  
D) Error  

**Difficulty:** Medium  

---

### Question 20
**What is the output of this code?**
```python
s = "abcabc"
print(s.index("bc"))
```

A) 1  
B) 3  
C) 4  
D) Error  

**Difficulty:** Easy  

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! You have a strong grasp of string operations.
- 14-17: Good job! Review the concepts you missed.
- 10-13: Fair. Consider revisiting string fundamentals.
- Below 10: Keep practicing! Review the strings material.

---

## Answer Key

1. **B) hello, world!** - The `lower()` method converts all characters to lowercase.

2. **B) Using triple quotes** - Triple quotes (""" or ''') allow multi-line strings.

3. **C) yth** - Slicing `s[1:4]` returns characters from index 1 to 3 (inclusive).

4. **A) strip()** - `strip()` removes whitespace from both ends of a string.

5. **A) My name is Alice and I am 25 years old.** - f-strings format variables directly in the string.

6. **B) ['Hello', 'World']** - `split()` splits by whitespace and returns a list.

7. **A) 7** - `find()` returns the index of the first occurrence of the substring.

8. **A) herro** - `replace()` replaces all occurrences of the specified character.

9. **B) `split()` splits by any whitespace, `split(' ')` splits by single space only** - `split()` handles tabs, newlines, and multiple spaces.

10. **A) True** - `isdigit()` returns True if all characters are digits.

11. **A) HelloHelloHello** - The `*` operator with strings repeats the string.

12. **A) ['123', '456']** - `re.findall()` returns all non-overlapping matches as a list of strings.

13. **B) 3** - The letter 'l' appears 3 times in "Hello, World!".

14. **A) To combine multiple strings into one** - `join()` concatenates strings with a separator.

15. **C) Hello World** - The separator " " joins the words with a space.

16. **B) nohtyP** - `[::-1]` reverses the string.

17. **C) Hello World** - `title()` capitalizes the first letter of each word.

18. **A) Hello** - `strip()` removes whitespace from both ends.

19. **A) 6** - `match.start()` returns the starting index of the match.

20. **A) 1** - `index()` returns the index of the first occurrence of the substring.

---

*Quiz completed! How did you score?* 🎯