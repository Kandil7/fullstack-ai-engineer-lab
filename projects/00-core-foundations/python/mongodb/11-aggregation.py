"""
W3Schools Python Tutorial - MongoDB 11: Aggregation
==============================================
Topics: Aggregation Pipeline Concept, $match, $group, $sort, $project

Run: python 11-aggregation.py
Reference: https://www.w3schools.com/python/python_mongodb_aggregation.asp
"""

# NOTE: This uses Python dicts as stand-ins for MongoDB documents.
# The syntax mirrors MongoDB operations.

# ============================================================
# Sample Data
# ============================================================

orders = [
    {"_id": 1, "customer": "Alice", "product": "Laptop", "price": 999.99, "quantity": 1, "date": "2024-01-15", "category": "Electronics"},
    {"_id": 2, "customer": "Bob", "product": "Mouse", "price": 29.99, "quantity": 2, "date": "2024-01-16", "category": "Electronics"},
    {"_id": 3, "customer": "Alice", "product": "Keyboard", "price": 79.99, "quantity": 1, "date": "2024-01-17", "category": "Electronics"},
    {"_id": 4, "customer": "Charlie", "product": "Desk", "price": 299.99, "quantity": 1, "date": "2024-01-18", "category": "Furniture"},
    {"_id": 5, "customer": "Bob", "product": "Chair", "price": 199.99, "quantity": 1, "date": "2024-01-19", "category": "Furniture"},
    {"_id": 6, "customer": "Diana", "product": "Monitor", "price": 399.99, "quantity": 2, "date": "2024-01-20", "category": "Electronics"},
    {"_id": 7, "customer": "Alice", "product": "Lamp", "price": 49.99, "quantity": 3, "date": "2024-01-21", "category": "Furniture"},
    {"_id": 8, "customer": "Charlie", "product": "Bookshelf", "price": 149.99, "quantity": 1, "date": "2024-01-22", "category": "Furniture"}
]

# ============================================================
# Aggregation Pipeline Concept
# ============================================================

# Aggregation processes data through a pipeline of stages.
# Each stage transforms the data and passes it to the next.
# MongoDB equivalent:
# db.orders.aggregate([
#     {$match: {category: "Electronics"}},
#     {$group: {_id: "$customer", total: {$sum: "$price"}}}
# ])

# Example 1: Simple aggregation pipeline
def aggregate(collection, pipeline):
    """Execute an aggregation pipeline"""
    result = collection
    for stage in pipeline:
        stage_type = stage[0]
        stage_args = stage[1] if len(stage) > 1 else {}
        
        if stage_type == "$match":
            result = agg_match(result, stage_args)
        elif stage_type == "$group":
            result = agg_group(result, stage_args)
        elif stage_type == "$sort":
            result = agg_sort(result, stage_args)
        elif stage_type == "$project":
            result = agg_project(result, stage_args)
        elif stage_type == "$limit":
            result = result[:stage_args.get("limit", 10)]
        elif stage_type == "$unwind":
            result = agg_unwind(result, stage_args)
    
    return result

# ============================================================
# $match Stage
# ============================================================

# Example 2: Filter documents
# MongoDB equivalent: {$match: {category: "Electronics"}}

def agg_match(collection, query):
    """Filter documents matching the query"""
    results = []
    for doc in collection:
        match = True
        for key, value in query.items():
            if isinstance(value, dict):
                for op, val in value.items():
                    doc_val = doc.get(key)
                    if op == "$gt" and not (doc_val > val):
                        match = False
                    elif op == "$lt" and not (doc_val < val):
                        match = False
                    elif op == "$gte" and not (doc_val >= val):
                        match = False
                    elif op == "$lte" and not (doc_val <= val):
                        match = False
                    elif op == "$ne" and not (doc_val != val):
                        match = False
            elif doc.get(key) != value:
                match = False
        if match:
            results.append(doc)
    return results

# Filter electronics only
pipeline = [("$match", {"category": "Electronics"})]
result = aggregate(orders, pipeline)
print("Electronics orders:")
for order in result:
    print(f"  {order['product']}: ${order['price']}")

# ============================================================
# $group Stage
# ============================================================

# Example 3: Group and aggregate
# MongoDB equivalent: {$group: {_id: "$customer", total: {$sum: "$price"}}}

def agg_group(collection, group_spec):
    """Group documents by field and apply accumulator"""
    group_field = group_spec["_id"].replace("$", "")
    accumulators = {k: v for k, v in group_spec.items() if k != "_id"}
    
    groups = {}
    for doc in collection:
        key = doc.get(group_field, "unknown")
        if key not in groups:
            groups[key] = []
        groups[key].append(doc)
    
    results = []
    for key, docs in groups.items():
        result = {"_id": key}
        for acc_name, acc_spec in accumulators.items():
            field = acc_spec.get("field", "").replace("$", "")
            op = acc_spec.get("op", "sum")
            
            if op == "sum":
                result[acc_name] = sum(doc.get(field, 0) for doc in docs)
            elif op == "avg":
                values = [doc.get(field, 0) for doc in docs]
                result[acc_name] = sum(values) / len(values) if values else 0
            elif op == "min":
                result[acc_name] = min(doc.get(field, 0) for doc in docs)
            elif op == "max":
                result[acc_name] = max(doc.get(field, 0) for doc in docs)
            elif op == "count":
                result[acc_name] = len(docs)
        
        results.append(result)
    
    return results

# Group by customer and sum total
pipeline = [
    ("$match", {}),
    ("$group", {
        "_id": "$customer",
        "total": {"op": "sum", "field": "$price"},
        "order_count": {"op": "count"}
    })
]
result = aggregate(orders, pipeline)
print("\nOrders by customer:")
for r in result:
    print(f"  {r['_id']}: ${r['total']:.2f} ({r['order_count']} orders)")

