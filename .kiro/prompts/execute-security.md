# Execute: Security Implementation

## Security-Specific Implementation Framework

This specialized execution framework is optimized for security-focused development tasks, emphasizing threat mitigation, vulnerability prevention, and compliance implementation.

## Security Implementation Process

### Phase 1: Security Requirements Analysis
**Security-Specific Analysis:**
- Threat modeling and attack surface analysis
- Compliance requirements and regulatory standards
- Data classification and protection requirements
- Authentication and authorization needs
- Security control requirements and risk tolerance
- Incident response and monitoring requirements

**Questions to Address:**
- What are the primary security threats and risks?
- What compliance standards must be met?
- What data needs protection and at what level?
- What authentication and authorization patterns are required?
- What security controls need to be implemented?
- What monitoring and incident response capabilities are needed?

### Phase 2: Security Architecture Design
**Security Architecture Planning:**
- Defense-in-depth security strategy
- Authentication and authorization architecture
- Data protection and encryption strategies
- Network security and access control design
- Monitoring and incident response architecture
- Security testing and validation approach

**Security Design Decisions:**
- Choose appropriate authentication mechanisms
- Define authorization patterns and access controls
- Plan data encryption and key management
- Design security monitoring and alerting
- Establish incident response procedures

### Phase 3: Implementation
**Systematic Security Implementation:**

#### Authentication Implementation
```typescript
// JWT-based authentication with refresh tokens
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

export class AuthService {
  private readonly JWT_SECRET = process.env.JWT_SECRET!;
  private readonly REFRESH_SECRET = process.env.REFRESH_SECRET!;
  private readonly ACCESS_TOKEN_EXPIRY = '15m';
  private readonly REFRESH_TOKEN_EXPIRY = '7d';

  async authenticateUser(email: string, password: string): Promise<AuthResult> {
    // Rate limiting check
    await this.checkRateLimit(email);
    
    // Find user with secure query
    const user = await this.userRepository.findByEmail(email);
    if (!user) {
      // Prevent user enumeration
      await this.simulatePasswordCheck();
      throw new AuthenticationError('Invalid credentials');
    }

    // Verify password with timing-safe comparison
    const isValidPassword = await bcrypt.compare(password, user.passwordHash);
    if (!isValidPassword) {
      await this.logFailedAttempt(email);
      throw new AuthenticationError('Invalid credentials');
    }

    // Generate secure tokens
    const accessToken = this.generateAccessToken(user);
    const refreshToken = this.generateRefreshToken(user);
    
    // Store refresh token securely
    await this.storeRefreshToken(user.id, refreshToken);
    
    return {
      accessToken,
      refreshToken,
      user: this.sanitizeUser(user)
    };
  }

  private generateAccessToken(user: User): string {
    return jwt.sign(
      { 
        userId: user.id, 
        email: user.email, 
        role: user.role,
        permissions: user.permissions 
      },
      this.JWT_SECRET,
      { 
        expiresIn: this.ACCESS_TOKEN_EXPIRY,
        issuer: 'taskflow-api',
        audience: 'taskflow-client'
      }
    );
  }
}
```

#### Authorization Implementation
```typescript
// Role-based access control middleware
export const authorize = (requiredPermissions: string[]) => {
  return async (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    try {
      const user = req.user;
      
      // Check if user has required permissions
      const hasPermission = requiredPermissions.every(permission =>
        user.permissions.includes(permission) || user.role === 'admin'
      );
      
      if (!hasPermission) {
        return res.status(403).json({
          error: 'Insufficient permissions',
          required: requiredPermissions,
          message: 'Access denied'
        });
      }
      
      next();
    } catch (error) {
      res.status(401).json({ error: 'Authorization failed' });
    }
  };
};

// Usage in routes
router.get('/admin/users', 
  authenticate,
  authorize(['user:read', 'admin:access']),
  getUsersController
);
```

