# Data Validation with Zod

> **Load Trigger**: Forms, API responses, external data, validation, schema work

## MUST Follow These Validation Rules

- **MUST validate ALL external data**: API responses, form inputs, URL params, environment variables
- **MUST use branded types**: For all IDs and domain-specific values
- **MUST fail fast**: Validate at system boundaries, throw errors immediately
- **MUST use type inference**: Always derive TypeScript types from Zod schemas
- **NEVER trust external data** without validation
- **MUST validate before using** any data from outside the application

## Schema Example (MANDATORY PATTERNS)

```typescript
import { z } from 'zod';

// MUST use branded types for ALL IDs
const UserIdSchema = z.string().uuid().brand<'UserId'>();
type UserId = z.infer<typeof UserIdSchema>;

// MUST include validation for ALL fields
export const userSchema = z.object({
  id: UserIdSchema,
  email: z.string().email(),
  username: z.string()
    .min(3)
    .max(20)
    .regex(/^[a-zA-Z0-9_]+$/),
  age: z.number().min(18).max(100),
  role: z.enum(['admin', 'user', 'guest']),
  metadata: z.object({
    lastLogin: z.string().datetime(),
    preferences: z.record(z.unknown()).optional(),
  }),
});

export type User = z.infer<typeof userSchema>;

// MUST validate ALL API responses
export const apiResponseSchema = <T extends z.ZodTypeAny>(dataSchema: T) =>
  z.object({
    success: z.boolean(),
    data: dataSchema,
    error: z.string().optional(),
    timestamp: z.string().datetime(),
  });
```

## Form Validation with React Hook Form

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

function UserForm(): ReactElement {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<User>({
    resolver: zodResolver(userSchema),
    mode: 'onBlur',
  });

  const onSubmit = async (data: User): Promise<void> => {
    // Handle validated data
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

## Branded Type Workflow

1. Define schema with `.brand<'TypeName'>()`
2. Export inferred type: `type MyType = z.infer<typeof schema>`
3. Always use `Schema.parse()` at system boundaries
4. Never assign unvalidated data to branded types
