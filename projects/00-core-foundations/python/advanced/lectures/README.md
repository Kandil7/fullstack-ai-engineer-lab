# Advanced Python Lectures (Topics 11-20)

A comprehensive collection of lecture notes and glossaries covering advanced Python topics 11-20, designed to provide deep understanding of Python's powerful features and patterns.

---

## 📚 What This Directory Contains

This directory contains detailed lecture notes and glossary files for advanced Python topics 11-20. Each topic includes:

- **Lecture File** (`XX-topic-lecture.md`): Comprehensive explanations, code examples, best practices, and exercises
- **Glossary File** (`XX-topic-glossary.md`): Alphabetical definitions with examples and quick reference tables

---

## 📋 All Topics

| # | Lecture | Glossary | Topic | Description |
|---|---------|----------|-------|-------------|
| 11 | [Lecture](lectures/11-collections-lecture.md) | [Glossary](lectures/11-collections-glossary.md) | **Collections** | Counter, defaultdict, namedtuple, deque, ChainMap, OrderedDict |
| 12 | [Lecture](lectures/12-property-lecture.md) | [Glossary](lectures/12-property-glossary.md) | **Properties** | Getters, setters, caching, validation, computed values |
| 13 | [Lecture](lectures/13-slots-lecture.md) | [Glossary](lectures/13-slots-glossary.md) | **Slots** | Memory optimization, performance benchmarks, inheritance |
| 14 | [Lecture](lectures/14-metaclasses-lecture.md) | [Glossary](lectures/14-metaclasses-glossary.md) | **Metaclasses** | Custom metaclasses, registries, singletons, __new__ vs __init__ |
| 15 | [Lecture](lectures/15-descriptors-lecture.md) | [Glossary](lectures/15-descriptors-glossary.md) | **Descriptors** | __get__, __set__, validation, computed attributes, data vs non-data |
| 16 | [Lecture](lectures/16-threading-lecture.md) | [Glossary](lectures/16-threading-glossary.md) | **Threading** | Threads, locks, semaphores, thread pools, producer-consumer |
| 17 | [Lecture](lectures/17-multiprocessing-lecture.md) | [Glossary](lectures/17-multiprocessing-glossary.md) | **Multiprocessing** | Processes, pools, shared state, parallel computing, IPC |
| 18 | [Lecture](lectures/18-unit-testing-lecture.md) | [Glossary](lectures/18-unit-testing-glossary.md) | **Unit Testing** | unittest, mocking, fixtures, parameterized tests, TDD |
| 19 | [Lecture](lectures/19-logging-lecture.md) | [Glossary](lectures/19-logging-glossary.md) | **Logging** | Levels, handlers, formatters, hierarchy, application logging |
| 20 | [Lecture](lectures/20-patterns-lecture.md) | [Glossary](lectures/20-patterns-glossary.md) | **Design Patterns** | Singleton, Factory, Observer, Strategy, Adapter, Decorator |

---

## 🎯 Recommended Learning Order

### Phase 1: Data Structures & Attribute Control (Topics 11-15)
1. **11 - Collections** → Master specialized containers for efficient data operations
2. **12 - Properties** → Learn Pythonic attribute management with getters/setters
3. **13 - Slots** → Understand memory optimization techniques
4. **14 - Metaclasses** → Control class creation and behavior
5. **15 - Descriptors** → Deep dive into attribute access customization

### Phase 2: Concurrency & Parallelism (Topics 16-17)
6. **16 - Threading** → Concurrent execution for I/O-bound tasks
7. **17 - Multiprocessing** → True parallelism for CPU-bound tasks

### Phase 3: Quality & Architecture (Topics 18-20)
8. **18 - Unit Testing** → Testing best practices and mocking
9. **19 - Logging** → Production-ready application logging
10. **20 - Design Patterns** → Reusable solutions to common problems

---

## 📖 How to Use Lectures + Glossaries Together

### For Each Topic:

1. **Read the Lecture First**
   - Start with the topic overview and learning objectives
   - Work through key concepts with code examples
   - Study common mistakes to avoid

