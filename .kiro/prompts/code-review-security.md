# Security-Focused Code Review

## Security Code Review Framework

This specialized code review framework focuses on identifying security vulnerabilities, validating security controls, and ensuring compliance with security best practices.

## Security Review Process

### Phase 1: Security Context Analysis
**Security Review Preparation:**
- Identify security-sensitive components and data flows
- Review threat model and security requirements
- Understand compliance requirements and standards
- Analyze attack surface and potential vulnerabilities
- Review previous security findings and remediation

**Security Context Questions:**
- What security-sensitive operations are being performed?
- What data is being processed and how sensitive is it?
- What authentication and authorization controls are in place?
- What external interfaces and integrations exist?
- What compliance requirements apply to this code?

### Phase 2: Vulnerability Assessment
**Common Vulnerability Categories:**

#### Authentication and Session Management
```typescript
// ❌ SECURITY ISSUE: Weak password requirements
const isValidPassword = (password: string) => password.length >= 6;

// ✅ SECURE: Strong password requirements
const isValidPassword = (password: string) => {
  const minLength = 12;
  const hasUpperCase = /[A-Z]/.test(password);
  const hasLowerCase = /[a-z]/.test(password);
  const hasNumbers = /\d/.test(password);
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
  
  return password.length >= minLength && 
         hasUpperCase && 
         hasLowerCase && 
         hasNumbers && 
         hasSpecialChar;
};

// ❌ SECURITY ISSUE: JWT secret in code
const JWT_SECRET = 'mysecret123';

// ✅ SECURE: JWT secret from environment
const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) {
  throw new Error('JWT_SECRET environment variable is required');
}
```

#### Input Validation and Injection Prevention
```typescript
// ❌ SECURITY ISSUE: SQL injection vulnerability
const getUserById = async (id: string) => {
  const query = `SELECT * FROM users WHERE id = '${id}'`;
  return await db.query(query);
};

// ✅ SECURE: Parameterized query
const getUserById = async (id: string) => {
  const query = 'SELECT * FROM users WHERE id = $1';
  return await db.query(query, [id]);
};

// ❌ SECURITY ISSUE: XSS vulnerability
const displayUserName = (name: string) => {
  return `<h1>Welcome ${name}</h1>`;
};

// ✅ SECURE: Proper escaping
import DOMPurify from 'isomorphic-dompurify';

const displayUserName = (name: string) => {
  const sanitizedName = DOMPurify.sanitize(name);
  return `<h1>Welcome ${sanitizedName}</h1>`;
};
```

#### Authorization and Access Control
```typescript
// ❌ SECURITY ISSUE: Missing authorization check
app.get('/admin/users', (req, res) => {
  const users = getAllUsers();
  res.json(users);
});

// ✅ SECURE: Proper authorization
app.get('/admin/users', authenticate, authorize(['admin']), (req, res) => {
  const users = getAllUsers();
  res.json(users);
});

// ❌ SECURITY ISSUE: Insecure direct object reference
app.get('/user/:id/profile', (req, res) => {
  const profile = getUserProfile(req.params.id);
  res.json(profile);
});

// ✅ SECURE: Access control validation
app.get('/user/:id/profile', authenticate, (req, res) => {
  const requestedUserId = req.params.id;
  const currentUserId = req.user.id;
  
  // Users can only access their own profile unless they're admin
  if (requestedUserId !== currentUserId && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Access denied' });
  }
  
  const profile = getUserProfile(requestedUserId);
  res.json(profile);
});
```

#### Data Protection and Encryption
```typescript
// ❌ SECURITY ISSUE: Storing passwords in plain text
const createUser = async (userData: any) => {
  const user = {
    ...userData,
    password: userData.password // Plain text password
  };
  return await db.users.create(user);
};

// ✅ SECURE: Proper password hashing
import bcrypt from 'bcrypt';

const createUser = async (userData: any) => {
  const saltRounds = 12;
  const hashedPassword = await bcrypt.hash(userData.password, saltRounds);
  
  const user = {
    ...userData,
    password: hashedPassword
  };
  return await db.users.create(user);
};

// ❌ SECURITY ISSUE: Sensitive data in logs
logger.info('User login attempt', { email, password });

// ✅ SECURE: No sensitive data in logs
logger.info('User login attempt', { email, timestamp: new Date().toISOString() });
```

