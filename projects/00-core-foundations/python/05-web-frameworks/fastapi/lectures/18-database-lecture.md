# Lecture 18: Working with Databases in FastAPI

## Overview

Databases are the backbone of most web applications, and FastAPI provides excellent support for working with various database systems. This lecture covers how to integrate databases into your FastAPI applications, from basic connection setup to advanced patterns like connection pooling, transactions, and database migrations.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Connect to different database types (PostgreSQL, MySQL, SQLite) from FastAPI
2. Understand synchronous vs asynchronous database drivers
3. Implement connection pooling for optimal performance
4. Execute basic CRUD operations
5. Handle database transactions properly
6. Use environment variables for database configuration
7. Implement database health checks
8. Understand common database patterns in FastAPI

---

## Key Concepts

### 1. Database Connection Options in FastAPI

FastAPI supports multiple ways to connect to databases:

#### Synchronous Drivers (Traditional)
```python
# Using SQLAlchemy synchronous engine
from sqlalchemy import create_engine

# SQLite (file-based)
engine = create_engine("sqlite:///./app.db")

# PostgreSQL
engine = create_engine("postgresql://user:password@localhost/dbname")

# MySQL
engine = create_engine("mysql+pymysql://user:password@localhost/dbname")
```

#### Asynchronous Drivers (Recommended for FastAPI)
```python
# Using SQLAlchemy async engine
from sqlalchemy.ext.asyncio import create_async_engine

# SQLite (requires aiosqlite)
engine = create_async_engine("sqlite+aiosqlite:///./app.db")

# PostgreSQL (requires asyncpg)
engine = create_async_engine("postgresql+asyncpg://user:password@localhost/dbname")

# MySQL (requires aiomysql)
engine = create_async_engine("mysql+aiomysql://user:password@localhost/dbname")
```

### 2. Environment-Based Configuration

Always use environment variables for database configuration:

```python
# config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./app.db"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
```

### 3. Connection Pooling

Connection pools manage database connections efficiently:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Create engine with connection pooling
engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost/dbname",
    pool_size=20,          # Maximum connections in pool
    max_overflow=10,       # Extra connections allowed
    pool_timeout=30,       # Seconds to wait for connection
    pool_recycle=1800,     # Recycle connections after 30 min
    pool_pre_ping=True,    # Verify connections before use
    echo=settings.DATABASE_ECHO  # SQL logging
)

# Create session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

---

## Code Examples

### Example 1: Basic Database Setup

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# For synchronous operations
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite specific
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Example 2: Async Database Setup

```python
# database.py (async version)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Async engine
DATABASE_URL = "sqlite+aiosqlite:///./app.db"
# For PostgreSQL: "postgresql+asyncpg://user:password@localhost/dbname"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

# Async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class
class Base(DeclarativeBase):
    pass

# Async dependency
async def get_async_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### Example 3: Database Models

```python
# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    posts = relationship("Post", back_populates="owner")
    
    def __repr__(self):
        return f"<User {self.email}>"

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    owner = relationship("User", back_populates="posts")
```

### Example 4: CRUD Operations

```python
# crud.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models, schemas

# Create
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=f"hashed_{user.password}"  # Use proper hashing!
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Read
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Update
def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

# Delete
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
```

### Example 5: FastAPI Endpoints with Database

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from . import models, schemas, crud

app = FastAPI(title="Database Demo API")

# Create tables (run once)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# Create user
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Get user
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Get multiple users
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
```

### Example 6: Database Health Check

```python
# health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import get_db

router = APIRouter()

@router.get("/health/database")
def database_health(db: Session = Depends(get_db)):
    try:
        # Execute a simple query
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "details": {
                "type": "postgresql",
                "pool_size": engine.pool.size(),
                "checked_in": engine.pool.checkedin(),
                "checked_out": engine.pool.checkedout()
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
```

---

## Common Mistakes to Avoid

### 1. Not Closing Database Sessions

```python
# BAD: Session might not close properly
def get_db():
    db = SessionLocal()
    yield db  # If exception occurs, session won't close

# GOOD: Use context manager or try/finally
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 2. Exposing Sensitive Information

```python
# BAD: Hardcoded credentials
DATABASE_URL = "postgresql://admin:secret123@localhost/db"

# GOOD: Use environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
```

### 3. Not Using Connection Pooling

```python
# BAD: Creating new connection for each request
def get_db():
    engine = create_engine(DATABASE_URL)  # New engine each time!
    Session = sessionmaker(bind=engine)
    db = Session()
    yield db
    db.close()

# GOOD: Reuse engine with connection pooling
engine = create_async_engine(DATABASE_URL, pool_size=5)
```

### 4. Ignoring Database Errors

```python
# BAD: No error handling
@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()  # What if this fails?
    return db_user

# GOOD: Handle exceptions
@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
```

---

## Best Practices

1. **Use Environment Variables**: Never hardcode database credentials
2. **Implement Connection Pooling**: Optimize connection usage
3. **Use Async Drivers**: For better performance with FastAPI
4. **Handle Transactions Properly**: Use try/except with rollback
5. **Add Database Health Checks**: Monitor database connectivity
6. **Use Migrations**: Track schema changes with Alembic
7. **Index Frequently Queried Columns**: Improve query performance
8. **Use Parameterized Queries**: Prevent SQL injection
9. **Close Sessions Properly**: Use dependency injection
10. **Log Database Operations**: For debugging and monitoring

---

## Practice Exercises

### Exercise 1: Basic CRUD API
Create a complete CRUD API for a "Todo" application with:
- Create, Read, Update, Delete operations
- Proper error handling
- Database session management

### Exercise 2: Connection Pooling
Configure a PostgreSQL connection with:
- Pool size of 20
- Max overflow of 10
- Connection recycling after 30 minutes
- Health check endpoint

### Exercise 3: Database Migration
Set up Alembic for database migrations:
- Initialize Alembic
- Create initial migration
- Add a new column via migration
- Test rollback functionality

---

## Summary

- FastAPI supports both sync and async database drivers
- Always use environment variables for configuration
- Implement connection pooling for production
- Use proper session management with dependency injection
- Handle database errors gracefully
- Use migrations for schema management
- Add health checks for monitoring

**Next Lecture**: We'll dive deeper into ORM patterns with SQLAlchemy, including relationship handling and query optimization.
