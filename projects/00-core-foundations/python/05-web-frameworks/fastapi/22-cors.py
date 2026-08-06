"""
22 - CORS (Cross-Origin Resource Sharing)
============================================
Configure CORS to allow or restrict cross-origin requests.
Essential for frontend apps on different domains/ports.

Run: uvicorn 22-cors:app --reload
"""

import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI(title="CORS in FastAPI")


# ----- CORS Configuration -----
# Allow all origins (development only!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----- Endpoints -----
@app.get("/")
def root():
    """Root endpoint — accessible from any origin."""
    return {
        "message": "CORS Demo",
        "note": "This API accepts requests from any origin",
    }


@app.get("/api/data")
def get_data():
    """API endpoint — CORS headers will be added automatically."""
    return {
        "data": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
        ],
        "cors_note": "Check response headers for Access-Control-Allow-Origin",
    }


@app.post("/api/submit")
def submit_data(payload: dict):
    """POST endpoint — preflight handled automatically."""
    return {"received": payload, "status": "ok"}


@app.options("/api/submit")
def preflight_submit():
    """
    Explicit preflight handler (usually handled by CORSMiddleware).
    Returns allowed methods and headers.
    """
    return {"message": "Preflight OK"}


# ----- Serve CORS test page -----
@app.get("/test-cors", response_class=HTMLResponse)
def cors_test_page():
    """HTML page to test CORS from the browser."""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>CORS Test</title></head>
    <body>
        <h1>CORS Test Page</h1>
        <button onclick="testFetch()">Test Fetch API</button>
        <button onclick="testXHR()">Test XMLHttpRequest</button>
        <pre id="output">Results will appear here...</pre>
        <script>
            function log(msg) {
                document.getElementById('output').textContent += msg + '\\n';
            }
            async function testFetch() {
                try {
                    const resp = await fetch('/api/data');
                    const data = await resp.json();
                    log('Fetch: ' + JSON.stringify(data));
                } catch (e) {
                    log('Fetch Error: ' + e.message);
                }
            }
            function testXHR() {
                const xhr = new XMLHttpRequest();
                xhr.open('GET', '/api/data');
                xhr.onload = () => log('XHR: ' + xhr.responseText);
                xhr.onerror = () => log('XHR Error');
                xhr.send();
            }
        </script>
    </body>
    </html>
    """


# ----- Restricted CORS (example) -----
# For production apps with specific frontend origins:
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "https://myapp.com",
#         "https://www.myapp.com",
#         "http://localhost:3000",  # Dev server
#     ],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],
#     allow_headers=["Authorization", "Content-Type"],
# )


# ----- Dynamic CORS based on request -----
@app.middleware("http")
async def dynamic_cors(request: Request, call_next):
    """
    Custom CORS middleware that sets origin dynamically.
    In production, validate the origin against a whitelist.
    """
    response = await call_next(request)

    origin = request.headers.get("origin")
    if origin:
        # In production: check against whitelist
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"

    return response


"""
Testing with curl:
    curl -v http://127.0.0.1:8000/
    # Look for: Access-Control-Allow-Origin: *

    curl -v -X OPTIONS http://127.0.0.1:8000/api/submit
    # Preflight response with allowed methods

    curl -H "Origin: http://example.com" http://127.0.0.1:8000/api/data
    # Check CORS headers in response

    Open in browser:
    http://127.0.0.1:8000/test-cors

    Test from different origin (run on port 3000):
    fetch('http://localhost:8000/api/data').then(r => r.json()).then(console.log)
"""

def _verify():
    """Smoke-test the app in-process with TestClient (no real server)."""
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        print("[skip] fastapi not installed")
        return

    client = TestClient(app)

    # CORS headers only appear on requests that carry an Origin header
    r = client.get("/", headers={"Origin": "http://example.com"})
    assert r.status_code == 200
    assert r.headers.get("Access-Control-Allow-Origin") is not None

    # Simulate a cross-origin request
    r = client.get("/api/data", headers={"Origin": "http://example.com"})
    assert r.status_code == 200
    assert r.headers.get("Access-Control-Allow-Origin") is not None
    assert len(r.json()["data"]) == 2

    r = client.post("/api/submit", json={"name": "test"})
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

    # Preflight request (CORS middleware handles OPTIONS automatically)
    r = client.options(
        "/api/submit",
        headers={
            "Origin": "http://example.com",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert r.status_code == 200
    assert r.headers.get("Access-Control-Allow-Methods") is not None

    r = client.get("/test-cors")
    assert r.status_code == 200
    assert "CORS Test Page" in r.text

    print("[OK] 22-cors: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        _verify()
