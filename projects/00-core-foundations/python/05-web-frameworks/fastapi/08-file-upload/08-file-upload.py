"""
08 - File Upload
==================
Handling file uploads in FastAPI using UploadFile and File.

Requires: pip install python-multipart

Run: uvicorn 08-file-upload:app --reload
"""

import os
import sys
import shutil
import hashlib
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel

app = FastAPI(title="File Upload in FastAPI")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def safe_upload_path(base_dir: str, client_name: str) -> str:
    """
    Build a safe on-disk path from a client-supplied filename.

    Prevents path traversal: an attacker could send filenames like
    "../../etc/passwd" to escape the upload directory. We strip directory
    components with os.path.basename, reject empty/relative names, then
    confirm the resolved realpath is still inside base_dir before returning.
    """
    safe_name = os.path.basename(client_name or "")
    if not safe_name or safe_name in ("..", "."):
        raise HTTPException(status_code=400, detail="Invalid filename")

    base_root = os.path.realpath(base_dir)
    full_path = os.path.realpath(os.path.join(base_root, safe_name))
    if os.path.commonpath([base_root, full_path]) != base_root:
        raise HTTPException(status_code=400, detail="Invalid filename")
    return full_path


class FileMetadata(BaseModel):
    filename: str
    content_type: str
    size: int
    md5_hash: str


# ----- Single file upload -----
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a single file.
    UploadFile provides:
    - filename: original filename
    - content_type: MIME type
    - file: file-like object (SpooledTemporaryFile)
    - read(), write(), seek(), close()
    """
    content = await file.read()
    size = len(content)
    md5 = hashlib.md5(content).hexdigest()

    # Save to disk — sanitize the client filename to prevent path traversal
    file_path = safe_upload_path(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": size,
        "size_human": f"{size / 1024:.2f} KB",
        "md5": md5,
        "saved_to": file_path,
    }


# ----- Upload with allowed types -----
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


@app.post("/upload/image/")
async def upload_image(file: UploadFile = File(...)):
    """Upload only image files with MIME type validation."""
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Allowed: {ALLOWED_TYPES}",
        )

    content = await file.read()
    max_size = 5 * 1024 * 1024  # 5MB
    if len(content) > max_size:
        raise HTTPException(status_code=400, detail="File too large. Max 5MB.")

    # Sanitize the client filename before embedding it in the saved name
    # (prevents path traversal via names like "../../evil.png").
    safe_name = os.path.basename(file.filename or "")
    if not safe_name or safe_name in ("..", "."):
        raise HTTPException(status_code=400, detail="Invalid filename")
    file_path = safe_upload_path(
        UPLOAD_DIR,
        f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_name}",
    )
    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "filename": file.filename,
        "saved_as": os.path.basename(file_path),
        "content_type": file.content_type,
        "size": len(content),
    }


# ----- Multiple file upload -----
@app.post("/upload/multiple/")
async def upload_multiple(files: list[UploadFile] = File(...)):
    """Upload multiple files at once."""
    results = []
    for file in files:
        content = await file.read()
        # Sanitize each client filename to prevent path traversal
        file_path = safe_upload_path(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(content)
        results.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
        })

    return {
        "total_files": len(results),
        "files": results,
    }


# ----- Upload with metadata -----
@app.post("/upload/document/")
async def upload_document(
    file: UploadFile = File(...),
    category: str = "general",
    description: str = "",
):
    """Upload file with additional metadata fields."""
    content = await file.read()

    # Organize by category. Both `category` and the filename are client
    # controlled, so sanitize both to prevent path traversal (e.g. a
    # category of "../../etc" escaping the upload root).
    safe_category = os.path.basename(category or "")
    if not safe_category or safe_category in ("..", "."):
        raise HTTPException(status_code=400, detail="Invalid category")
    category_dir = safe_upload_path(UPLOAD_DIR, safe_category)
    os.makedirs(category_dir, exist_ok=True)

    file_path = safe_upload_path(category_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "filename": file.filename,
        "category": category,
        "description": description,
        "content_type": file.content_type,
        "size": len(content),
        "path": file_path,
    }


# ----- Stream large files -----
@app.post("/upload/large/")
async def upload_large_file(file: UploadFile = File(...)):
    """
    Stream large files without loading entirely into memory.
    Uses file.read() in chunks.
    """
    chunk_size = 1024 * 1024  # 1MB chunks
    total_size = 0
    md5_hash = hashlib.md5()
    # Sanitize the client filename to prevent path traversal
    file_path = safe_upload_path(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        while chunk := await file.read(chunk_size):
            f.write(chunk)
            md5_hash.update(chunk)
            total_size += len(chunk)

    return {
        "filename": file.filename,
        "total_size": total_size,
        "total_size_human": f"{total_size / (1024 * 1024):.2f} MB",
        "md5": md5_hash.hexdigest(),
    }


# ----- List uploaded files -----
@app.get("/uploads/")
def list_uploads():
    """List all uploaded files."""
    files = []
    for root, dirs, filenames in os.walk(UPLOAD_DIR):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, UPLOAD_DIR)
            files.append({
                "name": filename,
                "path": rel_path,
                "size": os.path.getsize(filepath),
            })
    return {"total": len(files), "files": files}


"""
Testing with curl:
    curl -X POST http://127.0.0.1:8000/upload/ -F "file=@test.txt"

    curl -X POST http://127.0.0.1:8000/upload/image/ -F "file=@photo.jpg"

    curl -X POST http://127.0.0.1:8000/upload/multiple/ -F "files=@file1.txt" -F "files=@file2.pdf"

    curl -X POST http://127.0.0.1:8000/upload/document/ -F "file=@report.pdf" -F "category=reports" -F "description=Q4+report"

    curl http://127.0.0.1:8000/uploads/
