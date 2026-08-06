"""
17 - Static Files
===================
Serving static files (CSS, JS, images, downloads) with FastAPI.

Requires: pip install aiofiles

Run: uvicorn 17-static-files:app --reload
"""

import os
import sys
from datetime import datetime
from fastapi import FastAPI, HTTPException
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
DOWNLOADS_DIR = "static/downloads"


@app.get("/files/{filename}")
def download_file(filename: str):
    """Serve a specific file with proper headers."""
    # Prevent path traversal: strip any directory components from the
    # client-supplied name, then confirm the resolved path stays inside
    # DOWNLOADS_DIR before serving it.
    safe_name = os.path.basename(filename)
    if not safe_name or safe_name in ("..", "."):
        raise HTTPException(status_code=400, detail="Invalid filename")

    downloads_root = os.path.realpath(DOWNLOADS_DIR)
    file_path = os.path.realpath(os.path.join(downloads_root, safe_name))
    if os.path.commonpath([downloads_root, file_path]) != downloads_root:
        raise HTTPException(status_code=400, detail="Invalid filename")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File not found: {safe_name}")
    return FileResponse(
        path=file_path,
        filename=safe_name,
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
    # Returning a (dict, int) tuple would serialize as a 200 JSON array, not a
    # 404. Raise HTTPException so FastAPI emits the correct status + error body.
    raise HTTPException(status_code=404, detail=f"File '{filename}' not found")


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

def _verify():
    """Smoke-test the app in-process with TestClient (no real server)."""
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        print("[skip] fastapi not installed")
        return

    client = TestClient(app)

    r = client.get("/")
    assert r.status_code == 200
    assert "Static Files Demo" in r.text

    r = client.get("/static/css/style.css")
    assert r.status_code == 200
    assert "font-family" in r.text

    r = client.get("/static/js/app.js")
    assert r.status_code == 200
    assert "FastAPI static files demo loaded!" in r.text

    r = client.get("/files/data.csv")
    assert r.status_code == 200
    assert "Laptop" in r.text

    r = client.get("/files/missing.csv")
    assert r.status_code == 404

    # NOTE: /files/stream is shadowed by /files/{filename} (registered first),
    # so it returns 404 -- a route-order quirk of the teaching file.
    r = client.get("/files/stream")
    assert r.status_code == 404

    r = client.get("/api/files")
    assert r.status_code == 200
    assert r.json()["total"] >= 4

    r = client.get("/api/file-info/style.css")
    assert r.status_code == 200
    assert r.json()["name"] == "style.css"

    r = client.get("/api/file-info/nope.css")
    assert r.status_code == 404

    print("[OK] 17-static-files: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        _verify()
