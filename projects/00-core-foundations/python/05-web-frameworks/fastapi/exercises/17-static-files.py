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

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os


# =============================================================================
# Exercise 1: Basic Static File Serving
# =============================================================================

app1 = FastAPI(title="Exercise 1 - Basic Static Files")

# Mount static files directory (create ./static/ with some files first)
os.makedirs("static", exist_ok=True)
app1.mount("/static", StaticFiles(directory="static"), name="static")


@app1.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Static Files Exercise</h1>
        <p>Static files are served from /static/ directory.</p>
        <ul>
            <li><a href="/static/style.css">CSS file</a></li>
            <li><a href="/static/app.js">JS file</a></li>
            <li><a href="/static/logo.png">Image file</a></li>
        </ul>
    </body>
    </html>
    """


# =============================================================================
# Exercise 2: Multiple Static Directories
# =============================================================================

app2 = FastAPI(title="Exercise 2 - Multiple Static Directories")

# Mount multiple static directories
os.makedirs("static", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("media", exist_ok=True)

app2.mount("/static", StaticFiles(directory="static"), name="static_files")
app2.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app2.mount("/media", StaticFiles(directory="media"), name="media")


@app2.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Multiple Static Directories</h1>
        <ul>
            <li><a href="/static/style.css">Static file</a></li>
            <li><a href="/uploads/doc.pdf">Uploads file</a></li>
            <li><a href="/media/logo.png">Media file</a></li>
        </ul>
    </body>
    </html>
    """


# =============================================================================
# Exercise 3: Dynamic File Download
# =============================================================================

app3 = FastAPI(title="Exercise 3 - Dynamic File Download")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app3.get("/download/{filename}")
async def download_file(filename: str):
    # Validate filename - no path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename: path traversal detected")

    filepath = os.path.join(DOWNLOAD_DIR, filename)
    # Ensure the resolved path is within the download directory
    resolved = os.path.normpath(os.path.join(os.getcwd(), filepath))
    if not resolved.startswith(os.path.normpath(os.path.join(os.getcwd(), DOWNLOAD_DIR))):
        raise HTTPException(status_code=400, detail="Invalid filename: path traversal detected")

    if not os.path.isfile(filepath):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")

    return FileResponse(
        filepath,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


# =============================================================================
# Exercise 4: Static Files with Templates
# =============================================================================

app4 = FastAPI(title="Exercise 4 - Static Files with Templates")
os.makedirs("static", exist_ok=True)
app4.mount("/static", StaticFiles(directory="static"), name="static_assets")
templates = Jinja2Templates(directory="templates")


@app4.get("/", response_class=HTMLResponse)
async def styled_page(request: Request):
    try:
        return templates.TemplateResponse(
            "styled.html",
            {"request": request, "title": "Styled Page"}
        )
    except Exception:
        return HTMLResponse("""
        <html>
        <head>
            <link rel="stylesheet" href="/static/style.css">
            <title>Styled Page</title>
        </head>
        <body>
            <h1>Styled Page</h1>
            <p>This page loads CSS from /static/style.css and JS from /static/app.js</p>
            <script src="/static/app.js"></script>
        </body>
        </html>
        """)


# =============================================================================
# Exercise 5: Favicon and Robots.txt
# =============================================================================

app5 = FastAPI(title="Exercise 5 - Standard Web Files")


@app5.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    return """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /private/

Sitemap: https://example.com/sitemap.xml
"""


@app5.get("/sitemap.xml", response_class=PlainTextResponse)
async def sitemap():
    return """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://example.com/about</loc>
    <lastmod>2024-01-15</lastmod>
    <priority>0.8</priority>
  </url>
</urlset>
"""


@app5.get("/favicon.ico")
async def favicon():
    favicon_path = os.path.join("static", "favicon.ico")
    if os.path.isfile(favicon_path):
        return FileResponse(favicon_path, media_type="image/x-icon")
    # Return a simple SVG favicon as fallback
    return PlainTextResponse(
        content="""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">
        <rect width="16" height="16" rx="3" fill="#4A90D9"/>
        <text x="8" y="12" text-anchor="middle" fill="white" font-size="10" font-family="Arial">F</text>
        </svg>""",
        media_type="image/svg+xml"
    )


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
