# Core Development Philosophy

> **Load Trigger**: Always loaded for all tasks

## KISS (Keep It Simple, Stupid)

Simplicity should be a key goal in design. Choose straightforward solutions over complex ones whenever possible. Simple solutions are easier to understand, maintain, and debug.

## YAGNI (You Aren't Gonna Need It)

Avoid building functionality on speculation. Implement features only when they are needed, not when you anticipate they might be useful in the future.

## Component-First Architecture

Build with reusable, composable components. Each component should have a single, clear responsibility and be self-contained with its own styles, tests, and logic co-located.

## Performance by Default

With React 19's compiler, manual optimizations are largely unnecessary. Focus on clean, readable code and let the compiler handle performance optimizations.

## Design Principles (MUST FOLLOW)

- **Vertical Slice Architecture**: MUST organize by features, not layers
- **Composition Over Inheritance**: MUST use React's composition model
- **Fail Fast**: MUST validate inputs early with Zod, throw errors immediately

## Critical Rules Summary

1. **ENFORCE strict TypeScript** - ZERO compromises on type safety
2. **VALIDATE everything with Zod** - As much as possible
3. **MINIMUM 80% test coverage** - NO EXCEPTIONS
4. **MUST pass ALL SonarQube quality gates** - No merging without passing
5. **MUST co-locate related files** - Tests MUST be in `__tests__` folders
6. **MAXIMUM 200 lines per component** - Split if larger
7. **MAXIMUM cognitive complexity of 15** - Refactor if higher
8. **MUST handle ALL states** - Loading, error, empty, and success
9. **MUST use semantic commits** - feat:, fix:, docs:, refactor:, test:
10. **MUST write complete JSDoc** - ALL exports must be documented

## Forbidden Practices

- **NEVER use `any` type** (except library declaration merging with comments)
- **NEVER skip tests**
- **NEVER ignore TypeScript errors**
- **NEVER trust external data without validation**
- **NEVER exceed complexity limits**
