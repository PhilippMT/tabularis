# Context Loader

Load specific context modules based on task requirements.

## Usage

```
@context [module-id]
@context [module-id] [module-id] ...
```

## Available Modules

### Core (Always Loaded)
- `philosophy` - Core development principles (KISS, YAGNI, critical rules)
- `ai-guidelines` - AI workflow patterns, search commands

### React & Frontend
- `react19-features` - React 19 features, TypeScript integration, Actions API
- `component-guidelines` - JSDoc, props documentation, accessibility
- `state-management` - State hierarchy, TanStack Query patterns

### TypeScript & Validation
- `typescript-strict` - Compiler options, strict requirements, branded types
- `validation-zod` - Zod patterns, schema examples, form validation

### Quality & Testing
- `testing-strategy` - Testing standards, SonarQube, test examples
- `code-style` - ESLint, Prettier, formatting rules
- `pre-commit` - Pre-commit checklist, forbidden practices

### Security & Performance
- `security` - Input validation, auth patterns, vulnerability prevention
- `performance` - React 19 optimizations, bundle configuration

### Architecture
- `project-structure` - Vertical slice architecture, directory organization

## Process

1. **Identify the task type** from user request
2. **Scan for keywords** that match module triggers
3. **Load matching modules** by reading from `.kiro/context/`
4. **Apply loaded guidelines** to the current task

## Keyword Triggers

| Keywords | Load Module |
|----------|-------------|
| react, component, jsx, tsx, frontend | `react19-features` |
| typescript, type error, strict, interface | `typescript-strict` |
| zod, validation, schema, form, api response | `validation-zod` |
| test, vitest, coverage, TDD, mock | `testing-strategy` |
| state, useState, context, zustand, useQuery | `state-management` |
| security, auth, XSS, CSRF, sanitize | `security` |
| performance, bundle, lazy, optimization | `performance` |
| eslint, prettier, lint, format | `code-style` |
| commit, PR, review, merge | `pre-commit` |
| JSDoc, documentation, props, ARIA | `component-guidelines` |
| structure, architecture, directory | `project-structure` |

## Example

For a request like "Create a login form with validation":
1. Detect keywords: form, validation
2. Load: `react19-features`, `validation-zod`, `component-guidelines`
3. Apply React 19 patterns, Zod validation, proper documentation

## Module Paths

All modules are in `.kiro/context/`:
- `core/philosophy.md`
- `core/ai-guidelines.md`
- `react/react19-features.md`
- `typescript/typescript-strict.md`
- `validation/validation-zod.md`
- `testing/testing-strategy.md`
- `quality/component-guidelines.md`
- `quality/code-style.md`
- `quality/pre-commit.md`
- `state/state-management.md`
- `security/security.md`
- `performance/performance.md`
- `structure/project-structure.md`
