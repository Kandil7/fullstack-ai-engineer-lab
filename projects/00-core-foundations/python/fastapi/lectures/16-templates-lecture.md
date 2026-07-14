# Lecture 16: FastAPI Templates

## Topic Overview

FastAPI supports server-side templating using Jinja2, allowing you to render dynamic HTML pages. This is essential for building full-stack applications where you need to serve HTML responses with dynamic content, rather than just JSON APIs.

**Why Templates Matter:**
- **Server-side rendering** - Generate HTML on the server
- **Dynamic content** - Insert variables, loops, conditions
- **SEO friendly** - Search engines can index rendered pages
- **Faster initial load** - No need to wait for JavaScript to render
- **MVC pattern** - Separate presentation from logic

**Common Use Cases:**
- Traditional web applications
- Admin dashboards
- Email templates
- Documentation sites
- Landing pages with dynamic content

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Set up Jinja2 templates** - Configure FastAPI for templating
2. **Create template files** - Build HTML templates with Jinja2 syntax
3. **Pass variables to templates** - Send data from Python to HTML
4. **Use template inheritance** - Create reusable base templates
5. **Implement loops and conditions** - Dynamic content generation
6. **Handle forms** - Process and display form data
7. **Add static files** - Serve CSS, JavaScript, images
8. **Build complete pages** - Full-stack web application

---

## Key Concepts

### 1. Template Syntax Overview

```jinja2
{# Comment #}

{# Variable #}
{{ variable }}

{# Expression #}
{{ 1 + 2 }}
{{ items | length }}

{# Control Flow #}
{% if condition %}
    ...
{% elif other_condition %}
    ...
{% else %}
    ...
{% endif %}

{% for item in items %}
    <p>{{ item }}</p>
{% endfor %}

{# Template Inheritance #}
{% extends "base.html" %}
{% block content %}...{% endblock %}
```

### 2. Directory Structure

```
project/
├── main.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   └── components/
│       ├── header.html
│       └── footer.html
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    └── images/
        └── logo.png
```

### 3. Template vs JSON Response

```
Template Response:
- HTML rendered on server
- Full page returned
- Good for SEO
- Server-side logic

JSON Response:
- Data only
- Client renders UI
- More interactive
- Client-side logic
```

---

## Code Examples

### Example 1: Basic Template Setup

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

# Configure templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Pass variables to template
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,  # Required by Jinja2
            "title": "My App",
            "content": "Welcome to FastAPI Templates!"
        }
    )
```

### Example 2: Template with Variables

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/users/")
async def list_users(request: Request):
    users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
    ]
    
    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "users": users,
            "title": "User List"
        }
    )
```

**users.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    
    <ul>
        {% for user in users %}
        <li>
            <strong>{{ user.name }}</strong>
            - {{ user.email }}
        </li>
        {% endfor %}
    </ul>
    
    <p>Total users: {{ users | length }}</p>
</body>
</html>
```

### Example 3: Template Inheritance

**templates/base.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My App{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/style.css">
    {% block head %}{% endblock %}
</head>
<body>
    <header>
        <nav>
            <a href="/">Home</a>
            <a href="/users">Users</a>
            <a href="/about">About</a>
        </nav>
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>&copy; 2024 My App</p>
    </footer>
    
    <script src="/static/js/main.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

**templates/index.html:**
```html
{% extends "base.html" %}

{% block title %}Home - My App{% endblock %}

{% block content %}
<h1>Welcome to My App</h1>
<p>This is the home page.</p>

{% if user %}
    <p>Hello, {{ user.name }}!</p>
{% else %}
    <p>Please <a href="/login">login</a>.</p>
{% endif %}
{% endblock %}
```

**templates/about.html:**
```html
{% extends "base.html" %}

{% block title %}About - My App{% endblock %}

{% block content %}
<h1>About Us</h1>
<p>We are a company that builds great things.</p>

<h2>Our Team</h2>
<ul>
    {% for member in team %}
    <li>{{ member.name }} - {{ member.role }}</li>
    {% endfor %}
</ul>
{% endblock %}
```

### Example 4: Template with Conditions

```python
@app.get("/dashboard/")
async def dashboard(request: Request):
    user = {
        "name": "Alice",
        "role": "admin",
        "is_premium": True
    }
    
    notifications = [
        {"message": "New order received", "type": "info"},
        {"message": "Low stock warning", "type": "warning"},
    ]
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "notifications": notifications
        }
    )