#### Input Validation and Sanitization
```typescript
// Comprehensive input validation
import { z } from 'zod';
import DOMPurify from 'isomorphic-dompurify';

// SQL injection prevention with parameterized queries
export class SecureUserRepository {
  async findUsersByRole(role: string): Promise<User[]> {
    // Use parameterized query to prevent SQL injection
    return await this.db.query(
      'SELECT id, email, name, role FROM users WHERE role = $1 AND deleted_at IS NULL',
      [role]
    );
  }

  async updateUser(id: string, updates: Partial<User>): Promise<User> {
    // Validate and sanitize input
    const sanitizedUpdates = this.sanitizeUserInput(updates);
    
    // Use transaction for data integrity
    return await this.db.transaction(async (tx) => {
      const user = await tx.user.update({
        where: { id },
        data: sanitizedUpdates
      });
      
      // Log security-relevant changes
      await this.auditLog.logUserUpdate(id, sanitizedUpdates);
      
      return user;
    });
  }

  private sanitizeUserInput(input: Partial<User>): Partial<User> {
    const sanitized: Partial<User> = {};
    
    if (input.name) {
      sanitized.name = DOMPurify.sanitize(input.name.trim());
    }
    
    if (input.email) {
      sanitized.email = input.email.toLowerCase().trim();
    }
    
    // Never allow direct role updates through user input
    // Role changes should go through separate admin endpoints
    
    return sanitized;
  }
}
```

#### Data Encryption Implementation
```typescript
// Data encryption and key management
import crypto from 'crypto';

export class EncryptionService {
  private readonly ALGORITHM = 'aes-256-gcm';
  private readonly KEY_LENGTH = 32;
  private readonly IV_LENGTH = 16;
  private readonly TAG_LENGTH = 16;

  async encryptSensitiveData(data: string): Promise<EncryptedData> {
    const key = await this.getEncryptionKey();
    const iv = crypto.randomBytes(this.IV_LENGTH);
    
    const cipher = crypto.createCipher(this.ALGORITHM, key);
    cipher.setAAD(Buffer.from('taskflow-data'));
    
    let encrypted = cipher.update(data, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    
    const tag = cipher.getAuthTag();
    
    return {
      encrypted,
      iv: iv.toString('hex'),
      tag: tag.toString('hex')
    };
  }

  async decryptSensitiveData(encryptedData: EncryptedData): Promise<string> {
    const key = await this.getEncryptionKey();
    const iv = Buffer.from(encryptedData.iv, 'hex');
    const tag = Buffer.from(encryptedData.tag, 'hex');
    
    const decipher = crypto.createDecipher(this.ALGORITHM, key);
    decipher.setAAD(Buffer.from('taskflow-data'));
    decipher.setAuthTag(tag);
    
    let decrypted = decipher.update(encryptedData.encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    
    return decrypted;
  }

  private async getEncryptionKey(): Promise<Buffer> {
    // In production, use proper key management service
    const keyString = process.env.ENCRYPTION_KEY;
    if (!keyString) {
      throw new Error('Encryption key not configured');
    }
    
    return crypto.scryptSync(keyString, 'salt', this.KEY_LENGTH);
  }
}
```

### Phase 4: Security Controls Implementation
**Security Control Measures:**
- Rate limiting and DDoS protection
- Security headers and CORS configuration
- Content Security Policy implementation
- Session management and token security
- Audit logging and monitoring
- Error handling without information disclosure

**Security Controls Implementation:**
```typescript
// Rate limiting implementation
import rateLimit from 'express-rate-limit';

export const createRateLimit = (options: RateLimitOptions) => {
  return rateLimit({
    windowMs: options.windowMs,
    max: options.max,
    message: {
      error: 'Too many requests',
      retryAfter: Math.ceil(options.windowMs / 1000)
    },
    standardHeaders: true,
    legacyHeaders: false,
    handler: (req, res) => {
      // Log rate limit violations
      logger.warn('Rate limit exceeded', {
        ip: req.ip,
        userAgent: req.get('User-Agent'),
        endpoint: req.path
      });
      
      res.status(429).json({
        error: 'Rate limit exceeded',
        retryAfter: Math.ceil(options.windowMs / 1000)
      });
    }
  });
};

// Security headers middleware
export const securityHeaders = (req: Request, res: Response, next: NextFunction) => {
  // Prevent clickjacking
  res.setHeader('X-Frame-Options', 'DENY');
  
  // Prevent MIME type sniffing
  res.setHeader('X-Content-Type-Options', 'nosniff');
  
  // XSS protection
  res.setHeader('X-XSS-Protection', '1; mode=block');
  
  // Strict transport security
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  
  // Content Security Policy
  res.setHeader('Content-Security-Policy', 
    "default-src 'self'; " +
    "script-src 'self' 'unsafe-inline'; " +
    "style-src 'self' 'unsafe-inline'; " +
    "img-src 'self' data: https:; " +
    "connect-src 'self'; " +
    "font-src 'self'; " +
    "object-src 'none'; " +
    "media-src 'self'; " +
    "frame-src 'none';"
  );
  
  next();
};
```

