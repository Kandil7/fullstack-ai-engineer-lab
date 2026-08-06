# Lecture 11: FastAPI Background Tasks

## Topic Overview

Background tasks in FastAPI allow you to execute code after the response has been sent to the client. This is crucial for operations that don't need to block the user's request but still need to happen - like sending emails, processing uploads, updating analytics, or cleaning up resources.

**Why Background Tasks Matter:**
- **Improved response times** - Return responses immediately while heavy processing happens in the background
- **Better resource utilization** - Keep servers responsive under load
- **User experience** - Users don't wait for slow operations
- **Reliability** - Retry failed operations without affecting the main request

**Common Use Cases:**
- Sending confirmation emails after user registration
- Processing uploaded files (images, videos, documents)
- Updating analytics and metrics
- Cleaning up temporary files
- Syncing data with external services
- Generating reports

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Understand background task architecture** - How tasks are executed after responses
2. **Use FastAPI's BackgroundTasks** - Implement basic background processing
3. **Chain background tasks** - Execute multiple tasks in sequence
4. **Pass dependencies** - Use dependencies in background tasks
5. **Handle errors gracefully** - Implement error handling for background operations
6. **Choose the right approach** - When to use BackgroundTasks vs Celery vs async
7. **Monitor task execution** - Track and log background task progress
8. **Handle task failures** - Implement retry mechanisms

---

## Key Concepts

### 1. What Are Background Tasks?

Background tasks are functions that run after FastAPI sends the response to the client. They're perfect for:

- Operations that don't affect the immediate response
- Tasks that can tolerate delays
- Work that shouldn't block the event loop

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

@app.post("/users/")
async def create_user(background_tasks: BackgroundTasks):
    # This runs immediately
    user = create_user_in_db()
    
    # This runs AFTER the response is sent
    background_tasks.add_task(send_welcome_email, user.email)
    
    return {"message": "User created"}
```

### 2. Task Execution Model

```
Client Request
     │
     ▼
┌─────────────────┐
│  Endpoint       │
│  - Create user  │
│  - Add task     │
│  - Return 201   │
└─────────────────┘
     │
     ▼ (Response sent to client)
┌─────────────────┐
│  Background     │
│  Task Executes  │
│  - Send email   │
└─────────────────┘
```

### 3. Task Queue Behavior

FastAPI processes background tasks in order, one at a time. This ensures:
- Tasks don't conflict with each other
- Resource contention is minimized
- Predictable execution order

---

## Code Examples

### Example 1: Basic Background Task

```python
from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

def process_data(data: dict):
    """Simulate slow processing"""
    time.sleep(5)  # Simulate work
    print(f"Processed: {data}")

@app.post("/upload/")
async def upload_data(background_tasks: BackgroundTasks):
    data = {"content": "uploaded file"}
    
    # Add task to run after response
    background_tasks.add_task(process_data, data)
    
    return {"message": "Upload received, processing in background"}
```

### Example 2: Email Sending Background Task

```python
from fastapi import FastAPI, BackgroundTasks
from pydantic import EmailStr
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

def send_email(email: EmailStr, subject: str, body: str):
    """Send email in background"""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "noreply@example.com"
    msg["To"] = email
    
    # In production, use proper email service
    with smtplib.SMTP("localhost") as server:
        server.send_message(msg)
    print(f"Email sent to {email}")

@app.post("/register/")
async def register_user(
    email: EmailStr,
    name: str,
    background_tasks: BackgroundTasks
):
    # Create user in database
    user = {"email": email, "name": name}
    
    # Send welcome email in background
    background_tasks.add_task(
        send_email,
        email,
        "Welcome!",
        f"Hi {name}, welcome to our service!"
    )
    
    return {"message": "Registration successful"}
```

### Example 3: Multiple Chained Tasks

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def validate_file(file_path: str):
    """First task: validate the file"""
    print(f"Validating {file_path}")
    # Validation logic here
    return True

def process_file(file_path: str):
    """Second task: process the file"""
    print(f"Processing {file_path}")
    # Processing logic here

def update_analytics(file_path: str, success: bool):
    """Third task: update analytics"""
    print(f"Analytics updated for {file_path}: {success}")

@app.post("/files/")
async def upload_file(background_tasks: BackgroundTasks):
    file_path = "/uploads/document.pdf"
    
    # Chain tasks - each receives the return value of previous
    background_tasks.add_task(validate_file, file_path)
    background_tasks.add_task(process_file, file_path)
    background_tasks.add_task(update_analytics, file_path, True)
    
    return {"message": "File upload queued"}
```

### Example 4: Background Tasks with Dependencies

```python
from fastapi import FastAPI, BackgroundTasks, Depends
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def notify_admin(db: Session, user_email: str):
    """Background task using database dependency"""
    # Note: Dependencies are resolved at task execution time
    admin = db.query(User).filter(User.role == "admin").first()
    if admin:
        send_notification(admin.email, f"New user: {user_email}")

@app.post("/users/")
async def create_user(
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    user = User(email=email)
    db.add(user)
    db.commit()
    
    # Pass db dependency to background task
    background_tasks.add_task(notify_admin, db, email)
    
    return {"message": "User created"}
```

### Example 5: Error Handling in Background Tasks

