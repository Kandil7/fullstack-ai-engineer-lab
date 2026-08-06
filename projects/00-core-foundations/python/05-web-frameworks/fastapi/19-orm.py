"""
19 - ORM Relationships & Advanced Patterns
=============================================
Advanced SQLAlchemy ORM patterns: relationships, joins,
aggregations, and complex queries.

Requires: pip install sqlalchemy

Run: uvicorn 19-orm:app --reload
"""

import sys
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

# ----- Database setup -----
import pathlib
DB_PATH = pathlib.Path(__file__).parent.parent.parent / "outputs" / "dbs" / "orm_demo.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ----- ORM Models with Relationships -----
class AuthorDB(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship: one author has many books
    books = relationship("BookDB", back_populates="author", cascade="all, delete-orphan")


class BookDB(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column(String, index=True)
    price = Column(Float)
    published_year = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship: many books belong to one author
    author = relationship("AuthorDB", back_populates="books")


Base.metadata.create_all(bind=engine)


# ----- Pydantic Schemas -----
class AuthorCreate(BaseModel):
    name: str
    email: str


class AuthorResponse(BaseModel):
    id: int
    name: str
    email: str
    book_count: int = 0

    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    title: str
    genre: str
    price: float
    published_year: int
    author_id: int


class BookResponse(BaseModel):
    id: int
    title: str
    genre: str
    price: float
    published_year: int
    author_id: int
    author_name: str | None = None

    class Config:
        from_attributes = True


class BookWithAuthor(BaseModel):
    id: int
    title: str
    genre: str
    price: float
    author: AuthorCreate

    class Config:
        from_attributes = True


# ----- DB Dependency -----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="ORM Relationships & Advanced Patterns")


# ----- Author CRUD -----
@app.post("/authors/", response_model=AuthorResponse, status_code=201)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = AuthorDB(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return AuthorResponse(
        id=db_author.id,
        name=db_author.name,
        email=db_author.email,
        book_count=0,
    )


@app.get("/authors/", response_model=list[AuthorResponse])
def list_authors(db: Session = Depends(get_db)):
    authors = db.query(AuthorDB).all()
    return [
        AuthorResponse(
            id=a.id, name=a.name, email=a.email, book_count=len(a.books)
        )
        for a in authors
    ]


@app.get("/authors/{author_id}")
def get_author_with_books(author_id: int, db: Session = Depends(get_db)):
    """Get author with all their books (eager loading)."""
    author = db.query(AuthorDB).filter(AuthorDB.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return {
        "id": author.id,
        "name": author.name,
        "email": author.email,
        "books": [
            {"id": b.id, "title": b.title, "genre": b.genre, "price": b.price}
            for b in author.books
        ],
    }


# ----- Book CRUD -----
@app.post("/books/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Verify author exists
    author = db.query(AuthorDB).filter(AuthorDB.id == book.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    db_book = BookDB(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return BookResponse(
        id=db_book.id,
        title=db_book.title,
        genre=db_book.genre,
        price=db_book.price,
        published_year=db_book.published_year,
        author_id=db_book.author_id,
        author_name=author.name,
    )


@app.get("/books/", response_model=list[BookResponse])
def list_books(
    genre: str | None = None,
    min_price: float = 0,
    max_price: float = 10000,
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List books with filters using JOIN."""
    query = db.query(BookDB).join(AuthorDB)

    if genre:
        query = query.filter(BookDB.genre == genre)
    if min_price > 0:
        query = query.filter(BookDB.price >= min_price)
    if max_price < 10000:
        query = query.filter(BookDB.price <= max_price)
    if author_id:
        query = query.filter(BookDB.author_id == author_id)

    books = query.offset(skip).limit(limit).all()
    return [
        BookResponse(
            id=b.id, title=b.title, genre=b.genre, price=b.price,
            published_year=b.published_year, author_id=b.author_id,
            author_name=b.author.name,
        )
        for b in books
    ]


@app.get("/books/{book_id}", response_model=BookWithAuthor)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"deleted": True}


# ----- Aggregation queries -----
@app.get("/stats/by-genre")
def stats_by_genre(db: Session = Depends(get_db)):
    """Aggregate book stats by genre."""
    results = (
        db.query(
            BookDB.genre,
            func.count(BookDB.id).label("count"),
            func.avg(BookDB.price).label("avg_price"),
            func.min(BookDB.price).label("min_price"),
            func.max(BookDB.price).label("max_price"),
        )
        .group_by(BookDB.genre)
        .all()
    )
    return [
        {
            "genre": r.genre,
            "count": r.count,
            "avg_price": round(r.avg_price, 2),
            "min_price": r.min_price,
            "max_price": r.max_price,
        }
        for r in results
    ]


@app.get("/stats/by-author")
def stats_by_author(db: Session = Depends(get_db)):
    """Aggregate book stats by author."""
    results = (
        db.query(
            AuthorDB.name,
            func.count(BookDB.id).label("book_count"),
            func.sum(BookDB.price).label("total_value"),
        )
        .join(BookDB)
        .group_by(AuthorDB.id)
        .all()
    )
    return [
        {"author": r.name, "books": r.book_count, "total_value": round(r.total_value, 2)}
        for r in results
    ]


"""
Testing with curl:
    curl -X POST http://127.0.0.1:8000/authors/ -H "Content-Type: application/json" -d '{"name": "J.K. Rowling", "email": "jk@test.com"}'
    curl -X POST http://127.0.0.1:8000/books/ -H "Content-Type: application/json" -d '{"title": "Harry Potter", "genre": "Fantasy", "price": 29.99, "published_year": 1997, "author_id": 1}'
    curl http://127.0.0.1:8000/authors/1
    curl "http://127.0.0.1:8000/books/?genre=Fantasy"
    curl http://127.0.0.1:8000/stats/by-genre
    curl http://127.0.0.1:8000/stats/by-author
"""

def _verify():
    """Smoke-test the app in-process with TestClient (no real server).

    Uses a throwaway temp SQLite file (NOT the teaching DB) so verification
    never touches outputs/dbs/orm_demo.db and never leaves file locks.
    """
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        print("[skip] fastapi not installed")
        return

    import os
    import shutil
    import tempfile

    tmp_dir = tempfile.mkdtemp(prefix="fastapi_19_verify_")
    db_file = os.path.join(tmp_dir, "verify.db")
    try:
        verify_engine = create_engine(
            f"sqlite:///{db_file}", connect_args={"check_same_thread": False}
        )
        Base.metadata.create_all(bind=verify_engine)
        verify_session = sessionmaker(autocommit=False, autoflush=False, bind=verify_engine)

        def override_get_db():
            db = verify_session()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        client = TestClient(app)

        r = client.post(
            "/authors/",
            json={"name": "J.K. Rowling", "email": "jk@test.com"},
        )
        assert r.status_code == 201

        r = client.post(
            "/books/",
            json={"title": "Harry Potter", "genre": "Fantasy", "price": 29.99, "published_year": 1997, "author_id": 1},
        )
        assert r.status_code == 201
        assert r.json()["author_name"] == "J.K. Rowling"

        r = client.post(
            "/books/",
            json={"title": "Dune", "genre": "Sci-Fi", "price": 19.99, "published_year": 1965, "author_id": 1},
        )
        assert r.status_code == 201

        r = client.post(
            "/books/",
            json={"title": "Orphan", "genre": "Fantasy", "price": 9.99, "published_year": 2020, "author_id": 99},
        )
        assert r.status_code == 404  # Author not found

        r = client.get("/authors/1")
        assert r.status_code == 200
        assert len(r.json()["books"]) == 2

        r = client.get("/authors/999")
        assert r.status_code == 404

        r = client.get("/books/?genre=Fantasy")
        assert r.status_code == 200
        assert len(r.json()) == 1

        r = client.get("/books/1")
        assert r.status_code == 200
        assert r.json()["author"]["name"] == "J.K. Rowling"

        r = client.get("/stats/by-genre")
        assert r.status_code == 200
        genres = {g["genre"] for g in r.json()}
        assert genres == {"Fantasy", "Sci-Fi"}

        r = client.get("/stats/by-author")
        assert r.status_code == 200
        assert r.json()[0]["books"] == 2

        r = client.delete("/books/2")
        assert r.status_code == 200

        r = client.delete("/books/999")
        assert r.status_code == 404

        verify_engine.dispose()  # close all connections BEFORE removing the file
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    print("[OK] 19-orm: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        _verify()