```

**dashboard.html:**
```html
{% extends "base.html" %}

{% block content %}
<h1>Dashboard</h1>

<div class="user-info">
    <h2>Welcome, {{ user.name }}!</h2>
    
    {% if user.role == "admin" %}
        <span class="badge">Admin</span>
    {% elif user.role == "moderator" %}
        <span class="badge">Moderator</span>
    {% else %}
        <span class="badge">User</span>
    {% endif %}
    
    {% if user.is_premium %}
        <p class="premium">Premium Member</p>
    {% endif %}
</div>

{% if notifications %}
    <div class="notifications">
        <h3>Notifications</h3>
        <ul>
            {% for notif in notifications %}
                <li class="{{ notif.type }}">
                    {{ notif.message }}
                </li>
            {% endfor %}
        </ul>
    </div>
{% else %}
    <p>No new notifications.</p>
{% endif %}
{% endblock %}
```

### Example 5: Template with Forms

```python
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/contact/")
async def contact_form(request: Request):
    return templates.TemplateResponse(
        "contact.html",
        {"request": request, "errors": {}}
    )

@app.post("/contact/")
async def submit_contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    # Validate
    errors = {}
    if len(name) < 2:
        errors["name"] = "Name must be at least 2 characters"
    if "@" not in email:
        errors["email"] = "Invalid email address"
    if len(message) < 10:
        errors["message"] = "Message must be at least 10 characters"
    
    if errors:
        return templates.TemplateResponse(
            "contact.html",
            {
                "request": request,
                "errors": errors,
                "values": {"name": name, "email": email, "message": message}
            }
        )
    
    # Process form (send email, save to DB, etc.)
    return RedirectResponse("/contact/success", status_code=303)
```

**contact.html:**
```html
{% extends "base.html" %}

{% block content %}
<h1>Contact Us</h1>

<form method="post" action="/contact/">
    <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" 
               value="{{ values.name if values else '' }}">
        {% if errors.name %}
            <span class="error">{{ errors.name }}</span>
        {% endif %}
    </div>
    
    <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" name="email"
               value="{{ values.email if values else '' }}">
        {% if errors.email %}
            <span class="error">{{ errors.email }}</span>
        {% endif %}
    </div>
    
    <div class="form-group">
        <label for="message">Message:</label>
        <textarea id="message" name="message" rows="5">{{ values.message if values else '' }}</textarea>
        {% if errors.message %}
            <span class="error">{{ errors.message }}</span>
        {% endif %}
    </div>
    
    <button type="submit">Send Message</button>
</form>
{% endblock %}
```

### Example 6: Template Filters

```python
@app.get("/products/")
async def products(request: Request):
    items = [
        {"name": "Laptop", "price": 999.99, "in_stock": True},
        {"name": "Phone", "price": 699.99, "in_stock": False},
        {"name": "Tablet", "price": 499.99, "in_stock": True},
    ]
    
    return templates.TemplateResponse(
        "products.html",
        {
            "request": request,
            "products": items,
            "current_date": datetime.now()
        }
    )
```

**products.html:**
```html
{% extends "base.html" %}

{% block content %}
<h1>Products</h1>

<p>Current date: {{ current_date.strftime('%B %d, %Y') }}</p>

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Price</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        {% for product in products %}
        <tr class="{{ 'out-of-stock' if not product.in_stock }}">
            <td>{{ product.name | upper }}</td>
            <td>${{ "%.2f" | format(product.price) }}</td>
            <td>
                {% if product.in_stock %}
                    <span class="badge success">In Stock</span>
                {% else %}
                    <span class="badge danger">Out of Stock</span>
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<p>Total products: {{ products | length }}</p>
{% endblock %}
```

### Example 7: Custom Template Filters

```python
from fastapi.templating import Jinja2Templates
from markupsafe import Markup

templates = Jinja2Templates(directory="templates")

# Custom filter
def format_currency(value: float) -> str:
    return f"${value:,.2f}"

def truncate_text(text: str, length: int = 50) -> str:
    if len(text) > length:
        return text[:length] + "..."
    return text

