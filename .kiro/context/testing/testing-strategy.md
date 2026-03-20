# Testing Strategy

> **Load Trigger**: Testing, test creation, coverage, quality assurance

## MUST Meet These Testing Standards

- **MINIMUM 80% code coverage** - NO EXCEPTIONS
- **MUST co-locate tests** with components in `__tests__` folders
- **MUST use React Testing Library** for all component tests
- **MUST test user behavior** not implementation details
- **MUST mock external dependencies** appropriately
- **NEVER skip tests** for new features or bug fixes

## SonarQube Quality Gates (MUST PASS ALL)

- **Cognitive Complexity**: MAXIMUM 15 per function
- **Cyclomatic Complexity**: MAXIMUM 10 per function
- **Duplicated Lines**: MAXIMUM 3%
- **Technical Debt Ratio**: MAXIMUM 5%
- **ZERO tolerance** for critical/blocker issues
- **ALL new code** must have 80%+ coverage

## Test Example

```typescript
/**
 * @fileoverview Tests for UserProfile component
 * @module features/user/__tests__/UserProfile.test
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent } from '@testing-library/react';

describe('UserProfile', () => {
  it('should update user name on form submission', async () => {
    // Arrange
    const user = userEvent.setup();
    const onUpdate = vi.fn();

    // Act
    render(<UserProfile onUpdate={onUpdate} />);

    const input = screen.getByLabelText(/name/i);
    await user.type(input, 'John Doe');
    await user.click(screen.getByRole('button', { name: /save/i }));

    // Assert
    expect(onUpdate).toHaveBeenCalledWith(
      expect.objectContaining({ name: 'John Doe' })
    );
  });
});
```

## Test File Rules

- **MUST use `unknown` instead of `any`** in Vitest interface declarations
- **MUST use `globalThis` instead of `global`** for cross-platform compatibility
- **MUST include test config files** in appropriate TypeScript projects

## Acceptable Test Patterns

```typescript
// Library interface declaration merging
declare module "vitest" {
  interface Assertion {
    toCustomMatcher(): void;
  }
  interface AsymmetricMatchersContaining {
    toCustomMatcher(): unknown; // unknown, not any
  }
}

// Cross-platform global access
globalThis.fetch = vi.fn(); // Not global.fetch

// Vite environment variables in tests
Object.defineProperty(import.meta, "env", {
  value: { MODE: "test", DEV: false },
  writable: true,
});
```

## Test Configuration

```json
// tsconfig.node.json MUST include ALL Node.js config files
{
  "include": ["vite.config.ts", "vitest.config.ts", "eslint.config.js"]
}

// vite-env.d.ts MUST include vitest globals
/// <reference types="vite/client" />
/// <reference types="vitest/globals" />
```
