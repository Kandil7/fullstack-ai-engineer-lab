"""
FastAPI Exercise 16 - Templates
================================

Topics covered:
- Jinja2 templates in FastAPI
- Rendering HTML pages
- Template inheritance
- Passing data to templates

Requirements:
    pip install fastapi uvicorn jinja2 python-multipart

Run any exercise:
    uvicorn 16-templates:app1 --reload
    uvicorn 16-templates:app2 --reload
    uvicorn 16-templates:app3 --reload

Note: Create a 'templates/' directory with HTML files before running.
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List


# =============================================================================
# Exercise 1: Basic Template Rendering
# =============================================================================
# Create a simple page renderer:
#   - GET / shows a homepage with title and content
#   - GET /about shows an about page
#   - Use Jinja2Templates for rendering
#   - Templates directory: "./templates"
#
# Hints:
#   - Initialize: templates = Jinja2Templates(directory="templates")
#   - Render: return templates.TemplateResponse("page.html", {"request": request, ...})
#   - In templates: use {{ variable }} for variables
#
# Expected behavior:
#   GET http://localhost:8000/ -> HTML page with "Welcome to My Site"
#   GET http://localhost:8000/about -> HTML page with about info
#
# Test with:
#   curl http://localhost:8000/
#   Open browser: http://localhost:8000/
# =============================================================================

app1 = FastAPI(title="Exercise 1 - Basic Templates")
templates = Jinja2Templates(directory="templates")


@app1.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    # TODO: Render homepage template
    pass


@app1.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    # TODO: Render about template
    pass


# =============================================================================
# Exercise 2: Dynamic Content
# =============================================================================
# Create a page that displays dynamic data:
#   - GET /users shows a list of users
#   - GET /users/{user_id} shows user profile
#   - Pass data to template: users list, current user
#   - Handle 404 if user not found
#
# Hints:
#   - Pass data dict: {"request": request, "users": users, "current_user": user}
#   - In templates: use {% for user in users %} for loops
#   - Use {% if user %} for conditional rendering
#
# Expected behavior:
#   GET http://localhost:8000/users -> HTML list of users
#   GET http://localhost:8000/users/1 -> User profile page
#   GET http://localhost:8000/users/999 -> 404 page
#
# Test with:
#   curl http://localhost:8000/users
#   curl http://localhost:8000/users/1
# =============================================================================

app2 = FastAPI(title="Exercise 2 - Dynamic Templates")
templates2 = Jinja2Templates(directory="templates")

# Sample data
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
]


@app2.get("/users", response_class=HTMLResponse)
async def list_users(request: Request):
    # TODO: Render users list template
    pass


@app2.get("/users/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    # TODO: Render single user template
    pass


# =============================================================================
# Exercise 3: Forms and Processing
# =============================================================================
# Create a form-based application:
#   - GET /contact shows a contact form
#   - POST /contact processes the form
#   - GET /messages shows submitted messages
#   - Store messages in a list
#
# Hints:
#   - Use Form(...) for form fields
#   - In template: use <form method="post" action="/contact">
#   - Access form data with await request.form()
#   - Redirect after POST: return RedirectResponse("/messages")
#
# Expected behavior:
#   GET http://localhost:8000/contact -> HTML form
#   POST http://localhost:8000/contact -> Process and redirect
#   GET http://localhost:8000/messages -> List of messages
#
# Test with:
#   curl http://localhost:8000/contact
#   curl -X POST http://localhost:8000/contact -d "name=Test&email=test@example.com&message=Hello"
# =============================================================================

app3 = FastAPI(title="Exercise 3 - Forms")
templates3 = Jinja2Templates(directory="templates")

# Storage for messages
messages: List[dict] = []


@app3.get("/contact", response_class=HTMLResponse)
async def contact_form(request: Request):
    # TODO: Render contact form template
    pass


@app3.post("/contact", response_class=HTMLResponse)
async def submit_contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
):
    # TODO: Process form and show success page
    pass


@app3.get("/messages", response_class=HTMLResponse)
async def list_messages(request: Request):
    # TODO: Render messages list template
    pass


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# After completing the exercises:
#
# 1. Create templates/ directory with required HTML files:
#    - templates/home.html
#    - templates/about.html
#    - templates/users.html
#    - templates/user.html
#    - templates/404.html
#    - templates/contact.html
#    - templates/success.html
#    - templates/messages.html
#
# 2. Run: uvicorn 16-templates:app1 --reload
#    - Verify homepage and about pages render
#
# 3. Run: uvicorn 16-templates:app2 --reload
#    - Test users list and individual profiles
#
# 4. Run: uvicorn 16-templates:app3 --reload
#    - Test form submission and message display
# =============================================================================
