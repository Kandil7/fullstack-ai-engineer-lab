# Advanced Python Exercises

A comprehensive collection of 20 advanced Python exercise scripts covering essential topics for building production-grade applications.

## 📚 Topics Covered

| # | File | Topic | Description |
|---|------|-------|-------------|
| 01 | `01-decorators.py` | Decorators | Basic/class decorators, argument passing, stacking, caching |
| 02 | `02-generators.py` | Generators | Yield, pipelines, send(), infinite sequences, memory efficiency |
| 03 | `03-context-managers.py` | Context Managers | with statement, contextlib, resource management |
| 04 | `04-async-await.py` | Async/Await | asyncio, tasks, semaphores, producer-consumer |
| 05 | `05-type-hints.py` | Type Hints | Annotations, generics, protocols, TypeVar |
| 06 | `06-dataclasses.py` | Dataclasses | Fields, frozen classes, inheritance, serialization |
| 07 | `07-enum.py` | Enums | Auto values, flags, string enums, methods |
| 08 | `08-abc.py` | Abstract Classes | Interfaces, plugins, mixins, collections |
| 09 | `09-functools.py` | Functools | reduce, partial, lru_cache, total_ordering |
| 10 | `10-itertools.py` | Itertools | Combinatorics, groupby, chaining, infinite iterators |
| 11 | `11-collections.py` | Collections | Counter, defaultdict, namedtuple, deque, ChainMap |
| 12 | `12-property.py` | Properties | Getters/setters, caching, validation, computed values |
| 13 | `13-slots.py` | Slots | Memory optimization, performance benchmarks |
| 14 | `14-metaclasses.py` | Metaclasses | Custom metaclasses, registries, singletons |
| 15 | `15-descriptors.py` | Descriptors | __get__, __set__, validation, computed attributes |
| 16 | `16-threading.py` | Threading | Threads, locks, semaphores, thread pools |
| 17 | `17-multiprocessing.py` | Multiprocessing | Processes, pools, shared state, parallel computing |
| 18 | `18-unit-testing.py` | Unit Testing | unittest, mocking, fixtures, parameterized tests |
| 19 | `19-logging.py` | Logging | Levels, handlers, formatters, application logging |
| 20 | `20-patterns.py` | Design Patterns | Singleton, Factory, Observer, Strategy, Adapter |

## 🚀 How to Run

### Run Individual Files
```bash
# From the project root
python projects/00-core-foundations/python/advanced/01-decorators.py

# Or from the advanced directory
cd projects/00-core-foundations/python/advanced
python 01-decorators.py
```

### Run All Files
```bash
# Windows PowerShell
Get-ChildItem *.py | ForEach-Object { Write-Host "`n=== $($_.Name) ===" -ForegroundColor Cyan; python $_.Name }

# Linux/Mac
for f in *.py; do echo "=== $f ==="; python "$f"; done
```

## 📖 Recommended Learning Order

### Beginner-Intermediate
1. **01-decorators.py** - Essential for understanding Python's power
2. **02-generators.py** - Memory-efficient iteration
3. **05-type-hints.py** - Modern Python best practices
4. **06-dataclasses.py** - Clean class definitions
5. **12-property.py** - Attribute management

### Intermediate
6. **03-context-managers.py** - Resource management
7. **07-enum.py** - Constants and states
8. **08-abc.py** - Interface design
9. **09-functools.py** - Functional programming tools
10. **10-itertools.py** - Efficient iteration patterns
11. **11-collections.py** - Specialized containers

### Advanced
12. **13-slots.py** - Memory optimization
13. **14-metaclasses.py** - Class creation control
14. **15-descriptors.py** - Attribute access customization
15. **16-threading.py** - Concurrent programming (I/O-bound)
16. **17-multiprocessing.py** - Parallel programming (CPU-bound)
17. **18-unit-testing.py** - Testing best practices
18. **19-logging.py** - Application logging
19. **20-patterns.py** - Design patterns in Python
20. **04-async-await.py** - Async programming (most complex)

## 🎯 Each File Contains

- **3-5 complete working examples** with real implementations
- **Output comments** showing expected results
- **Progressive difficulty** within each topic
- **Practical use cases** for real-world applications
- **80-200 lines** of well-commented code

## 💡 Key Concepts by File

### Decorators (01)
- Function wrapping and metadata preservation
- Decorators with arguments
- Class decorators
- Stacking multiple decorators

### Generators (02)
- Lazy evaluation for memory efficiency
- Generator pipelines for data processing
- send() for bidirectional communication
- Infinite sequences with iteration control

### Async/Await (04)
- Concurrent I/O operations
- Task creation and management
- Synchronization primitives
- Async iteration patterns

### Design Patterns (20)
- **Singleton**: Single instance guarantee
- **Factory**: Object creation abstraction
- **Observer**: Event notification system
- **Strategy**: Algorithm interchangeability
- **Adapter**: Interface compatibility

## 🔗 Related Topics

After completing these exercises, explore:
- **Decorators + Metaclasses**: Advanced class modification
- **Generators + Async**: Async generators (Python 3.6+)
- **Descriptors + Properties**: Deep attribute control
- **Patterns + ABCs**: Interface-driven design