# ============================================================
# $sort Stage
# ============================================================

# Example 4: Sort results
# MongoDB equivalent: {$sort: {total: -1}}

def agg_sort(collection, sort_spec):
    """Sort documents by field(s)"""
    items = list(collection)
    for field, direction in reversed(list(sort_spec.items())):
        items.sort(key=lambda x: x.get(field, 0), reverse=(direction == -1))
    return items

# Sort by total descending
pipeline = [
    ("$match", {}),
    ("$group", {
        "_id": "$customer",
        "total": {"op": "sum", "field": "$price"}
    }),
    ("$sort", {"total": -1})
]
result = aggregate(orders, pipeline)
print("\nCustomers sorted by total (highest first):")
for r in result:
    print(f"  {r['_id']}: ${r['total']:.2f}")

# ============================================================
# $project Stage
# ============================================================

# Example 5: Reshape documents
# MongoDB equivalent: {$project: {name: 1, total: 1, _id: 0}}

def agg_project(collection, project_spec):
    """Reshape documents based on projection"""
    results = []
    for doc in collection:
        projected = {}
        for field, include in project_spec.items():
            if include == 1 or include is True:
                if field in doc:
                    projected[field] = doc[field]
            elif include == 0 or include is False:
                pass  # Exclude field
            elif isinstance(include, dict):
                # Computed field
                if "$multiply" in include:
                    f1 = include["$multiply"][0].replace("$", "")
                    f2 = include["$multiply"][1].replace("$", "")
                    projected[field] = doc.get(f1, 0) * doc.get(f2, 0)
        
        # Always include _id unless explicitly excluded
        if "_id" not in project_spec or project_spec.get("_id") != 0:
            projected["_id"] = doc["_id"]
        
        results.append(projected)
    return results

# Project name and total
pipeline = [
    ("$match", {}),
    ("$group", {
        "_id": "$customer",
        "total": {"op": "sum", "field": "$price"}
    }),
    ("$project", {"_id": 0, "customer": 1, "total": 1})
]
result = aggregate(orders, pipeline)
print("\nProjected (name + total):")
for r in result:
    print(f"  {r}")

# ============================================================
# $unwind Stage
# ============================================================

# Example 6: Deconstruct array field
# MongoDB equivalent: {$unwind: "$tags"}

def agg_unwind(collection, unwind_spec):
    """Unwind an array field into separate documents"""
    field = unwind_spec.get("path", "").replace("$", "")
    results = []
    for doc in collection:
        if field in doc and isinstance(doc[field], list):
            for item in doc[field]:
                new_doc = doc.copy()
                new_doc[field] = item
                results.append(new_doc)
        else:
            results.append(doc)
    return results

# Example with tags
products = [
    {"_id": 1, "name": "Laptop", "tags": ["electronics", "computers"]},
    {"_id": 2, "name": "Mouse", "tags": ["electronics", "accessories"]}
]

pipeline = [("$unwind", {"path": "$tags"})]
result = aggregate(products, pipeline)
print("\nUnwound tags:")
for r in result:
    print(f"  {r['name']}: {r['tags']}")

# ============================================================
# Complex Pipeline
# ============================================================

# Example 7: Multi-stage pipeline
# MongoDB equivalent:
# db.orders.aggregate([
#     {$match: {category: "Electronics"}},
#     {$group: {_id: "$customer", total: {$sum: {$multiply: ["$price", "$quantity"]}}}},
#     {$sort: {total: -1}},
#     {$limit: 3}
# ])

pipeline = [
    ("$match", {"category": "Electronics"}),
    ("$group", {
        "_id": "$customer",
        "total_spent": {"op": "sum", "field": "$price"},
        "items_bought": {"op": "sum", "field": "$quantity"}
    }),
    ("$sort", {"total_spent": -1}),
    ("$limit", 3)
]
result = aggregate(orders, pipeline)
print("\nTop 3 electronics buyers:")
for r in result:
    print(f"  {r['_id']}: ${r['total_spent']:.2f} ({r['items_bought']} items)")

# ============================================================
# Common Aggregation Patterns
# ============================================================

# Example 8: Average order value by customer
pipeline = [
    ("$group", {
        "_id": "$customer",
        "avg_order": {"op": "avg", "field": "$price"},
        "order_count": {"op": "count"}
    }),
    ("$sort", {"avg_order": -1})
]
result = aggregate(orders, pipeline)
print("\nAverage order value by customer:")
for r in result:
    print(f"  {r['_id']}: ${r['avg_order']:.2f} (avg of {r['order_count']} orders)")

# Example 9: Min and max prices
pipeline = [
    ("$group", {
        "_id": "$category",
        "min_price": {"op": "min", "field": "$price"},
        "max_price": {"op": "max", "field": "$price"}
    })
]
result = aggregate(orders, pipeline)
print("\nPrice range by category:")
for r in result:
    print(f"  {r['_id']}: ${r['min_price']:.2f} - ${r['max_price']:.2f}")

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 60)
print("SUMMARY: Aggregation Pipeline")
print("=" * 60)
print("""
1. Aggregation processes data through a pipeline of stages
2. $match - Filter documents (like find())
3. $group - Group by field and apply accumulators (sum, avg, min, max, count)
4. $sort - Sort results by field(s)
5. $project - Reshape documents, include/exclude fields
6. $unwind - Deconstruct array fields into separate documents
7. $limit - Limit number of results
8. Stages are executed in order, each transforms data
9. Use dot notation for nested fields: "$address.city"
10. Complex analytics can be built by chaining stages
""")
