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

from fastapi import FastAPI, Depends, HTTPException, Query, Header
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Boolean,
    DateTime, ForeignKey, func, or_
)
from sqlalchemy.orm import (
    declarative_base, Session, sessionmaker,
    relationship, joinedload, selectinload
)

app = FastAPI(title="ORM Exercises")

SQLALCHEMY_DATABASE_URL = "sqlite:///./exercises_19.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ============================================================
# Exercise 19.1: SQLAlchemy Model Definitions
# ============================================================

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}')>"


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False, index=True)

    author = relationship("User")
    post = relationship("Post", back_populates="comments")

    def __repr__(self):
        return f"<Comment(id={self.id}, post_id={self.post_id})>"


# ============================================================
# Exercise 19.2: Database Session Management
# ============================================================

Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency that yields SQLAlchemy sessions, auto-closing after request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# Pydantic Models
# ============================================================

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    post_count: int = 0

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = False


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    author_id: int

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    author_id: int
    post_id: int

    class Config:
        from_attributes = True


class PostDetail(PostResponse):
    comments: List[CommentResponse] = []
    author: Optional[UserResponse] = None


class UserPublic(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


# ============================================================
# Exercise 19.3: CRUD with ORM
# ============================================================

def fake_hash_password(password: str) -> str:
    """Simulate password hashing for demo purposes."""
    return f"hashed_{password}"


@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=fake_hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        is_active=db_user.is_active,
        created_at=db_user.created_at,
        post_count=0
    )


@app.get("/users", response_model=List[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    users = db.query(User).offset(skip).limit(limit).all()
    result = []
    for user in users:
        post_count = db.query(func.count(Post.id)).filter(Post.author_id == user.id).scalar()
        result.append(UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
            post_count=post_count or 0
        ))
    return result


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    post_count = db.query(func.count(Post.id)).filter(Post.author_id == user_id).scalar()
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        post_count=post_count or 0
    )


@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user_update.username
    db_user.email = user_update.email
    if user_update.password:
        db_user.hashed_password = fake_hash_password(user_update.password)
    db.commit()
    db.refresh(db_user)
    post_count = db.query(func.count(Post.id)).filter(Post.author_id == user_id).scalar()
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        is_active=db_user.is_active,
        created_at=db_user.created_at,
        post_count=post_count or 0
    )


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted with all content"}


# Post endpoints

@app.post("/users/{user_id}/posts", response_model=PostResponse, status_code=201)
async def create_post(user_id: int, post: PostCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_post = Post(**post.model_dump(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return PostResponse(**{c: getattr(db_post, c) for c in PostResponse.model_fields})


@app.get("/users/{user_id}/posts", response_model=List[PostResponse])
async def list_user_posts(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    posts = db.query(Post).filter(Post.author_id == user_id).all()
    return [PostResponse(**{c: getattr(p, c) for c in PostResponse.model_fields}) for p in posts]


@app.get("/posts", response_model=List[PostResponse])
async def list_published_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    posts = db.query(Post).filter(Post.published == True).offset(skip).limit(limit).all()
    return [PostResponse(**{c: getattr(p, c) for c in PostResponse.model_fields}) for p in posts]


@app.get("/posts/{post_id}", response_model=PostDetail)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).options(
        joinedload(Post.author),
        selectinload(Post.comments)
    ).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    author = UserPublic(id=post.author.id, username=post.author.username, email=post.author.email) if post.author else None
    comments = [CommentResponse(**{c: getattr(cm, c) for c in CommentResponse.model_fields}) for cm in post.comments]

    return PostDetail(
        **{c: getattr(post, c) for c in PostResponse.model_fields},
        author=author,
        comments=comments
    )


@app.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_update: PostCreate,
    user_id: int = Header(alias="X-User-Id"),
    db: Session = Depends(get_db)
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != user_id:
        raise HTTPException(status_code=403, detail="Only the author can update this post")
    db_post.title = post_update.title
    db_post.content = post_update.content
    db_post.published = post_update.published
    db.commit()
    db.refresh(db_post)
    return PostResponse(**{c: getattr(db_post, c) for c in PostResponse.model_fields})


@app.delete("/posts/{post_id}")
async def delete_post(
    post_id: int,
    user_id: int = Header(alias="X-User-Id"),
    db: Session = Depends(get_db)
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != user_id:
        raise HTTPException(status_code=403, detail="Only the author can delete this post")
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted"}


# Comment endpoints

@app.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=201)
async def create_comment(
    post_id: int,
    comment: CommentCreate,
    user_id: int = Header(alias="X-User-Id"),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_comment = Comment(content=comment.content, author_id=user_id, post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return CommentResponse(**{c: getattr(db_comment, c) for c in CommentResponse.model_fields})


# ============================================================
# Exercise 19.4: Query Optimization with Joins
# ============================================================

@app.get("/feed", response_model=List[PostDetail])
async def get_feed(db: Session = Depends(get_db)):
    """Get latest 20 published posts with author info (eager loaded)."""
    posts = db.query(Post).options(
        joinedload(Post.author),
        selectinload(Post.comments)
    ).filter(
        Post.published == True
    ).order_by(
        Post.created_at.desc()
    ).limit(20).all()

    result = []
    for post in posts:
        author = UserPublic(id=post.author.id, username=post.author.username, email=post.author.email) if post.author else None
        comments = [CommentResponse(**{c: getattr(cm, c) for c in CommentResponse.model_fields}) for cm in post.comments]
        result.append(PostDetail(
            **{c: getattr(post, c) for c in PostResponse.model_fields},
            author=author,
            comments=comments
        ))
    return result


@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get blog statistics."""
    user_count = db.query(func.count(User.id)).scalar()
    post_count = db.query(func.count(Post.id)).scalar()
    comment_count = db.query(func.count(Comment.id)).scalar()
    return {"users": user_count or 0, "posts": post_count or 0, "comments": comment_count or 0}


@app.get("/search", response_model=List[PostResponse])
async def search_posts(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    """Search posts by title/content using multiple terms."""
    terms = q.split()
    conditions = [
        or_(
            Post.title.contains(term),
            Post.content.contains(term)
        )
        for term in terms
    ]
    posts = db.query(Post).filter(
        Post.published == True,
        or_(*conditions)
    ).order_by(Post.created_at.desc()).limit(20).all()
    return [PostResponse(**{c: getattr(p, c) for c in PostResponse.model_fields}) for p in posts]


# ============================================================
# Exercise 19.5: Async SQLAlchemy (Bonus)
# ============================================================
# Note: To use async SQLAlchemy, install aiosqlite:
#   pip install aiosqlite sqlalchemy[asyncio]
#
# Then use:
#   from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
#   async_engine = create_async_engine("sqlite+aiosqlite:///./exercises_19.db")
#   async_session = async_sessionmaker(async_engine, expire_on_commit=False)
#
# For this exercise file, the sync version above is the primary implementation.
# Uncomment and adapt the code below for async support:

# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
#
# ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./exercises_19.db"
# async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
# async_session = async_sessionmaker(async_engine, expire_on_commit=False)
#
# async def get_async_db():
#     async with async_session() as session:
#         yield session
