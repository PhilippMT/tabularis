# CLAUDE.md

Guidance for Claude Code when working with React 19 applications.

> **Progressive Disclosure**: This file contains core principles (~100 lines). Detailed guidance loads on-demand from `.kiro/context/`. Use `@context [module]` to load specific modules.

## Core Philosophy

- **KISS**: Choose straightforward solutions over complex ones
- **YAGNI**: Implement features only when needed, not speculatively
- **Component-First**: Single responsibility, co-located tests/styles
- **Performance by Default**: Trust React 19 compiler, write clean code
- **Vertical Slice Architecture**: Organize by features, not layers
- **Fail Fast**: Validate inputs early with Zod, throw errors immediately

## Critical Rules (MUST FOLLOW)

1.  **TypeScript**: Strict mode, NEVER use `any`, explicit return types
2.  **Validation**: Use Zod for ALL external data (APIs, forms, URLs)
3.  **Testing**: MINIMUM 80% coverage, co-locate in `__tests__/`
4.  **Components**: MAX 200 lines, handle ALL states (loading/error/empty/success)
5.  **Documentation**: JSDoc for ALL exports, `@fileoverview` in each file
6.  **Commits**: Semantic format (feat:, fix:, docs:, refactor:, test:)
7.  **STATE PROTOCOL**: You **MUST** read `.kiro/TEAM_STATE.md` on activation and **MUST** update it before handoff.

## React 19 Essentials

- Use `ReactElement` (not `JSX.Element`) for return types
- Use Actions API with `useActionState` for forms
- Let compiler handle optimization (no manual memo)
- Use Suspense for async operations

## Quick Reference

| Task | Context Module |
|------|----------------|
| Components/UI | `@context react19-features` |
| TypeScript issues | `@context typescript-strict` |
| Forms/validation | `@context validation-zod` |
| Testing | `@context testing-strategy` |
| State management | `@context state-management` |
| Security/auth | `@context security` |
| Before commit | `@context pre-commit` |

## AI Guidelines

- Check existing patterns before implementing new ones
- Use `rg` (ripgrep) instead of `grep` or `find`
- Use Archon MCP for task management and RAG research
- Run tests with `npx vitest` (not `npm run test`)

## Forbidden Practices

- `any` type (use `unknown` if truly unknown)
- `JSX.Element` (use `ReactElement`)
- `undefined` to optional props (use conditional spreads)
- Skipping tests or documentation
- `@ts-ignore` / `@ts-expect-error`
- `console.log` in committed code

## Context System

Detailed guidance is modularized in `.kiro/context/`:

```
.kiro/context/
├── core/           # Always loaded
├── react/          # React 19 patterns
├── typescript/     # Strict TS config
├── validation/     # Zod patterns
├── testing/        # Test strategy
├── quality/        # Style, docs, pre-commit
├── state/          # State management
├── security/       # Security patterns
├── performance/    # Optimization
└── structure/      # Project architecture
```

**Load specific context**: `@context [module-id]`
**Full reference**: See `CLAUDE-full.md` or browse `.kiro/context/`

---

_For complete guidance, see `.kiro/context/` modules or `CLAUDE-full.md`_