def nl2br(text: str) -> Markup:
    """Convert newlines to <br> tags"""
    return Markup(text.replace("\n", "<br>"))

# Add filters to template
templates.env.filters["currency"] = format_currency
templates.env.filters["truncate"] = truncate_text
templates.env.filters["nl2br"] = nl2br

@app.get("/blog/{post_id}")
async def blog_post(request: Request, post_id: int):
    post = get_post(post_id)
    return templates.TemplateResponse(
        "post.html",
        {
            "request": request,
            "post": post
        }
    )
```

**post.html:**
```html
<article>
    <h1>{{ post.title }}</h1>
    <p class="date">{{ post.date.strftime('%B %d, %Y') }}</p>
    <div class="content">
        {{ post.content | nl2br | safe }}
    </div>
    <p class="read-more">{{ post.excerpt | truncate(100) }}</p>
</article>
```

### Example 8: Template with Static Files

```python
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
```

**templates/base.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{% block title %}My App{% endblock %}</title>
    
    <!-- CSS -->
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    
    {% block head %}{% endblock %}
</head>
<body>
    {% include "components/navbar.html" %}
    
    <main class="container">
        {% block content %}{% endblock %}
    </main>
    
    {% include "components/footer.html" %}
    
    <!-- JavaScript -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/main.js"></script>
    
    {% block scripts %}{% endblock %}
</body>
</html>
```

---

## Common Mistakes to Avoid

### Mistake 1: Forgetting the Request Object

```python
# ❌ WRONG - Missing request
@app.get("/")
async def root():
    return templates.TemplateResponse("index.html", {"title": "Home"})

# ✅ CORRECT - Include request
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home"})
```

### Mistake 2: XSS Vulnerabilities

```python
# ❌ WRONG - Unescaped user input
user_input = "<script>alert('xss')</script>"
# In template: {{ user_input }}  # Escaped by default
# But: {{ user_input | safe }}  # ❌ XSS vulnerability!

# ✅ CORRECT - Let Jinja2 escape automatically
# Or use | safe only for trusted content
```

### Mistake 3: Not Using Template Inheritance

```python
# ❌ WRONG - Duplicating HTML structure in every template
# index.html - full HTML
# about.html - full HTML (same header/footer)
# contact.html - full HTML (same header/footer)

# ✅ CORRECT - Use template inheritance
# base.html - common structure
# index.html - extends base.html
# about.html - extends base.html
# contact.html - extends base.html
```

---

## Best Practices

1. **Always use template inheritance** - DRY principle for HTML
2. **Keep logic in Python** - Templates should be simple
3. **Use autoescaping** - Prevent XSS by default
4. **Organize templates** - Group related templates in folders
5. **Use components** - Reusable template fragments
6. **Cache templates** - Jinja2 caches by default
7. **Validate form data** - Always validate before processing
8. **Use static files** - Serve CSS, JS, images via StaticFiles

---

## Practice Exercises

### Exercise 1: Blog Application
Build a blog with:
- List of posts on homepage
- Individual post pages
- About page
- Contact form

### Exercise 2: Admin Dashboard
Create an admin dashboard with:
- User management table
- Statistics cards
- Charts (use Chart.js)
- Form for adding items

### Exercise 3: E-commerce Product Pages
Build product pages with:
- Product listing with filters
- Product detail pages
- Shopping cart view
- Checkout form

### Exercise 4: Documentation Site
Create documentation with:
- Sidebar navigation
- Content pages
- Search functionality
- Code highlighting

### Exercise 5: Email Templates
Build email templates:
- Welcome email
- Password reset
- Order confirmation
- Newsletter

---

## Summary

- **Templates** allow server-side HTML rendering
- **Jinja2** is the template engine for FastAPI
- **Always pass `request`** to TemplateResponse
- **Use template inheritance** to avoid code duplication
- **Autoescaping** prevents XSS by default
- **Static files** serve CSS, JS, images
- **Forms** require both GET (display) and POST (process) handlers
- **Filters** transform template output

---

## Further Reading

- [FastAPI Templates Documentation](https://fastapi.tiangolo.com/advanced/templates/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Jinja2 Template Designer](https://jinja.palletsprojects.com/en/3.1.x/templates/)
