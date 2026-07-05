# Glossary: ORM Patterns in FastAPI

## Quick Reference Table

| Term | Definition | Related Terms |
|------|------------|---------------|
| Association Object | Model representing a many-to-many relationship with extra fields | Many-to-Many, Relationship |
| Back Populates | Attribute that creates bidirectional relationship | Relationship, Foreign Key |
| Cascade | Operations that automatically apply to related objects | Delete, Orphan |
| Column | Field in a database table | Table, Type |
| Declarative Base | Base class for all SQLAlchemy models | Model, Base |
| Eager Loading | Loading related objects in the same query | Lazy Loading, Joinedload |
| Foreign Key | Column linking to another table's primary key | Relationship, Primary Key |
| Hybrid Property | Python property that works in Python and SQL | Property, Column |
| Joinedload | Eager loading strategy using JOIN | Selectinload, Lazy |
| Lazy Loading | Loading related objects on access | Eager Loading |
| Mapper | SQLAlchemy component mapping classes to tables | Model, Table |
| Model | Python class representing a database table | Table, Column |
| Orphan Deletion | Deleting objects when removed from relationship | Cascade, Relationship |
| Primary Key | Unique identifier for a table row | Column, Foreign Key |
| Relationship | Link between two models | Foreign Key, Back Populates |
| Selectinload | Eager loading strategy using separate query | Joinedload |
| Session | Database connection workspace | Transaction, Engine |
| Table | Database structure for organizing data | Column, Row |
| Validator | Function that validates data on set | Pydantic, Model |

---

## Detailed Definitions

### Association Object

**Definition**: A model that represents a many-to-many relationship while allowing additional fields on the relationship itself.

**Why It Matters**: Standard many-to-many tables can't store extra data. Association objects solve this.

**Code Example**:
```python
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Enrollment(Base):
    """Association object with extra fields"""
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    grade = Column(Float, nullable=True)
    
    # Relationships to both models
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    
    # Relationship to association object
    enrollments = relationship("Enrollment", back_populates="student")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    
    # Relationship to association object
    enrollments = relationship("Enrollment", back_populates="course")

# Usage
def enroll_student(db: Session, student_id: int, course_id: int):
    enrollment = Enrollment(
        student_id=student_id,
        course_id=course_id,
        grade=None  # Initial grade
    )
    db.add(enrollment)
    db.commit()
    return enrollment
```

**Related Terms**: Many-to-Many, Relationship, Foreign Key

---

### Back Populates

**Definition**: SQLAlchemy feature that creates bidirectional relationships between two models.

**Why It Matters**: Allows access to related objects from both sides of a relationship.

**Code Example**:
```python
class Parent(Base):
    __tablename__ = "parents"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    
    # This creates a双向 relationship
    children = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = "children"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    parent_id = Column(Integer, ForeignKey("parents.id"))
    
    # This completes the bidirectional relationship
    parent = relationship("Parent", back_populates="children")

# Usage
parent = db.query(Parent).first()
print(parent.children)  # Access children from parent

child = db.query(Child).first()
print(child.parent)  # Access parent from child
```

**Related Terms**: Relationship, Foreign Key

---

### Cascade

**Definition**: Operations that automatically apply to related objects when the parent object is modified or deleted.

**Code Example**:
```python
class Parent(Base):
    __tablename__ = "parents"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    
    # Cascade options:
    # - save-update: Add/update children when parent is saved
    # - delete: Delete children when parent is deleted
    # - delete-orphan: Delete children when parent is deleted OR removed from relationship
    children = relationship(
        "Child",
        back_populates="parent",
        cascade="all, delete-orphan",
        passive_deletes=True  # Let database handle deletes
    )

class Child(Base):
    __tablename__ = "children"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    parent_id = Column(Integer, ForeignKey("parents.id", ondelete="CASCADE"))
    
    parent = relationship("Parent", back_populates="children")

# Usage
parent = Parent(name="Parent 1")
child1 = Child(name="Child 1")
child2 = Child(name="Child 2")

parent.children = [child1, child2]
db.add(parent)
db.commit()

# Now deleting parent will also delete children
db.delete(parent)
db.commit()
```

**Related Terms**: Delete, Orphan, Relationship

---

### Column

**Definition**: A field in a database table that stores a specific type of data.

**Code Example**:
```python
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Enum

class Product(Base):
    __tablename__ = "products"
    
    # Integer column
    id = Column(Integer, primary_key=True, index=True)
    
    # String column with length
    name = Column(String(200), nullable=False)
    
    # Text for longer content
    description = Column(Text)
    
    # Float for decimal numbers
    price = Column(Float, nullable=False)
    
    # Boolean
    is_active = Column(Boolean, default=True)
    
    # DateTime
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Enum
    status = Column(
        Enum('draft', 'published', 'archived', name='product_status'),
        default='draft'
    )
    
    # Column with unique constraint
    sku = Column(String(50), unique=True, nullable=False)
    
    # Column with index
    category = Column(String(50), index=True)
```

**Related Terms**: Table, Type, Constraint

---

### Declarative Base

