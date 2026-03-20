# Security Specialist - Code Examples

> **Load Trigger**: Security implementation, authentication, authorization

## JWT Authentication Implementation

```typescript
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

interface TokenPayload {
  userId: string;
  email: string;
  role: string;
}

class AuthService {
  private readonly JWT_SECRET = process.env.JWT_SECRET!;
  private readonly JWT_EXPIRES_IN = '24h';
  private readonly SALT_ROUNDS = 12;

  async hashPassword(password: string): Promise<string> {
    return bcrypt.hash(password, this.SALT_ROUNDS);
  }

  async verifyPassword(password: string, hash: string): Promise<boolean> {
    return bcrypt.compare(password, hash);
  }

  generateToken(payload: TokenPayload): string {
    return jwt.sign(payload, this.JWT_SECRET, {
      expiresIn: this.JWT_EXPIRES_IN,
    });
  }

  verifyToken(token: string): TokenPayload {
    return jwt.verify(token, this.JWT_SECRET) as TokenPayload;
  }
}
```

## Authorization Middleware

```typescript
import { Request, Response, NextFunction } from 'express';

type Role = 'admin' | 'editor' | 'viewer';

const ROLE_HIERARCHY: Record<Role, number> = {
  admin: 3,
  editor: 2,
  viewer: 1,
};

export function requireRole(minimumRole: Role) {
  return (req: Request, res: Response, next: NextFunction) => {
    const userRole = req.user?.role as Role;

    if (!userRole) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    if (ROLE_HIERARCHY[userRole] < ROLE_HIERARCHY[minimumRole]) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    next();
  };
}

// Usage
app.delete('/api/users/:id', requireRole('admin'), deleteUser);
```

## Input Sanitization with Zod

```typescript
import { z } from 'zod';

// Sanitize and validate user input
const UserInputSchema = z.object({
  email: z
    .string()
    .email()
    .toLowerCase()
    .trim(),
  password: z
    .string()
    .min(8)
    .regex(/[A-Z]/, 'Must contain uppercase')
    .regex(/[a-z]/, 'Must contain lowercase')
    .regex(/[0-9]/, 'Must contain number')
    .regex(/[^A-Za-z0-9]/, 'Must contain special character'),
  name: z
    .string()
    .min(2)
    .max(100)
    .regex(/^[a-zA-Z\s'-]+$/, 'Invalid characters'),
});

// Prevent SQL injection through parameterized queries
// Prisma handles this automatically
const user = await prisma.user.findUnique({
  where: { email: validatedEmail }, // Never concatenate user input
});
```

## Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

// Global rate limiter
export const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: { error: 'Too many requests, please try again later' },
  standardHeaders: true,
  legacyHeaders: false,
});

// Strict limiter for authentication endpoints
export const authLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 5, // 5 failed attempts per hour
  message: { error: 'Too many login attempts' },
  skipSuccessfulRequests: true,
});

// Usage
app.use('/api/', globalLimiter);
app.use('/api/auth/login', authLimiter);
```

## Security Headers

```typescript
import helmet from 'helmet';

app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", 'data:', 'https:'],
        connectSrc: ["'self'"],
        fontSrc: ["'self'"],
        objectSrc: ["'none'"],
        mediaSrc: ["'self'"],
        frameSrc: ["'none'"],
      },
    },
    hsts: {
      maxAge: 31536000,
      includeSubDomains: true,
      preload: true,
    },
    referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
  })
);
```

## CSRF Protection

```typescript
import csrf from 'csurf';

// CSRF protection for state-changing requests
const csrfProtection = csrf({
  cookie: {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
  },
});

app.use(csrfProtection);

// Provide token to frontend
app.get('/api/csrf-token', (req, res) => {
  res.json({ csrfToken: req.csrfToken() });
});
```

## Security Checklist

```markdown
## Pre-Deployment Security Checklist

### Authentication
- [ ] Passwords hashed with bcrypt (12+ rounds)
- [ ] JWT tokens with appropriate expiration
- [ ] Refresh token rotation implemented
- [ ] Failed login attempt limiting

### Authorization
- [ ] Role-based access control implemented
- [ ] Resource ownership verified
- [ ] API endpoints require authentication

### Input Validation
- [ ] All inputs validated with Zod
- [ ] File uploads validated (type, size)
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)

### Transport Security
- [ ] HTTPS enforced
- [ ] HSTS header configured
- [ ] Secure cookies (HttpOnly, Secure, SameSite)

### Logging & Monitoring
- [ ] Security events logged
- [ ] Sensitive data NOT logged
- [ ] Alerting for suspicious activity
```
