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
from typing import Optional
import os
import shutil

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# =============================================================================
# Exercise 1: Basic File Upload
# =============================================================================
# Create an app that handles file uploads:
#   POST /upload
#       - Accept a single file
#       - Return: {
#           "filename": <original filename>,
#           "size": <file size in bytes>,
#           "content_type": <mime type>,
#           "content_preview": <first 100 chars if text>
#       }
#
# Hints:
#   - Use UploadFile = File(...)
#   - file.filename -> original filename
#   - file.content_type -> MIME type
#   - file.size -> file size (may be None until read)
#   - await file.read() -> file contents as bytes
#   - Decode bytes: content.decode("utf-8") for text preview
#
# Expected behavior:
#   POST /upload with file "hello.txt" containing "Hello, World!"
#       -> {"filename": "hello.txt", "size": 13, "content_type": "text/plain", "content_preview": "Hello, World!"}
#
# Test with:
#   echo "Hello, World!" > hello.txt
#   curl -X POST http://localhost:8000/upload -F "file=@hello.txt"
# =============================================================================

app1 = FastAPI(title="Exercise 8.1 - Basic File Upload")


@app1.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    pass  # TODO: Read file, return metadata and content preview


# =============================================================================
# Exercise 2: Save File to Disk
# =============================================================================
# Create an app that uploads and saves files:
#   POST /upload-file
#       - Accept a single file
#       - Save to uploads/ directory
#       - Return: {
#           "filename": <original filename>,
#           "saved_path": <path where saved>,
#           "size": <size in bytes>,
#           "md5": <md5 hash of content>
#       }
#
#   GET /files
#       - List all uploaded files
#       - Return: {"files": [{"filename": ..., "size": ...}, ...]}
#
# Hints:
#   - Save file: with open(f"uploads/{file.filename}", "wb") as f: shutil.copyfileobj(file.file, f)
#   - Or use: file.file is the SpooledTemporaryFile object
#   - For MD5: import hashlib; hashlib.md5(content).hexdigest()
#   - os.listdir(UPLOAD_DIR) to list files
#   - os.path.getsize() to get file size
#
# Expected behavior:
#   POST /upload-file with "test.txt" -> saves file, returns metadata
#   GET /files -> lists all uploaded files
#
# Test with:
#   curl -X POST http://localhost:8000/upload-file -F "file=@test.txt"
#   curl http://localhost:8000/files
# =============================================================================

app2 = FastAPI(title="Exercise 8.2 - Save to Disk")


@app2.post("/upload-file")
async def upload_and_save(file: UploadFile = File(...)):
    pass  # TODO: Save file to uploads/, return metadata with MD5


@app2.get("/files")
def list_files():
    pass  # TODO: List all files in uploads/ directory


# =============================================================================
# Exercise 3: Multiple Files and Form + File
# =============================================================================
# Create an app that handles:
#   POST /upload-multiple
#       - Accept multiple files (files: list[UploadFile])
#       - Return: {
#           "count": <number of files>,
#           "files": [{"filename": ..., "size": ..., "content_type": ...}, ...],
#           "total_size": <sum of all sizes>
#       }
#
#   POST /upload-with-metadata
#       - Accept: file (UploadFile), title (str Form), description (str Form)
#       - Return: {
#           "title": title,
#           "description": description,
#           "filename": file.filename,
#           "size": <file size>
#       }
#
# Hints:
#   - Multiple files: files: list[UploadFile] = File(...)
#   - Form + File: title: str = Form(...), file: UploadFile = File(...)
#   - You CANNOT combine Body() with File/Form
#   - Iterate over files: for f in files: ...
#
# Expected behavior:
#   POST /upload-multiple with 3 files -> count: 3, files array, total_size
#   POST /upload-with-metadata -> returns metadata + file info
#
# Test with:
#   curl -X POST http://localhost:8000/upload-multiple \
#     -F "files=@file1.txt" -F "files=@file2.txt" -F "files=@file3.txt"
#   curl -X POST http://localhost:8000/upload-with-metadata \
#     -F "title=My Document" -F "description=A test file" -F "file=@doc.txt"
# =============================================================================

app3 = FastAPI(title="Exercise 8.3 - Multiple Files and Metadata")


@app3.post("/upload-multiple")
async def upload_multiple(files: list[UploadFile] = File(...)):
    pass  # TODO: Process all files, return count and metadata


@app3.post("/upload-with-metadata")
async def upload_with_metadata(
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
):
    pass  # TODO: Return combined metadata and file info


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# After completing the exercises:
#
# 1. Run: uvicorn 08-file-upload:app1 --reload
#    - Test single file upload
#    - Verify filename, size, content_type are correct
#    - Verify content preview works
#
# 2. Run: uvicorn 08-file-upload:app2 --reload
#    - Test file save to disk
#    - Verify file exists in uploads/
#    - Verify MD5 hash is correct
#    - Test GET /files lists uploaded files
#
# 3. Run: uvicorn 08-file-upload:app3 --reload
#    - Test multiple file upload
#    - Test form data + file combination
#    - Verify count and total_size are correct
#
# Cleanup:
#   rm -rf uploads/
# =============================================================================
