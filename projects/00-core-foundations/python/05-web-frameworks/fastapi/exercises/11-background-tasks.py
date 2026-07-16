"""
FastAPI Exercise 11 - Background Tasks
=======================================

Topics covered:
- Using BackgroundTasks from FastAPI
- Running tasks after sending response
- Task dependencies and chaining
- Common use cases (email, logging, cleanup)

Requirements:
    pip install fastapi uvicorn

Run any exercise:
    uvicorn 11-background-tasks:app1 --reload
    uvicorn 11-background-tasks:app2 --reload
    uvicorn 11-background-tasks:app3 --reload
"""

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import time


# =============================================================================
# Exercise 1: Simple Background Task
# =============================================================================

app1 = FastAPI(title="Exercise 1 - Simple Background Task")


class EmailRequest(BaseModel):
    email: str
    message: str


def send_email_task(email: str, message: str):
    """Simulate sending an email with a delay."""
    time.sleep(2)
    print(f"  [Background] Sending email to {email}: {message}")


@app1.post("/send-email")
async def send_email(request: EmailRequest, background_tasks: BackgroundTasks):
    """Send email via background task - returns immediately."""
    background_tasks.add_task(send_email_task, request.email, request.message)
    return {"status": "sent", "email": request.email}


# =============================================================================
# Exercise 2: Background Task with Multiple Steps
# =============================================================================

app2 = FastAPI(title="Exercise 2 - Multi-step Background Task")

users_db = {}


class RegisterRequest(BaseModel):
    username: str
    email: str


def register_user_background(username: str, email: str):
    """Handle multi-step registration in background."""
    time.sleep(0.5)
    print(f"  [Background] Saving user {username} to database...")
    users_db[username] = {"username": username, "email": email}
    time.sleep(0.5)
    print(f"  [Background] Sending welcome email to {email}...")
    time.sleep(0.5)
    print(f"  [Background] Registration logged for {username}")


@app2.post("/register")
async def register_user(request: RegisterRequest, background_tasks: BackgroundTasks):
    """Register user - background task handles email, logging."""
    background_tasks.add_task(
        register_user_background, request.username, request.email
    )
    return {"status": "registered", "username": request.username}


# =============================================================================
# Exercise 3: Background Tasks with Dependencies
# =============================================================================

app3 = FastAPI(title="Exercise 3 - Chained Background Tasks")


class OrderRequest(BaseModel):
    order_id: str
    items: list[str]
    total: float


def process_payment(order_id: str, total: float):
    """Simulate payment processing."""
    time.sleep(1)
    print(f"  [Background] Processing payment of ${total} for {order_id}...")


def update_inventory(items: list[str]):
    """Simulate inventory update."""
    time.sleep(1)
    print(f"  [Background] Updating inventory for items: {items}...")


def send_confirmation(order_id: str):
    """Simulate sending confirmation email."""
    time.sleep(0.5)
    print(f"  [Background] Sending confirmation for {order_id}...")


def log_analytics(order_id: str, items: list[str], total: float):
    """Simulate logging analytics event."""
    time.sleep(0.5)
    print(f"  [Background] Logging analytics for {order_id}: {len(items)} items, ${total}")


@app3.post("/orders")
async def create_order(request: OrderRequest, background_tasks: BackgroundTasks):
    """Create order - chain multiple background tasks."""
    background_tasks.add_task(process_payment, request.order_id, request.total)
    background_tasks.add_task(update_inventory, request.items)
    background_tasks.add_task(send_confirmation, request.order_id)
    background_tasks.add_task(log_analytics, request.order_id, request.items, request.total)
    return {"status": "processing", "order_id": request.order_id}
