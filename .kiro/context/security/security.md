# Security Requirements

> **Load Trigger**: Security, authentication, authorization, input validation, XSS, CSRF

## Input Validation (MUST IMPLEMENT ALL)

- **MUST sanitize ALL user inputs** with Zod before processing
- **MUST validate file uploads**: type, size, and content
- **MUST prevent XSS** with proper escaping
- **MUST implement CSP headers** in production
- **NEVER use dangerouslySetInnerHTML** without sanitization

## API Security

- **MUST validate ALL API responses** with Zod schemas
- **MUST handle errors gracefully** without exposing internals
- **NEVER log sensitive data** (passwords, tokens, PII)

## Authentication Patterns

- Use JWT tokens with proper expiration
- Implement refresh token rotation
- Store tokens securely (httpOnly cookies preferred)
- Validate tokens on every protected route

## Authorization Patterns

- Implement role-based access control (RBAC)
- Check permissions at API boundaries
- Never trust client-side role checks alone

## Common Vulnerabilities to Prevent

| Vulnerability | Prevention |
|---------------|------------|
| XSS | Escape output, CSP headers |
| CSRF | CSRF tokens, SameSite cookies |
| SQL Injection | Parameterized queries (Prisma handles this) |
| Path Traversal | Validate file paths, use allowlists |
