# =============================================================================
# Django CSRF Protection - Reference Guide
# =============================================================================
# CSRF (Cross-Site Request Forgery) protection prevents malicious websites
# from making requests on behalf of your users.
#
# W3chools Django Tutorial: https://www.w3schools.com/django/django_csrf.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. What is CSRF?
# ---------------------------------------------------------------------------
# CSRF is an attack where a malicious website tricks a user's browser into
# making unintended requests to another site where they're authenticated.
#
# Example attack scenario:
#   1. User is logged into bank.com
#   2. User visits malicious-site.com
#   3. malicious-site.com contains hidden form to bank.com/transfer
#   4. Browser sends request with user's bank cookies
#   5. Bank processes the transfer (thinking it's from the user)

# Django's CSRF protection:
#   1. Generates unique token per session
#   2. Requires token in all POST/PUT/DELETE requests
#   3. Validates token server-side
#   4. Rejects requests without valid token

# ---------------------------------------------------------------------------
# 2. Enabling CSRF Protection
# ---------------------------------------------------------------------------
# CSRF middleware is enabled by default in settings.py:

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',  # ← This one
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# DO NOT remove CsrfViewMiddleware unless you know what you're doing!

# ---------------------------------------------------------------------------
# 3. Using CSRF Token in Templates
# ---------------------------------------------------------------------------
# Every POST form MUST include the CSRF token.

# --- Basic form usage ---
# <form method="post" action="/submit/">
#     {% csrf_token %}
#     <!-- form fields -->
#     <button type="submit">Submit</button>
# </form>

# --- What {% csrf_token %} generates ---
# <input type="hidden" name="csrfmiddlewaretoken"
#        value="a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6">

# --- Manual CSRF token (for JavaScript) ---
# In base template:
# <script>
#     const csrfToken = '{{ csrf_token }}';
# </script>
#
# In JavaScript fetch:
# fetch('/api/submit/', {
#     method: 'POST',
#     headers: {
#         'Content-Type': 'application/json',
#         'X-CSRFToken': csrfToken,
#     },
#     body: JSON.stringify(data),
# });

# --- CSRF cookie for AJAX ---
# The cookie is named 'csrftoken' by default
# Settings:
# CSRF_COOKIE_NAME = 'csrftoken'      # Cookie name
# CSRF_COOKIE_SECURE = True            # Only send over HTTPS
# CSRF_COOKIE_HTTPONLY = False          # Allow JavaScript access

# ---------------------------------------------------------------------------
# 4. CSRF in Django Views
# ---------------------------------------------------------------------------

# --- Standard POST view (CSRF enforced automatically) ---
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def submit_form(request):
    """CSRF is enforced automatically for POST."""
    if request.method == 'POST':
        # Process form data
        name = request.POST.get('name')
        # ...
        return redirect('success')
    return render(request, 'form.html')

# --- Exempt view from CSRF (use carefully!) ---
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def api_webhook(request):
    """Webhook endpoint - CSRF not needed (no user session)."""
    if request.method == 'POST':
        # Process webhook data
        data = request.body
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'POST only'}, status=405)

# When to use @csrf_exempt:
#   - Webhook endpoints (no user session)
#   - API endpoints with token authentication (no cookies)
#   - Third-party integrations
#
# NEVER use @csrf_exempt for regular form submissions!

# ---------------------------------------------------------------------------
# 5. CSRF in AJAX Requests
# ---------------------------------------------------------------------------
# AJAX requests need to include the CSRF token in headers.

# --- Method 1: Include token in header ---
# <script>
#     function getCookie(name) {
#         let cookieValue = null;
#         if (document.cookie && document.cookie !== '') {
#             const cookies = document.cookie.split(';');
#             for (let i = 0; i < cookies.length; i++) {
#                 const cookie = cookies[i].trim();
#                 if (cookie.substring(0, name.length + 1) === (name + '=')) {
#                     cookieValue = decodeURIComponent(
#                         cookie.substring(name.length + 1)
#                     );
#                     break;
#                 }
#             }
#         }
#         return cookieValue;
#     }
#
#     const csrftoken = getCookie('csrftoken');
#
#     fetch('/submit/', {
#         method: 'POST',
#         headers: {
#             'Content-Type': 'application/json',
#             'X-CSRFToken': csrftoken,
#         },
#         body: JSON.stringify({data: 'value'}),
#     });
# </script>

# --- Method 2: jQuery AJAX setup ---
# <script>
#     function getCookie(name) {
#         let cookieValue = null;
#         if (document.cookie && document.cookie !== '') {
#             const cookies = document.cookie.split(';');
#             for (let i = 0; i < cookies.length; i++) {
#                 const cookie = cookies[i].trim();
#                 if (cookie.substring(0, name.length + 1) === (name + '=')) {
#                     cookieValue = decodeURIComponent(
#                         cookie.substring(name.length + 1)
#                     );
#                     break;
#                 }
#             }
#         }
#         return cookieValue;
#     }
#
#     $.ajaxSetup({
#         beforeSend: function(xhr, settings) {
#             if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)
#                 && !this.crossDomain) {
#                 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
#             }
#         }
#     });
# </script>