**Definition**: The base class from which all SQLAlchemy models inherit. Provides the foundation for model definitions.

**Code Example**:
```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class for all models"""
    pass

# Modern approach with type annotations
from typing import Annotated
from sqlalchemy.orm import mapped_column, Mapped

int_pk = Annotated[int, mapped_column(primary_key=True)]
str_100 = Annotated[str, mapped_column(String(100))]

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int_pk]
    username: Mapped[str_100]
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
```

**Related Terms**: Model, Table, Column

---

### Eager Loading

**Definition**: Loading related objects in the same query as the main object, preventing N+1 query problems.

**Code Example**:
```python
from sqlalchemy.orm import joinedload, selectinload

# Method 1: joinedload - Uses SQL JOIN
stmt = (
    select(Course)
    .options(joinedload(Course.professor))
    .where(Course.id == course_id)
)

# Method 2: selectinload - Uses separate IN query
stmt = (
    select(Course)
    .options(selectinload(Course.enrollments))
    .where(Course.id == course_id)
)

# Method 3: Subquery loading
from sqlalchemy.orm import subqueryload
stmt = (
    select(Course)
    .options(subqueryload(Course.students))
    .where(Course.id == course_id)
)

# Multiple eager loads
stmt = (
    select(Course)
    .options(
        joinedload(Course.professor),
        selectinload(Course.enrollments)
            .selectinload(Enrollment.student)
    )
    .where(Course.id == course_id)
)

# Execution
result = db.execute(stmt)
courses = result.unique().scalars().all()
```

**Related Terms**: Lazy Loading, Joinedload, Selectinload

---

### Foreign Key

**Definition**: A column that creates a link between two tables by referencing the primary key of another table.

**Code Example**:
```python
from sqlalchemy import ForeignKey

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Foreign key with options
    product_id = Column(
        Integer, 
        ForeignKey("products.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    
    # Composite foreign key
    category_id = Column(Integer)
    item_id = Column(Integer)
    
    __table_args__ = (
        ForeignKeyConstraint(
            ['category_id', 'item_id'],
            ['categories.id', 'items.id']
        ),
    )
```

**Related Terms**: Primary Key, Relationship, Constraint

---

### Hybrid Property

**Definition**: A Python property that can work both in Python code and in SQL expressions.

**Code Example**:
```python
from sqlalchemy.ext.hybrid import hybrid_property

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    _email = Column("email", String(255))
    
    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @full_name.inplace.setter
    def full_name(self, value):
        first, last = value.split(' ', 1)
        self.first_name = first
        self.last_name = last
    
    @hybrid_property
    def email(self):
        return self._email
    
    @email.inplace.setter
    def email(self, value):
        if '@' not in value:
            raise ValueError("Invalid email")
        self._email = value

# Usage
user = db.query(User).first()
print(user.full_name)  # Python side

# SQL filtering with hybrid property
users = db.query(User).filter(User.full_name.ilike("%john%")).all()
```

**Related Terms**: Property, Column, Python

---

### Joinedload

**Definition**: Eager loading strategy that uses SQL JOIN to load related objects.

**Code Example**:
```python
from sqlalchemy.orm import joinedload

# Single relationship
stmt = (
    select(Course)
    .options(joinedload(Course.professor))
    .where(Course.id == 1)
)

# Multiple relationships
stmt = (
    select(Order)
    .options(
        joinedload(Order.user),
        joinedload(Order.items)
            .selectinload(OrderItem.product)
    )
    .where(Order.id == 1)
)

# Joinedload with filtering
stmt = (
    select(Author)
    .options(
        joinedload(Author.books).filter(Book.published == True)
    )
    .where(Author.id == 1)
)

result = db.execute(stmt)
author = result.unique().scalar_one_or_none()
```

**Related Terms**: Selectinload, Eager Loading, Lazy Loading

---

### Lazy Loading

**Definition**: Loading related objects only when they are accessed, not when the parent object is loaded.

**Code Example**:
```python
# Default lazy loading (no options needed)
author = db.query(Author).first()
books = author.books  # Triggers new query here

# Explicit lazy loading options
from sqlalchemy.orm import lazyload

stmt = (
    select(Author)
    .options(lazyload(Author.books))  # Explicit lazy loading
    .where(Author.id == 1)
)

# Disable lazy loading globally
from sqlalchemy.orm import configure_mappers
configure_mappers()  # Call once

# Or per relationship
books = relationship("Book", lazy="noload")  # Never load automatically
books = relationship("Book", lazy="raise")  # Raise error if accessed
```

**Related Terms**: Eager Loading, Joinedload, Selectinload

---

### Model

**Definition**: A Python class that maps to a database table, defining its structure and relationships.

**Code Example**:
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional

class Base(DeclarativeBase):
    pass

class User(Base):
    """User model representing the users table"""
    __tablename__ = "users"
    
    # Modern approach with type annotations
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active
        }
