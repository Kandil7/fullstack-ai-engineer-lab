# Lecture 17: FastAPI Static Files

## Topic Overview

Static files are files that are served directly to clients without any server-side processing. This includes CSS stylesheets, JavaScript files, images, fonts, and other assets. FastAPI provides built-in support for serving static files using Starlette's StaticFiles class.

**Why Static Files Matter:**
- **Separation of concerns** - Keep assets separate from Python code
- **Performance** - Serve files directly without processing overhead
- **Caching** - Browsers can cache static files
- **CDN support** - Can be served from content delivery networks
- **Security** - Properly configured, prevents directory traversal

**Common Static File Types:**
- **CSS** - Stylesheets (.css)
- **JavaScript** - Scripts (.js)
- **Images** - Photos, icons (.png, .jpg, .svg)
- **Fonts** - Web fonts (.woff2, .ttf)
- **Documents** - PDFs, downloads (.pdf)
- **Media** - Videos, audio (.mp4, .mp3)

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Configure static file serving** - Set up FastAPI to serve static files
2. **Organize static directory** - Structure assets properly
3. **Serve CSS and JavaScript** - Include styles and scripts in pages
4. **Handle images and fonts** - Serve media assets
5. **Implement caching** - Configure browser caching headers
6. **Use CDN integration** - Serve files from external CDNs
7. **Secure static files** - Prevent directory traversal attacks
8. **Optimize assets** - Compression and minification

---

## Key Concepts

### 1. Static Files vs Dynamic Content

```
Static Files:
- CSS, JS, Images, Fonts
- No server-side processing
- Can be cached
- Served from file system or CDN
- Fast delivery

Dynamic Content:
- HTML pages with variables
- API responses
- Server-side processing
- Generated per request
- Cannot be cached (usually)
```

### 2. Directory Structure

```
project/
├── main.py
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── bootstrap.min.css
│   ├── js/
│   │   ├── main.js
│   │   └── app.js
│   ├── images/
│   │   ├── logo.png
│   │   ├── hero.jpg
│   │   └── favicon.ico
│   ├── fonts/
│   │   ├── custom.woff2
│   │   └── icon-font.ttf
│   └── downloads/
│       └── report.pdf
└── templates/
    └── index.html
```

### 3. How Static Files Work

```
Browser Request:
GET /static/css/style.css

FastAPI Response:
1. Mount checks if path matches "/static"
2. StaticFiles looks up file in directory
3. Returns file with appropriate Content-Type
4. Browser receives and caches file

Content-Type headers:
- .css → text/css
- .js → application/javascript
- .png → image/png
- .jpg → image/jpeg
- .woff2 → font/woff2
```

---

## Code Examples

### Example 1: Basic Static Files Setup

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    return templates.TemplateResponse("index.html", {"request": request})
```

### Example 2: Multiple Static Directories

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Multiple static directories
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/media", StaticFiles(directory="media"), name="media")
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")
```

### Example 3: HTML with Static Files

```python
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

**templates/index.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My App</title>
    
    <!-- CSS -->
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    
    <!-- Favicon -->
    <link rel="icon" href="/static/images/favicon.ico" type="image/x-icon">
</head>
<body>
    <header>
        <img src="/static/images/logo.png" alt="Logo" class="logo">
    </header>
    
    <main>
        <h1>Welcome to My App</h1>
        <p>This page uses static files.</p>
    </main>
    
    <!-- JavaScript -->
    <script src="/static/js/main.js"></script>
    <script src="/static/js/app.js"></script>
</body>
</html>
```

### Example 4: Static Files with CSS

**static/css/style.css:**
```css
/* Reset and base styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
}

/* Header */
header {
    background: #35424a;
    color: #ffffff;
    padding: 20px 0;
}

header .logo {
    height: 50px;
}

/* Main content */
main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* Footer */
footer {
    background: #35424a;
    color: #ffffff;
    text-align: center;
    padding: 20px 0;
    margin-top: 40px;
}

/* Utility classes */
.container {
    width: 80%;
    margin: auto;
    overflow: hidden;
}

.btn {
    display: inline-block;
    background: #e8491d;
    color: #fff;
    padding: 10px 20px;
    text-decoration: none;
    border-radius: 5px;
}

.btn:hover {
    background: #333;
}
```

### Example 5: Static Files with JavaScript

**static/js/main.js:**
```javascript
// Main application JavaScript

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('App loaded!');
    
    // Initialize components
    initNavigation();
    initForms();
});

// Navigation toggle
function initNavigation() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
}

// Form validation
function initForms() {
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
            }
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
        } else {
            input.classList.remove('error');
        }
    });
    
    return isValid;
}

// API calls
async function fetchData(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}
```

### Example 6: Serving Images

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve images directory
app.mount("/images", StaticFiles(directory="static/images"), name="images")
```

**HTML usage:**
```html
<!-- Direct image -->
<img src="/images/logo.png" alt="Logo">

<!-- Responsive image -->
<img src="/images/hero.jpg" alt="Hero" class="hero-image">

<!-- SVG icon -->
<img src="/images/icon.svg" alt="Icon" width="24" height="24">

