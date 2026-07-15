# Lecture 19: ORM Patterns with SQLAlchemy in FastAPI

## Overview

Object-Relational Mapping (ORM) is a powerful technique that bridges the gap between object-oriented Python code and relational databases. This lecture provides an in-depth exploration of SQLAlchemy ORM patterns, including model design, relationship handling, query optimization, and advanced patterns for building robust database-backed FastAPI applications.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Design effective SQLAlchemy models with proper relationships
2. Implement all relationship types (one-to-one, one-to-many, many-to-many)
3. Write efficient queries using the ORM
4. Use eager loading and lazy loading appropriately
5. Implement model mixins and inheritance
6. Handle complex queries with joins and subqueries
7. Optimize database performance with proper indexing
8. Use advanced patterns like association objects and hybrid properties

---

## Key Concepts

### 1. Model Design Principles

Effective model design is crucial for maintainable applications:

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

# Base mixin for common fields
class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Unique constraints
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    
    # Regular columns
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Using mixin
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    def __str__(self):
        return self.username
```

### 2. Relationship Types

#### One-to-Many Relationship
```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Author(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    
    # One author has many books
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    
    # Each book belongs to one author
    author = relationship("Author", back_populates="books")
```

#### One-to-One Relationship
```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    
    # One user has one profile
    profile = relationship("Profile", back_populates="user", uselist=False)

class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True)
    bio = Column(Text)
    avatar_url = Column(String(500))
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    # Profile belongs to one user
    user = relationship("User", back_populates="profile")
```

#### Many-to-Many Relationship
```python
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

# Association table
student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True),
    Column("enrolled_at", DateTime, default=datetime.utcnow)
)

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    
    # Many students can take many courses
    courses = relationship("Course", secondary=student_course, back_populates="students")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    
    # Many courses can have many students
    students = relationship("Student", secondary=student_course, back_populates="courses")
```

---

## Code Examples

### Example 1: Complex Model with All Relationship Types

```python
# models.py
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, 
    ForeignKey, Float, Table, Index
)
from sqlalchemy.orm import (
    DeclarativeBase, relationship, validates
)
from datetime import datetime

class Base(DeclarativeBase):
    pass

# Many-to-Many association with extra fields
class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    grade = Column(Float, nullable=True)
    
    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    
    __table_args__ = (
        Index('ix_enrollment_student', 'student_id'),
        Index('ix_enrollment_course', 'course_id'),
    )

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    
    # One department has many professors
    professors = relationship("Professor", back_populates="department")

class Professor(Base):
    __tablename__ = "professors"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    
    # Many professors belong to one department
    department = relationship("Department", back_populates="professors")
    
    # One professor teaches many courses
    courses = relationship("Course", back_populates="professor")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    credits = Column(Integer, default=3)
    professor_id = Column(Integer, ForeignKey("professors.id"))
    
    # Many courses taught by one professor
    professor = relationship("Professor", back_populates="courses")
    
    # Many-to-many with students
    enrollments = relationship("Enrollment", back_populates="course")
    
    # Property to get students
    @property
    def students(self):
        return [enrollment.student for enrollment in self.enrollments]

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True)
    
    # Many-to-many with courses
    enrollments = relationship("Enrollment", back_populates="student")
    
    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Invalid email address")
        return email
```

### Example 2: CRUD Operations with Relationships

```python
# crud.py
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select
from typing import List, Optional

# Create with relationships
def create_department_with_professors(
    db: Session, 
    department: DepartmentCreate, 
    professors: List[ProfessorCreate]
):
    # Create department
    db_department = Department(name=department.name)
    db.add(db_department)
    db.flush()
    
    # Create professors
    for prof in professors:
        db_professor = Professor(
            name=prof.name,
            department_id=db_department.id
        )
        db.add(db_professor)
    
    db.commit()
    db.refresh(db_department)
    return db_department

