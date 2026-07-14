# Python Dictionaries Quiz

## Topic Overview
This quiz covers Python dictionary operations including dictionary comprehensions, common patterns, and nested dictionaries. Test your understanding of how to work with dictionaries effectively in Python.

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
my_dict = {"name": "Alice", "age": 25}
print(my_dict["name"])
```

A) Alice  
B) name  
C) 25  
D) Error  

**Difficulty:** Easy  

---

### Question 2
**How do you add a new key-value pair to a dictionary?**

A) add()  
B) insert()  
C) my_dict[key] = value  
D) append()  

**Difficulty:** Easy  

---

### Question 3
**What is the output of this code?**
```python
my_dict = {"a": 1, "b": 2, "c": 3}
print(len(my_dict))
```

A) 2  
B) 3  
C) 6  
D) Error  

**Difficulty:** Easy  

---

### Question 4
**What is the output of this code?**
```python
my_dict = {"a": 1, "b": 2, "c": 3}
del my_dict["b"]
print(my_dict)
```

A) {"a": 1, "c": 3}  
B) {"a": 1, "b": 2}  
C) {"b": 2, "c": 3}  
D) Error  

**Difficulty:** Easy  

---

### Question 5
**What is the output of this code?**
```python
my_dict = {"name": "Alice", "age": 25}
print("name" in my_dict)
```

A) Alice  
B) True  
C) False  
D) Error  

**Difficulty:** Easy  

---

### Question 6
**What is the output of this code?**
```python
my_dict = {"a": 1, "b": 2, "c": 3}
print(my_dict.keys())
```

A) [1, 2, 3]  
B) ["a", "b", "c"]  
C) dict_keys(["a", "b", "c"])  
D) Error  

**Difficulty:** Easy  

---

### Question 7
**What is the output of this code?**
```python
my_dict = {"a": 1, "b": 2, "c": 3}
print(my_dict.values())
```

A) ["a", "b", "c"]  
B) [1, 2, 3]  
C) dict_values([1, 2, 3])  
D) Error  

**Difficulty:** Easy  

---

### Question 8
**What is the output of this code?**
```python
my_dict = {"a": 1, "b": 2, "c": 3}
print(my_dict.items())
```

A) [("a", 1), ("b", 2), ("c", 3)]  
B) dict_items([("a", 1), ("b", 2), ("c", 3)])  
C) ["a", "b", "c"]  
D) Error  

**Difficulty:** Easy  

---

### Question 9
**What is the output of this code?**
```python
my_dict = {"a": 1, "b": 2, "c": 3}
result = {v: k for k, v in my_dict.items()}
print(result)
```

A) {"a": 1, "b": 2, "c": 3}  
B) {1: "a", 2: "b", 3: "c"}  
C) ["a", "b", "c"]  
D) Error  

**Difficulty:** Medium  

---

### Question 10
**What is the output of this code?**
```python
my_dict = {"a": 1, "b": 2, "c": 3}
result = {k: v * 2 for k, v in my_dict.items()}
print(result)
```

A) {"a": 1, "b": 2, "c": 3}  
B) {"a": 2, "b": 4, "c": 6}  
C) {"a": 1, "b": 2, "c": 3, "a": 2, "b": 4, "c": 6}  
D) Error  

**Difficulty:** Medium  

---

### Question 11
**What is the output of this code?**
```python
my_dict = {"a": 1, "b": 2, "c": 3}
result = {k: v for k, v in my_dict.items() if v > 1}
print(result)
```

A) {"a": 1}  
B) {"b": 2, "c": 3}  
C) {"a": 1, "b": 2, "c": 3}  
D) Error  

**Difficulty:** Medium  

---

### Question 12
**What is the output of this code?**
```python
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}
result = {**dict1, **dict2}
print(result)
```

A) {"a": 1, "b": 2, "b": 3, "c": 4}  
B) {"a": 1, "b": 3, "c": 4}  
C) {"a": 1, "b": 2, "c": 4}  
D) Error  

**Difficulty:** Medium  

---

### Question 13
**What is the output of this code?**
```python
my_dict = {"name": "Alice", "age": 25}
print(my_dict.get("email", "Not found"))
```

A) None  
B) Error  
C) Not found  
D) ""  

**Difficulty:** Easy  

---

### Question 14
**What is the output of this code?**
```python
nested = {"person": {"name": "Alice", "age": 25}}
print(nested["person"]["name"])
```

A) Alice  
B) person  
C) name  
D) Error  

**Difficulty:** Easy  

---

### Question 15
**What is the output of this code?**
```python
my_dict = {"a": 1, "b": 2, "c": 3}
my_dict.update({"d": 4})
print(my_dict)
```

A) {"a": 1, "b": 2, "c": 3}  
B) {"a": 1, "b": 2, "c": 3, "d": 4}  
C) {"d": 4}  
D) Error  

**Difficulty:** Easy  

---

### Question 16
**What is the output of this code?**
```python
my_dict = {"a": 1, "b": 2, "c": 3}
result = my_dict.pop("b")
print(result)
print(my_dict)
```

A) 2 {"a": 1, "c": 3}  
B) {"a": 1, "c": 3} 2  
C) 2 {"a": 1, "b": 2, "c": 3}  
D) Error  

**Difficulty:** Medium  

---

### Question 17
**What is the time complexity of looking up a key in a dictionary?**

A) O(1)  
B) O(n)  
C) O(log n)  
D) O(n²)  

**Difficulty:** Medium  

---

### Question 18
**What is the output of this code?**
```python
my_dict = {"a": 1, "b": 2, "c": 3}
result = dict.fromkeys(["x", "y", "z"], 0)
print(result)
```

A) {"a": 1, "b": 2, "c": 3}  
B) {"x": 0, "y": 0, "z": 0}  
C) {"x": None, "y": None, "z": None}  
D) Error  

**Difficulty:** Medium  

---

### Question 19
**What is the output of this code?**
```python
my_dict = {"a": 1, "b": 2, "c": 3}
for key, value in my_dict.items():
    print(f"{key}: {value}", end=" ")
