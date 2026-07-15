"""
08 - File Upload
==================
Handling file uploads in FastAPI using UploadFile and File.

Requires: pip install python-multipart

Run: uvicorn 08-file-upload:app --reload
"""

import os
import shutil
import hashlib
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel

app = FastAPI(title="File Upload in FastAPI")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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

    # Save to disk
    file_path = os.path.join(UPLOAD_DIR, file.filename)
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

    file_path = os.path.join(UPLOAD_DIR, f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
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
        file_path = os.path.join(UPLOAD_DIR, file.filename)
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

    # Organize by category
    category_dir = os.path.join(UPLOAD_DIR, category)
    os.makedirs(category_dir, exist_ok=True)

    file_path = os.path.join(category_dir, file.filename)
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
    file_path = os.path.join(UPLOAD_DIR, file.filename)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