# --- Method 3: Include in form data (for multipart/form-data) ---
# <script>
#     const form = document.getElementById('myForm');
#     const formData = new FormData(form);
#     // CSRF token is already in the form data from {% csrf_token %}
#
#     fetch('/submit/', {
#         method: 'POST',
#         body: formData,
#     });
# </script>

# ---------------------------------------------------------------------------
# 6. CSRF Settings
# ---------------------------------------------------------------------------
# settings.py configuration:

# CSRF_COOKIE_NAME = 'csrftoken'        # Default: 'csrftoken'
# CSRF_COOKIE_AGE = 31449600            # Default: 1 year (seconds)
# CSRF_COOKIE_DOMAIN = None             # Default: current domain
# CSRF_COOKIE_PATH = '/'                # Default: '/'
# CSRF_COOKIE_SECURE = False            # Set True in production (HTTPS)
# CSRF_COOKIE_HTTPONLY = False          # Set True for extra security
# CSRF_USE_SESSIONS = False             # Store in cookie vs session
# CSRF_FAILURE_VIEW = 'myapp.views.csrf_failure'  # Custom error view

# Production settings:
# CSRF_COOKIE_SECURE = True       # Only send over HTTPS
# CSRF_COOKIE_HTTPONLY = True     # Prevent JavaScript access
# CSRF_COOKIE_SAMESITE = 'Lax'   # Prevent cross-site sending

# ---------------------------------------------------------------------------
# 7. CSRF Failure View
# ---------------------------------------------------------------------------
# Customize what happens when CSRF validation fails.

# myapp/views.py:
# from django.shortcuts import render
#
# def csrf_failure(request, reason=''):
#     """Custom CSRF failure view."""
#     return render(request, '403_csrf.html', {
#         'reason': reason,
#     }, status=403)

# settings.py:
# CSRF_FAILURE_VIEW = 'myapp.views.csrf_failure'

# templates/403_csrf.html:
# <!DOCTYPE html>
# <html>
# <head>
#     <title>CSRF Verification Failed</title>
# </head>
# <body>
#     <h1>CSRF Verification Failed</h1>
#     <p>Sorry, your request could not be processed.</p>
#     <p>Reason: {{ reason }}</p>
#     <p>Please go back and try again.</p>
# </body>
# </html>

# ---------------------------------------------------------------------------
# 8. Common CSRF Errors and Solutions
# ---------------------------------------------------------------------------
# Error: "CSRF verification failed. Request aborted."
#
# Causes and solutions:
#
# 1. Missing {% csrf_token %} in template
#    → Add {% csrf_token %} inside <form>
#
# 2. AJAX request without CSRF header
#    → Add X-CSRFToken header to AJAX requests
#
# 3. Cookie not being sent
#    → Check CSRF_COOKIE_SECURE (must match HTTPS)
#    → Check CSRF_COOKIE_DOMAIN
#
# 4. Cross-origin request
#    → CORS and CSRF are different things
#    → Use django-cors-headers for CORS
#
# 5. Form action URL mismatch
#    → Ensure form action points to same domain
#
# 6. Session expired
#    → Check SESSION_COOKIE_AGE
#
# 7. @csrf_exempt used incorrectly
#    → Only for webhooks/APIs without cookies

# ---------------------------------------------------------------------------
# 9. CSRF vs CORS
# ---------------------------------------------------------------------------
# CSRF and CORS are different security mechanisms:
#
# CSRF (Cross-Site Request Forgery):
#   - Prevents malicious sites from making requests
#   - Uses tokens in forms/headers
#   - Protects state-changing operations (POST, PUT, DELETE)
#
# CORS (Cross-Origin Resource Sharing):
#   - Controls which domains can access your API
#   - Uses HTTP headers (Access-Control-Allow-Origin)
#   - Protects data access from different domains

# For APIs with token auth (JWT, API keys):
#   → CSRF not needed (no cookies)
#   → CORS needed for browser-based access
#
# For session-based apps:
#   → CSRF needed (cookies auto-sent)
#   → CORS not needed (same origin)

# ---------------------------------------------------------------------------
# 10. CSRF Best Practices
# ---------------------------------------------------------------------------
# 1. Always include {% csrf_token %} in POST forms
# 2. Never remove CsrfViewMiddleware
# 3. Only use @csrf_exempt for webhooks/APIs
# 4. For AJAX, include X-CSRFToken header
# 5. Set CSRF_COOKIE_SECURE=True in production
# 6. Use HTTPS in production (required for secure cookies)
# 7. Don't put CSRF tokens in URLs (they'll be logged)
# 8. Keep CSRF tokens secret (don't expose in JavaScript variables)
# 9. Use SameSite cookie attribute for extra protection
# 10. Test CSRF protection regularly with security scans
