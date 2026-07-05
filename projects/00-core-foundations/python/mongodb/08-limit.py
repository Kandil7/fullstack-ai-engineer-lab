"""
W3Schools Python Tutorial - MongoDB 08: Limit and Skip
==============================================
Topics: limit(), skip(), Pagination Pattern, count_documents

Run: python 08-limit.py
Reference: https://www.w3schools.com/python/python_mongodb_limit.asp
"""

# NOTE: This uses Python dicts as stand-ins for MongoDB documents.
# The syntax mirrors MongoDB operations.

# ============================================================
# Sample Data
# ============================================================

products = [
    {"_id": 1, "name": "Laptop", "price": 999.99, "category": "Electronics"},
    {"_id": 2, "name": "Mouse", "price": 29.99, "category": "Electronics"},
    {"_id": 3, "name": "Keyboard", "price": 79.99, "category": "Electronics"},
    {"_id": 4, "name": "Monitor", "price": 399.99, "category": "Electronics"},
    {"_id": 5, "name": "Desk", "price": 299.99, "category": "Furniture"},
    {"_id": 6, "name": "Chair", "price": 199.99, "category": "Furniture"},
    {"_id": 7, "name": "Lamp", "price": 49.99, "category": "Furniture"},
    {"_id": 8, "name": "Bookshelf", "price": 149.99, "category": "Furniture"},
    {"_id": 9, "name": "Notebook", "price": 12.99, "category": "Stationery"},
    {"_id": 10, "name": "Pen Set", "price": 24.99, "category": "Stationery"},
    {"_id": 11, "name": "Stapler", "price": 15.99, "category": "Stationery"},
    {"_id": 12, "name": "Tape Dispenser", "price": 8.99, "category": "Stationery"}
]

# ============================================================
# Limit Results
# ============================================================

# Example 1: Limit to first 5 results
# MongoDB equivalent: db.products.find().limit(5)

def limit_results(collection, limit):
    """Return only the first 'limit' documents"""
    return collection[:limit]

first_5 = limit_results(products, 5)
print("First 5 products:")
for product in first_5:
    print(f"  {product['name']}: ${product['price']}")

# Example 2: Limit to 3 results
first_3 = limit_results(products, 3)
print("\nFirst 3 products:")
for product in first_3:
    print(f"  {product['name']}: ${product['price']}")

# ============================================================
# Skip Results
# ============================================================

# Example 3: Skip first 5 results
# MongoDB equivalent: db.products.find().skip(5)

def skip_results(collection, skip):
    """Skip the first 'skip' documents"""
    return collection[skip:]

skip_5 = skip_results(products, 5)
print("\nAfter skipping 5:")
for product in skip_5[:5]:  # Show first 5 of remaining
    print(f"  {product['name']}: ${product['price']}")

# Example 4: Skip first 10
skip_10 = skip_results(products, 10)
print("\nAfter skipping 10:")
for product in skip_10:
    print(f"  {product['name']}: ${product['price']}")

# ============================================================
# Limit and Skip Together
# ============================================================

# Example 5: Get products 6-10 (page 2 with 5 per page)
# MongoDB equivalent: db.products.find().skip(5).limit(5)

def paginate(collection, skip=0, limit=5):
    """Get a page of results"""
    return collection[skip:skip + limit]

page_2 = paginate(products, skip=5, limit=5)
print("\nPage 2 (products 6-10):")
for product in page_2:
    print(f"  {product['name']}: ${product['price']}")

# Example 6: Get products 11-12 (page 3)
page_3 = paginate(products, skip=10, limit=5)
print("\nPage 3 (products 11-12):")
for product in page_3:
    print(f"  {product['name']}: ${product['price']}")

# ============================================================
# Pagination Pattern
# ============================================================

# Example 7: Full pagination implementation
def get_page(collection, page_number, page_size=5):
    """Get a specific page of results"""
    skip = (page_number - 1) * page_size
    return collection[skip:skip + page_size]

def get_total_pages(collection, page_size=5):
    """Calculate total number of pages"""
    return (len(collection) + page_size - 1) // page_size

def get_pagination_info(collection, page_number, page_size=5):
    """Get full pagination information"""
    total_items = len(collection)
    total_pages = get_total_pages(collection, page_size)
    items_on_page = len(get_page(collection, page_number, page_size))
    
    return {
        "page": page_number,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
        "items_on_page": items_on_page,
        "has_next": page_number < total_pages,
        "has_prev": page_number > 1
    }

# Display all pages
print("\n" + "=" * 40)
print("Pagination Demo (5 items per page)")
print("=" * 40)