# Read with eager loading
def get_course_with_details(db: Session, course_id: int):
    stmt = (
        select(Course)
        .options(
            joinedload(Course.professor),
            joinedload(Course.enrollments)
                .selectinload(Enrollment.student)
        )
        .where(Course.id == course_id)
    )
    result = db.execute(stmt)
    return result.unique().scalar_one_or_none()

# Read with filtering
def get_courses_by_department(
    db: Session, 
    department_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Course]:
    stmt = (
        select(Course)
        .join(Professor)
        .where(Professor.department_id == department_id)
        .offset(skip)
        .limit(limit)
    )
    result = db.execute(stmt)
    return result.scalars().all()

# Update with relationships
def update_student_courses(
    db: Session,
    student_id: int,
    course_ids: List[int]
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return None
    
    # Clear existing enrollments
    student.enrollments.clear()
    
    # Add new enrollments
    for course_id in course_ids:
        course = db.query(Course).filter(Course.id == course_id).first()
        if course:
            enrollment = Enrollment(student_id=student_id, course_id=course_id)
            db.add(enrollment)
    
    db.commit()
    db.refresh(student)
    return student

# Delete with cascade
def delete_department(db: Session, department_id: int):
    department = db.query(Department).filter(Department.id == department_id).first()
    if department:
        # Cascading delete will remove related professors
        db.delete(department)
        db.commit()
        return True
    return False
```

### Example 3: Advanced Query Patterns

```python
# queries.py
from sqlalchemy import func, and_, or_, select
from sqlalchemy.orm import Session, joinedload

# Complex filtering
def search_courses(
    db: Session,
    query: Optional[str] = None,
    department_id: Optional[int] = None,
    min_credits: Optional[int] = None,
    max_credits: Optional[int] = None
):
    stmt = select(Course)
    
    filters = []
    
    if query:
        filters.append(
            or_(
                Course.title.ilike(f"%{query}%"),
                Course.description.ilike(f"%{query}%")
            )
        )
    
    if department_id:
        stmt = stmt.join(Professor)
        filters.append(Professor.department_id == department_id)
    
    if min_credits:
        filters.append(Course.credits >= min_credits)
    
    if max_credits:
        filters.append(Course.credits <= max_credits)
    
    if filters:
        stmt = stmt.where(and_(*filters))
    
    result = db.execute(stmt)
    return result.scalars().all()

# Aggregation queries
def get_course_statistics(db: Session, course_id: int):
    stmt = (
        select(
            func.count(Enrollment.id).label("total_enrolled"),
            func.avg(Enrollment.grade).label("average_grade"),
            func.min(Enrollment.grade).label("min_grade"),
            func.max(Enrollment.grade).label("max_grade")
        )
        .where(Enrollment.course_id == course_id)
    )
    result = db.execute(stmt)
    return result.one()

# Subquery example
def get_students_above_average(db: Session, course_id: int):
    # Subquery for average grade
    avg_subquery = (
        select(func.avg(Enrollment.grade))
        .where(Enrollment.course_id == course_id)
        .scalar_subquery()
    )
    
    # Main query
    stmt = (
        select(Student)
        .join(Enrollment)
        .where(
            and_(
                Enrollment.course_id == course_id,
                Enrollment.grade > avg_subquery
            )
        )
    )
    
    result = db.execute(stmt)
    return result.scalars().all()

# Join with multiple relationships
def get_department_statistics(db: Session, department_id: int):
    stmt = (
        select(
            Department.name,
            func.count(Professor.id).label("professor_count"),
            func.count(Course.id).label("course_count"),
            func.count(Enrollment.id).label("student_count")
        )
        .join(Professor)
        .join(Course, Professor.id == Course.professor_id)
        .outerjoin(Enrollment)
        .where(Department.id == department_id)
        .group_by(Department.name)
    )
    
    result = db.execute(stmt)
    return result.one()
```

### Example 4: Model Mixins and Inheritance

```python
# mixins.py
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

# Timestamp mixin
class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Soft delete mixin
class SoftDeleteMixin:
    is_deleted = Column(String(1), default='N')
    deleted_at = Column(DateTime, nullable=True)
    
    def soft_delete(self):
        self.is_deleted = 'Y'
        self.deleted_at = datetime.utcnow()

# Audit mixin
class AuditMixin:
    created_by = Column(String(100))
    updated_by = Column(String(100))
    
    def set_created_by(self, user_id: str):
        self.created_by = user_id
    
    def set_updated_by(self, user_id: str):
        self.updated_by = user_id

# Using mixins
class Product(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)

class Order(Base, TimestampMixin, AuditMixin):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    order_number = Column(String(50), unique=True)
    total = Column(Float)

# Table inheritance (single table)
class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    type = Column(String(20))  # discriminator column
    
    __mapper_args__ = {
        'polymorphic_identity': 'employee',
        'polymorphic_on': type
    }

class Manager(Employee):
    __mapper_args__ = {
        'polymorphic_identity': 'manager'
    }
    
    department = Column(String(100))

class Developer(Employee):
    __mapper_args__ = {
        'polymorphic_identity': 'developer'
    }
    
    programming_language = Column(String(50))
```

---

## Common Mistakes to Avoid

### 1. N+1 Query Problem

```python
# BAD: N+1 queries - 1 query for departments + N queries for professors
departments = db.query(Department).all()
for dept in departments:
    # This triggers a new query for each department!
    print(dept.professors)

# GOOD: Eager loading
departments = db.query(Department).options(
    joinedload(Department.professors)
).all()
```

### 2. Not Using Relationships Properly

```python
# BAD: Manual foreign key management
@app.post("/courses/")
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(
        title=course.title,
        professor_id=course.professor_id  # Manual FK
    )
    db.add(db_course)
    db.commit()
    return db_course

# GOOD: Using relationships
@app.post("/courses/")
def create_course(
    course: CourseCreate, 
    db: Session = Depends(get_db)
):
    professor = db.query(Professor).filter(Professor.id == course.professor_id).first()
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")
    
    db_course = Course(title=course.title, professor=professor)
    db.add(db_course)
    db.commit()
    return db_course
```

### 3. Forgetting to Close Sessions

```python
# BAD: Session leak
def get_courses():
    db = SessionLocal()
    courses = db.query(Course).all()
    return courses  # Session never closed!

# GOOD: Use dependency injection
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses
```

---

## Best Practices

1. **Use Mixins**: Share common fields across models
2. **Implement Cascade Rules**: Define what happens when parent is deleted
3. **Use Eager Loading**: Prevent N+1 query problems
4. **Add Proper Indexes**: Optimize query performance
5. **Use Type Hints**: Improve code clarity and IDE support
6. **Validate Data**: Use Pydantic models for API validation
7. **Handle Transactions**: Use try/except with rollback
8. **Use Migrations**: Track schema changes with Alembic
9. **Document Relationships**: Use docstrings to explain complex relationships
10. **Test Database Operations**: Write tests for CRUD operations

---

## Practice Exercises

### Exercise 1: E-Commerce Models
Create models for an e-commerce application:
- Products with categories
- Users with orders
- Order items with quantities
- Reviews with ratings

### Exercise 2: Blog Platform
Implement a blog platform with:
- Users and roles (admin, author, reader)
- Posts with comments
- Tags with many-to-many relationships
- Categories with hierarchy (self-referential)

### Exercise 3: Query Optimization
Optimize the following queries:
1. Get all posts with author and comments
2. Search posts by multiple criteria
3. Calculate statistics (average comments per post)
4. Find top authors by post count

---

## Summary

- SQLAlchemy ORM provides powerful tools for database operations
- Relationships define how models interact
- Use mixins for code reuse
- Eager loading prevents N+1 queries
- Proper indexing improves performance
- Handle transactions carefully
- Use migrations for schema management

**Next Lecture**: We'll explore advanced ORM patterns including async operations and complex queries.
