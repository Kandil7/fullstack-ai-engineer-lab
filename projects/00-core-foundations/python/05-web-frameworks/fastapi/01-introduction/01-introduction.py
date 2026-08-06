"""
01 - Introduction to FastAPI
=============================
FastAPI is a modern, high-performance Python web framework for building APIs.
It is based on Python type hints, is async-native, and auto-generates docs.

Key advantages:
- Fast: Very high performance (on par with Node.js and Go)
- Fast to code: Great developer experience
- Fewer bugs: Reduce human-induced errors
- Intuitive: Great editor support (autocompletion everywhere)
- Easy: Designed to be easy to use and learn
- Short: Minimize code duplication
- Robust: Get production-ready code with automatic docs

Install: pip install fastapi uvicorn

Run: uvicorn 01-introduction:app --reload
"""

import sys
from fastapi import FastAPI

# Create an instance of FastAPI
# The 'title' and 'version' appear in the auto-generated docs
app = FastAPI(
    title="GeeksforGeeks FastAPI Tutorial",
    description="A comprehensive FastAPI learning series",
    version="1.0.0",
)


# Path operation decorator: @app.get() tells FastAPI that the function below
# handles GET requests to the path "/"
# The function name doesn't matter; it's just used internally by Python
@app.get("/")
def read_root():
    """Root endpoint returning a welcome message."""
    return {"message": "Welcome to FastAPI!", "docs": "Visit /docs for Swagger UI"}


# FastAPI uses Python type hints for automatic validation and documentation
@app.get("/hello/{name}")
def say_hello(name: str) -> dict:
    """
    Simple endpoint demonstrating path parameters.

    FastAPI automatically:
    - Validates that 'name' is a string
    - Converts it to the correct type
    - Documents it in the API docs
    """
    return {"message": f"Hello, {name}! Welcome to FastAPI."}


# Returning complex data structures
@app.get("/server-info")
def server_info():
    """FastAPI auto-converts return values to JSON."""
    return {
        "framework": "FastAPI",
        "language": "Python",
        "version": "0.100+",
        "features": [
            "Type hints",
            "Auto documentation",
            "Async support",
            "Data validation",
        ],
        "is_awesome": True,
    }


# Multiple HTTP methods on same path
@app.post("/submit")
def submit_data():
    """Demo: POST method on a path."""
    return {"status": "received", "method": "POST"}


@app.put("/update")
def update_data():
    """Demo: PUT method on a path."""
    return {"status": "updated", "method": "PUT"}


@app.delete("/remove")
def remove_data():
    """Demo: DELETE method on a path."""
    return {"status": "removed", "method": "DELETE"}


"""
Testing with curl:
    curl http://127.0.0.1:8000/
    curl http://127.0.0.1:8000/hello/Alice
    curl http://127.0.0.1:8000/server-info
    curl -X POST http://127.0.0.1:8000/submit
    curl -X PUT http://127.0.0.1:8000/update
    curl -X DELETE http://127.0.0.1:8000/remove

    Auto-generated docs:
    Swagger UI:  http://127.0.0.1:8000/docs
    ReDoc:       http://127.0.0.1:8000/redoc
    OpenAPI JSON: http://127.0.0.1:8000/openapi.json
"""

def _verify():
    """Smoke-test the app in-process with TestClient (no real server)."""
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        print("[skip] fastapi not installed")
        return

    client = TestClient(app)

    r = client.get("/")
    assert r.status_code == 200
    assert "Welcome to FastAPI!" in r.json()["message"]

    r = client.get("/hello/Alice")
    assert r.status_code == 200
    assert r.json()["message"] == "Hello, Alice! Welcome to FastAPI."

    r = client.get("/server-info")
    assert r.status_code == 200
    assert r.json()["framework"] == "FastAPI"
    assert "features" in r.json()

    r = client.post("/submit")
    assert r.status_code == 200
    assert r.json()["method"] == "POST"

    r = client.put("/update")
    assert r.status_code == 200
    assert r.json()["method"] == "PUT"

    r = client.delete("/remove")
    assert r.status_code == 200
    assert r.json()["method"] == "DELETE"

    r = client.get("/does-not-exist")
    assert r.status_code == 404

    print("[OK] 01-introduction: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        _verify()
