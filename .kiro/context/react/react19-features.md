# React 19 Key Features

> **Load Trigger**: Frontend work, component creation, React-related tasks

## Automatic Optimizations

- **React Compiler**: Eliminates need for `useMemo`, `useCallback`, and `React.memo`
- Let the compiler handle performance - write clean, readable code

## Core Features

- **Server Components**: Use for data fetching and static content
- **Actions**: Handle async operations with built-in pending states
- **use() API**: Simplified data fetching and context consumption
- **Document Metadata**: Native support for SEO tags
- **Enhanced Suspense**: Better loading states and error boundaries

## React 19 TypeScript Integration (MANDATORY)

- **MUST use `ReactElement` instead of `JSX.Element`** for return types
- **MUST import `ReactElement` from 'react'** explicitly
- **NEVER use `JSX.Element` namespace** - use React types directly

```typescript
// ✅ CORRECT: Modern React 19 typing
import { ReactElement } from 'react';

function MyComponent(): ReactElement {
  return <div>Content</div>;
}

const renderHelper = (): ReactElement | null => {
  return condition ? <span>Helper</span> : null;
};

// ❌ FORBIDDEN: Legacy JSX namespace
function MyComponent(): JSX.Element {  // Cannot find namespace 'JSX'
  return <div>Content</div>;
}
```

## Actions API Example

```typescript
import { useActionState, ReactElement } from 'react';

function ContactForm(): ReactElement {
  const [state, submitAction, isPending] = useActionState(
    async (previousState: unknown, formData: FormData) => {
      const result = contactSchema.safeParse({
        email: formData.get('email'),
        message: formData.get('message'),
      });

      if (!result.success) {
        return { error: result.error.flatten() };
      }

      await sendEmail(result.data);
      return { success: true };
    },
    null
  );

  return (
    <form action={submitAction}>
      <button disabled={isPending}>
        {isPending ? 'Sending...' : 'Send'}
      </button>
    </form>
  );
}
```

## Instant UI Patterns

- Use Suspense boundaries for ALL async operations
- Leverage Server Components for data fetching
- Use the new Actions API for form handling
- Let React Compiler handle optimization

## Component Template (All States)

```typescript
export function FeatureComponent(): ReactElement {
  const { data, isLoading, error } = useQuery({
    queryKey: ['feature'],
    queryFn: fetchFeature
  });

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorBoundary error={error} />;
  if (!data) return <EmptyState />;

  return <FeatureContent data={data} />;
}
```