<!-- Favicon -->
<link rel="icon" href="/images/favicon.ico">
```

### Example 7: Serving Fonts

```python
app.mount("/fonts", StaticFiles(directory="static/fonts"), name="fonts")
```

**CSS usage:**
```css
/* Custom font */
@font-face {
    font-family: 'CustomFont';
    src: url('/fonts/custom.woff2') format('woff2'),
         url('/fonts/custom.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}

body {
    font-family: 'CustomFont', Arial, sans-serif;
}

/* Icon font */
@font-face {
    font-family: 'IconFont';
    src: url('/fonts/icon-font.woff2') format('woff2');
}

.icon-home::before {
    font-family: 'IconFont';
    content: "\e001";
}
```

### Example 8: Static Files with CDN

```python
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Configure CDN URLs
CDN_URL = "https://cdn.example.com/v1"

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "cdn_url": CDN_URL
        }
    )
```

**templates/index.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <!-- CDN for Bootstrap -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    
    <!-- CDN for Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Local CSS -->
    <link rel="stylesheet" href="/static/css/style.css">
    
    <!-- Or use configured CDN -->
    <link rel="stylesheet" href="{{ cdn_url }}/css/custom.css">
</head>
<body>
    <!-- Content -->
    
    <!-- CDN Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Local Scripts -->
    <script src="/static/js/main.js"></script>
</body>
</html>
```

### Example 9: Static Files with Caching

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Custom static files with caching headers
from starlette.staticfiles import StaticFiles as StarletteStaticFiles
from starlette.responses import Response

class CachedStaticFiles(StarletteStaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        
        # Add caching headers
        if path.endswith(('.css', '.js', '.png', '.jpg', '.woff2')):
            response.headers["Cache-Control"] = "public, max-age=31536000"
        elif path.endswith('.html'):
            response.headers["Cache-Control"] = "no-cache"
        
        return response

app.mount("/static", CachedStaticFiles(directory="static"), name="static")
```

### Example 10: Security - Preventing Directory Traversal

```python
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

app = FastAPI()

# Safe static file serving
STATIC_DIR = Path("static").resolve()

@app.get("/files/{file_path:path}")
async def serve_file(file_path: str):
    # Construct full path
    full_path = (STATIC_DIR / file_path).resolve()
    
    # Security check: ensure path is within static directory
    if not str(full_path).startswith(str(STATIC_DIR)):
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    # Check if file exists
    if not full_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Serve file
    from starlette.responses import FileResponse
    return FileResponse(full_path)
```

---

## Common Mistakes to Avoid

### Mistake 1: Not Mounting Static Files

```python
# ❌ WRONG - Static files not accessible
app = FastAPI()

@app.get("/")
async def root():
    return templates.TemplateResponse("index.html", {})
# CSS/JS links won't work!

# ✅ CORRECT - Mount static files
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
```

### Mistake 2: Wrong Path in HTML

```python
# ❌ WRONG - Path doesn't match mount
app.mount("/assets", StaticFiles(directory="static"), name="static")

# In HTML:
# <link rel="stylesheet" href="/static/css/style.css">  # ❌

# ✅ CORRECT - Match the mount path
# <link rel="stylesheet" href="/assets/css/style.css">  # ✅
```

### Mistake 3: No Directory Structure

```python
# ❌ WRONG - All files in one directory
static/
├── style.css
├── main.js
├── logo.png
└── font.woff2

# ✅ CORRECT - Organized structure
static/
├── css/
│   └── style.css
├── js/
│   └── main.js
├── images/
│   └── logo.png
└── fonts/
    └── font.woff2
```

---

## Best Practices

1. **Organize by type** - Separate CSS, JS, images, fonts
2. **Use descriptive names** - `main.js` not `a.js`
3. **Implement caching** - Set appropriate Cache-Control headers
4. **Use CDNs for libraries** - Bootstrap, jQuery, Font Awesome
5. **Minify production assets** - Reduce file sizes
6. **Enable gzip** - Compress text-based files
7. **Use versioning** - `style.css?v=1.2.3` for cache busting
8. **Secure file serving** - Prevent directory traversal
9. **Set proper Content-Type** - Browsers need correct MIME types
10. **Use relative paths** - More portable across environments

---

## Practice Exercises

### Exercise 1: Portfolio Website
Create a portfolio with:
- CSS for styling
- JavaScript for interactivity
- Images for projects
- Responsive design

### Exercise 2: Blog with Static Assets
Build a blog with:
- Custom CSS theme
- Image optimization
- Font loading strategy
- Performance optimization

### Exercise 3: E-commerce Product Images
Implement product images with:
- Multiple sizes
- Lazy loading
- Fallback images
- Image gallery

### Exercise 4: Documentation Site
Create documentation with:
- Syntax highlighting CSS
- Search JavaScript
- Custom fonts
- PDF downloads

### Exercise 5: Dashboard with Charts
Build a dashboard with:
- Chart.js integration
- Custom CSS dashboard
- Data visualization
- Real-time updates

---

## Summary

- **Static files** are served directly without processing
- **Use `app.mount()`** to serve static directories
- **Organize files** by type (css, js, images, fonts)
- **Match HTML paths** to mount configuration
- **Implement caching** for better performance
- **Use CDNs** for popular libraries
- **Secure serving** to prevent directory traversal
- **Optimize assets** for production

---

## Further Reading

- [FastAPI StaticFiles Documentation](https://fastapi.tiangolo.com/advanced/static-files/)
- [Starlette StaticFiles](https://www.starlette.io/staticfiles/)
- [Web Performance Optimization](https://web.dev/performance/)
