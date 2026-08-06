"""
16 - Templates
================
Serving HTML templates with Jinja2 in FastAPI.
Useful for server-rendered pages alongside your API.

Requires: pip install jinja2

Run: uvicorn 16-templates:app --reload
"""

import sys
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Templates in FastAPI")

# Initialize templates directory
templates = Jinja2Templates(directory="templates")

# Create templates directory if it doesn't exist
import os
os.makedirs("templates", exist_ok=True)

# ----- Create template files programmatically -----
# In production, these would be separate .html files

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ title }}</h1>
    <p>Welcome, {{ name }}!</p>
    <p>Current time: {{ timestamp }}</p>
    <ul>
    {% for item in items %}
        <li>{{ item.name }} - ${{ item.price }}</li>
    {% endfor %}
    </ul>
</body>
</html>
"""

USER_PROFILE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>User Profile</title></head>
<body>
    <h1>{{ user.name }}</h1>
    <p>Email: {{ user.email }}</p>
    <p>Age: {{ user.age }}</p>
    {% if user.bio %}
        <p>Bio: {{ user.bio }}</p>
    {% endif %}
    <p>Member since: {{ user.created_at }}</p>
    <a href="/dashboard">Back to Dashboard</a>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Dashboard</title></head>
<body>
    <h1>Dashboard</h1>
    <p>Welcome back, {{ user.name }}!</p>
    <h2>Your Items:</h2>
    <table border="1">
        <tr><th>Name</th><th>Price</th><th>In Stock</th></tr>
        {% for item in items %}
        <tr>
            <td>{{ item.name }}</td>
            <td>${{ "%.2f"|format(item.price) }}</td>
            <td>{{ "Yes" if item.in_stock else "No" }}</td>
        </tr>
        {% endfor %}
    </table>
    <p>Total items: {{ items|length }}</p>
</body>
</html>
"""

ERROR_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Error {{ status_code }}</title></head>
<body>
    <h1>Error {{ status_code }}</h1>
    <p>{{ message }}</p>
    <a href="/">Go Home</a>
</body>
</html>
"""

# Write templates to files
with open("templates/index.html", "w") as f:
    f.write(INDEX_TEMPLATE)
with open("templates/profile.html", "w") as f:
    f.write(USER_PROFILE_TEMPLATE)
with open("templates/dashboard.html", "w") as f:
    f.write(DASHBOARD_TEMPLATE)
with open("templates/error.html", "w") as f:
    f.write(ERROR_TEMPLATE)


# ----- Routes -----
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Render the home page with template variables."""
    items = [
        {"name": "Laptop", "price": 999.99},
        {"name": "Phone", "price": 699.99},
        {"name": "Tablet", "price": 499.99},
    ]
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "FastAPI Templates Demo",
            "name": "Developer",
            "items": items,
            "timestamp": datetime.now().isoformat(),
        },
    )


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    """Dashboard page with user data and items."""
    user = {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30,
        "bio": "Full-stack developer",
        "created_at": "2024-01-15",
    }
    items = [
        {"name": "Widget A", "price": 29.99, "in_stock": True},
        {"name": "Widget B", "price": 49.99, "in_stock": False},
        {"name": "Widget C", "price": 19.99, "in_stock": True},
    ]
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user, "items": items},
    )


@app.get("/users/{user_id}", response_class=HTMLResponse)
def user_profile(request: Request, user_id: int):
    """Dynamic user profile page."""
    users = {
        1: {"name": "Alice", "email": "alice@test.com", "age": 30, "bio": "Developer", "created_at": "2024-01"},
        2: {"name": "Bob", "email": "bob@test.com", "age": 25, "bio": None, "created_at": "2024-03"},
    }
    user = users.get(user_id)
    if not user:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "status_code": 404, "message": f"User {user_id} not found"},
            status_code=404,
        )
    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "user": user},
    )


# ----- Template with API data -----
@app.get("/products-page", response_class=HTMLResponse)
def products_page(request: Request):
    """Template that could combine API data with rendering."""
    products = [
        {"name": "Laptop", "price": 999.99, "category": "Electronics"},
        {"name": "Book", "price": 19.99, "category": "Education"},
        {"name": "Headphones", "price": 149.99, "category": "Electronics"},
    ]
    categories = list(set(p["category"] for p in products))

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Products</title></head>
    <body>
        <h1>Products ({len(products)} items)</h1>
        <h2>Categories: {', '.join(categories)}</h2>
        <ul>
        {''.join(f"<li>{p['name']} - ${p['price']} ({p['category']})</li>" for p in products)}
        </ul>
        <p>Rendered at: {datetime.now().isoformat()}</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


"""
Testing with curl:
    curl http://127.0.0.1:8000/
    curl http://127.0.0.1:8000/dashboard
    curl http://127.0.0.1:8000/users/1
    curl http://127.0.0.1:8000/users/999  # 404 page
    curl http://127.0.0.1:8000/products-page

    Open in browser for best experience!
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
    assert "FastAPI Templates Demo" in r.text

    r = client.get("/dashboard")
    assert r.status_code == 200
    assert "Widget A" in r.text

    r = client.get("/users/1")
    assert r.status_code == 200
    assert "alice@test.com" in r.text

    r = client.get("/users/999")
    assert r.status_code == 404
    assert "not found" in r.text

    r = client.get("/products-page")
    assert r.status_code == 200
    assert "Products" in r.text

    print("[OK] 16-templates: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        _verify()
