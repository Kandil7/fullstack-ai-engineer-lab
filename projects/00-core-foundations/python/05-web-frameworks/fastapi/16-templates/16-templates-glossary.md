# Glossary: FastAPI Templates

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Template | HTML file with dynamic content | `index.html` |
| Jinja2 | Python template engine | `{{ variable }}` |
| Variable | Dynamic value in template | `{{ user.name }}` |
| Filter | Transform template output | `{{ name | upper }}` |
| Block | Overridable template section | `{% block title %}` |
| Inheritance | Base template extension | `{% extends "base.html" %}` |
| Include | Insert template fragment | `{% include "header.html" %}` |
| Control Flow | Loops and conditions | `{% for %}`, `{% if %}` |
| Macro | Reusable template function | `{% macro form() %}` |
| Autoescape | Auto HTML escaping | Enabled by default |
| Static Files | CSS, JS, images | `/static/css/style.css` |
| Mount | Serve static directory | `app.mount("/static")` |
| TemplateResponse | FastAPI response class | `templates.TemplateResponse()` |
| Component | Reusable template part | `components/header.html` |
| Context | Data passed to template | `{"request": request}` |

---

## Terms - Alphabetical Order

### Autoescape

**Definition:** Jinja2 feature that automatically escapes HTML special characters to prevent XSS attacks.

**Example:**
```python
# Autoescape is enabled by default
templates = Jinja2Templates(directory="templates")

# User input is escaped automatically
# Input: <script>alert('xss')</script>
# Output: &lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt;
```

**In template:**
```html
{# Autoescaped - safe #}
{{ user_input }}

{# Disabled autoescape - use only for trusted content #}
{{ trusted_html | safe }}
```

**Related Terms:** XSS, Safe Filter, Security

---

### Base Template

**Definition:** Foundation template containing common structure that other templates extend.

**Example:**
```html
{# templates/base.html #}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My App{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <header>
        {% block header %}
        <nav>...</nav>
        {% endblock %}
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        {% block footer %}
        <p>Copyright 2024</p>
        {% endblock %}
    </footer>
</body>
</html>
```

**Related Terms:** Template Inheritance, Block, Extend

---

### Block

**Definition:** Placeholder in base template that can be overridden by child templates.

**Example:**
```html
{# base.html #}
{% block title %}Default Title{% endblock %}
{% block content %}{% endblock %}
{% block scripts %}{% endblock %}

{# child.html #}
{% extends "base.html" %}

{% block title %}Custom Title{% endblock %}

{% block content %}
<h1>Custom Content</h1>
<p>This overrides the base template.</p>
{% endblock %}
```

**Related Terms:** Extend, Override, Template Inheritance

---

### Component

**Definition:** Reusable template fragment included in multiple pages.

**Example:**
```html
{# components/navbar.html #}
<nav class="navbar">
    <a href="/">Home</a>
    <a href="/about">About</a>
    <a href="/contact">Contact</a>
</nav>

{# components/footer.html #}
<footer>
    <p>&copy; 2024 My Company</p>
</footer>

{# Using components in base.html #}
<body>
    {% include "components/navbar.html" %}
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    {% include "components/footer.html" %}
</body>
```

**Related Terms:** Include, Partial, Reusable

---

### Context

**Definition:** Dictionary of variables passed to template for rendering.

**Example:**
```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/profile/{user_id}")
async def profile(request: Request, user_id: int):
    user = get_user(user_id)
    
    # Context dictionary
    context = {
        "request": request,      # Required
        "user": user,            # User object
        "title": "Profile",      # String
        "is_owner": True,        # Boolean
        "items": ["a", "b"],    # List
    }
    
    return templates.TemplateResponse("profile.html", context)
```

**In template:**
```html
<h1>{{ title }}</h1>
<p>User: {{ user.name }}</p>
{% if is_owner %}
    <a href="/edit">Edit Profile</a>
{% endif %}
```

**Related Terms:** TemplateResponse, Variables, Request

---

### Extend

**Definition:** Directive to inherit from a base template.

**Example:**
```html
{# index.html #}
{% extends "base.html" %}

{% block title %}Home Page{% endblock %}

{% block content %}
<h1>Welcome!</h1>
{% endblock %}
```

**Multiple levels:**
```html
{# base.html #}
{% block title %}Default{% endblock %}

{# layout.html #}
{% extends "base.html" %}
{% block title %}Layout{% endblock %}

{# page.html #}
{% extends "layout.html" %}
{% block title %}Page Title{% endblock %}
```

**Related Terms:** Base Template, Block, Inheritance

---

### Filter

**Definition:** Function that transforms template variable output.

**Example:**
```html
{# Built-in filters #}
{{ name | upper }}           {# JOHN #}
{{ name | lower }}           {# john #}
{{ name | capitalize }}      {# John #}
{{ name | title }}           {# John #}

{{ text | truncate(50) }}    {# First 50 chars... #}
{{ text | striptags }}       {# Remove HTML tags #}

{{ list | length }}          {# 5 #}
{{ list | first }}           {# First item #}
{{ list | last }}            {# Last item #}
{{ list | join(", ") }}      {# a, b, c #}

{{ price | currency }}       {# $1,234.56 #}
{{ date | dateformat }}      {# Jan 1, 2024 #}

{# Chaining filters #}
{{ name | lower | capitalize }}  {# John #}
```