```

A) a: 1 b: 2 c: 3  
B) 1: a 2: b 3: c  
C) a b c 1 2 3  
D) Error  

**Difficulty:** Easy  

---

### Question 20
**What is the output of this code?**
```python
my_dict = {"a": 1, "b": 2, "c": 3}
result = {k: v for k, v in my_dict.items() if k != "b"}
print(result)
```

A) {"b": 2}  
B) {"a": 1, "c": 3}  
C) {"a": 1, "b": 2, "c": 3}  
D) Error  

**Difficulty:** Medium  

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! You have a strong grasp of dictionary operations.
- 14-17: Good job! Review the concepts you missed.
- 10-13: Fair. Consider revisiting dictionary fundamentals.
- Below 10: Keep practicing! Review the dictionaries material.

---

## Answer Key

1. **A) Alice** - Dictionary keys are used to access their corresponding values.

2. **C) my_dict[key] = value** - You can add or update key-value pairs using square bracket notation.

3. **B) 3** - `len()` returns the number of key-value pairs in the dictionary.

4. **A) {"a": 1, "c": 3}** - `del` removes the specified key-value pair.

5. **B) True** - The `in` operator checks if a key exists in the dictionary.

6. **C) dict_keys(["a", "b", "c"])** - `keys()` returns a view object containing the dictionary's keys.

7. **C) dict_values([1, 2, 3])** - `values()` returns a view object containing the dictionary's values.

8. **B) dict_items([("a", 1), ("b", 2), ("c", 3)])** - `items()` returns a view object containing (key, value) tuples.

9. **B) {1: "a", 2: "b", 3: "c"}** - The dictionary comprehension swaps keys and values.

10. **B) {"a": 2, "b": 4, "c": 6}** - The dictionary comprehension multiplies each value by 2.

11. **B) {"b": 2, "c": 3}** - The dictionary comprehension filters values greater than 1.

12. **B) {"a": 1, "b": 3, "c": 4}** - Dictionary unpacking merges dictionaries, with later values overwriting earlier ones.

13. **C) Not found** - `get()` returns the default value if the key doesn't exist.

14. **A) Alice** - Nested dictionaries can be accessed using multiple key lookups.

15. **B) {"a": 1, "b": 2, "c": 3, "d": 4}** - `update()` adds or updates key-value pairs.

16. **A) 2 {"a": 1, "c": 3}** - `pop()` removes the key and returns its value.

17. **A) O(1)** - Dictionary lookups are constant time due to hash table implementation.

18. **B) {"x": 0, "y": 0, "z": 0}** - `fromkeys()` creates a new dictionary with the specified keys and default value.

19. **A) a: 1 b: 2 c: 3** - The for loop iterates over key-value pairs.

20. **B) {"a": 1, "c": 3}** - The dictionary comprehension filters out the key "b".

---

*Quiz completed! How did you score?* 🎯