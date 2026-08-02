"""
11 - Background Tasks
=======================
Background tasks run after the response is sent to the client.
Useful for: sending emails, logging, cleanup, notifications.

Run: uvicorn 11-background-tasks:app --reload
"""

import time
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Background Tasks in FastAPI")


# ----- Background task functions -----
# These functions run AFTER the response is sent to the client.
# They must accept only simple arguments (or use Depends for DI).


def send_email(to: str, subject: str, body: str):
    """Simulate sending an email (takes time)."""
    print(f"\n📧 Sending email to {to}")
    print(f"   Subject: {subject}")
    print(f"   Body: {body}")
    time.sleep(1)  # Simulate SMTP delay
    print(f"   ✅ Email sent successfully at {datetime.now().isoformat()}\n")


def write_log(log_type: str, message: str, details: str = ""):
    """Simulate writing to a log file."""
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] [{log_type}] {message}"
    if details:
        log_entry += f" | {details}"
    print(f"📝 LOG: {log_entry}")


def process_image(image_url: str, output_format: str = "webp"):
    """Simulate background image processing."""
    print(f"\n🖼️  Processing image: {image_url}")
    time.sleep(2)  # Simulate heavy processing
    print(f"   ✅ Converted to {output_format}\n")


def generate_report(user_id: int, report_type: str):
    """Simulate report generation."""
    print(f"\n📊 Generating {report_type} report for user {user_id}")
    time.sleep(1)
    print(f"   ✅ Report generated\n")


# ----- Simple background task -----
@app.post("/notify/")
def notify_user(
    email: str,
    message: str,
    background_tasks: BackgroundTasks,
):
    """
    Send a notification email in the background.
    The client gets an immediate response; email sends asynchronously.
    """
    background_tasks.add_task(send_email, to=email, subject="Notification", body=message)
    return {"status": "queued", "message": "Notification will be sent shortly"}


# ----- Multiple background tasks -----
@app.post("/register/")
def register_user(
    email: str,
    name: str,
    background_tasks: BackgroundTasks,
):
    """
    Register user and trigger multiple background tasks.
    Tasks execute in order after the response is sent.
    """
    # These all run after the response
    background_tasks.add_task(write_log, "INFO", "New user registered", f"user={name}")
    background_tasks.add_task(
        send_email,
        to=email,
        subject="Welcome!",
        body=f"Hi {name}, welcome to our platform!",
    )
    background_tasks.add_task(
        send_email,
        to="admin@example.com",
        subject="New Registration",
        body=f"User {name} ({email}) just registered.",
    )

    return {"status": "registered", "name": name, "email": email}


# ----- Background task with Pydantic model -----
class OrderRequest(BaseModel):
    customer_email: str
    product: str
    quantity: int = 1


@app.post("/orders/")
def create_order(
    order: OrderRequest,
    background_tasks: BackgroundTasks,
):
    """
    Process an order and send confirmation in background.
    """
    background_tasks.add_task(
        write_log, "ORDER", "Order created", f"product={order.product}"
    )
    background_tasks.add_task(
        send_email,
        to=order.customer_email,
        subject=f"Order Confirmation - {order.product}",
        body=f"Your order for {order.quantity}x {order.product} has been placed!",
    )
    return {
        "status": "created",
        "order_id": 42,
        "product": order.product,
        "quantity": order.quantity,
    }


# ----- Simulated long-running background job -----
@app.post("/process/")
def trigger_processing(
    image_url: str,
    background_tasks: BackgroundTasks,
    format: str = "webp",
):
    """
    Trigger a long-running background job.
    Client doesn't wait for processing to finish.
    """
    background_tasks.add_task(process_image, image_url, format)
    background_tasks.add_task(write_log, "PROCESS", "Image processing started", image_url)
    return {
        "status": "processing_started",
        "image_url": image_url,
        "estimated_time": "2-5 seconds",
    }


# ----- Background task with Depends -----
def get_user_service():
    """Dependency that provides user-related utilities."""
    return {"service": "user-service", "version": "1.0"}


@app.post("/users/{user_id}/send-welcome/")
def send_welcome(
    user_id: int,
    background_tasks: BackgroundTasks,
    service: dict = Depends(get_user_service),
):
    """
    Background task that uses dependency injection.
    FastAPI resolves the dependency before passing to the task.
    """
    background_tasks.add_task(
        send_email,
        to=f"user{user_id}@example.com",
        subject="Welcome!",
        body=f"Hello User {user_id}! Your account is ready.",
    )
    background_tasks.add_task(
        write_log,
        "INFO",
        f"Welcome email queued via {service['service']}",
    )
    return {"status": "welcome_queued", "user_id": user_id}


"""
Testing with curl:
    curl -X POST "http://127.0.0.1:8000/notify/?email=alice@test.com&message=Hello"
    curl -X POST "http://127.0.0.1:8000/register/?email=bob@test.com&name=Bob"
    curl -X POST http://127.0.0.1:8000/orders/ -H "Content-Type: application/json" -d '{"customer_email": "charlie@test.com", "product": "Laptop", "quantity": 1}'
    curl -X POST "http://127.0.0.1:8000/process/?image_url=https://example.com/photo.jpg&format=png"
    curl -X POST http://127.0.0.1:8000/users/42/send-welcome/

    Check the terminal output for background task logs!
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
