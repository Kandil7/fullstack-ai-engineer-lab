# Data Structures & Algorithms — Python Lectures

> A comprehensive collection of 20 lectures covering fundamental DSA concepts with Python implementations

## Overview

This directory contains 20 lectures on data structures and algorithms, each with:
- **Lecture file** (300-500 lines): Detailed explanations, code examples, and exercises
- **Glossary file** (200-400 lines): Quick reference, definitions, and related terms

## Learning Order

### Phase 1: Foundational Data Structures (Lectures 1-6)

| Lecture | Topic | Key Concepts |
|---------|-------|--------------|
| 01 | Introduction | Big O notation, algorithm analysis, Python basics |
| 02 | Arrays | Array operations, dynamic arrays, slicing |
| 03 | Stacks | LIFO, push/pop, applications |
| 04 | Queues | FIFO, enqueue/dequeue, circular queues |
| 05 | Linked Lists | Nodes, pointers, singly/doubly lists |
| 06 | Hash Tables | Hashing, collisions, dictionary operations |

### Phase 2: Tree Structures (Lectures 7-10)

| Lecture | Topic | Key Concepts |
|---------|-------|--------------|
| 07 | Trees | Tree terminology, traversals, representations |
| 08 | Binary Trees | Binary tree properties, traversals |
| 09 | Binary Search Trees | BST operations, search, insert, delete |
| 10 | AVL Trees | Self-balancing BSTs, rotations |

### Phase 3: Graph Algorithms (Lectures 11)

| Lecture | Topic | Key Concepts |
|---------|-------|--------------|
| 11 | Graphs | Graph representations, BFS, DFS |

### Phase 4: Search Algorithms (Lectures 12-13)

| Lecture | Topic | Key Concepts |
|---------|-------|--------------|
| 12 | Linear Search | Sequential search, O(n) complexity |
| 13 | Binary Search | Efficient search, O(log n) complexity |

### Phase 5: Sorting Algorithms (Lectures 14-20)

| Lecture | Topic | Key Concepts |
|---------|-------|--------------|
| 14 | Bubble Sort | Adjacent swaps, O(n²) complexity |
| 15 | Selection Sort | Minimum selection, O(n²) complexity |
| 16 | Insertion Sort | Insertion into sorted portion, adaptive |
| 17 | Quick Sort | Divide-and-conquer, pivot partitioning |
| 18 | Counting Sort | Non-comparison, frequency counting |
| 19 | Radix Sort | Digit-based sorting, LSD/MSD variants |
| 20 | Merge Sort | Divide-and-conquer, stable O(n log n) |

## Study Schedule

### Week 1: Foundations
- **Day 1-2:** Lecture 01 (Introduction)
- **Day 3-4:** Lectures 02-03 (Arrays, Stacks)
- **Day 5-6:** Lectures 04-05 (Queues, Linked Lists)
- **Day 7:** Lecture 06 (Hash Tables)

### Week 2: Trees
- **Day 1-2:** Lectures 07-08 (Trees, Binary Trees)
- **Day 3-4:** Lectures 09-10 (BST, AVL Trees)
- **Day 5:** Lecture 11 (Graphs)

### Week 3: Search Algorithms
- **Day 1-2:** Lectures 12-13 (Linear, Binary Search)
- **Day 3-4:** Lectures 14-15 (Bubble, Selection Sort)
- **Day 5-6:** Lecture 16 (Insertion Sort)
- **Day 7:** Lecture 17 (Quick Sort)

### Week 4: Advanced Sorting
- **Day 1-2:** Lectures 18-19 (Counting, Radix Sort)
- **Day 3-4:** Lecture 20 (Merge Sort)
- **Day 5-7:** Review and practice

## Complexity Quick Reference

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Linear Search | O(1) | O(n) | O(n) | O(1) | Yes |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) | Yes |
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Counting Sort | O(n + k) | O(n + k) | O(n + k) | O(n + k) | Yes |
| Radix Sort | O(d(n + b)) | O(d(n + b)) | O(d(n + b)) | O(n + b) | Yes |

## Prerequisites

- Python 3.8+ installed
- Basic Python knowledge (variables, loops, functions)
- Understanding of basic math (exponents, logarithms)
- Text editor or IDE

## How to Use These Lectures

1. **Follow the order:** Lectures build on each other
2. **Read the lecture:** Understand concepts and code examples
3. **Study the glossary:** Use for quick reference and review
4. **Complete exercises:** Practice is essential for mastery
5. **Implement from scratch:** Don't just copy—understand and recreate
6. **Test your code:** Verify implementations work correctly

## File Naming Convention

```
XX-topic-lecture.md    # Main lecture content
XX-topic-glossary.md  # Quick reference and definitions
```

Where `XX` is the lecture number (01-20).

## Additional Resources

- [Python Documentation](https://docs.python.org/)
- [Algorithm Visualizations](https://visualgo.net/)
- [Big O Cheat Sheet](https://www.bigocheatsheet.com/)
- [LeetCode Problems](https://leetcode.com/)
- [HackerRank](https://www.hackerrank.com/)

## Contributing

To add or modify lectures:
1. Follow the existing format and structure
2. Include code examples with comments
3. Add glossary entries for new terms
4. Test all code examples
5. Update this README if adding new lectures

## License

This educational content is provided for learning purposes. Use freely for study and reference.