### Phase 3: Security Control Validation
**Security Control Checklist:**

#### Rate Limiting and DDoS Protection
```typescript
// ✅ SECURE: Rate limiting implementation
import rateLimit from 'express-rate-limit';

const loginRateLimit = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // Limit each IP to 5 requests per windowMs
  message: 'Too many login attempts, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
});

app.post('/auth/login', loginRateLimit, loginController);
```

#### Security Headers
```typescript
// ✅ SECURE: Security headers middleware
const securityHeaders = (req: Request, res: Response, next: NextFunction) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  next();
};

app.use(securityHeaders);
```

#### Error Handling
```typescript
// ❌ SECURITY ISSUE: Information disclosure in errors
app.use((error: Error, req: Request, res: Response, next: NextFunction) => {
  res.status(500).json({
    error: error.message,
    stack: error.stack, // Exposes internal information
    query: req.query    // May contain sensitive data
  });
});

// ✅ SECURE: Safe error handling
app.use((error: Error, req: Request, res: Response, next: NextFunction) => {
  // Log full error details securely
  logger.error('Application error', {
    message: error.message,
    stack: error.stack,
    url: req.url,
    method: req.method,
    ip: req.ip
  });
  
  // Return generic error to client
  res.status(500).json({
    error: 'Internal server error',
    timestamp: new Date().toISOString()
  });
});
```

### Phase 4: Compliance Validation
**Compliance Requirements Check:**

#### GDPR Compliance
```typescript
// ✅ GDPR: Data minimization and purpose limitation
const collectUserData = (userData: any) => {
  // Only collect necessary data
  const { email, name, preferences } = userData;
  
  return {
    email,
    name,
    preferences,
    createdAt: new Date(),
    // Don't collect unnecessary personal data
  };
};

// ✅ GDPR: Right to deletion
const deleteUserData = async (userId: string) => {
  await db.transaction(async (tx) => {
    // Delete user data from all tables
    await tx.userProfiles.delete({ where: { userId } });
    await tx.userPreferences.delete({ where: { userId } });
    await tx.users.delete({ where: { id: userId } });
    
    // Log deletion for audit trail
    await tx.auditLog.create({
      data: {
        action: 'USER_DATA_DELETED',
        userId,
        timestamp: new Date()
      }
    });
  });
};
```

#### SOC 2 Compliance
```typescript
// ✅ SOC 2: Audit logging
const auditLog = {
  logUserAction: async (userId: string, action: string, details: any) => {
    await db.auditLog.create({
      data: {
        userId,
        action,
        details: JSON.stringify(details),
        timestamp: new Date(),
        ipAddress: details.ipAddress,
        userAgent: details.userAgent
      }
    });
  }
};

// ✅ SOC 2: Access monitoring
const monitorAccess = async (req: Request, res: Response, next: NextFunction) => {
  await auditLog.logUserAction(req.user?.id, 'RESOURCE_ACCESS', {
    resource: req.path,
    method: req.method,
    ipAddress: req.ip,
    userAgent: req.get('User-Agent')
  });
  
  next();
};
```

### Phase 5: Security Testing Validation
**Security Test Coverage:**

#### Authentication Tests
```typescript
describe('Authentication Security', () => {
  it('should prevent brute force attacks', async () => {
    const email = 'test@example.com';
    
    // Attempt multiple failed logins
    for (let i = 0; i < 6; i++) {
      await request(app)
        .post('/auth/login')
        .send({ email, password: 'wrongpassword' })
        .expect(i < 5 ? 401 : 429);
    }
  });

  it('should invalidate tokens on logout', async () => {
    const { token } = await loginUser();
    
    await request(app)
      .post('/auth/logout')
      .set('Authorization', `Bearer ${token}`)
      .expect(200);
    
    // Token should no longer work
    await request(app)
      .get('/protected')
      .set('Authorization', `Bearer ${token}`)
      .expect(401);
  });
});
```

