# MongoDB Lecture 05: Querying Documents

## 🎯 Topic Overview

Querying Documents — core concepts and Python implementation.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Understand MongoDB querying documents concepts
2. Implement operations using PyMongo
3. Handle edge cases and common errors
4. Apply best practices
5. Compare with relational database equivalents

---

## 1. Introduction

MongoDB is a NoSQL document database that stores data in flexible, JSON-like documents. This lecture covers querying documents with Python using PyMongo.

---

## 2. Core Concepts

### 1. find()

`db.users.find()` returns all documents. `db.users.find({'age': 25})` filters results.

### 2. find_one()

`db.users.find_one({'name': 'Alice'})` returns the first matching document or None.

### 3. Projection

`db.users.find({}, {'name': 1, '_id': 0})` includes/excludes specific fields.

### 4. Pretty Printing

Use `pprint` from pprint module for readable output of nested documents.

---

## 3. Common Mistakes

### Not handling ObjectId serialization
ObjectId is not JSON serializable by default. Use bson.json_util for proper serialization:
```python
from bson import json_util
import json

# Serialize a document with ObjectId
json.dumps(doc, default=json_util.default)
```

### Using implicit database references
Explicit syntax is clearer and less error-prone:
```python
# OK but implicit
col = client.mydb.users

# Better - explicit
col = client['mydb']['users']
```

### Not handling connection errors
Always handle connection failures:
```python
from pymongo.errors import ConnectionFailure
try:
    client = MongoClient('localhost', 27017)
    client.admin.command('ping')
except ConnectionFailure:
    print('Server not available')
```

---

## 4. Best Practices

1. Use **explicit** database/collection references `client['db']['col']`
2. Handle **connection errors** with try/except
3. Create **indexes** for frequently queried fields
4. Use **projections** to limit returned fields
5. **Close connections** in production code
6. **Validate input** before database operations

---

## 5. Practice Exercises

### Exercise 1: Basic CRUD
Implement all CRUD operations (Create, Read, Update, Delete) for a simple document collection.

### Exercise 2: Error Handling
Add proper error handling, input validation, and connection management to your CRUD operations.

### Exercise 3: SQL Comparison
Write the equivalent SQL queries for each MongoDB operation and compare the approaches.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| MongoDB | NoSQL document database - flexible, scalable |
| Document | JSON-like data structure (Python dict) |
| Collection | Group of related documents (like SQL table) |
| PyMongo | Official Python driver for MongoDB |
| CRUD | Create, Read, Update, Delete operations |
| Performance | Use indexes and projections for speed |
