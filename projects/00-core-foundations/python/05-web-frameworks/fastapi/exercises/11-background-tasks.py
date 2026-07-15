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
import json


# =============================================================================
# Exercise 1: Simple Background Task
# =============================================================================
# Create an endpoint that:
#   1. Receives a POST request with {"email": "...", "message": "..."}
#   2. Immediately returns {"status": "sent", "email": "..."}
#   3. In background: simulate sending email (sleep 2s, log to console)
#
# Hints:
#   - Define a separate function for the background work
#   - Add it with background_tasks.add_task()
#   - The response is sent BEFORE the task completes
#
# Expected behavior:
#   POST http://localhost:8000/send-email
#   Body: {"email": "test@example.com", "message": "Hello!"}
#   Response: {"status": "sent", "email": "test@example.com"} (immediate)
#   Console: "Sending email to test@example.com..." (after ~2s)
#
# Test with:
#   curl -X POST http://localhost:8000/send-email \
#     -H "Content-Type: application/json" \
#     -d '{"email": "test@example.com", "message": "Hello!"}'
# =============================================================================

app1 = FastAPI(title="Exercise 1 - Simple Background Task")


class EmailRequest(BaseModel):
    email: str
    message: str


# TODO: Create a background function for sending email
def send_email_task(email: str, message: str):
    # TODO: Simulate email sending
    pass


@app1.post("/send-email")
async def send_email(request: EmailRequest, background_tasks: BackgroundTasks):
    # TODO: Add background task and return response
    pass


# =============================================================================
# Exercise 2: Background Task with Multiple Steps
# =============================================================================
# Create an endpoint for user registration that:
#   1. Receives {"username": "...", "email": "..."}
#   2. Returns {"status": "registered", "username": "..."}
#   3. Background task does:
#      a. Save user to a "database" (dict/file)
#      b. Send welcome email
#      c. Log the registration
#
# Hints:
#   - Create a single function that does all steps
#   - Pass all needed parameters to the background function
#   - Use print() for logging (simulating a logging service)
#
# Expected behavior:
#   POST http://localhost:8000/register
#   Body: {"username": "john", "email": "john@example.com"}
#   Response: {"status": "registered", "username": "john"} (immediate)
#   Console output (in background):
#     "Saving user john to database..."
#     "Sending welcome email to john@example.com..."
#     "Registration logged for john"
#
# Test with:
#   curl -X POST http://localhost:8000/register \
#     -H "Content-Type: application/json" \
#     -d '{"username": "john", "email": "john@example.com"}'
# =============================================================================

app2 = FastAPI(title="Exercise 2 - Multi-step Background Task")

# Simulated database
users_db = {}


class RegisterRequest(BaseModel):
    username: str
    email: str


# TODO: Create a background function for user registration
def register_user_background(username: str, email: str):
    # TODO: Implement multi-step registration
    pass


@app2.post("/register")
async def register_user(request: RegisterRequest, background_tasks: BackgroundTasks):
    # TODO: Add background task and return response
    pass


# =============================================================================
# Exercise 3: Background Tasks with Dependencies
# =============================================================================
# Create an endpoint that processes an order:
#   1. Receives {"order_id": "...", "items": ["item1", "item2"], "total": 100}
#   2. Returns {"status": "processing", "order_id": "..."}
#   3. Background tasks (in order):
#      a. Process payment
#      b. Update inventory
#      c. Send confirmation email
#      d. Log analytics event
#
# Hints:
#   - Each step should be a separate function
#   - Chain them in the background task function
#   - Pass the order data between functions
#
# Expected behavior:
#   POST http://localhost:8000/orders
#   Body: {"order_id": "ORD-001", "items": ["laptop", "mouse"], "total": 1299}
#   Response: {"status": "processing", "order_id": "ORD-001"}
#   Console: "Processing payment for ORD-001..."
#            "Updating inventory..."
#            "Sending confirmation..."
#            "Logging analytics..."
#
# Test with:
#   curl -X POST http://localhost:8000/orders \
#     -H "Content-Type: application/json" \
#     -d '{"order_id": "ORD-001", "items": ["laptop"], "total": 999}'
# =============================================================================

app3 = FastAPI(title="Exercise 3 - Chained Background Tasks")


class OrderRequest(BaseModel):
    order_id: str
    items: list[str]
    total: float


# TODO: Create background functions for each step
def process_payment(order_id: str, total: float):
    # TODO: Simulate payment processing
    pass


def update_inventory(items: list[str]):
    # TODO: Simulate inventory update
    pass


def send_confirmation(order_id: str):
    # TODO: Send confirmation email
    pass


def log_analytics(order_id: str, items: list[str], total: float):
    # TODO: Log analytics event
    pass


@app3.post("/orders")
async def create_order(request: OrderRequest, background_tasks: BackgroundTasks):
    # TODO: Chain all background tasks in order
    pass


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# After completing the exercises:
#
# 1. Run: uvicorn 11-background-tasks:app1 --reload
#    - POST /send-email should return immediately
#    - Check console for delayed email log
#
# 2. Run: uvicorn 11-background-tasks:app2 --reload
#    - POST /register should return immediately
#    - Check console for all 3 steps logged in background
#
# 3. Run: uvicorn 11-background-tasks:app3 --reload
#    - POST /orders should return immediately
#    - Check console for all 4 steps executed in sequence
# =============================================================================
