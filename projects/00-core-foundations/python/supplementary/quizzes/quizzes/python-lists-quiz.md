# Python Lists Quiz

## Topic Overview
This quiz covers Python list operations including list comprehensions, slicing, and common algorithms. Test your understanding of how to work with lists effectively in Python.

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
my_list = [1, 2, 3, 4, 5]
print(my_list[0])
```

A) 1  
B) 2  
C) 5  
D) Error  

**Difficulty:** Easy  

---

### Question 2
**What is the output of this code?**
```python
my_list = [1, 2, 3, 4, 5]
print(len(my_list))
```

A) 4  
B) 5  
C) 6  
D) Error  

**Difficulty:** Easy  

---

### Question 3
**How do you add an element to the end of a list?**

A) add()  
B) insert()  
C) append()  
D) push()  

**Difficulty:** Easy  

---

### Question 4
**What is the output of this code?**
```python
my_list = [1, 2, 3, 4, 5]
my_list.append(6)
print(my_list)
```

A) [1, 2, 3, 4, 5]  
B) [1, 2, 3, 4, 5, 6]  
C) [6, 1, 2, 3, 4, 5]  
D) Error  

**Difficulty:** Easy  

---

### Question 5
**What is the output of this code?**
```python
my_list = [1, 2, 3, 4, 5]
print(my_list[1:4])
```

A) [1, 2, 3, 4]  
B) [2, 3, 4]  
C) [2, 3, 4, 5]  
D) [1, 2, 3]  

**Difficulty:** Easy  

---

### Question 6
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

### Question 7
**What is the output of this code?**
```python
my_list = [1, 2, 3, 4, 5]
my_list.remove(3)
print(my_list)
```

A) [1, 2, 4, 5]  
B) [1, 2, 3, 5]  
C) [1, 2, 4]  
D) Error  

**Difficulty:** Easy  

---

### Question 8
**What is the output of this code?**
```python
my_list = [3, 1, 4, 1, 5, 9, 2, 6]
my_list.sort()
print(my_list)
```

A) [9, 6, 5, 4, 3, 2, 1, 1]  
B) [1, 1, 2, 3, 4, 5, 6, 9]  
C) [3, 1, 4, 1, 5, 9, 2, 6]  
D) Error  

**Difficulty:** Easy  

---

### Question 9
**What is the output of this code?**
```python
my_list = [1, 2, 3, 4, 5]
result = [x * 2 for x in my_list]
print(result)
```

A) [1, 2, 3, 4, 5]  
B) [2, 4, 6, 8, 10]  
C) [1, 4, 9, 16, 25]  
D) Error  

**Difficulty:** Medium  

---

### Question 10
**What is a list comprehension?**

A) A way to compress a list  
B) A concise way to create lists based on existing lists  
C) A way to sort a list  
D) A way to merge lists  

**Difficulty:** Easy  

---

### Question 11
**What is the output of this code?**
```python
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = [x for x in my_list if x % 2 == 0]
print(result)
```

A) [1, 3, 5, 7, 9]  
B) [2, 4, 6, 8, 10]  
C) [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  
D) Error  

**Difficulty:** Medium  

---

### Question 12
**What is the output of this code?**
```python
my_list = [1, 2, 3, 4, 5]
print(my_list[-1])
```

A) 1  
B) 5  
C) 0  
D) Error  

**Difficulty:** Easy  

---

### Question 13
**What is the output of this code?**
```python
my_list = [1, 2, 3, 4, 5]
my_list.reverse()
print(my_list)
```

A) [1, 2, 3, 4, 5]  
B) [5, 4, 3, 2, 1]  
C) [1, 2, 3, 4]  
D) Error  

**Difficulty:** Easy  

---

### Question 14
**What is the output of this code?**
```python
list1 = [1, 2, 3]
list2 = [4, 5, 6]
result = list1 + list2
print(result)
```

A) [1, 2, 3, 4, 5, 6]  
B) [1, 2, 3] + [4, 5, 6]  
C) [5, 7, 9]  
D) Error  

**Difficulty:** Easy  

---

### Question 15
**What is the output of this code?**
```python
my_list = [1, 2, 3, 2, 1]
print(my_list.count(2))
```

A) 1  
B) 2  
C) 3  
D) Error  

**Difficulty:** Easy  

---

### Question 16
**What is the output of this code?**
```python
my_list = [1, 2, 3, 4, 5]
print(my_list[::2])
```

A) [1, 2, 3, 4, 5]  
B) [2, 4]  
C) [1, 3, 5]  
D) [1, 2, 3, 4]  

**Difficulty:** Medium  

---

### Question 17
**What is the time complexity of checking if an element exists in a list?**

A) O(1)  
B) O(n)  
C) O(log n)  
D) O(n²)  

**Difficulty:** Medium  

---

### Question 18
**What is the output of this code?**
```python
my_list = [1, 2, 3, 4, 5]
result = list(map(lambda x: x ** 2, my_list))
print(result)
```

A) [1, 2, 3, 4, 5]  
B) [2, 4, 6, 8, 10]  
C) [1, 4, 9, 16, 25]  
D) Error  

**Difficulty:** Medium  

---

### Question 19
**What is the output of this code?**
```python
my_list = [1, 2, 3, 4, 5]
result = list(filter(lambda x: x > 3, my_list))
print(result)
```

A) [1, 2, 3]  
B) [4, 5]  
C) [1, 2, 3, 4, 5]  
D) Error  

**Difficulty:** Medium  

---

### Question 20
**What is the output of this code?**
```python
nested = [[1, 2], [3, 4], [5, 6]]
result = [item for sublist in nested for item in sublist]
print(result)
```

A) [[1, 2], [3, 4], [5, 6]]  
B) [1, 2, 3, 4, 5, 6]  
C) [1, 3, 5, 2, 4, 6]  
D) Error  

**Difficulty:** Hard  

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! You have a strong grasp of list operations.
- 14-17: Good job! Review the concepts you missed.
- 10-13: Fair. Consider revisiting list fundamentals.
- Below 10: Keep practicing! Review the lists material.

---

## Answer Key

1. **A) 1** - List indices start at 0, so `my_list[0]` returns the first element.

2. **B) 5** - `len()` returns the number of elements in the list.

3. **C) append()** - `append()` adds an element to the end of a list.

4. **B) [1, 2, 3, 4, 5, 6]** - `append()` adds the element to the end of the list.

5. **B) [2, 3, 4]** - Slicing `my_list[1:4]` returns elements from index 1 to 3 (inclusive).

6. **A) [1, 2, 10, 3, 4, 5]** - `insert(2, 10)` inserts 10 at index 2, shifting other elements.

7. **A) [1, 2, 4, 5]** - `remove(3)` removes the first occurrence of 3.

8. **B) [1, 1, 2, 3, 4, 5, 6, 9]** - `sort()` sorts the list in ascending order.

9. **B) [2, 4, 6, 8, 10]** - The list comprehension multiplies each element by 2.

10. **B) A concise way to create lists based on existing lists** - List comprehensions provide a concise syntax for creating lists.

11. **B) [2, 4, 6, 8, 10]** - The list comprehension filters even numbers.

12. **B) 5** - Negative indexing counts from the end. `[-1]` returns the last element.

13. **B) [5, 4, 3, 2, 1]** - `reverse()` reverses the list in place.

14. **A) [1, 2, 3, 4, 5, 6]** - The `+` operator concatenates two lists.

15. **B) 2** - `count(2)` returns the number of times 2 appears in the list.

16. **C) [1, 3, 5]** - `::2` means take every 2nd element starting from index 0.

17. **B) O(n)** - Checking membership in a list requires scanning through all elements.

18. **C) [1, 4, 9, 16, 25]** - `map()` applies the lambda function to each element.

19. **B) [4, 5]** - `filter()` keeps only elements where the lambda returns True.

20. **B) [1, 2, 3, 4, 5, 6]** - The nested list comprehension flattens the nested list.

---

*Quiz completed! How did you score?* 🎯