### Phase 5: Security Testing Implementation
**Security Testing Strategy:**
- Static Application Security Testing (SAST)
- Dynamic Application Security Testing (DAST)
- Dependency vulnerability scanning
- Penetration testing for critical paths
- Security code review and threat modeling
- Compliance validation testing

**Security Testing Examples:**
```typescript
// Security-focused unit tests
describe('Authentication Security', () => {
  it('should prevent timing attacks on login', async () => {
    const startTime = Date.now();
    
    try {
      await authService.authenticateUser('nonexistent@example.com', 'password');
    } catch (error) {
      // Should take similar time as valid user check
    }
    
    const endTime = Date.now();
    const duration = endTime - startTime;
    
    // Should take at least minimum time to prevent timing attacks
    expect(duration).toBeGreaterThan(100);
  });

  it('should rate limit failed login attempts', async () => {
    const email = 'test@example.com';
    
    // Attempt multiple failed logins
    for (let i = 0; i < 5; i++) {
      try {
        await authService.authenticateUser(email, 'wrongpassword');
      } catch (error) {
        // Expected to fail
      }
    }
    
    // Next attempt should be rate limited
    await expect(
      authService.authenticateUser(email, 'wrongpassword')
    ).rejects.toThrow('Rate limit exceeded');
  });
});

// SQL injection prevention test
describe('SQL Injection Prevention', () => {
  it('should prevent SQL injection in user queries', async () => {
    const maliciousInput = "'; DROP TABLE users; --";
    
    // Should not execute malicious SQL
    const result = await userRepository.findUsersByRole(maliciousInput);
    
    // Should return empty array, not crash or execute malicious SQL
    expect(result).toEqual([]);
    
    // Verify users table still exists
    const userCount = await userRepository.count();
    expect(userCount).toBeGreaterThan(0);
  });
});
```

### Phase 6: Monitoring and Incident Response
**Security Monitoring Implementation:**
- Security event logging and correlation
- Anomaly detection and alerting
- Incident response automation
- Forensic data collection and preservation
- Security metrics and reporting
- Threat intelligence integration

### Phase 7: Compliance Documentation
**Security Documentation Requirements:**
- Security architecture documentation
- Threat model and risk assessment
- Security control implementation guide
- Incident response procedures
- Compliance mapping and evidence
- Security training and awareness materials

## Security-Specific Validation Checklist

### Authentication Security Validation
- [ ] Password policies enforce strong passwords
- [ ] Multi-factor authentication implemented where required
- [ ] Session management prevents session fixation
- [ ] Token security prevents token theft and replay
- [ ] Account lockout prevents brute force attacks
- [ ] Password reset process is secure

### Authorization Security Validation
- [ ] Role-based access control properly implemented
- [ ] Principle of least privilege enforced
- [ ] Authorization checks on all protected resources
- [ ] Privilege escalation prevented
- [ ] Cross-user data access prevented
- [ ] Admin functions properly protected

### Data Protection Validation
- [ ] Sensitive data encrypted at rest and in transit
- [ ] Encryption keys properly managed
- [ ] Data classification implemented
- [ ] Data retention policies enforced
- [ ] Data deletion is secure and complete
- [ ] Personal data handling complies with regulations

### Input Validation Security
- [ ] All inputs validated and sanitized
- [ ] SQL injection prevention implemented
- [ ] Cross-site scripting (XSS) prevention implemented
- [ ] Command injection prevention implemented
- [ ] File upload security implemented
- [ ] API input validation comprehensive

### Infrastructure Security Validation
- [ ] Security headers properly configured
- [ ] HTTPS enforced for all communications
- [ ] CORS properly configured
- [ ] Rate limiting prevents abuse
- [ ] Error handling doesn't leak information
- [ ] Logging captures security events

## Security Implementation Success Criteria

### Threat Mitigation
- All identified threats have appropriate controls
- Security controls are properly implemented and tested
- Defense-in-depth strategy is effective
- Attack surface is minimized
- Incident response procedures are tested

### Compliance Achievement
- All regulatory requirements are met
- Compliance evidence is documented
- Audit trails are comprehensive
- Privacy requirements are satisfied
- Security policies are enforced

### Security Monitoring
- Security events are properly logged
- Anomalies are detected and alerted
- Incident response is automated where possible
- Security metrics are tracked and reported
- Threat intelligence is integrated

### Continuous Improvement
- Security testing is automated
- Vulnerability management is systematic
- Security training is provided
- Security reviews are regular
- Lessons learned are incorporated

This security-specific execution framework ensures systematic, comprehensive security implementation with thorough validation and continuous monitoring.