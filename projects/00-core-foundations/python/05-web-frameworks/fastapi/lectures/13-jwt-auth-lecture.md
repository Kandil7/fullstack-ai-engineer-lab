# Lecture 13: JWT Authentication in FastAPI

## Topic Overview

JSON Web Tokens (JWT) have become the standard for implementing authentication in modern web applications. JWT provides a stateless, scalable way to verify user identity without storing session data on the server.

**Why JWT Matters:**
- **Stateless** - No server-side session storage needed
- **Scalable** - Works across multiple servers easily
- **Self-contained** - Token contains all user information
- **Secure** - Signed with cryptographic algorithms
- **Standard** - Industry-standard format supported everywhere

**How JWT Works:**
```
1. User logs in with credentials
2. Server validates credentials
3. Server creates JWT token
4. Token sent to client
5. Client stores token (localStorage/cookie)
6. Client sends token with each request
7. Server validates token without database lookup
```

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Understand JWT structure** - Header, payload, signature
2. **Create JWT tokens** - Generate tokens with user data
3. **Validate JWT tokens** - Verify authenticity and expiration
4. **Implement token refresh** - Handle expired tokens gracefully
5. **Use FastAPI Security** - Leverage built-in security utilities
6. **Store tokens securely** - Best practices for client-side storage
7. **Handle token errors** - Graceful error handling
8. **Implement logout** - Token blacklisting strategies

---

## Key Concepts

### 1. JWT Token Structure

A JWT token consists of three parts separated by dots:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

**Header** (Base64 encoded):
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload** (Base64 encoded):
```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1516242622
}
```

**Signature**:
```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret
)
```

### 2. Token Expiration

```python
from datetime import datetime, timedelta

# Token expires in 15 minutes
access_token_expire = timedelta(minutes=15)

# Token expires in 7 days
refresh_token_expire = timedelta(days=7)
```

### 3. Token Flow

```
Login Flow:
┌─────────┐     ┌─────────┐     ┌─────────┐
│  Client  │────▶│  Server  │────▶│  DB     │
└─────────┘     └─────────┘     └─────────┘
      │               │
      │  POST /login  │
      │──────────────▶│
      │               │ Validate
      │               │──────────▶
      │               │◀──────────
      │  {token: "xxx"}│
      │◀──────────────│

API Request Flow:
┌─────────┐     ┌─────────┐
│  Client  │────▶│  Server  │
└─────────┘     └─────────┘
      │               │
      │ Authorization │
      │ Bearer xxx    │
      │──────────────▶│
      │               │ Validate
      │               │ signature
      │               │ expiration
      │  Response     │
      │◀──────────────│
```

---

## Code Examples

### Example 1: Basic JWT Implementation

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel

app = FastAPI()

# Configuration
SECRET_KEY = "your-secret-key-keep-it-safe"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User model
class User(BaseModel):
    username: str
    email: str
    disabled: bool = False

class UserInDB(User):
    hashed_password: str

# Fake database
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "john@example.com",
        "hashed_password": pwd_context.hash("secret123"),
        "disabled": False,
    }
}

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
```

### Example 2: Token Refresh System

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
    type: Optional[str] = None  # "access" or "refresh"

def create_token(data: dict, expires_delta: timedelta, token_type: str = "access"):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_tokens(user_id: str):
    access_token = create_token(
        data={"sub": user_id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access"
    )
    refresh_token = create_token(
        data={"sub": user_id},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh"
    )
    return {"access_token": access_token, "refresh_token": refresh_token}

@app.post("/token", response_model=Token)
async def login(username: str, password: str):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    tokens = create_tokens(user.id)
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer"
    }

@app.post("/token/refresh")
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if username is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Create new tokens
    tokens = create_tokens(username)
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer"
    }

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if username is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

@app.get("/users/me")
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user
```

### Example 3: Token Blacklisting (Logout)

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Set

app = FastAPI()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# In-memory blacklist (use Redis in production)
blacklisted_tokens: Set[str] = set()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def is_token_blacklisted(token: str) -> bool:
    return token in blacklisted_tokens

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token"
    )
    
    # Check if token is blacklisted
    if is_token_blacklisted(token):
        raise credentials_exception
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    return username

@app.post("/token")
async def login(username: str, password: str):
    if not authenticate_user(username, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token}

@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    # Add token to blacklist
    blacklisted_tokens.add(token)
    return {"message": "Successfully logged out"}

@app.get("/protected")
async def protected_route(current_user = Depends(get_current_user)):
    return {"message": f"Hello {current_user}"}
