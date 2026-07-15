"""
FastAPI Exercise 17 - Static Files
====================================

Topics covered:
- Serving static files in FastAPI
- Mounting static directories
- CSS, JavaScript, and image serving
- Combining static files with templates

Requirements:
    pip install fastapi uvicorn

Run any exercise:
    uvicorn 17-static-files:app1 --reload
    uvicorn 17-static-files:app2 --reload
    uvicorn 17-static-files:app3 --reload

Note: Create directories and files before running:
    mkdir -p static/css static/js static/images
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os


# =============================================================================
# Exercise 1: Basic Static File Serving
# =============================================================================
# Mount static files directory:
#   - Serve files from "./static" at path "/static"
#   - GET /static/css/style.css should return the CSS file
#   - GET /static/js/app.js should return the JS file
#
# Hints:
#   - Use app.mount("/static", StaticFiles(directory="static"))
#   - Files are served at their relative path
#   - Ensure the static/ directory exists before running
#
# Expected behavior:
#   GET http://localhost:8000/static/css/style.css -> CSS content
#   GET http://localhost:8000/static/js/app.js -> JS content
#   GET http://localhost:8000/static/images/logo.png -> Image
#
# Test with:
#   curl http://localhost:8000/static/css/style.css
#   Open browser: http://localhost:8000/static/css/style.css
# =============================================================================

app1 = FastAPI(title="Exercise 1 - Basic Static Files")

# TODO: Mount static files directory


@app1.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
    <head>
        <link rel="stylesheet" href="/static/css/style.css">
    </head>
    <body>
        <h1>Static Files Exercise</h1>
    </body>
    </html>
    """


# =============================================================================
# Exercise 2: Multiple Static Directories
# =============================================================================
# Serve multiple static directories:
#   - "./static" at "/static"
#   - "./uploads" at "/uploads"
#   - "./media" at "/media"
#   - Each directory serves different content types
#
# Hints:
#   - Mount each directory separately
#   - Order matters: mount after all routes
#   - Create directories if they don't exist
#
# Expected behavior:
#   GET /static/style.css -> from static/ directory
#   GET /uploads/document.pdf -> from uploads/ directory
#   GET /media/video.mp4 -> from media/ directory
#
# Test with:
#   curl http://localhost:8000/static/style.css
#   curl http://localhost:8000/uploads/document.pdf
# =============================================================================

app2 = FastAPI(title="Exercise 2 - Multiple Static Directories")

# TODO: Mount multiple static directories


@app2.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Multiple Static Directories</h1>
        <a href="/uploads/doc.pdf">Download Document</a>
        <img src="/media/logo.png" alt="Logo">
    </body>
    </html>
    """


# =============================================================================
# Exercise 3: Dynamic File Download
# =============================================================================
# Create file download endpoints:
#   - GET /download/{filename} serves files from downloads/ directory
#   - Validate filename (no path traversal)
#   - Return 404 if file not found
#   - Add Content-Disposition header for download
#
# Hints:
#   - Use FileResponse for file serving
#   - Validate: filename should not contain ".." or "/"
#   - Set headers: {"Content-Disposition": f"attachment; filename={filename}"}
#
# Expected behavior:
#   GET /download/report.pdf -> Downloads the PDF file
#   GET /download/../../../etc/passwd -> 400 Bad Request
#   GET /download/missing.txt -> 404 Not Found
#
# Test with:
#   curl -O http://localhost:8000/download/report.pdf
#   curl http://localhost:8000/download/../../../etc/passwd
# =============================================================================

app3 = FastAPI(title="Exercise 3 - Dynamic File Download")


@app3.get("/download/{filename}")
async def download_file(filename: str):
    # TODO: Validate filename and serve file
    pass


# =============================================================================
# Exercise 4: Static Files with Templates
# =============================================================================
# Combine static files with Jinja2 templates:
#   - Serve CSS/JS from static/ directory
#   - Templates reference static files
#   - Create a complete HTML page with:
#     * Linked CSS stylesheet
#     * Linked JavaScript file
#     * Image from static/images/
#
# Hints:
#   - In templates, use: <link rel="stylesheet" href="/static/css/style.css">
#   - Use url_for for dynamic URLs: url_for('static', path='css/style.css')
#   - Mount static AFTER defining routes
#
# Expected behavior:
#   GET http://localhost:8000/ -> Full HTML page with styled content
#   CSS and JS load correctly
#   Images display properly
#
# Test with:
#   curl http://localhost:8000/
#   Open browser: http://localhost:8000/
# =============================================================================

app4 = FastAPI(title="Exercise 4 - Static Files with Templates")
templates = Jinja2Templates(directory="templates")


@app4.get("/", response_class=HTMLResponse)
async def styled_page(request: Request):
    # TODO: Render template that uses static files
    pass


# =============================================================================
# Exercise 5: Favicon and Robots.txt
# =============================================================================
# Serve standard web files:
#   - GET /favicon.ico serves favicon
#   - GET /robots.txt serves robots file
#   - GET /sitemap.xml serves sitemap
#   - Return proper content types
#
# Hints:
#   - Use FileResponse with media_type
#   - Or mount static at root with specific paths
#   - Consider using StaticFiles for /favicon.ico specifically
#
# Expected behavior:
#   GET http://localhost:8000/favicon.ico -> favicon image
#   GET http://localhost:8000/robots.txt -> robots.txt content
#   GET http://localhost:8000/sitemap.xml -> XML sitemap
#
# Test with:
#   curl http://localhost:8000/robots.txt
#   curl http://localhost:8000/favicon.ico
# =============================================================================

app5 = FastAPI(title="Exercise 5 - Standard Web Files")


@app5.get("/robots.txt")
async def robots():
    # TODO: Serve robots.txt
    pass


@app5.get("/sitemap.xml")
async def sitemap():
    # TODO: Serve sitemap.xml
    pass


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# After completing the exercises:
#
# 1. Create required directories:
#    mkdir -p static/css static/js static/images
#    mkdir -p uploads media downloads templates
#
# 2. Create sample files:
#    echo "body { color: red; }" > static/css/style.css
#    echo "console.log('hello');" > static/js/app.js
#
# 3. Run each app and verify:
#    - Files are served with correct content types
#    - No path traversal attacks possible
#    - 404 for missing files
#    - Templates correctly reference static assets
# =============================================================================
