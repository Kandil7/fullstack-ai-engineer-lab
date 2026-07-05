# MongoDB with Python - Tutorial Files

Complete MongoDB tutorial using Python dicts as stand-ins for MongoDB documents. Each file demonstrates core MongoDB operations with both dict-based and equivalent MongoDB code.

## Files Overview

| # | File | Topics | Lines |
|---|------|--------|-------|
| 01 | [01-getting-started.py](01-getting-started.py) | What is MongoDB, Document Model vs Relational, PyMongo Concept, CRUD Overview | ~120 |
| 02 | [02-databases.py](02-databases.py) | Databases Concept, Creating/Using Databases, Collection Concept | ~130 |
| 03 | [03-collection.py](03-collection.py) | Collections Concept, Creating/Dropping Collections | ~120 |
| 04 | [04-insert.py](04-insert.py) | insert_one, insert_many, _id Field, Automatic IDs, Inserting Documents | ~160 |
| 05 | [05-find.py](05-find.py) | find() for all, find() with query, find_one(), Querying Nested Fields, Projection | ~150 |
| 06 | [06-query.py](06-query.py) | Comparison Operators ($eq, $ne, $gt, $lt), Logical Operators ($and, $or), $in, $regex | ~180 |
| 07 | [07-sort.py](07-sort.py) | sort() Ascending/Descending, Sorting by Multiple Fields | ~140 |
| 08 | [08-limit.py](08-limit.py) | limit(), skip(), Pagination Pattern, count_documents | ~160 |
| 09 | [09-delete.py](09-delete.py) | delete_one(), delete_many(), Deleting with Filters | ~150 |
| 10 | [10-update.py](10-update.py) | update_one(), update_many(), $set, $unset, $inc, $push, upsert | ~170 |
| 11 | [11-aggregation.py](11-aggregation.py) | Aggregation Pipeline Concept, $match, $group, $sort, $project | ~180 |

## Key Concepts

- **Document Model**: Data stored as JSON-like documents (dicts) instead of rows
- **Collections**: Groups of documents (like tables in SQL)
- **CRUD Operations**: Create, Read, Update, Delete
- **Query Operators**: Comparison ($gt, $lt, $eq) and logical ($and, $or)
- **Aggregation Pipeline**: Data transformation through multiple stages

## Running the Files

Each file is self-contained and runs with Python's standard library:

```bash
python 01-getting-started.py
python 02-databases.py
python 03-collection.py
python 04-insert.py
python 05-find.py
python 06-query.py
python 07-sort.py
python 08-limit.py
python 09-delete.py
python 10-update.py
python 11-aggregation.py
```

## MongoDB Equivalent Syntax

Every operation includes comments showing the real MongoDB syntax:

```python
# Dict-based approach
users = [{"_id": 1, "name": "Alice"}]
result = [u for u in users if u["age"] > 25]

# MongoDB equivalent:
# db.users.find({"age": {"$gt": 25}})
```

## Learning Path

1. Start with `01-getting-started.py` for MongoDB fundamentals
2. Learn database/collection concepts with `02-03`
3. Master CRUD operations with `04-10`
4. Explore advanced analytics with `11-aggregation.py`
