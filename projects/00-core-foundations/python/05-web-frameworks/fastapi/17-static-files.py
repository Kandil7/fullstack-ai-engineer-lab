"""
17 - Static Files
===================
Serving static files (CSS, JS, images, downloads) with FastAPI.

Requires: pip install aiofiles

Run: uvicorn 17-static-files:app --reload
"""

import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI(title="Static Files in FastAPI")

# Create directories for demo
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("static/images", exist_ok=True)
os.makedirs("static/downloads", exist_ok=True)


# ----- Create demo static files -----
with open("static/css/style.css", "w") as f:
    f.write("""
body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
h1 { color: #333; }
.card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 10px 0; }
""")

with open("static/js/app.js", "w") as f:
    f.write("""
console.log("FastAPI static files demo loaded!");
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM ready');
});
""")

with open("static/images/README.txt", "w") as f:
    f.write("Place image files here (PNG, JPG, SVG, etc.)")

with open("static/downloads/data.csv", "w") as f:
    f.write("name,price,category\nLaptop,999.99,Electronics\nPhone,699.99,Electronics\nBook,19.99,Education\n")


# ----- Mount static files directory -----
# This serves everything under /static/ URL path
app.mount("/static", StaticFiles(directory="static"), name="static")


# ----- HTML page that uses static files -----
@app.get("/", response_class=HTMLResponse)
def home():
    """HTML page demonstrating static file usage."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Static Files Demo</title>
        <link rel="stylesheet" href="/static/css/style.css">
    </head>
    <body>
        <h1>FastAPI Static Files Demo</h1>
        <div class="card">
            <h2>Available Static Files</h2>
            <ul>
                <li><a href="/static/css/style.css">CSS Stylesheet</a></li>
                <li><a href="/static/js/app.js">JavaScript</a></li>
                <li><a href="/static/downloads/data.csv">CSV Download</a></li>
            </ul>
        </div>
        <div class="card">
            <h2>API Endpoints</h2>
            <ul>
                <li><a href="/files/data">Download via FileResponse</a></li>
                <li><a href="/files/stream">Stream large file</a></li>
                <li><a href="/api/files">List available files</a></li>
            </ul>
        </div>
        <script src="/static/js/app.js"></script>
    </body>
    </html>
    """


# ----- Serve individual file with FileResponse -----
@app.get("/files/{filename}")
def download_file(filename: str):
    """Serve a specific file with proper headers."""
    file_path = os.path.join("static/downloads", filename)
    if not os.path.exists(file_path):
        return HTMLResponse(content=f"<h1>File not found: {filename}</h1>", status_code=404)
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",
    )


# ----- Streaming large files -----
@app.get("/files/stream")
def stream_file():
    """Stream a file for large downloads."""
    file_path = "static/downloads/data.csv"
    if not os.path.exists(file_path):
        return HTMLResponse(content="<h1>File not found</h1>", status_code=404)

    def file_iterator():
        with open(file_path, "rb") as f:
            yield from f

    return StreamingResponse(
        file_iterator(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=data.csv"},
    )


# ----- List static files -----
@app.get("/api/files")
def list_files():
    """List all available static files."""
    files = []
    for root, dirs, filenames in os.walk("static"):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, "static")
            files.append({
                "name": filename,
                "path": f"/static/{rel_path}",
                "size": os.path.getsize(filepath),
                "type": "file",
            })
    return {"files": files, "total": len(files)}


# ----- Custom file serving with metadata -----
@app.get("/api/file-info/{filename}")
def file_info(filename: str):
    """Get metadata about a static file."""
    for root, dirs, filenames in os.walk("static"):
        if filename in filenames:
            filepath = os.path.join(root, filename)
            stat = os.stat(filepath)
            return {
                "name": filename,
                "path": os.path.relpath(filepath, "static"),
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "download_url": f"/static/{os.path.relpath(filepath, 'static')}",
            }
    return {"error": f"File '{filename}' not found"}, 404


# Note: GZipMiddleware is added in 10-middleware.py
# For production, add it here too if needed


"""
Testing with curl:
    curl http://127.0.0.1:8000/
    curl http://127.0.0.1:8000/static/css/style.css
    curl http://127.0.0.1:8000/static/js/app.js
    curl -O http://127.0.0.1:8000/files/data.csv
    curl http://127.0.0.1:8000/api/files
    curl http://127.0.0.1:8000/api/file-info/style.css

    Open in browser:
    http://127.0.0.1:8000/
    http://127.0.0.1:8000/static/css/style.css
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