total_pages = get_total_pages(products, 5)
print(f"Total products: {len(products)}")
print(f"Total pages: {total_pages}")

for page in range(1, total_pages + 1):
    info = get_pagination_info(products, page, 5)
    items = get_page(products, page, 5)
    print(f"\nPage {info['page']}:")
    for item in items:
        print(f"  {item['name']}: ${item['price']}")
    print(f"  Items on page: {info['items_on_page']}, Has next: {info['has_next']}")

# ============================================================
# Count Documents
# ============================================================

# Example 8: Count all documents
# MongoDB equivalent: db.products.count_documents({})

def count_all(collection):
    """Count all documents"""
    return len(collection)

print(f"\nTotal products: {count_all(products)}")

# Example 9: Count with filter
# MongoDB equivalent: db.products.count_documents({"category": "Electronics"})

def count_filtered(collection, query):
    """Count documents matching a query"""
    count = 0
    for doc in collection:
        match = True
        for key, value in query.items():
            if doc.get(key) != value:
                match = False
                break
        if match:
            count += 1
    return count

electronics_count = count_filtered(products, {"category": "Electronics"})
print(f"Electronics products: {electronics_count}")

furniture_count = count_filtered(products, {"category": "Furniture"})
print(f"Furniture products: {furniture_count}")

# ============================================================
# Advanced Pagination
# ============================================================

# Example 10: Cursor-style pagination (using _id)
def get_page_by_id(collection, last_id=None, limit=5):
    """Get next page using _id-based pagination"""
    if last_id is None:
        start = 0
    else:
        # Find index of last_id
        start = 0
        for i, doc in enumerate(collection):
            if doc["_id"] == last_id:
                start = i + 1
                break
    
    return collection[start:start + limit]

print("\n" + "=" * 40)
print("ID-based Pagination")
print("=" * 40)

# Get first batch
batch1 = get_page_by_id(products, None, 4)
print("\nBatch 1:")
for product in batch1:
    print(f"  {product['_id']}: {product['name']}")

# Get next batch using last _id
last_id = batch1[-1]["_id"]
batch2 = get_page_by_id(products, last_id, 4)
print("\nBatch 2:")
for product in batch2:
    print(f"  {product['_id']}: {product['name']}")

# Get next batch
last_id = batch2[-1]["_id"]
batch3 = get_page_by_id(products, last_id, 4)
print("\nBatch 3:")
for product in batch3:
    print(f"  {product['_id']}: {product['name']}")

# ============================================================
# Limit with Sort
# ============================================================

# Example 11: Get top 3 most expensive products
def top_n_products(collection, n, sort_field="price", reverse=True):
    """Get top N products by a field"""
    sorted_products = sorted(collection, key=lambda x: x.get(sort_field, 0), reverse=reverse)
    return sorted_products[:n]

top_3_expensive = top_n_products(products, 3)
print("\nTop 3 most expensive:")
for i, product in enumerate(top_3_expensive, 1):
    print(f"  {i}. {product['name']}: ${product['price']}")

# ============================================================
# Practical Examples
# ============================================================

# Example 12: Search with pagination
def search_paginated(collection, query, page=1, page_size=5):
    """Search with pagination"""
    # Filter
    filtered = []
    for doc in collection:
        match = True
        for key, value in query.items():
            if isinstance(value, str) and value.lower() in str(doc.get(key, "")).lower():
                continue
            elif doc.get(key) != value:
                match = False
                break
        if match:
            filtered.append(doc)
    
    # Paginate
    skip = (page - 1) * page_size
    results = filtered[skip:skip + page_size]
    
    return {
        "results": results,
        "total": len(filtered),
        "page": page,
        "total_pages": (len(filtered) + page_size - 1) // page_size
    }

# Search for electronics
search_result = search_paginated(products, {"category": "Electronics"}, page=1, page_size=2)
print("\nSearch 'Electronics' (page 1, 2 per page):")
print(f"  Found {search_result['total']} items, showing page {search_result['page']}/{search_result['total_pages']}")
for product in search_result["results"]:
    print(f"    {product['name']}: ${product['price']}")

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 60)
print("SUMMARY: Limit, Skip, and Pagination")
print("=" * 60)
print("""
1. limit(n) returns only the first n documents
2. skip(n) skips the first n documents
3. skip().limit() implements pagination
4. Page formula: skip = (page - 1) * page_size
5. count_documents() counts matching documents
6. Use _id-based pagination for large datasets
7. Combine sort + limit for top-N queries
8. Always calculate total_pages for UI pagination
9. Consider cursor-based pagination for real-time data
""")
