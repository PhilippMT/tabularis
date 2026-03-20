# Component Guidelines

> **Load Trigger**: Component creation, documentation, JSDoc, props

## MANDATORY JSDoc Documentation

**MUST document ALL exported functions, classes, and complex logic following Google JSDoc standards**

```typescript
/**
 * Calculates the discount price for a product.
 *
 * @param originalPrice - The original price in cents (must be positive)
 * @param discountPercent - The discount percentage (0-100)
 * @param minPrice - The minimum allowed price after discount in cents
 * @returns The calculated discount price in cents
 * @throws {ValidationError} If any parameter is invalid
 *
 * @example
 * ```typescript
 * const discountedPrice = calculateDiscount(10000, 25, 1000);
 * console.log(discountedPrice); // 7500
 * ```
 */
export function calculateDiscount(
  originalPrice: number,
  discountPercent: number,
  minPrice: number,
): number {
  if (originalPrice <= 0) {
    throw new ValidationError("Original price must be positive");
  }
  const discountAmount = originalPrice * (discountPercent / 100);
  return Math.max(originalPrice - discountAmount, minPrice);
}
```

## Component Documentation

```typescript
/**
 * Button component with multiple variants and sizes.
 *
 * @component
 * @example
 * ```tsx
 * <Button variant="primary" size="medium" onClick={handleSubmit}>
 *   Submit Form
 * </Button>
 * ```
 */
interface ButtonProps {
  /** Visual style variant of the button */
  variant: "primary" | "secondary";
  /** Size of the button @default 'medium' */
  size?: "small" | "medium" | "large";
  /** Click handler for the button */
  onClick: (event: React.MouseEvent<HTMLButtonElement>) => void;
  /** Content to be rendered inside the button */
  children: React.ReactNode;
  /** Whether the button is disabled @default false */
  disabled?: boolean;
}
```

## Code Comment Standards

```typescript
// 1. File headers (REQUIRED for all files)
/**
 * @fileoverview User authentication service.
 * @module features/auth/services/authService
 */

// 2. Complex logic (REQUIRED when cognitive complexity > 5)
/**
 * Validates user permissions against required roles.
 * Uses hierarchical role system where admin > editor > viewer.
 */

// 3. TODOs (MUST include issue number)
// TODO(#123): Implement rate limiting for login attempts

// 4. Inline explanations (REQUIRED for non-obvious code)
// Use exponential backoff with jitter to prevent thundering herd
```

## MANDATORY JSDoc Rules

- **MUST include @param** for every parameter with description
- **MUST include @returns** with description (unless void)
- **MUST include @throws** for any thrown errors
- **MUST include @example** for complex functions
- **MUST add file-level @fileoverview** for each module

## Component Best Practices

- **MAXIMUM 200 lines** per component file
- **MUST follow single responsibility** principle
- **MUST validate props** with Zod when accepting external data
- **MUST implement error boundaries** for all feature modules
- **MUST handle ALL states**: loading, error, empty, and success
- **NEVER return null** without explicit empty state handling
- **MUST include ARIA labels** for accessibility

## Component Integration

- **MUST verify actual prop names** before using components
- **MUST use exact callback parameter types** from interfaces
- **NEVER assume prop names** - verify interfaces first