```python
from fastapi import FastAPI, BackgroundTasks
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

def risky_operation(data: dict):
    """Background task that might fail"""
    try:
        # Simulate operation that might fail
        if data.get("force_error"):
            raise ValueError("Operation failed!")
        
        logger.info("Operation completed successfully")
    except Exception as e:
        logger.error(f"Background task failed: {e}")
        # Store error for later inspection
        # Could also retry or send alert

@app.post("/process/")
async def process_data(background_tasks: BackgroundTasks):
    data = {"content": "some data", "force_error": False}
    
    background_tasks.add_task(risky_operation, data)
    
    return {"message": "Processing queued"}
```

### Example 6: Background Tasks with Class Methods

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

class EmailService:
    def __init__(self, smtp_server: str):
        self.smtp_server = smtp_server
    
    def send(self, to: str, subject: str, body: str):
        print(f"Sending to {to} via {self.smtp_server}")
        # Actual email sending logic

# Create service instance
email_service = EmailService("smtp.example.com")

@app.post("/notify/")
async def notify_user(
    email: str,
    message: str,
    background_tasks: BackgroundTasks
):
    # Pass bound method to background task
    background_tasks.add_task(
        email_service.send,
        email,
        "Notification",
        message
    )
    
    return {"message": "Notification queued"}
```

### Example 7: Async Background Tasks

```python
from fastapi import FastAPI, BackgroundTasks
import asyncio

app = FastAPI()

async def async_process(data: dict):
    """Async background task"""
    await asyncio.sleep(2)  # Simulate async work
    print(f"Async processed: {data}")

@app.post("/async/")
async def trigger_async(background_tasks: BackgroundTasks):
    data = {"key": "value"}
    
    # Background tasks can be async
    background_tasks.add_task(async_process, data)
    
    return {"message": "Async processing queued"}
```

---

## Common Mistakes to Avoid

### Mistake 1: Relying on Task Completion

```python
# ❌ WRONG - Don't assume task is done when response returns
@app.post("/upload/")
async def upload(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_file)
    # Task might not be done yet!
    result = check_file_status()  # Could fail
    return {"status": result}

# ✅ CORRECT - Use polling or webhooks for status
@app.post("/upload/")
async def upload(background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    background_tasks.add_task(process_file, task_id)
    return {"task_id": task_id, "status": "queued"}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    return {"task_id": task_id, "status": get_task_status(task_id)}
```

### Mistake 2: Passing Non-Serializable Data

```python
# ❌ WRONG - Database session can't be pickled
def background_task(db: Session):
    # Session is not serializable!
    pass

background_tasks.add_task(background_task, db)

# ✅ CORRECT - Pass IDs, not objects
def background_task(user_id: int):
    # Create new session in task
    with SessionLocal() as db:
        user = db.query(User).get(user_id)
        # Process user

background_tasks.add_task(background_task, user.id)
```

### Mistake 3: Not Handling Exceptions

```python
# ❌ WRONG - Exceptions silently fail
def background_task():
    raise ValueError("Oops")  # No one sees this error

# ✅ CORRECT - Log and handle exceptions
def background_task():
    try:
        risky_operation()
    except Exception as e:
        logger.error(f"Task failed: {e}")
        # Store error, send alert, etc.
```

---

## Best Practices

1. **Keep tasks small and focused** - Each task should do one thing well
2. **Handle exceptions** - Always wrap task code in try/except
3. **Log extensively** - Background tasks are harder to debug
4. **Don't pass database sessions** - Pass IDs instead
5. **Use async for I/O-bound tasks** - Better performance for network operations
6. **Implement retries** - Use exponential backoff for critical tasks
7. **Consider task persistence** - For critical tasks, use Celery or similar
8. **Monitor task execution** - Track success/failure rates

---

## Background Tasks vs Celery

| Feature | FastAPI BackgroundTasks | Celery |
|---------|------------------------|--------|
| Complexity | Simple | Complex |
| Persistence | In-memory | Redis/RabbitMQ |
| Scaling | Single process | Distributed |
| Retry | Manual | Built-in |
| Monitoring | Basic | Flower dashboard |
| Best for | Simple tasks | Critical/long tasks |

**Use BackgroundTasks when:**
- Task is simple and short-lived
- Failure is acceptable
- Single server deployment
- Quick development

**Use Celery when:**
- Task must complete (critical)
- Long-running operations
- Distributed systems
- Need retry logic and monitoring

---

## Practice Exercises

### Exercise 1: Image Processing Pipeline
Create a background task that processes uploaded images:
- Resize to thumbnail
- Generate preview
- Update database with file paths

### Exercise 2: Email Queue System
Build an email sending system with:
- Welcome emails
- Password reset emails
- Notification emails
- Error handling and logging

### Exercise 3: Data Export
Create background task that:
- Exports database to CSV
- Sends email when complete
- Handles large datasets efficiently

### Exercise 4: Report Generation
Build a reporting system:
- Generate PDF reports
- Store in cloud storage
- Notify user when ready

### Exercise 5: Cache Invalidation
Create background task that:
- Invalidates cache keys
- Updates related caches
- Logs cache operations

---

## Summary

- **Background tasks** run after the response is sent to the client
- **Use BackgroundTasks** for simple, non-critical operations
- **Chain tasks** by adding multiple tasks to the queue
- **Pass simple data** - IDs instead of complex objects
- **Handle exceptions** - Don't let tasks fail silently
- **Consider Celery** for critical or distributed tasks
- **Monitor execution** - Track task success and failures

---

## Further Reading

- [FastAPI Official Documentation - Background Tasks](https://fastapi.tiangolo.com/advanced/background-tasks/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Task Queue Patterns](https://realpython.com/python-task-queues/)
