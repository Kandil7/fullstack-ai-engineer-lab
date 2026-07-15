# Python Data Structures Quiz

## Topic Overview
This quiz covers Python's built-in data structures including lists, tuples, sets, and dictionaries. Test your understanding of when to use each data structure, common operations, and their time complexity characteristics.

## Instructions
- Each question has 4 options (A, B, C, D)
- Select the best answer for each question
- Check your answers using the Answer Key at the end
- Track your score: 1 point per correct answer

---

## Questions

### Question 1
**Which data structure is ordered and allows duplicate elements?**

A) Set  
B) Dictionary  
C) List  
D) All of the above  

**Difficulty:** Easy  

---

### Question 2
**What is the output of this code?**
```python
my_list = [1, 2, 3, 4, 5]
print(my_list[2])
```

A) 1  
B) 2  
C) 3  
D) 4  

**Difficulty:** Easy  

---

### Question 3
**What is the output of this code?**
```python
my_tuple = (1, 2, 3)
my_tuple[0] = 10
print(my_tuple)
```

A) (10, 2, 3)  
B) Error  
C) [10, 2, 3]  
D) (1, 2, 3)  

**Difficulty:** Easy  

---

### Question 4
**Which data structure is unordered and does not allow duplicate elements?**

A) List  
B) Tuple  
C) Set  
D) Dictionary  

**Difficulty:** Easy  

---

### Question 5
**What is the output of this code?**
```python
my_dict = {"a": 1, "b": 2, "c": 3}
print(my_dict["b"])
```

A) 1  
B) 2  
C) 3  
D) Error  

**Difficulty:** Easy  

---

### Question 6
**What is the time complexity of accessing an element by index in a list?**

A) O(1)  
B) O(n)  
C) O(log n)  
D) O(n²)  

**Difficulty:** Medium  

---

### Question 7
**What is the output of this code?**
```python
my_set = {1, 2, 3, 2, 1}
print(len(my_set))
```

A) 5  
B) 3  
C) Error  
D) 0  

**Difficulty:** Easy  

---

### Question 8
**Which of the following is immutable?**

A) List  
B) Dictionary  
C) Set  
D) Tuple  

**Difficulty:** Easy  

---

### Question 9
**What is the output of this code?**
```python
my_list = [1, 2, 3, 4, 5]
print(my_list[-2])
```

A) 4  
B) 5  
C) 2  
D) Error  

**Difficulty:** Easy  

---

### Question 10
**What is the time complexity of checking if an element exists in a set?**

A) O(1)  
B) O(n)  
C) O(log n)  
D) O(n²)  

**Difficulty:** Medium  

---

### Question 11
**What is the output of this code?**
```python
my_dict = {"a": 1, "b": 2}
my_dict["c"] = 3
print(my_dict)
```

A) {"a": 1, "b": 2}  
B) {"a": 1, "b": 2, "c": 3}  
C) Error  
D) None  

**Difficulty:** Easy  

---

### Question 12
**Which method removes the last element from a list?**

A) remove()  
B) pop()  
C) delete()  
D) clear()  

**Difficulty:** Easy  

---

### Question 13
**What is the output of this code?**
```python
set1 = {1, 2, 3}
set2 = {3, 4, 5}
print(set1 & set2)
```

A) {1, 2, 3, 4, 5}  
B) {3}  
C) {1, 2, 4, 5}  
D) Error  

**Difficulty:** Medium  

---

### Question 14
**What is the difference between a list and a tuple?**

A) Lists are faster than tuples  
B) Tuples are immutable, lists are mutable  
C) Lists can store different data types, tuples cannot  
D) There is no difference  

**Difficulty:** Medium  

---

### Question 15
**What is the output of this code?**
```python
my_list = [1, 2, 3, 4, 5]
my_list.insert(2, 10)
print(my_list)
```

A) [1, 2, 10, 3, 4, 5]  
B) [1, 10, 2, 3, 4, 5]  
C) [1, 2, 3, 10, 4, 5]  
D) [10, 1, 2, 3, 4, 5]  

**Difficulty:** Medium  

---

### Question 16
**What is the output of this code?**
```python
my_dict = {"a": 1, "b": 2, "c": 3}
print("a" in my_dict)
```

A) 1  
B) True  
C) False  
D) Error  

**Difficulty:** Easy  

---

### Question 17
**What is the time complexity of appending an element to the end of a list?**

A) O(1)  
B) O(n)  
C) O(log n)  
D) O(n²)  

**Difficulty:** Medium  

---

### Question 18
**Which data structure is best for counting occurrences of elements?**

A) List  
B) Tuple  
C) Set  
D) Dictionary  

**Difficulty:** Medium  

---

### Question 19
**What is the output of this code?**
```python
my_set = {1, 2, 3}
my_set.add(4)
my_set.add(2)
print(my_set)
```

A) {1, 2, 3, 4, 2}  
B) {1, 2, 3, 4}  
C) {2, 4}  
D) Error  

**Difficulty:** Medium  

---

### Question 20
**What is the output of this code?**
```python
my_list = [[1, 2], [3, 4], [5, 6]]
print(my_list[1][0])
```

A) 1  
B) 2  
C) 3  
D) 4  

**Difficulty:** Medium  

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! You have a strong grasp of data structures.
- 14-17: Good job! Review the concepts you missed.
- 10-13: Fair. Consider revisiting data structure fundamentals.
- Below 10: Keep practicing! Review the data structures material.

---

## Answer Key

1. **C) List** - Lists are ordered collections that allow duplicate elements.

2. **C) 3** - List indices start at 0, so index 2 returns the third element.

3. **B) Error** - Tuples are immutable, so you cannot modify their elements.

4. **C) Set** - Sets are unordered collections that automatically remove duplicates.

5. **B) 2** - Dictionary keys are used to access their corresponding values.

6. **A) O(1)** - List indexing uses array indexing, which is a constant-time operation.

7. **B) 3** - Sets automatically remove duplicates, so only 3 unique elements remain.

8. **D) Tuple** - Tuples are the only immutable data structure among the options.

9. **A) 4** - Negative indexing counts from the end. `[-2]` returns the second-to-last element.

10. **A) O(1)** - Set membership testing is a constant-time operation due to hash table implementation.

11. **B) {"a": 1, "b": 2, "c": 3}** - Dictionaries are mutable, so new key-value pairs can be added.

12. **B) pop()** - `pop()` removes and returns the last element (or element at specified index).

13. **B) {3}** - The `&` operator returns the intersection of two sets (common elements).

14. **B) Tuples are immutable, lists are mutable** - This is the primary difference between lists and tuples.

15. **A) [1, 2, 10, 3, 4, 5]** - `insert(2, 10)` inserts 10 at index 2, shifting other elements.

16. **B) True** - The `in` operator checks if a key exists in a dictionary.

17. **A) O(1)** - Appending to the end of a list is an amortized constant-time operation.

18. **D) Dictionary** - Dictionaries are ideal for counting occurrences using keys as elements and values as counts.

19. **B) {1, 2, 3, 4}** - Sets automatically handle duplicates, so adding 2 again has no effect.

20. **C) 3** - `my_list[1]` returns `[3, 4]`, and `[0]` returns the first element of that sublist.

---

*Quiz completed! How did you score?* 🎯