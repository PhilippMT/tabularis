# Project Structure (Vertical Slice Architecture)

> **Load Trigger**: Project setup, architecture, file organization

## Directory Structure

```
src/
├── features/              # Feature-based modules
│   └── [feature]/
│       ├── __tests__/     # Co-located tests (MUST be documented)
│       ├── components/    # Feature components (MUST have JSDoc)
│       ├── hooks/         # Feature-specific hooks (MUST have JSDoc)
│       ├── api/           # API integration (MUST document endpoints)
│       ├── schemas/       # Zod validation schemas (MUST document rules)
│       ├── types/         # TypeScript types (MUST document complex types)
│       └── index.ts       # Public API (MUST have @module documentation)
├── shared/
│   ├── components/        # Shared UI components (MUST have prop docs)
│   ├── hooks/            # Shared custom hooks (MUST have examples)
│   ├── utils/            # Helper functions (MUST have JSDoc)
│   └── types/            # Shared TypeScript types
└── test/                 # Test utilities and setup
```

## Feature Module Example

```
src/features/auth/
├── __tests__/
│   ├── LoginForm.test.tsx
│   └── useAuth.test.ts
├── components/
│   ├── LoginForm.tsx
│   └── LogoutButton.tsx
├── hooks/
│   └── useAuth.ts
├── api/
│   └── authApi.ts
├── schemas/
│   └── authSchemas.ts
├── types/
│   └── auth.types.ts
└── index.ts              # Public exports only
```

## Key Principles

- **Organize by features**, not layers
- **Co-locate related files** (tests with components)
- **Export only public API** from index.ts
- **Keep features independent** - minimize cross-feature imports