```

**Related Terms**: Table, Column, Declarative Base

---

### Orphan Deletion

**Definition**: Deleting objects when they are removed from a parent relationship, even if the parent still exists.

**Code Example**:
```python
class Parent(Base):
    __tablename__ = "parents"
    
    id = Column(Integer, primary_key=True)
    
    # delete-orphan means children are deleted when removed from list
    children = relationship(
        "Child",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

class Child(Base):
    __tablename__ = "children"
    
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("parents.id"))
    
    parent = relationship("Parent", back_populates="children")

# Usage
parent = Parent()
child = Child()
parent.children.append(child)
db.add(parent)
db.commit()

# Removing child from parent's list deletes it
parent.children.remove(child)
db.commit()  # Child is now deleted from database
```

**Related Terms**: Cascade, Delete, Relationship

---

### Primary Key

**Definition**: A unique identifier for each row in a database table.

**Code Example**:
```python
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    
    # Single primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # String primary key (not recommended for most cases)
    # code = Column(String(10), primary_key=True)

# Composite primary key
class OrderItem(Base):
    __tablename__ = "order_items"
    
    order_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    
    __table_args__ = (
        PrimaryKeyConstraint('order_id', 'product_id'),
    )
```

**Related Terms**: Column, Foreign Key, Unique

---

### Relationship

**Definition**: A Python-level link between two models, defining how they interact.

**Code Example**:
```python
from sqlalchemy.orm import relationship

class Author(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    
    # One-to-many relationship
    books = relationship(
        "Book",
        back_populates="author",  # Bidirectional
        cascade="all, delete-orphan",  # Cascading operations
        lazy="select",  # Loading strategy
        foreign_keys="[Book.author_id]"  # Explicit foreign key
    )

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    author_id = Column(Integer, ForeignKey("authors.id"))
    
    # Many-to-one relationship
    author = relationship(
        "Author",
        back_populates="books",
        lazy="joined"  # Eager loading
    )
    
    # Many-to-many relationship
    tags = relationship(
        "Tag",
        secondary="book_tags",
        back_populates="books"
    )
```

**Related Terms**: Foreign Key, Back Populates, Cascade

---

### Selectinload

**Definition**: Eager loading strategy that uses a separate IN query to load related objects.

**Code Example**:
```python
from sqlalchemy.orm import selectinload

# Basic selectinload
stmt = (
    select(Course)
    .options(selectinload(Course.enrollments))
    .where(Course.id == 1)
)

# Multiple selectinloads
stmt = (
    select(User)
    .options(
        selectinload(User.posts),
        selectinload(User.comments)
    )
    .where(User.id == 1)
)

# Nested selectinload
stmt = (
    select(Author)
    .options(
        selectinload(Author.books)
            .selectinload(Book.reviews)
            .selectinload(Review.user)
    )
    .where(Author.id == 1)
)

result = db.execute(stmt)
author = result.unique().scalar_one_or_none()
```

**Related Terms**: Joinedload, Eager Loading, Lazy Loading

---

### Table

**Definition**: A collection of related data organized in rows and columns within a database.

**Code Example**:
```python
from sqlalchemy import Table, Column, Integer, String, MetaData

# Association table (no ORM model)
student_course = Table(
    "student_course",
    MetaData(),
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("course_id", Integer, ForeignKey("courses.id")),
    Column("enrolled_at", DateTime, default=datetime.utcnow)
)

# Table with constraints
from sqlalchemy import UniqueConstraint, CheckConstraint

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)
    
    __table_args__ = (
        UniqueConstraint('name', name='uq_product_name'),
        CheckConstraint('price > 0', name='ck_positive_price'),
        Index('ix_products_name', 'name')
    )
```

**Related Terms**: Column, Row, Schema

---

### Validator

**Definition**: A function that validates data when setting an attribute on a model.

**Code Example**:
```python
from sqlalchemy.orm import validates
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    age = Column(Integer)
    
    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Invalid email address")
        return email.lower()
    
    @validates('age')
    def validate_age(self, key, age):
        if age < 0 or age > 150:
            raise ValueError("Invalid age")
        return age

# Usage
user = User(email="TEST@EXAMPLE.COM", age=25)
print(user.email)  # "test@example.com"

try:
    invalid_user = User(email="invalid", age=200)
except ValueError as e:
    print(e)  # "Invalid email address"
```

**Related Terms**: Pydantic, Model, Column

---

## Loading Strategies Comparison

| Strategy | Use Case | Performance |
|----------|----------|-------------|
| Lazy | When related data is rarely needed | Best for single objects |
| Joined | When related data is always needed | Good for 1:1, 1:N |
| Selectin | When multiple related collections | Good for N:M |
| Subquery | Complex nested relationships | Moderate |

---

## Summary

Understanding these ORM concepts is essential for building efficient FastAPI applications. Key takeaways:

1. **Association Objects**: Use for many-to-many with extra data
2. **Cascade Rules**: Define parent-child deletion behavior
3. **Eager Loading**: Prevent N+1 queries
4. **Hybrid Properties**: Work in Python and SQL
5. **Validators**: Ensure data integrity
6. **Proper Indexing**: Optimize query performance

**Next**: Move to the testing lecture to learn how to test your database operations.
