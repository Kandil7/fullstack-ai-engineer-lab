# Qdrant Cheat Sheet

## Collection Management

### Creating Collections
```python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient("localhost", port=6333)

client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=1536,  # Embedding dimension
        distance=Distance.COSINE
    )
)
```

### Collection Operations
```python
# List collections
collections = client.get_collections()

# Get collection info
info = client.get_collection("documents")
print(info.points_count)

# Delete collection
client.delete_collection("documents")
```

---

## Vector Operations

### Inserting Points
```python
from qdrant_client.models import PointStruct

client.upsert(
    collection_name="documents",
    points=[
        PointStruct(
            id=1,
            vector=[0.1, 0.2, 0.3, ...],  # 1536 dimensions
            payload={
                "text": "This is a document",
                "source": "web",
                "created_at": "2024-01-15"
            }
        )
    ]
)
```

### Searching
```python
# Basic search
results = client.search(
    collection_name="documents",
    query_vector=[0.1, 0.2, 0.3, ...],
    limit=10
)

# Search with filter
results = client.search(
    collection_name="documents",
    query_vector=[0.1, 0.2, 0.3, ...],
    query_filter={
        "must": [
            {"key": "source", "match": {"value": "web"}}
        ]
    },
    limit=10
)

# Process results
for result in results:
    print(f"ID: {result.id}, Score: {result.score}")
    print(f"Payload: {result.payload}")
```

### Retrieving Points
```python
# Get by ID
point = client.retrieve(
    collection_name="documents",
    ids=[1, 2, 3]
)

# Scroll through points
points, next_offset = client.scroll(
    collection_name="documents",
    limit=100,
    with_payload=True
)
```

### Updating Points
```python
# Update payload
client.set_payload(
    collection_name="documents",
    payload={"status": "processed"},
    points=[1, 2, 3]
)

# Delete points
client.delete(
    collection_name="documents",
    points_selector=[1, 2, 3]
)
```

---

## Filtering

### Basic Filters
```python
# Match exact value
filter_condition = {
    "must": [
        {"key": "source", "match": {"value": "web"}}
    ]
}

# Match multiple values
filter_condition = {
    "must": [
        {
            "key": "category",
            "match": {"any": ["news", "blog", "docs"]}
        }
    ]
}

# Range filter
filter_condition = {
    "must": [
        {
            "key": "score",
            "range": {"gte": 0.5, "lte": 1.0}
        }
    ]
}
```

### Complex Filters
```python
# Must (AND)
filter_condition = {
    "must": [
        {"key": "source", "match": {"value": "web"}},
        {"key": "language", "match": {"value": "en"}}
    ]
}

# Should (OR)
filter_condition = {
    "should": [
        {"key": "category", "match": {"value": "news"}},
        {"key": "category", "match": {"value": "blog"}}
    ]
}

# Must NOT
filter_condition = {
    "must_not": [
        {"key": "status", "match": {"value": "deleted"}}
    ]
}
```

---

## Hybrid Search

### Combining Vector and Keyword Search
```python
results = client.search(
    collection_name="documents",
    query_vector=[0.1, 0.2, 0.3, ...],
    query_filter={
        "must": [
            {
                "key": "text",
                "match": {"text": "machine learning"}
            }
        ]
    },
    limit=10
)
```

### Reranking
```python
# Get more candidates, then rerank
results = client.search(
    collection_name="documents",
    query_vector=[0.1, 0.2, 0.3, ...],
    limit=20
)

# Custom reranking
reranked = sorted(results, key=lambda x: x.score, reverse=True)[:10]
```

---

## Indexing

### Payload Index
```python
# Create payload index
client.create_payload_index(
    collection_name="documents",
    field_name="source",
    field_schema="keyword"
)

# Index types
# "keyword" - exact match
# "integer" - numeric range
# "float" - numeric range
# "bool" - boolean
# "text" - full-text search
```

### Managing Indexes
```python
# Delete index
client.delete_payload_index(
    collection_name="documents",
    field_name="source"
)
```

---

## Client Usage

### Python Client
```python
from qdrant_client import QdrantClient

# Connect to Qdrant
client = QdrantClient("localhost", port=6333)

# Or with API key (Qdrant Cloud)
client = QdrantClient(
    url="https://your-cluster.qdrant.io",
    api_key="your-api-key"
)
```

### REST API
```bash
# Create collection
curl -X PUT http://localhost:6333/collections/documents \
  -H 'Content-Type: application/json' \
  -d '{
    "vectors": {
      "size": 1536,
      "distance": "Cosine"
    }
  }'

# Search
curl -X POST http://localhost:6333/collections/documents/points/search \
  -H 'Content-Type: application/json' \
  -d '{
    "vector": [0.1, 0.2, 0.3],
    "limit": 10
  }'
```

---

## Configuration

### Docker
```yaml
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  qdrant_data:
```

### Environment Variables
```bash
QDRANT__SERVICE__HTTP_PORT=6333
QDRANT__SERVICE__GRPC_PORT=6334
QDRANT__STORAGE__STORAGE_PATH=/qdrant/storage
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `client.create_collection()` | Create new collection |
| `client.upsert()` | Insert/update points |
| `client.search()` | Vector similarity search |
| `client.retrieve()` | Get points by ID |
| `client.delete()` | Delete points |
| `client.scroll()` | Iterate through points |
| `client.get_collection()` | Get collection info |

---

*Last updated: Phase 0*