"""

def _verify():
    """Smoke-test the app in-process with TestClient (no real server)."""
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        print("[skip] fastapi not installed")
        return

    client = TestClient(app)
    created_paths = []  # track files written so we can clean them up

    try:
        r = client.post(
            "/upload/",
            files={"file": ("verify_hello.txt", b"hello fastapi", "text/plain")},
        )
        assert r.status_code == 200
        assert "md5" in r.json()
        created_paths.append(r.json()["saved_to"])

        r = client.post(
            "/upload/image/",
            files={"file": ("verify_photo.jpg", b"\xff\xd8\xff\xe0fakejpeg", "image/jpeg")},
        )
        assert r.status_code == 200
        created_paths.append(os.path.join(UPLOAD_DIR, r.json()["saved_as"]))

        r = client.post(
            "/upload/image/",
            files={"file": ("verify_evil.txt", b"not an image", "text/plain")},
        )
        assert r.status_code == 400  # MIME type rejected

        r = client.post(
            "/upload/multiple/",
            files=[
                ("files", ("verify_a.txt", b"aaa", "text/plain")),
                ("files", ("verify_b.txt", b"bbb", "text/plain")),
            ],
        )
        assert r.status_code == 200
        assert r.json()["total_files"] == 2
        # response does not include saved paths, so track them for cleanup
        created_paths.append(os.path.join(UPLOAD_DIR, "verify_a.txt"))
        created_paths.append(os.path.join(UPLOAD_DIR, "verify_b.txt"))

        r = client.post(
            "/upload/document/",
            files={"file": ("verify_report.txt", b"report data", "text/plain")},
            params={"category": "verify_cat", "description": "Q4 report"},
        )
        assert r.status_code == 200
        assert r.json()["category"] == "verify_cat"
        assert r.json()["description"] == "Q4 report"
        created_paths.append(r.json()["path"])

        r = client.get("/uploads/")
        assert r.status_code == 200
        assert "total" in r.json()
    finally:
        # Clean up only the files this verification created (Windows: close first)
        for p in created_paths:
            try:
                os.remove(p)
            except OSError:
                pass
        try:
            os.rmdir(os.path.join(UPLOAD_DIR, "verify_cat"))
        except OSError:
            pass

    print("[OK] 08-file-upload: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        _verify()
