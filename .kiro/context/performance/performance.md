# Performance Guidelines

> **Load Trigger**: Performance optimization, bundle size, lazy loading

## React 19 Optimizations

- **Trust the compiler** - avoid manual memoization
- **Use Suspense** for data fetching boundaries
- **Implement code splitting** at route level
- **Lazy load** heavy components

## Bundle Optimization

```typescript
/**
 * @fileoverview Vite configuration for optimized production builds
 * @module vite.config
 */

// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        /**
         * Manual chunk strategy for optimal loading performance.
         * Separates vendor libraries from application code.
         */
        manualChunks: {
          // React core - rarely changes
          "react-vendor": ["react", "react-dom"],
          // Data fetching - moderate change frequency
          "query-vendor": ["@tanstack/react-query"],
          // Form handling - moderate change frequency
          "form-vendor": ["react-hook-form", "zod"],
        },
      },
    },
  },
});
```

## Code Splitting Pattern

```typescript
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App(): ReactElement {
  return (
    <Suspense fallback={<Skeleton />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

## Performance Checklist

- [ ] Route-level code splitting implemented
- [ ] Heavy components lazy loaded
- [ ] Images optimized and lazy loaded
- [ ] Bundle analyzed for unnecessary dependencies
- [ ] TanStack Query configured with appropriate staleTime
