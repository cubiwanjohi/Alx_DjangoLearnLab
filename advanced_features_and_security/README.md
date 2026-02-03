## HTTPS and SSL/TLS Security Measures

### 1. SSL Redirect
- **Setting**: `SECURE_SSL_REDIRECT = True`
- **Purpose**: Automatically redirects all HTTP traffic to HTTPS, ensuring data in transit is encrypted.

### 2. HSTS (HTTP Strict Transport Security)
- **Settings**: `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD`
- **Purpose**: Instructs browsers to remember that the site should only be accessed via HTTPS, preventing protocol downgrade attacks.

### 3. Secure Cookies
- **Settings**: `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`
- **Purpose**: Ensures that session and CSRF cookies are never sent over an unencrypted HTTP connection.

### 4. Browser Protection Headers
- **X-Frame-Options**: Set to `DENY` to prevent clickjacking.
- **Content-Type Sniffing**: Disabled to prevent browsers from interpreting files as a different MIME type.
- **XSS Filter**: Enabled to use the browser's built-in protection against cross-site scripting.