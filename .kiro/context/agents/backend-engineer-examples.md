# Backend Engineer - Code Examples

> **Load Trigger**: Backend implementation, API development, when examples needed

## API Design Patterns

### RESTful Resource Design
```typescript
GET    /api/v1/tasks           // List resources
POST   /api/v1/tasks           // Create resource
GET    /api/v1/tasks/:id       // Get specific resource
PUT    /api/v1/tasks/:id       // Update resource
DELETE /api/v1/tasks/:id       // Delete resource

// Consistent response format
{
  "success": true,
  "data": { /* resource data */ },
  "meta": {
    "timestamp": "2026-01-04T17:00:00Z",
    "version": "1.0"
  }
}
```

## Authentication Implementation

```typescript
interface AuthService {
  async login(email: string, password: string): Promise<AuthResult> {
    const user = await prisma.user.findUnique({ where: { email } })
    if (!user || !user.isActive) {
      throw new UnauthorizedError('Invalid credentials')
    }

    const isValid = await bcrypt.compare(password, user.passwordHash)
    if (!isValid) {
      throw new UnauthorizedError('Invalid credentials')
    }

    const token = jwt.sign(
      { userId: user.id, email: user.email },
      process.env.JWT_SECRET,
      { expiresIn: '24h' }
    )

    await prisma.user.update({
      where: { id: user.id },
      data: { lastLoginAt: new Date() }
    })

    return { token, user: sanitizeUser(user) }
  }
}
```

## Task Status Workflow

```typescript
const VALID_STATUS_TRANSITIONS = {
  'todo': ['doing', 'cancelled'],
  'doing': ['review', 'blocked', 'cancelled'],
  'review': ['done', 'doing'],
  'blocked': ['todo', 'doing'],
  'done': [], // Final state
  'cancelled': ['todo'] // Can be reopened
}

const isValidStatusTransition = (current: string, next: string): boolean => {
  return VALID_STATUS_TRANSITIONS[current]?.includes(next) || false
}
```

## Permission System

```typescript
interface PermissionService {
  async canViewTask(userId: string, taskId: string): Promise<boolean> {
    const task = await prisma.task.findUnique({
      where: { id: taskId },
      include: { team: { include: { memberships: true } } }
    })
    if (!task) return false
    return task.team.memberships.some(m => m.userId === userId)
  }

  async canEditTask(userId: string, taskId: string): Promise<boolean> {
    const task = await prisma.task.findUnique({
      where: { id: taskId },
      include: { team: { include: { memberships: true } } }
    })
    if (!task) return false
    if (task.reporterId === userId || task.assigneeId === userId) return true
    const membership = task.team.memberships.find(m => m.userId === userId)
    return membership && ['owner', 'admin'].includes(membership.role)
  }
}
```

## Input Validation

```typescript
import { z } from 'zod'

const CreateTaskSchema = z.object({
  title: z.string().min(1).max(500),
  description: z.string().optional(),
  priority: z.enum(['low', 'medium', 'high', 'critical']).default('medium'),
  assigneeId: z.string().uuid().optional(),
  teamId: z.string().uuid(),
  tags: z.array(z.string()).optional(),
  dueDate: z.string().datetime().optional()
})

const validateRequest = (schema: z.ZodSchema) => {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.body = schema.parse(req.body)
      next()
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: 'Invalid input data',
            details: error.errors.map(e => ({
              field: e.path.join('.'),
              message: e.message
            }))
          }
        })
      }
      next(error)
    }
  }
}
```

## Error Handling

```typescript
class APIError extends Error {
  constructor(message: string, public statusCode: number, public code: string) {
    super(message)
    this.name = 'APIError'
  }
}

class ValidationError extends APIError {
  constructor(message: string) { super(message, 400, 'VALIDATION_ERROR') }
}

class UnauthorizedError extends APIError {
  constructor(message = 'Unauthorized') { super(message, 401, 'UNAUTHORIZED') }
}

class ForbiddenError extends APIError {
  constructor(message = 'Forbidden') { super(message, 403, 'FORBIDDEN') }
}

class NotFoundError extends APIError {
  constructor(resource: string, id?: string) {
    super(id ? `${resource} with id ${id} not found` : `${resource} not found`, 404, 'NOT_FOUND')
  }
}

// Global error handler
const errorHandler = (error: Error, req: Request, res: Response, next: NextFunction) => {
  logger.error('API Error', { error: error.message, url: req.url, method: req.method })

  if (error instanceof APIError) {
    return res.status(error.statusCode).json({
      success: false,
      error: { code: error.code, message: error.message }
    })
  }

  res.status(500).json({
    success: false,
    error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' }
  })
}
```

## Caching Strategy

```typescript
import Redis from 'ioredis'
const redis = new Redis(process.env.REDIS_URL)

const getCachedUser = async (userId: string): Promise<User | null> => {
  const cacheKey = `user:${userId}`
  const cached = await redis.get(cacheKey)

  if (cached) return JSON.parse(cached)

  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: { id: true, email: true, firstName: true, lastName: true, isActive: true }
  })

  if (user) {
    await redis.setex(cacheKey, 300, JSON.stringify(user)) // 5 min cache
  }
  return user
}
```

## Testing Examples

```typescript
describe('TaskService', () => {
  it('should create task with valid data', async () => {
    const task = await taskService.createTask('user-123', {
      title: 'Test task',
      teamId: 'team-123',
      priority: 'high'
    })

    expect(task.title).toBe('Test task')
    expect(task.status).toBe('todo')
  })

  it('should throw error for invalid team access', async () => {
    await expect(
      taskService.createTask('user-123', { title: 'Test', teamId: 'invalid' })
    ).rejects.toThrow(ForbiddenError)
  })
})
```
