"""
Exercise 19: ORM with SQLAlchemy in FastAPI

Master SQLAlchemy ORM integration with FastAPI applications.
Topics: SQLAlchemy models, sessions, relationships, migrations, async ORM.

Prerequisites:
- SQLite basics (exercise 18)
- Python dataclasses and type hints
- FastAPI dependency injection

Estimated time: 75-100 minutes
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

app = FastAPI(title="ORM Exercises")

# ============================================================
# Exercise 19.1: SQLAlchemy Model Definitions
# ============================================================
"""
Problem:
    Define SQLAlchemy ORM models for a blog application.

Models to create:
    User:
        - id: Integer, primary key
        - username: String(50), unique, not null
        - email: String(100), unique, not null
        - hashed_password: String(200), not null
        - is_active: Boolean, default True
        - created_at: DateTime, default now
        - relationship: posts (one-to-many with Post)

    Post:
        - id: Integer, primary key
        - title: String(200), not null
        - content: Text, not null
        - published: Boolean, default False
        - created_at: DateTime, default now
        - updated_at: DateTime, nullable
        - author_id: Integer, foreign key to users.id
        - relationship: author (many-to-one with User)
        - relationship: comments (one-to-many with Comment)

    Comment:
        - id: Integer, primary key
        - content: Text, not null
        - created_at: DateTime, default now
        - author_id: Integer, foreign key to users.id
        - post_id: Integer, foreign key to posts.id
        - relationship: author (many-to-one with User)
        - relationship: post (many-to-one with Post)

Hints:
    - Use declarative_base() for model base class
    - Use Column(), String(), Integer(), etc. from sqlalchemy
    - Use ForeignKey("users.id") for relationships
    - Use relationship("User", back_populates="posts") for back-references
    - Define __tablename__ for each model

Expected behavior:
    Models should be importable and usable with SQLAlchemy sessions.
    Relationships should be lazy-loaded by default.

TODO:
    - Define all three models with proper relationships
    - Add appropriate indexes on frequently queried columns
    - Define __repr__ methods for debugging
"""

# TODO: Import SQLAlchemy components
# TODO: Create Base class
# TODO: Define User, Post, Comment models


# ============================================================
# Exercise 19.2: Database Session Management
# ============================================================
"""
Problem:
    Create a robust database session management system.

Requirements:
    1. Create get_db() dependency that yields SQLAlchemy sessions
    2. Implement session cleanup on request completion
    3. Handle session errors gracefully
    4. Support both sync and async sessions (bonus)
    5. Create init_db() function to create all tables

Architecture:
    - Use SessionLocal for synchronous sessions
    - Use AsyncSession for async operations (bonus)
    - Sessions should auto-rollback on exceptions
    - Connections should be returned to pool after each request

Hints:
    - from sqlalchemy.orm import Session, sessionmaker
    - from sqlalchemy import create_engine
    - SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    - Use yield in FastAPI dependencies for automatic cleanup
    - try/finally ensures session.close() is called

Test cases:
    # Session works normally
    GET /users
    -> 200 [list of users]

    # Session rolls back on error
    POST /users (invalid data)
    -> 400 (database unchanged)

    # Database initialized
    GET /health
    -> 200 {"database": "ready"}
"""

# TODO: Write database session management code


# ============================================================
# Exercise 19.3: CRUD with ORM
# ============================================================
"""
Problem:
    Implement CRUD operations using SQLAlchemy ORM.

User Endpoints:
    POST   /users          - Create user (hash password)
    GET    /users          - List users (paginated)
    GET    /users/{id}     - Get user with posts count
    PUT    /users/{id}     - Update user
    DELETE /users/{id}     - Delete user and all their posts/comments

Post Endpoints:
    POST   /users/{id}/posts   - Create post for user
    GET    /users/{id}/posts   - List user's posts
    GET    /posts              - List all published posts
    GET    /posts/{id}         - Get post with comments
    PUT    /posts/{id}         - Update post (only by author)
    DELETE /posts/{id}         - Delete post

