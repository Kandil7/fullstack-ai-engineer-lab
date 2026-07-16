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
from typing import List


# =============================================================================
# Exercise 1: Basic Template Rendering
# =============================================================================

app1 = FastAPI(title="Exercise 1 - Basic Templates")
templates = Jinja2Templates(directory="templates")


@app1.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    try:
        return templates.TemplateResponse(
            "home.html",
            {"request": request, "title": "Welcome to My Site", "content": "This is the homepage content."}
        )
    except Exception:
        return HTMLResponse(
            "<h1>Welcome to My Site</h1><p>This is the homepage content.</p>"
            "<p><small>Create a templates/home.html file for custom rendering.</small></p>"
        )


@app1.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    try:
        return templates.TemplateResponse(
            "about.html",
            {"request": request, "title": "About Us", "content": "We are learning FastAPI templates!"}
        )
    except Exception:
        return HTMLResponse(
            "<h1>About Us</h1><p>We are learning FastAPI templates!</p>"
            "<p><small>Create a templates/about.html file for custom rendering.</small></p>"
        )


# =============================================================================
# Exercise 2: Dynamic Content
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
    try:
        return templates2.TemplateResponse(
            "users.html",
            {"request": request, "users": users, "total": len(users)}
        )
    except Exception:
        user_list = "".join(
            f"<li>{u['name']} - {u['email']}</li>" for u in users
        )
        return HTMLResponse(
            f"<h1>Users ({len(users)})</h1><ul>{user_list}</ul>"
        )


@app2.get("/users/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    user = next((u for u in users if u["id"] == user_id), None)
    if user is None:
        try:
            return templates2.TemplateResponse(
                "404.html",
                {"request": request, "message": f"User {user_id} not found"},
                status_code=404
            )
        except Exception:
            return HTMLResponse(f"<h1>404 - User {user_id} not found</h1>", status_code=404)
    try:
        return templates2.TemplateResponse(
            "user.html",
            {"request": request, "user": user}
        )
    except Exception:
        return HTMLResponse(
            f"<h1>{user['name']}</h1><p>Email: {user['email']}</p>"
        )


# =============================================================================
# Exercise 3: Forms and Processing
# =============================================================================

app3 = FastAPI(title="Exercise 3 - Forms")
templates3 = Jinja2Templates(directory="templates")

# Storage for messages
messages: List[dict] = []


@app3.get("/contact", response_class=HTMLResponse)
async def contact_form(request: Request):
    try:
        return templates3.TemplateResponse(
            "contact.html",
            {"request": request}
        )
    except Exception:
        return HTMLResponse("""
        <h1>Contact Us</h1>
        <form method="post" action="/contact">
            <label>Name: <input type="text" name="name" required></label><br><br>
            <label>Email: <input type="email" name="email" required></label><br><br>
            <label>Message:<br><textarea name="message" rows="5" cols="40" required></textarea></label><br><br>
            <button type="submit">Send</button>
        </form>
        """)


@app3.post("/contact", response_class=HTMLResponse)
async def submit_contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
):
    msg = {"id": len(messages) + 1, "name": name, "email": email, "message": message}
    messages.append(msg)
    try:
        return templates3.TemplateResponse(
            "success.html",
            {"request": request, "name": name, "email": email}
        )
    except Exception:
        return HTMLResponse(f"""
        <h1>Thank you, {name}!</h1>
        <p>Your message has been received.</p>
        <a href="/messages">View all messages</a>
        """)


@app3.get("/messages", response_class=HTMLResponse)
async def list_messages(request: Request):
    try:
        return templates3.TemplateResponse(
            "messages.html",
            {"request": request, "messages": messages}
        )
    except Exception:
        msg_list = "".join(
            f"<li><strong>{m['name']}</strong> ({m['email']}): {m['message']}</li>"
            for m in messages
        ) if messages else "<li>No messages yet.</li>"
        return HTMLResponse(f"<h1>Messages</h1><ul>{msg_list}</ul>")


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