**Related Terms:** Template Filters, Pipes, Transformations

---

### Include

**Definition:** Directive to insert another template's content.

**Example:**
```html
{# Simple include #}
{% include "components/header.html" %}

{# Include with context #}
{% include "components/alert.html" with {"message": "Hello!"} %}

{# Conditional include #}
{% include "components/sidebar.html" if show_sidebar %}

{# Silent failure if missing #}
{% include "components/optional.html" ignore missing %}
```

**Related Terms:** Component, Partial, Reusable

---

### Jinja2

**Definition:** Python template engine used by FastAPI for server-side HTML rendering.

**Example:**
```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "name": "World"}
    )
```

**Template syntax:**
```html
{# Comment #}
{{ variable }}
{% if condition %}...{% endif %}
{% for item in items %}...{% endfor %}
```

**Related Terms:** Template, FastAPI, Server-Side Rendering

---

### Macro

**Definition:** Reusable template function for generating repeated HTML.

**Example:**
```html
{# components/forms.html #}
{% macro input(name, label, type="text", value="", error="") %}
<div class="form-group">
    <label for="{{ name }}">{{ label }}</label>
    <input type="{{ type }}" id="{{ name }}" name="{{ name }}" value="{{ value }}">
    {% if error %}
        <span class="error">{{ error }}</span>
    {% endif %}
</div>
{% endmacro %}

{% macro textarea(name, label, value="", rows=4) %}
<div class="form-group">
    <label for="{{ name }}">{{ label }}</label>
    <textarea id="{{ name }}" name="{{ name }}" rows="{{ rows }}">{{ value }}</textarea>
</div>
{% endmacro %}

{# Using macros #}
{% from "components/forms.html" import input, textarea %}

<form>
    {{ input("name", "Name", value=form.name, error=errors.name) }}
    {{ input("email", "Email", type="email", value=form.email) }}
    {{ textarea("message", "Message", value=form.message) }}
</form>
```

**Related Terms:** Reusable, Function, Component

---

### Mount

**Definition:** FastAPI method to serve static files directory.

**Example:**
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Multiple static directories
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/media", StaticFiles(directory="media"), name="media")
```

**Usage in HTML:**
```html
<link rel="stylesheet" href="/static/css/style.css">
<script src="/static/js/main.js"></script>
<img src="/static/images/logo.png" alt="Logo">
```

**Related Terms:** Static Files, StaticFiles, Assets

---

### Request Object

**Definition:** Required variable passed to every Jinja2 template in FastAPI.

**Example:**
```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    # request is required by Jinja2
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,  # REQUIRED
            "title": "Home"
        }
    )