```

### Example 4: JWT with Custom Claims

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

class TokenPayload(BaseModel):
    sub: str
    email: str
    roles: List[str]
    permissions: List[str]
    exp: datetime
    iat: datetime
    jti: str  # JWT ID for uniqueness

def create_token(
    user_id: str,
    email: str,
    roles: List[str],
    permissions: List[str]
):
    now = datetime.utcnow()
    payload = {
        "sub": user_id,
        "email": email,
        "roles": roles,
        "permissions": permissions,
        "iat": now,
        "exp": now + timedelta(minutes=30),
        "jti": str(uuid.uuid4())  # Unique token ID
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload(**payload)
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    return decode_token(token)

@app.get("/admin/")
async def admin_only(current_user = Depends(get_current_user)):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Admin role required")
    return {"message": f"Welcome admin {current_user.email}"}

@app.get("/user/")
async def user_only(current_user = Depends(get_current_user)):
    if "user" not in current_user.roles:
        raise HTTPException(status_code=403, detail="User role required")
    return {"message": f"Welcome {current_user.email}"}

@app.post("/token")
async def login(username: str, password: str):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(
        user_id=user.id,
        email=user.email,
        roles=user.roles,
        permissions=user.permissions
    )
    return {"access_token": token}
```

### Example 5: JWT with Database

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import databases

app = FastAPI()

DATABASE_URL = "sqlite:///./jwt_demo.db"
database = databases.Database(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)
    hashed_password = Column(String)
    is_active = Column(bool, default=True)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

async def get_user_from_db(username: str):
    query = User.__table__.select().where(User.username == username)
    result = await database.fetch_one(query)
    return result

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
    except jwt.JWTError:
        raise HTTPException(status_code=401)
    
    user = await get_user_from_db(username)
    if user is None:
        raise HTTPException(status_code=401)
    
    return user

@app.get("/users/me")
async def read_users_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }
```

---

## Common Mistakes to Avoid

### Mistake 1: Using Weak Secret Keys

```python
# ❌ WRONG - Weak, predictable secret
SECRET_KEY = "secret123"

# ✅ CORRECT - Strong, random secret
import secrets
SECRET_KEY = secrets.token_urlsafe(32)
# Or from environment variable
SECRET_KEY = os.getenv("SECRET_KEY")
```

### Mistake 2: Not Validating Token Type

```python
# ❌ WRONG - Any token works
def get_user(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get("sub")

# ✅ CORRECT - Validate token type
def get_user(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    if payload.get("type") != "access":
        raise HTTPException(401, "Invalid token type")
    return payload.get("sub")
```

### Mistake 3: Storing Tokens in localStorage

```python
# ❌ WRONG - Vulnerable to XSS
localStorage.setItem("token", token)

# ✅ CORRECT - Use httpOnly cookies
# Set-Cookie: token=xxx; HttpOnly; Secure; SameSite=Strict
```

---

## Best Practices

1. **Use strong secret keys** - Minimum 256 bits
2. **Set short expiration** - 15-30 minutes for access tokens
3. **Implement refresh tokens** - For seamless user experience
4. **Validate all claims** - Check expiration, issuer, audience
5. **Use HTTPS only** - Never send tokens over HTTP
6. **Don't store sensitive data** - Keep payload minimal
7. **Implement token blacklisting** - For logout functionality
8. **Use httpOnly cookies** - More secure than localStorage
9. **Rotate tokens** - Issue new tokens on sensitive operations
10. **Monitor token usage** - Log suspicious activity

---

## Practice Exercises

### Exercise 1: Complete JWT System
Build a complete JWT authentication system with:
- Registration with password hashing
- Login returning access and refresh tokens
- Token refresh endpoint
- Protected routes

### Exercise 2: Role-Based JWT
Implement JWT with role-based access:
- Admin, User, Guest roles
- Role checking middleware
- Permission-based endpoints

### Exercise 3: Token Blacklisting
Create a token blacklisting system:
- Logout endpoint
- Token blacklist storage
- Check blacklist on each request

### Exercise 4: JWT with Database
Build JWT system with database:
- User storage in PostgreSQL
- Token claims from database
- User lookup on each request

### Exercise 5: Multi-Factor Authentication
Implement MFA with JWT:
- TOTP verification
- MFA enrollment flow
- Backup codes

---

## Summary

- **JWT** is a stateless, secure authentication standard
- **Three parts**: Header, Payload, Signature
- **Access tokens** are short-lived (15-30 minutes)
- **Refresh tokens** are long-lived (7-30 days)
- **Always validate** token signature and expiration
- **Use strong secrets** and store securely
- **Implement blacklisting** for logout
- **Prefer httpOnly cookies** over localStorage

---

## Further Reading

- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT.io](https://jwt.io/)
- [OAuth 2.0 Specification](https://oauth.net/2/)