Request/Response Models:
    UserCreate:  username, email, password
    UserResponse: id, username, email, is_active, created_at, post_count
    PostCreate:  title, content, published (optional, default False)
    PostResponse: id, title, content, published, created_at, author_id
    PostDetail:  PostResponse + comments: list[CommentResponse]
    CommentCreate: content

Hints:
    - Use db.query(User).filter(User.id == user_id).first()
    - Use db.add(), db.commit(), db.refresh() for creates
    - Use db.delete() and db.commit() for deletes
    - Use db.query(User).count() for totals
    - Use .options(joinedload(User.posts)) for eager loading
    - Use db.query(Post).filter(Post.published == True)

Test cases:
    # Create user
    POST /users {"username": "alice", "email": "alice@example.com", "password": "secret"}
    -> 201 {"id": 1, "username": "alice", ...}

    # Create post
    POST /users/1/posts {"title": "My Post", "content": "Hello world"}
    -> 201 {"id": 1, "title": "My Post", "author_id": 1}

    # Get post with comments
    GET /posts/1
    -> 200 {"id": 1, "title": "My Post", "comments": []}

    # Delete user (cascades to posts and comments)
    DELETE /users/1
    -> 200 {"message": "User deleted with all content"}
"""

# TODO: Write CRUD endpoint code


# ============================================================
# Exercise 19.4: Query Optimization with Joins
# ============================================================
"""
Problem:
    Implement optimized queries that avoid N+1 problems.

Endpoints:
    GET /feed          - Get latest 20 published posts with author info
    GET /posts/{id}    - Get post with author and all comments (eager loaded)
    GET /stats         - Get blog statistics (user count, post count, comment count)
    GET /search        - Search posts by title/content

Requirements:
    1. Use eager loading (joinedload) to avoid N+1 queries
    2. Use subqueries for statistics
    3. Use full-text search simulation (LIKE with multiple terms)
    4. Profile queries (bonus: use SQLAlchemy's query logging)

Hints:
    - from sqlalchemy.orm import joinedload, selectinload
    - .options(joinedload(Post.author), selectinload(Post.comments))
    - Use func.count() for aggregates
    - Use or_(Post.title.contains(term), Post.content.contains(term))
    - Feed endpoint: Post.published == True, order_by(Post.created_at.desc())

Test cases:
    # Feed with author info (single query, no N+1)
    GET /feed
    -> 200 [{"id": 1, "title": "...", "author": {"username": "alice"}, ...}]

    # Statistics
    GET /stats
    -> 200 {"users": 5, "posts": 23, "comments": 142}

    # Search
    GET /search?q=python+fastapi
    -> 200 [matching posts with highlights]
"""

# TODO: Write optimized query code


# ============================================================
# Exercise 19.5: Async SQLAlchemy (Bonus)
# ============================================================
"""
Problem:
    Convert the application to use async SQLAlchemy.

Requirements:
    1. Use AsyncSession and create_async_engine
    2. Implement async get_db() dependency
    3. Convert all CRUD operations to async
    4. Handle async context managers properly

Async architecture:
    - engine = create_async_engine(DATABASE_URL, echo=True)
    - async_session = async_sessionmaker(engine, expire_on_commit=False)
    - async def get_async_db():
          async with async_session() as session:
              yield session

Hints:
    - pip install aiosqlite  (for async SQLite)
    - pip install sqlalchemy[asyncio]
    - Use: "sqlite+aiosqlite:///./database.db"
    - Use: await db.execute(select(User).where(...))
    - Use: result.scalars().all() to get list
    - Use: await db.commit()

Test cases:
    # Async user creation
    POST /async/users {"username": "bob", "email": "bob@test.com", "password": "pass"}
    -> 201 {"id": 1, "username": "bob"}

    # Async listing
    GET /async/users
    -> 200 [users with async response times]
"""

# TODO: Write async SQLAlchemy code (bonus exercise)
