"""
07 - Form Data
================
Handling HTML form submissions (application/x-www-form-urlencoded)
and multipart/form-data in FastAPI.

Requires: pip install python-multipart

Run: uvicorn 07-form-data:app --reload
"""

import sys
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Form Data in FastAPI")


# ----- Simple form login -----
@app.post("/login/")
def login(username: str = Form(...), password: str = Form(...)):
    """
    Form(...) means the field is required.
    FastAPI automatically reads form fields from the request body.
    Content-Type: application/x-www-form-urlencoded
    """
    if username == "admin" and password == "secret":
        return {"message": "Login successful", "username": username}
    raise HTTPException(status_code=401, detail="Invalid credentials")


# ----- Form with optional fields -----
@app.post("/contact/")
def contact_form(
    name: str = Form(..., min_length=1),
    email: str = Form(...),
    subject: str = Form(default="General Inquiry"),
    message: str = Form(..., min_length=10),
    subscribe: bool = Form(default=False),
):
    """
    Form submission with required and optional fields.
    """
    return {
        "status": "received",
        "name": name,
        "email": email,
        "subject": subject,
        "message_length": len(message),
        "subscribed": subscribe,
    }


# ----- Registration form -----
class RegistrationResult(BaseModel):
    username: str
    email: str
    role: str
    message: str


@app.post("/register/", response_model=RegistrationResult)
def register_user(
    username: str = Form(..., min_length=3, max_length=20),
    email: str = Form(...),
    password: str = Form(..., min_length=8),
    confirm_password: str = Form(...),
    role: str = Form(default="user"),
):
    """
    Registration form with password confirmation validation.
    """
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    valid_roles = ["user", "admin", "moderator"]
    if role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Must be one of: {valid_roles}",
        )

    return RegistrationResult(
        username=username,
        email=email,
        role=role,
        message="Registration successful!",
    )


# ----- Form + JSON body -----
@app.post("/feedback/")
def submit_feedback(
    rating: int = Form(..., ge=1, le=5),
    comment: str = Form(default=""),
    recommend: bool = Form(default=True),
):
    """
    Form data with validation constraints.
    rating: ge=1, le=5 means 1-5 scale.
    """
    return {
        "status": "submitted",
        "rating": rating,
        "stars": "★" * rating + "☆" * (5 - rating),
        "comment_length": len(comment),
        "would_recommend": recommend,
    }


# ----- Form with file-like data -----
@app.post("/profile-update/")
def update_profile(
    full_name: str = Form(...),
    bio: str = Form(default="", max_length=500),
    website: str = Form(default=""),
    location: str = Form(default=""),
):
    """
    Profile update via form fields.
    In real apps, use UploadFile for file uploads (see 08-file-upload.py).
    """
    return {
        "updated": True,
        "profile": {
            "full_name": full_name,
            "bio": bio,
            "website": website,
            "location": location,
        },
    }


# ----- Serve an HTML form -----
@app.get("/form", response_class=HTMLResponse)
def get_form():
    """Serve a simple HTML form for testing."""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>FastAPI Form Demo</title></head>
    <body>
        <h1>Contact Form</h1>
        <form action="/contact/" method="post">
            <label>Name: <input type="text" name="name" required></label><br><br>
            <label>Email: <input type="email" name="email" required></label><br><br>
            <label>Subject: <input type="text" name="subject" value="General Inquiry"></label><br><br>
            <label>Message:<br>
                <textarea name="message" required minlength="10"></textarea>
            </label><br><br>
            <label><input type="checkbox" name="subscribe" value="true"> Subscribe to newsletter</label><br><br>
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """


# ----- Multiple forms on same page -----
@app.get("/multi-form", response_class=HTMLResponse)
def get_multi_form():
    """Serve an HTML page with login and registration forms."""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Multi-Form Demo</title></head>
    <body>
        <h1>Login</h1>
        <form action="/login/" method="post">
            <input type="text" name="username" placeholder="Username" required><br><br>
            <input type="password" name="password" placeholder="Password" required><br><br>
            <button type="submit">Login</button>
        </form>

        <hr>

        <h1>Register</h1>
        <form action="/register/" method="post">
            <input type="text" name="username" placeholder="Username (3-20 chars)" required><br><br>
            <input type="email" name="email" placeholder="Email" required><br><br>
            <input type="password" name="password" placeholder="Password (min 8 chars)" required><br><br>
            <input type="password" name="confirm_password" placeholder="Confirm Password" required><br><br>
            <select name="role">
                <option value="user">User</option>
                <option value="admin">Admin</option>
                <option value="moderator">Moderator</option>
            </select><br><br>
            <button type="submit">Register</button>
        </form>
    </body>
    </html>
    """


"""
Testing with curl:
    curl -X POST http://127.0.0.1:8000/login/ -d "username=admin&password=secret"
    curl -X POST http://127.0.0.1:8000/contact/ -d "name=Alice&email=alice@test.com&message=Hello+FastAPI"
    curl -X POST http://127.0.0.1:8000/register/ -d "username=alice&email=alice@test.com&password=password123&confirm_password=password123&role=user"
    curl -X POST http://127.0.0.1:8000/feedback/ -d "rating=5&comment=Great+API&recommend=true"
    curl -X POST http://127.0.0.1:8000/profile-update/ -d "full_name=Alice+Smith&bio=Developer&website=https://alice.dev"

    Open in browser:
    http://127.0.0.1:8000/form
    http://127.0.0.1:8000/multi-form
"""

def _verify():
    """Smoke-test the app in-process with TestClient (no real server)."""
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        print("[skip] fastapi not installed")
        return

    client = TestClient(app)

    r = client.post("/login/", data={"username": "admin", "password": "secret"})
    assert r.status_code == 200
    assert r.json()["message"] == "Login successful"

    r = client.post("/login/", data={"username": "admin", "password": "wrong"})
    assert r.status_code == 401

    r = client.post(
        "/contact/",
        data={"name": "Alice", "email": "alice@test.com", "message": "Hello FastAPI"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "received"

    r = client.post(
        "/register/",
        data={
            "username": "alice", "email": "alice@test.com",
            "password": "password123", "confirm_password": "password123",
            "role": "user",
        },
    )
    assert r.status_code == 200
    assert r.json()["message"] == "Registration successful!"

    r = client.post(
        "/register/",
        data={
            "username": "bob", "email": "bob@test.com",
            "password": "password123", "confirm_password": "different",
        },
    )
    assert r.status_code == 400  # Password mismatch

    r = client.post("/feedback/", data={"rating": 5, "comment": "Great API"})
    assert r.status_code == 200
    assert r.json()["rating"] == 5

    r = client.post("/feedback/", data={"rating": 9})
    assert r.status_code == 422  # rating must be 1-5

    r = client.post(
        "/profile-update/",
        data={"full_name": "Alice Smith", "bio": "Developer"},
    )
    assert r.status_code == 200
    assert r.json()["updated"] is True

    r = client.get("/form")
    assert r.status_code == 200
    assert "Contact Form" in r.text

    print("[OK] 07-form-data: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        _verify()