#### Input Validation Tests
```typescript
describe('Input Validation Security', () => {
  it('should prevent SQL injection', async () => {
    const maliciousInput = "'; DROP TABLE users; --";
    
    const response = await request(app)
      .get(`/users/search?name=${encodeURIComponent(maliciousInput)}`)
      .expect(200);
    
    // Should return empty results, not execute malicious SQL
    expect(response.body.users).toEqual([]);
    
    // Verify users table still exists
    const userCount = await db.users.count();
    expect(userCount).toBeGreaterThan(0);
  });

  it('should sanitize XSS attempts', async () => {
    const xssPayload = '<script>alert("xss")</script>';
    
    const response = await request(app)
      .post('/comments')
      .send({ content: xssPayload })
      .expect(201);
    
    // Content should be sanitized
    expect(response.body.comment.content).not.toContain('<script>');
  });
});
```

## Security Review Checklist

### Authentication and Authorization
- [ ] Strong password policies enforced
- [ ] Multi-factor authentication implemented where required
- [ ] Session management secure (no session fixation, proper timeout)
- [ ] JWT tokens properly signed and validated
- [ ] Authorization checks on all protected endpoints
- [ ] Principle of least privilege enforced
- [ ] Role-based access control properly implemented

### Input Validation and Injection Prevention
- [ ] All user inputs validated and sanitized
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (proper output encoding)
- [ ] Command injection prevention
- [ ] Path traversal prevention
- [ ] File upload security implemented
- [ ] API input validation comprehensive

### Data Protection
- [ ] Sensitive data encrypted at rest and in transit
- [ ] Encryption keys properly managed
- [ ] Passwords properly hashed (bcrypt, scrypt, or Argon2)
- [ ] Sensitive data not logged or exposed in errors
- [ ] Data retention policies implemented
- [ ] Secure data deletion implemented

### Security Controls
- [ ] Rate limiting implemented for sensitive endpoints
- [ ] Security headers properly configured
- [ ] HTTPS enforced for all communications
- [ ] CORS properly configured
- [ ] Content Security Policy implemented
- [ ] Error handling doesn't leak information
- [ ] Audit logging captures security events

### Infrastructure Security
- [ ] Dependencies regularly updated and scanned
- [ ] Environment variables used for secrets
- [ ] No hardcoded credentials or secrets
- [ ] Proper file permissions and access controls
- [ ] Security monitoring and alerting implemented
- [ ] Incident response procedures documented

### Compliance Requirements
- [ ] GDPR compliance (if applicable)
- [ ] HIPAA compliance (if applicable)
- [ ] SOC 2 compliance (if applicable)
- [ ] PCI DSS compliance (if applicable)
- [ ] Industry-specific requirements met
- [ ] Audit trails comprehensive and tamper-proof

## Security Review Report Template

### Executive Summary
- Overall security posture assessment
- Critical vulnerabilities identified
- Compliance status summary
- Recommended priority actions

### Detailed Findings

#### Critical Issues (Fix Immediately)
- **Issue**: [Description]
- **Impact**: [Security impact and business risk]
- **Location**: [File and line number]
- **Recommendation**: [Specific fix instructions]
- **Timeline**: Immediate

#### High Priority Issues (Fix Within 1 Week)
- **Issue**: [Description]
- **Impact**: [Security impact and business risk]
- **Location**: [File and line number]
- **Recommendation**: [Specific fix instructions]
- **Timeline**: 1 week

#### Medium Priority Issues (Fix Within 1 Month)
- **Issue**: [Description]
- **Impact**: [Security impact and business risk]
- **Location**: [File and line number]
- **Recommendation**: [Specific fix instructions]
- **Timeline**: 1 month

### Security Best Practices Validation
- Authentication and authorization implementation
- Input validation and injection prevention
- Data protection and encryption
- Security controls and monitoring
- Compliance requirements adherence

### Recommendations
- Immediate security improvements
- Long-term security strategy enhancements
- Security training and awareness needs
- Security tool and process improvements

## Output Format

Save a new file to `.kiro/code-reviews/security-[appropriate-name].md`

This security-focused code review framework ensures comprehensive security validation and provides actionable recommendations for maintaining a strong security posture.