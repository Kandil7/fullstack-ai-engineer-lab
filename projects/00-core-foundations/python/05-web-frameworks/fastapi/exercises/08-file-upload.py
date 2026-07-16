"""
FastAPI Exercise 08 - File Upload
==================================

Topics covered:
- Uploading files with UploadFile
- File metadata and content reading
- Multiple file uploads
- Saving files to disk
- File size limits

Requirements:
    pip install fastapi uvicorn python-multipart

Run any exercise:
    uvicorn 08-file-upload:app1 --reload
    uvicorn 08-file-upload:app2 --reload
    uvicorn 08-file-upload:app3 --reload
"""

from fastapi import FastAPI, UploadFile, File, Form
import os
import shutil
import hashlib

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# =============================================================================
# Exercise 1: Basic File Upload
# =============================================================================

app1 = FastAPI(title="Exercise 8.1 - Basic File Upload")


@app1.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file and return its metadata with content preview."""
    content = await file.read()
    preview = content[:100].decode("utf-8", errors="replace")
    return {
        "filename": file.filename,
        "size": len(content),
        "content_type": file.content_type,
        "content_preview": preview,
    }


# =============================================================================
# Exercise 2: Save File to Disk
# =============================================================================

app2 = FastAPI(title="Exercise 8.2 - Save to Disk")


@app2.post("/upload-file")
async def upload_and_save(file: UploadFile = File(...)):
    """Upload a file, save to disk, and return metadata with MD5 hash."""
    content = await file.read()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)
    md5_hash = hashlib.md5(content).hexdigest()
    return {
        "filename": file.filename,
        "saved_path": file_path,
        "size": len(content),
        "md5": md5_hash,
    }


@app2.get("/files")
def list_files():
    """List all uploaded files with metadata."""
    files = []
    for fname in os.listdir(UPLOAD_DIR):
        fpath = os.path.join(UPLOAD_DIR, fname)
        if os.path.isfile(fpath):
            files.append({"filename": fname, "size": os.path.getsize(fpath)})
    return {"files": files}


# =============================================================================
# Exercise 3: Multiple Files and Form + File
# =============================================================================

app3 = FastAPI(title="Exercise 8.3 - Multiple Files and Metadata")


@app3.post("/upload-multiple")
async def upload_multiple(files: list[UploadFile] = File(...)):
    """Upload multiple files and return aggregate metadata."""
    file_list = []
    total_size = 0
    for f in files:
        content = await f.read()
        file_list.append({
            "filename": f.filename,
            "size": len(content),
            "content_type": f.content_type,
        })
        total_size += len(content)
    return {"count": len(files), "files": file_list, "total_size": total_size}


@app3.post("/upload-with-metadata")
async def upload_with_metadata(
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
):
    """Upload a file with additional metadata fields."""
    content = await file.read()
    return {
        "title": title,
        "description": description,
        "filename": file.filename,
        "size": len(content),
    }