2. **Use the Glossary as Reference**
   - Look up unfamiliar terms while reading the lecture
   - Use the quick reference table for rapid review
   - Review code examples for each term

3. **Practice the Exercises**
   - Complete all practice exercises in the lecture
   - Try extending the examples with your own variations
   - Compare your solutions with the provided examples

4. **Review Before Moving On**
   - Re-read the glossary quick reference table
   - Ensure you understand all terms before progressing
   - Mark any areas needing further study

---

## 📅 Study Schedule

### Option 1: Intensive (2 weeks)
| Week | Days | Topics |
|------|------|--------|
| 1 | Mon-Wed | Topics 11-13 (Collections, Properties, Slots) |
| 1 | Thu-Fri | Topics 14-15 (Metaclasses, Descriptors) |
| 2 | Mon-Wed | Topics 16-17 (Threading, Multiprocessing) |
| 2 | Thu-Fri | Topics 18-20 (Testing, Logging, Patterns) |

### Option 2: Standard (4 weeks)
| Week | Days | Topics |
|------|------|--------|
| 1 | Mon, Wed, Fri | Topics 11-12 (Collections, Properties) |
| 2 | Mon, Wed, Fri | Topics 13-14 (Slots, Metaclasses) |
| 3 | Mon, Wed, Fri | Topics 15-17 (Descriptors, Threading, Multiprocessing) |
| 4 | Mon, Wed, Fri | Topics 18-20 (Testing, Logging, Patterns) |

### Option 3: Relaxed (8 weeks)
- One topic per week
- Spend extra time on exercises and practice
- Review previous topics regularly

---

## 📋 Prerequisites

Before starting these lectures, you should be familiar with:

### Required Knowledge (Topics 1-10)
- **Decorators**: Function and class decorators
- **Generators**: yield, generator expressions, pipelines
- **Context Managers**: with statement, contextlib
- **Async/Await**: Basic asyncio concepts
- **Type Hints**: Annotations, generics
- **Dataclasses**: Field definitions, frozen classes
- **Enums**: Basic enum usage
- **ABCs**: Abstract base classes, interfaces
- **Functools**: reduce, partial, lru_cache
- **Itertools**: chain, groupby, combinations

### Python Fundamentals
- Object-oriented programming (classes, inheritance, polymorphism)
- Functions and closures
- Exception handling
- List comprehensions and generator expressions
- Basic understanding of the Python data model

### Development Environment
- Python 3.7+ installed
- Text editor or IDE
- Terminal/command line access

---

## 🎓 Learning Objectives

By completing all 10 topics (11-20), you will be able to:

### Data Structures & Attributes
- Use specialized collection types for efficient data operations
- Implement properties for controlled attribute access
- Optimize memory usage with __slots__
- Control class creation with metaclasses
- Build custom descriptors for attribute validation

### Concurrency
- Write thread-safe code with locks and semaphores
- Implement producer-consumer patterns
- Use multiprocessing for CPU-bound parallel tasks
- Choose between threading and multiprocessing appropriately

### Quality & Architecture
- Write comprehensive unit tests with mocking
- Configure production-ready logging systems
- Apply design patterns to solve common problems
- Make informed architectural decisions

---

## 🔗 Additional Resources

### Official Documentation
- [collections](https://docs.python.org/3/library/collections.html)
- [property](https://docs.python.org/3/library/functions.html#property)
- [threading](https://docs.python.org/3/library/threading.html)
- [multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- [unittest](https://docs.python.org/3/library/unittest.html)
- [logging](https://docs.python.org/3/library/logging.html)

### Related Topics in This Repository
- **Topics 1-10**: Foundational advanced Python (decorators, generators, etc.)
- **Exercises Directory**: Practice problems for each topic
- **Projects**: Real-world applications using these concepts

---

## 📝 Notes

- Each lecture file is 300-500 lines with detailed explanations
- Each glossary file is 200-400 lines with comprehensive definitions
- All code examples are tested and working with Python 3.7+
- Cross-references between related topics are provided throughout

---

*Last updated: July 2026*