```

**Template access:**
```html
{# Access request properties #}
<p>URL: {{ request.url }}</p>
<p>Method: {{ request.method }}</p>
<p>Client: {{ request.client.host }}</p>
```

**Related Terms:** Context, TemplateResponse, ASGI

---

### Safe Filter

**Definition:** Jinja2 filter to disable HTML escaping for trusted content.

**Example:**
```html
{# Autoescaped (safe) #}
{{ user_input }}  {# <script> becomes &lt;script&gt; #}

{# Disable escaping (use carefully!) #}
{{ trusted_html | safe }}  {# Renders as HTML #}

{# Common use: rich text editor content #}
<div class="content">
    {{ post.content | safe }}
</div>
```

**Python side:**
```python
from markupsafe import Markup

def nl2br(text: str) -> Markup:
    """Convert newlines to <br> tags"""
    return Markup(text.replace("\n", "<br>"))

templates.env.filters["nl2br"] = nl2br
```

**Related Terms:** Autoescape, XSS, Markup

---

### Static Files

**Definition:** Files served directly without processing (CSS, JavaScript, images, fonts).

**Example:**
```
project/
├── main.py
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── bootstrap.min.css
│   ├── js/
│   │   ├── main.js
│   │   └── app.js
│   ├── images/
│   │   ├── logo.png
│   │   └── hero.jpg
│   └── fonts/
│       └── custom.woff2
└── templates/
    └── index.html
```

```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

**Related Terms:** Mount, StaticFiles, Assets

---

### Template

**Definition:** HTML file containing Jinja2 syntax for dynamic content generation.

**Example:**
```html
{# templates/user_list.html #}
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    
    {% if users %}
        <ul>
            {% for user in users %}
            <li>
                <strong>{{ user.name }}</strong>
                - {{ user.email }}
            </li>
            {% endfor %}
        </ul>
        <p>Total: {{ users | length }}</p>
    {% else %}
        <p>No users found.</p>
    {% endif %}
</body>
</html>
```

**Related Terms:** Jinja2, HTML, Dynamic Content

---

### Template Inheritance

**Definition:** Mechanism for templates to extend base templates, reusing common structure.

**Example:**
```html
{# base.html #}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Default{% endblock %}</title>
</head>
<body>
    <nav>{% block nav %}Default Nav{% endblock %}</nav>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>{% block footer %}Default Footer{% endblock %}</footer>
</body>
</html>

{# child.html #}
{% extends "base.html" %}

{% block title %}Custom Title{% endblock %}

{% block content %}
<h1>Custom Content</h1>
{% endblock %}

{# footer and nav inherit from base #}
```

**Related Terms:** Extend, Block, Base Template

---

### TemplateResponse

**Definition:** FastAPI class for returning rendered templates as HTTP responses.

**Example:**
```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Basic usage
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# With status code and headers
@app.get("/custom")
async def custom(request: Request):
    return templates.TemplateResponse(
        "page.html",
        {"request": request, "data": "value"},
        status_code=200,
        headers={"X-Custom": "header"}
    )

# With media type
@app.get("/json-or-html")
async def json_or_html(request: Request, format: str = "html"):
    if format == "json":
        return {"data": "value"}  # JSON response
    return templates.TemplateResponse("page.html", {"request": request})
```

**Related Terms:** Response, HTML, Context

---

### Variable

**Definition:** Dynamic value inserted into template using `{{ }}` syntax.

**Example:**
```python
@app.get("/user/{user_id}")
async def user_profile(request: Request, user_id: int):
    user = {
        "name": "Alice",
        "age": 30,
        "is_active": True,
        "roles": ["admin", "user"],
        "address": {"city": "NYC", "zip": "10001"}
    }
    
    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "user": user}
    )
```

**Template usage:**
```html
{# Simple variable #}
<h1>{{ user.name }}</h1>

{# Nested access #}
<p>{{ user.address.city }}</p>

{# List access #}
<p>First role: {{ user.roles[0] }}</p>

{# Expression #}
<p>Age in 5 years: {{ user.age + 5 }}</p>

{# Conditional #}
{% if user.is_active %}
    <span>Active</span>
{% endif %}

{# Loop #}
{% for role in user.roles %}
    <span class="badge">{{ role }}</span>
{% endfor %}
```

**Related Terms:** Context, Expression, Template

---

## Code Examples Collection

### Complete Template Setup

```python
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from typing import Optional

app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Custom filters
def format_date(value, fmt="%B %d, %Y"):
    return value.strftime(fmt)

templates.env.filters["dateformat"] = format_date

# Routes
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )

@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse(
        "about.html",
        {"request": request}
    )

@app.get("/contact")
async def contact_form(request: Request):
    return templates.TemplateResponse(
        "contact.html",
        {"request": request, "errors": {}, "values": {}}
    )

@app.post("/contact")
async def contact_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    # Validate
    errors = {}
    if len(name) < 2:
        errors["name"] = "Name too short"
    if "@" not in email:
        errors["email"] = "Invalid email"
    
    if errors:
        return templates.TemplateResponse(
            "contact.html",
            {"request": request, "errors": errors, "values": {"name": name, "email": email, "message": message}}
        )
    
    # Process form
    return RedirectResponse("/contact/success", status_code=303)

@app.get("/contact/success")
async def contact_success(request: Request):
    return templates.TemplateResponse(
        "success.html",
        {"request": request}
    )
```

### Template Helper Functions

```python
from markupsafe import Markup
from datetime import datetime

# Register custom filters
templates.env.filters["currency"] = lambda x: f"${x:,.2f}"
templates.env.filters["nl2br"] = lambda x: Markup(x.replace("\n", "<br>"))
templates.env.filters["timeago"] = lambda x: f"{(datetime.now() - x).days} days ago"

# Register global functions
templates.env.globals["now"] = datetime.now()
templates.env.globals["app_name"] = "My App"

# In template:
# {{ price | currency }}  →  $1,234.56
# {{ text | nl2br }}  →  text with <br> tags
# {{ date | timeago }}  →  5 days ago
# {{ now }}  →  current datetime
# {{ app_name }}  →  My App
```

---

## Quick Reference Card

### Template Syntax

```html
{# Comment #}

{{ variable }}
{{ object.property }}
{{ list[0] }}
{{ expr | filter }}

{% if condition %}...{% endif %}
{% for item in list %}...{% endfor %}

{% extends "base.html" %}
{% block name %}...{% endblock %}
{% include "partial.html" %}
{% from "macros.html" import macro %}
```

### Common Filters

| Filter | Output |
|--------|--------|
| `upper` | UPPERCASE |
| `lower` | lowercase |
| `capitalize` | Capitalize |
| `title` | Title Case |
| `truncate(50)` | First 50 chars... |
| `length` | 5 |
| `join(", ")` | a, b, c |
| `first` | First item |
| `last` | Last item |
| `sort` | Sorted list |
| `reverse` | Reversed list |

### FastAPI Template API

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "key": "value"}
    )
```

### File Structure

```
project/
├── main.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── components/
│       ├── header.html
│       └── footer.html
└── static/
    ├── css/
    ├── js/
    └── images/
```
