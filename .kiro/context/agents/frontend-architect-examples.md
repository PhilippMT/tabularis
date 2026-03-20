# Frontend Architect - Code Examples

> **Load Trigger**: Component development, React patterns, state management

## Component Template

```typescript
/**
 * @fileoverview Feature component with proper state handling
 * @module features/[feature]/components/FeatureComponent
 */

import { ReactElement } from 'react';
import { useQuery } from '@tanstack/react-query';

interface FeatureComponentProps {
  /** Unique identifier for the feature */
  id: string;
  /** Callback when action is performed */
  onAction: (result: ActionResult) => void;
  /** Optional CSS class name */
  className?: string;
}

/**
 * Feature component with all state handling.
 *
 * @component
 * @example
 * ```tsx
 * <FeatureComponent
 *   id="123"
 *   onAction={handleAction}
 * />
 * ```
 */
export function FeatureComponent({
  id,
  onAction,
  className,
}: FeatureComponentProps): ReactElement {
  const { data, isLoading, error } = useQuery({
    queryKey: ['feature', id],
    queryFn: () => fetchFeature(id),
  });

  if (isLoading) return <Skeleton className={className} />;
  if (error) return <ErrorDisplay error={error} />;
  if (!data) return <EmptyState message="No data found" />;

  return (
    <div className={className} role="region" aria-label="Feature content">
      <FeatureContent data={data} onAction={onAction} />
    </div>
  );
}
```

## Custom Hook Template

```typescript
/**
 * @fileoverview Custom hook for feature data management
 * @module features/[feature]/hooks/useFeature
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

interface UseFeatureOptions {
  enabled?: boolean;
  onSuccess?: (data: Feature) => void;
}

/**
 * Hook for managing feature data with caching.
 *
 * @param id - Feature identifier
 * @param options - Query options
 * @returns Feature query result with mutation helpers
 *
 * @example
 * ```tsx
 * const { data, update, isUpdating } = useFeature('123');
 * ```
 */
export function useFeature(id: string, options?: UseFeatureOptions) {
  const queryClient = useQueryClient();

  const query = useQuery({
    queryKey: ['feature', id],
    queryFn: () => api.getFeature(id),
    enabled: options?.enabled ?? true,
  });

  const mutation = useMutation({
    mutationFn: (updates: FeatureUpdate) => api.updateFeature(id, updates),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['feature', id] });
      options?.onSuccess?.(data);
    },
  });

  return {
    ...query,
    update: mutation.mutate,
    isUpdating: mutation.isPending,
  };
}
```

## Form Component with Validation

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const formSchema = z.object({
  email: z.string().email('Invalid email address'),
  name: z.string().min(2, 'Name must be at least 2 characters'),
});

type FormData = z.infer<typeof formSchema>;

export function ContactForm(): ReactElement {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(formSchema),
    mode: 'onBlur',
  });

  const onSubmit = async (data: FormData): Promise<void> => {
    await submitContact(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} aria-label="Contact form">
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
          {...register('email')}
        />
        {errors.email && (
          <span id="email-error" role="alert">
            {errors.email.message}
          </span>
        )}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}
```

## Accessible Modal Component

```typescript
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export function Modal({
  isOpen,
  onClose,
  title,
  children,
}: ModalProps): ReactElement | null {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;

    if (isOpen) {
      dialog.showModal();
    } else {
      dialog.close();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <dialog
      ref={dialogRef}
      onClose={onClose}
      aria-labelledby="modal-title"
      className="modal"
    >
      <header>
        <h2 id="modal-title">{title}</h2>
        <button
          onClick={onClose}
          aria-label="Close modal"
          type="button"
        >
          ×
        </button>
      </header>
      <div className="modal-content">{children}</div>
    </dialog>
  );
}
```

## Responsive Layout Pattern

```typescript
export function ResponsiveGrid({
  children,
}: {
  children: React.ReactNode;
}): ReactElement {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {children}
    </div>
  );
}
```
