# LibraryProject

This is a basic Django project created to demonstrate Django project setup and running the development server.


## Permissions and Groups

Custom permissions were added to the Book model:
- can_view
- can_create
- can_edit
- can_delete

User groups were created using the Django admin interface:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: all permissions

Views are protected using Django's permission_required decorator.

## Security Best Practices Implemented

The following security measures were implemented in this Django project:

### Secure Settings
- DEBUG is set to False to prevent sensitive information leakage.
- Browser security headers are enabled to mitigate XSS and clickjacking:
  - SECURE_BROWSER_XSS_FILTER
  - SECURE_CONTENT_TYPE_NOSNIFF
  - X_FRAME_OPTIONS
- CSRF and session cookies are secured to HTTPS only.

### CSRF Protection
- All HTML forms include Django's {% csrf_token %} tag to protect against CSRF attacks.

### Secure Data Access
- Django ORM is used for all database queries to prevent SQL injection.
- User input is validated and sanitized using Django ModelForms.

### Content Security Policy
- A Content Security Policy (CSP) header is added via custom middleware.
- The policy restricts content loading to same-origin sources only.

### Testing
- Permissions and access controls were tested manually by assigning users to groups.
- Forms were tested to ensure CSRF protection is enforced.
- Views were verified to handle user input securely.


## HTTPS and Secure Redirect Configuration

This project is configured to enforce HTTPS and apply secure communication best practices.

### HTTPS Enforcement
- All HTTP requests are redirected to HTTPS using `SECURE_SSL_REDIRECT`.
- HTTP Strict Transport Security (HSTS) is enabled with a duration of one year.
- Subdomains are included in the HSTS policy, and preload support is enabled.

### Secure Cookies
- Session cookies are restricted to HTTPS connections only.
- CSRF cookies are restricted to HTTPS connections only.

### Secure HTTP Headers
- Clickjacking protection is enforced using `X_FRAME_OPTIONS = "DENY"`.
- MIME type sniffing is disabled to prevent content-type attacks.
- Browser XSS filtering is enabled.

### Deployment Notes
In a production environment, HTTPS must be enabled at the web server level using valid SSL/TLS certificates.
This can be achieved using servers such as Nginx or Apache configured with certificate files provided by a trusted certificate authority.

### Security Review
These settings ensure that all communication between clients and the server is encrypted, cookies are protected, and common web-based attacks are mitigated.
Further improvements may include automated certificate renewal and additional monitoring.
