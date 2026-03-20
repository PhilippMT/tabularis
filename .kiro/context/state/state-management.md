# State Management

> **Load Trigger**: State management, React Query, Zustand, context, hooks

## MUST Follow This State Hierarchy

1. **Local State**: `useState` ONLY for component-specific state
2. **Context**: For cross-component state within a single feature
3. **Server State**: MUST use TanStack Query for ALL API data
4. **Global State**: Zustand ONLY when truly needed app-wide
5. **URL State**: MUST use search params for shareable state

## MANDATORY Server State Pattern

```typescript
/**
 * @fileoverview User data fetching hook with caching
 * @module features/user/hooks/useUser
 */

import { useQuery, useMutation } from "@tanstack/react-query";

/**
 * Custom hook for fetching and managing user data.
 *
 * @param id - The unique identifier of the user to fetch
 * @returns Query result object with user data, loading, and error states
 *
 * @example
 * ```tsx
 * const { data: user, isLoading, error } = useUser('123');
 *
 * if (isLoading) return <Spinner />;
 * if (error) return <ErrorMessage error={error} />;
 * return <UserProfile user={user} />;
 * ```
 */
function useUser(id: UserId) {
  return useQuery({
    queryKey: ["user", id],
    queryFn: async () => {
      const response = await fetch(`/api/users/${id}`);

      if (!response.ok) {
        throw new ApiError("Failed to fetch user", response.status);
      }

      const data = await response.json();

      // MUST validate with Zod - this is non-negotiable
      return userSchema.parse(data);
    },
    staleTime: 5 * 60 * 1000, // Consider data fresh for 5 minutes
    retry: 3,
  });
}
```

## State Selection Guide

| Use Case | Solution |
|----------|----------|
| Form input values | `useState` |
| Toggle/modal state | `useState` |
| Cross-component in feature | React Context |
| API data | TanStack Query |
| User preferences app-wide | Zustand |
| Filter/search params | URL search params |
