# Glossary: Database Concepts in FastAPI

## Quick Reference Table

| Term | Definition | Related Terms |
|------|------------|---------------|
| Connection Pool | Cache of database connections for reuse | Engine, Session |
| CRUD | Create, Read, Update, Delete operations | API, Database |
| Database URL | Connection string for database access | Engine, Configuration |
| Dependency Injection | FastAPI pattern for database sessions | Depends, Session |
| Engine | SQLAlchemy database connection manager | Connection Pool, URL |
| Migration | Version-controlled database schema changes | Alembic, Schema |
| ORM | Object-Relational Mapping library | SQLAlchemy, Models |
| Pool | Collection of reusable database connections | Connection, Engine |
| Query | Request to retrieve or modify data | SQL, ORM |
| Schema | Database structure definition | Table, Column |
| Session | Database connection handle for operations | Transaction, Engine |
| Table | Organized data storage structure | Column, Row |
| Transaction | Group of operations treated as single unit | Commit, Rollback |

---

## Detailed Definitions

### Connection Pool

**Definition**: A cache of database connections maintained so connections can be reused, reducing the overhead of establishing new connections.

**Why It Matters**: Database connections are expensive to create. Connection pooling allows multiple requests to share connections efficiently.

**Code Example**:
```python
from sqlalchemy.ext.asyncio import create_async_engine

# Create engine with connection pooling
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=20,        # Maximum connections in pool
    max_overflow=10,     # Extra connections beyond pool_size
    pool_timeout=30,     # Seconds to wait for connection
    pool_recycle=1800,   # Recycle connections after 30 min
    pool_pre_ping=True   # Test connections before use
)

# Check pool status
print(f"Pool size: {engine.pool.size()}")
print(f"Checked in: {engine.pool.checkedin()}")
print(f"Checked out: {engine.pool.checkedout()}")
```

**Related Terms**: Engine, Session, Pool

---

### CRUD

**Definition**: Acronym for the four basic operations: Create, Read, Update, Delete. These operations form the foundation of most database interactions.

**Code Example**:
```python
from sqlalchemy.orm import Session
from . import models, schemas

# CREATE
def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# READ
def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

# UPDATE
def update_item(db: Session, item_id: int, item_update: schemas.ItemUpdate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        update_data = item_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
    return db_item

# DELETE
def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False
```

**Related Terms**: API, Database, Query

---

### Database URL

**Definition**: A connection string that specifies how to connect to a database, including driver, credentials, host, port, and database name.

**Format**: `driver://username:password@host:port/database_name`

**Code Example**:
```python
# SQLite (file-based)
DATABASE_URL = "sqlite:///./app.db"
DATABASE_URL_ASYNC = "sqlite+aiosqlite:///./app.db"

# PostgreSQL
DATABASE_URL = "postgresql://user:password@localhost:5432/mydb"
DATABASE_URL_ASYNC = "postgresql+asyncpg://user:password@localhost:5432/mydb"

# MySQL
DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/mydb"
DATABASE_URL_ASYNC = "mysql+aiomysql://user:password@localhost:3306/mydb"

# Environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
```

**Related Terms**: Engine, Configuration, Environment Variables

---

### Dependency Injection

**Definition**: FastAPI's pattern for providing database sessions to route handlers. Uses the `Depends` function to inject dependencies.

**Code Example**:
```python
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Using dependency in route
@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Multiple dependencies
@app.post("/items/")
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_item(db=db, item=item)
```

**Related Terms**: Session, Depends, FastAPI

---

### Engine

**Definition**: The core SQLAlchemy component that manages database connections and provides the interface for executing queries.

**Code Example**:
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

# Synchronous engine
sync_engine = create_engine(
    "postgresql://user:pass@localhost/db",
    echo=True,
    pool_size=5
)

# Async engine
async_engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    echo=True,
    pool_size=5,
    future=True
)

