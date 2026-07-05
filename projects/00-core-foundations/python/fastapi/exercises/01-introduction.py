"""
FastAPI Exercise 01 - Introduction to FastAPI
=============================================

Topics covered:
- Creating a basic FastAPI application
- Understanding the ASGI server
- Reading and running FastAPI apps
- Interactive documentation (Swagger UI, ReDoc)

Requirements:
    pip install fastapi uvicorn

Run any exercise:
    uvicorn 01-introduction:app1 --reload
    uvicorn 01-introduction:app2 --reload
    uvicorn 01-introduction:app3 --reload
"""

from fastapi import FastAPI


# =============================================================================
# Exercise 1: Your First FastAPI Application
# =============================================================================
# Create a FastAPI application that returns a JSON response with:
#   - "message": "Hello, FastAPI!"
#   - "version": "1.0.0"
#
# Hints:
#   - Use FastAPI() to create the app instance
#   - Use @app.get("/") to define a route
#   - Return a dict; FastAPI auto-converts to JSON
#
# Expected behavior:
#   GET http://localhost:8000/
#   Response: {"message": "Hello, FastAPI!", "version": "1.0.0"}
#
# Test with:
#   curl http://localhost:8000/
# =============================================================================

app1 = FastAPI(title="Exercise 1")


@app1.get("/")
def root():
    pass  # TODO: Return the expected JSON response


# =============================================================================
# Exercise 2: Multiple Routes
# =============================================================================
# Create a FastAPI app with THREE routes:
#   GET /          -> {"page": "home"}
#   GET /about     -> {"page": "about"}
#   GET /contact   -> {"page": "contact"}
#
# Hints:
#   - Each route needs its own @app.get() decorator
#   - Route paths are case-sensitive
#   - Function names can be anything (but use descriptive names)
#
# Expected behavior:
#   GET http://localhost:8000/        -> {"page": "home"}
#   GET http://localhost:8000/about   -> {"page": "about"}
#   GET http://localhost:8000/contact -> {"page": "contact"}
#
# Test with:
#   curl http://localhost:8000/
#   curl http://localhost:8000/about
#   curl http://localhost:8000/contact
# =============================================================================

app2 = FastAPI(title="Exercise 2")


@app2.get("/")
def home():
    pass  # TODO: Return {"page": "home"}


@app2.get("/about")
def about():
    pass  # TODO: Return {"page": "about"}


@app2.get("/contact")
def contact():
    pass  # TODO: Return {"page": "contact"}


# =============================================================================
# Exercise 3: App Metadata and Documentation
# =============================================================================
# Create a FastAPI app with:
#   - title: "Book Store API"
#   - description: "A simple API for managing books"
#   - version: "0.1.0"
#   - A GET / endpoint that returns the API info as:
#     {"name": "Book Store API", "docs_url": <the docs URL>}
#
# Hints:
#   - Pass metadata to FastAPI(title=..., description=..., version=...)
#   - Access docs URL from app.openapi_url or hardcode "/docs"
#   - The Swagger UI is auto-generated at /docs
#
# Expected behavior:
#   GET http://localhost:8000/ -> {"name": "Book Store API", "docs_url": "/docs"}
#   Visit http://localhost:8000/docs to see Swagger UI
#   Visit http://localhost:8000/redoc to see ReDoc
#
# Test with:
#   curl http://localhost:8000/
#   Open browser: http://localhost:8000/docs
# =============================================================================

app3 = FastAPI(
    title="TODO: Set the title",
    description="TODO: Set the description",
    version="TODO: Set the version",
)


@app3.get("/")
def api_info():
    pass  # TODO: Return {"name": <title>, "docs_url": "/docs"}


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# After completing the exercises:
#
# 1. Run: uvicorn 01-introduction:app1 --reload
#    - Visit http://localhost:8000/ - should see JSON
#    - Visit http://localhost:8000/docs - should see Swagger UI
#
# 2. Run: uvicorn 01-introduction:app2 --reload
#    - Test all three endpoints
#    - Verify each returns the correct page JSON
#
# 3. Run: uvicorn 01-introduction:app3 --reload
#    - Verify API metadata appears in /docs
#    - Verify GET / returns name and docs_url
# =============================================================================
