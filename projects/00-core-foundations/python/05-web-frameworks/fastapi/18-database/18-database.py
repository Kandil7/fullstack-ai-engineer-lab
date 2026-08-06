"""
18 - Database (SQLAlchemy)
============================
Database integration using SQLAlchemy with SQLite.
Covers: connection setup, models, CRUD operations, and sessions.

Requires: pip install sqlalchemy

Run: uvicorn 18-database:app --reload
"""

import sys
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# ----- Database setup -----
import pathlib
DB_PATH = pathlib.Path(__file__).parent.parent.parent / "outputs" / "dbs" / "fastapi_demo.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ----- ORM Model -----
class ItemDB(Base):
    """SQLAlchemy model for items table."""
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Item {self.name}>"


# Create tables
Base.metadata.create_all(bind=engine)


# ----- Pydantic models -----
class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    is_available: bool = True


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    is_available: bool | None = None


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ----- Database dependency -----
def get_db():
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----- FastAPI app -----
app = FastAPI(title="Database with SQLAlchemy")


# ----- CRUD Operations -----
@app.post("/items/", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item in the database."""
    db_item = ItemDB(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/items/", response_model=list[ItemResponse])
def list_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List all items with pagination."""
    items = db.query(ItemDB).offset(skip).limit(limit).all()
    return items


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific item by ID."""
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    """Update an existing item."""
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item."""
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"deleted": True, "id": item_id}


# ----- Query filtering -----
@app.get("/search/")
def search_items(
    name: str = "",
    min_price: float = 0,
    max_price: float = 10000,
    available_only: bool = False,
    db: Session = Depends(get_db),
):
    """Search items with filters."""
    query = db.query(ItemDB)

    if name:
        query = query.filter(ItemDB.name.ilike(f"%{name}%"))
    if min_price > 0:
        query = query.filter(ItemDB.price >= min_price)
    if max_price < 10000:
        query = query.filter(ItemDB.price <= max_price)
    if available_only:
        query = query.filter(ItemDB.is_available == True)

    items = query.all()
    return {"count": len(items), "items": items}


# ----- Database stats -----
@app.get("/stats/")
def get_stats(db: Session = Depends(get_db)):
    """Get database statistics."""
    total = db.query(ItemDB).count()
    available = db.query(ItemDB).filter(ItemDB.is_available == True).count()
    return {
        "total_items": total,
        "available": available,
        "unavailable": total - available,
    }


"""
Testing with curl:
    curl -X POST http://127.0.0.1:8000/items/ -H "Content-Type: application/json" -d '{"name": "Laptop", "price": 999.99, "description": "A powerful laptop"}'

    curl http://127.0.0.1:8000/items/
    curl http://127.0.0.1:8000/items/1
    curl -X PUT http://127.0.0.1:8000/items/1 -H "Content-Type: application/json" -d '{"price": 899.99}'
    curl -X DELETE http://127.0.0.1:8000/items/1
    curl "http://127.0.0.1:8000/search/?name=laptop&min_price=500"
    curl http://127.0.0.1:8000/stats/

    Database file: fastapi_demo.db (SQLite)
"""

def _verify():
    """Smoke-test the app in-process with TestClient (no real server).

    Uses a throwaway temp SQLite file (NOT the teaching DB) so verification
    never touches outputs/dbs/fastapi_demo.db and never leaves file locks.
    """
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        print("[skip] fastapi not installed")
        return

    import os
    import shutil
    import tempfile

    tmp_dir = tempfile.mkdtemp(prefix="fastapi_18_verify_")
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
            "/items/",
            json={"name": "Laptop", "price": 999.99, "description": "A powerful laptop"},
        )
        assert r.status_code == 201
        assert r.json()["name"] == "Laptop"

        r = client.post("/items/", json={"name": "Phone", "price": 699.99})
        assert r.status_code == 201

        r = client.get("/items/")
        assert r.status_code == 200
        assert len(r.json()) == 2

        r = client.get("/items/1")
        assert r.status_code == 200
        assert r.json()["price"] == 999.99

        r = client.get("/items/999")
        assert r.status_code == 404

        r = client.put("/items/1", json={"price": 899.99})
        assert r.status_code == 200
        assert r.json()["price"] == 899.99

        r = client.delete("/items/2")
        assert r.status_code == 200
        assert r.json()["deleted"] is True

        r = client.get("/search/?name=laptop&min_price=500")
        assert r.status_code == 200
        assert r.json()["count"] == 1

        r = client.get("/stats/")
        assert r.status_code == 200
        assert r.json()["total_items"] == 1

        verify_engine.dispose()  # close all connections BEFORE removing the file
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    print("[OK] 18-database: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        _verify()