# Engine with events
from sqlalchemy import event

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()
```

**Related Terms**: Connection Pool, Session, URL

---

### Migration

**Definition**: Version-controlled changes to database schema, allowing safe evolution of database structure over time.

**Code Example**:
```bash
# Initialize Alembic
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "create users table"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1

# Show current version
alembic current
```

**Python Migration Example**:
```python
# alembic/versions/001_create_users.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, unique=True, nullable=False),
        sa.Column('username', sa.String, unique=True),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now())
    )
    op.create_index('ix_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('ix_users_email')
    op.drop_table('users')
```

**Related Terms**: Alembic, Schema, Table

---

### ORM (Object-Relational Mapping)

**Definition**: A technique that maps Python classes to database tables, allowing database operations using Python objects instead of raw SQL.

**Code Example**:
```python
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    
    # Relationship
    posts = relationship("Post", back_populates="owner")
    
    def __repr__(self):
        return f"<User {self.email}>"

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationship
    owner = relationship("User", back_populates="posts")
```

**Related Terms**: SQLAlchemy, Models, Table

---

### Query

**Definition**: A request to retrieve or modify data in the database. In SQLAlchemy, queries are built using the Query API.

**Code Example**:
```python
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

# Simple query
users = db.query(models.User).all()
user = db.query(models.User).filter(models.User.id == 1).first()

# Filtering
active_users = db.query(models.User).filter(models.User.is_active == True).all()

# Complex filtering
filtered = db.query(models.User).filter(
    and_(
        models.User.is_active == True,
        or_(
            models.User.email.contains("@example.com"),
            models.User.username.startswith("admin")
        )
    )
).all()

# Ordering
sorted_users = db.query(models.User).order_by(models.User.created_at.desc()).all()

# Pagination
page = db.query(models.User).offset(10).limit(10).all()

# Count
count = db.query(models.User).filter(models.User.is_active == True).count()
```

**Related Terms**: SQL, ORM, Filter

---

### Schema

**Definition**: The structure of a database, including tables, columns, relationships, and constraints. Also refers to Pydantic models for API request/response validation.

**Database Schema**:
```python
# SQLAlchemy models define database schema
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
```

**API Schema (Pydantic)**:
```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Request schema
class ProductCreate(BaseModel):
    name: str
    price: float
    category_id: Optional[int] = None

# Response schema
class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# Update schema
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
```

**Related Terms**: Table, Column, Model, Pydantic

---

### Session

**Definition**: A workspace for interacting with the database. Manages transactions and provides the interface for executing queries.

**Code Example**:
```python
from sqlalchemy.orm import Session
from .database import SessionLocal

# Synchronous session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Async session
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# Using session in route
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user
```

**Related Terms**: Engine, Transaction, Dependency Injection

---

### Table

**Definition**: An organized collection of data in a database, consisting of rows (records) and columns (fields).

**Code Example**:
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

# Define table structure
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

# Table constraints
from sqlalchemy import UniqueConstraint, CheckConstraint

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True)
    table_number = Column(Integer)
    date = Column(DateTime)
    guest_count = Column(Integer)
    
    __table_args__ = (
        UniqueConstraint('table_number', 'date', name='uq_table_date'),
        CheckConstraint('guest_count > 0', name='ck_positive_guests')
    )
```

**Related Terms**: Column, Row, Schema

---

### Transaction

**Definition**: A sequence of database operations performed as a single logical unit of work. Either all operations succeed (commit), or all are undone (rollback).

**Code Example**:
```python
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

def transfer_funds(db: Session, from_account: int, to_account: int, amount: float):
    try:
        # Start transaction
        from_user = db.query(Account).filter(Account.id == from_account).first()
        to_user = db.query(Account).filter(Account.id == to_account).first()
        
        if not from_user or not to_user:
            raise ValueError("Account not found")
        
        if from_user.balance < amount:
            raise ValueError("Insufficient funds")
        
        # Perform operations
        from_user.balance -= amount
        to_user.balance += amount
        
        # Commit transaction
        db.commit()
        return {"status": "success", "message": f"Transferred {amount}"}
        
    except (ValueError, SQLAlchemyError) as e:
        # Rollback on error
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Using context manager
from contextlib import contextmanager

@contextmanager
def transactional_session(db: Session):
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
```

**Related Terms**: Commit, Rollback, Session

---

### Commit

**Definition**: Finalizing and saving all changes made during a transaction to the database.

**Code Example**:
```python
# Single operation
def create_item(db: Session, item: ItemCreate):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()  # Save changes
    db.refresh(db_item)  # Get updated data
    return db_item

# Multiple operations in one commit
def create_user_with_profile(db: Session, user: UserCreate, profile: ProfileCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.flush()  # Get ID without committing
    
    db_profile = Profile(user_id=db_user.id, **profile.model_dump())
    db.add(db_profile)
    
    db.commit()  # Both user and profile saved together
    return db_user
```

**Related Terms**: Transaction, Rollback, Flush

---

### Rollback

**Definition**: Undoing all changes made during a transaction, restoring the database to its state before the transaction began.

**Code Example**:
```python
def risky_operation(db: Session):
    try:
        # Perform operations
        user = User(name="test")
        db.add(user)
        db.flush()  # Get ID
        
        # This might fail
        perform_dangerous_operation()
        
        db.commit()
    except Exception as e:
        # Undo all changes
        db.rollback()
        raise

# Automatic rollback with context manager
from contextlib import asynccontextmanager

@asynccontextmanager
async def safe_session(session: AsyncSession):
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
```

**Related Terms**: Transaction, Commit, Exception

---

### Flush

**Definition**: Sending pending changes to the database without committing the transaction. Useful for getting auto-generated IDs.

**Code Example**:
```python
def create_with_related(db: Session, parent_data, child_data):
    # Create parent
    parent = Parent(**parent_data)
    db.add(parent)
    db.flush()  # Now parent.id is available
    
    # Create child with parent's ID
    child = Child(parent_id=parent.id, **child_data)
    db.add(child)
    
    db.commit()
    return parent
```

**Related Terms**: Commit, Session, Transaction

---

### Index

**Definition**: A data structure that improves query performance by allowing faster data retrieval.

**Code Example**:
```python
from sqlalchemy import Column, Integer, String, Index

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    category = Column(String(50))
    price = Column(Float)
    
    # Single column index
    __table_args__ = (
        Index('ix_products_category', 'category'),
        Index('ix_products_price', 'price'),
    )

# Composite index
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    status = Column(String(20))
    created_at = Column(DateTime)
    
    __table_args__ = (
        Index('ix_orders_user_status', 'user_id', 'status'),
        Index('ix_orders_created', 'created_at'),
    )
```

**Related Terms**: Query, Performance, Table

---

### ForeignKey

**Definition**: A constraint that links two tables by referencing the primary key of another table.

**Code Example**:
```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Author(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    
    # One-to-many relationship
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    author_id = Column(Integer, ForeignKey("authors.id"))  # Foreign key
    
    # Many-to-one relationship
    author = relationship("Author", back_populates="books")

# Composite foreign key
class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    
    order = relationship("Order")
    product = relationship("Product")
```

**Related Terms**: Relationship, Primary Key, Table

---

## Quick Commands Reference

```bash
# Database setup
python -m pip install sqlalchemy aiosqlite asyncpg

# Alembic migrations
alembic init alembic
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1
alembic history

# Testing database
pytest --create-db
pytest --reset-db
```

---

## Summary

Understanding these database concepts is essential for building robust FastAPI applications. The key takeaways are:

1. **Connection Pooling**: Use it for production to optimize performance
2. **ORM**: Map Python classes to database tables for cleaner code
3. **Sessions**: Manage database connections properly
4. **Transactions**: Ensure data consistency
5. **Migrations**: Track and version schema changes
6. **Indexes**: Improve query performance

**Next**: Move to the ORM glossary for detailed SQLAlchemy patterns.
