# Context Module System

## Progressive Disclosure for Reduced Context Rot

This system breaks the monolithic CLAUDE.md into focused, on-demand modules. Instead of loading 958 lines of guidance for every task, agents load only the ~100 lines of core context plus relevant modules.

## How It Works

### Always Loaded (Core Context ~100 lines)
- `core/philosophy.md` - KISS, YAGNI, critical rules
- `core/ai-guidelines.md` - AI workflow patterns, search commands

### On-Demand Modules (Load as needed)

| Module | Path | When to Load |
|--------|------|--------------|
| React 19 | `react/react19-features.md` | Component/frontend work |
| TypeScript | `typescript/typescript-strict.md` | Type errors, TS config |
| Validation | `validation/validation-zod.md` | Forms, API, external data |
| Testing | `testing/testing-strategy.md` | Test creation, coverage |
| Components | `quality/component-guidelines.md` | JSDoc, props, a11y |
| Code Style | `quality/code-style.md` | Linting, formatting |
| Pre-commit | `quality/pre-commit.md` | Before commit/PR |
| State | `state/state-management.md` | State, React Query |
| Security | `security/security.md` | Auth, security tasks |
| Performance | `performance/performance.md` | Optimization |
| Structure | `structure/project-structure.md` | Architecture |

## Loading Context

### Via Prompt
```
@context react19-features
@context validation-zod testing-strategy
```

### In Agent System Prompts
Reference specific modules based on agent specialty:
- Frontend Architect: Load react, components, state
- Backend Engineer: Load validation, security
- Test Orchestrator: Load testing, pre-commit

### Keyword Detection
Agents should scan requests for trigger keywords and load matching modules. See `index.yaml` for keyword mappings.

## Context Reduction Achieved

| Metric | Before | After |
|--------|--------|-------|
| Always loaded | 958 lines | ~100 lines |
| Typical task | 958 lines | ~200-300 lines |
| Full reference | 958 lines | ~800 lines (all modules) |

## Directory Structure

```
.kiro/context/
├── README.md           # This file
├── index.yaml          # Module manifest with triggers
├── core/
│   ├── philosophy.md   # Always loaded
│   └── ai-guidelines.md # Always loaded
├── react/
│   └── react19-features.md
├── typescript/
│   └── typescript-strict.md
├── validation/
│   └── validation-zod.md
├── testing/
│   └── testing-strategy.md
├── quality/
│   ├── component-guidelines.md
│   ├── code-style.md
│   └── pre-commit.md
├── state/
│   └── state-management.md
├── security/
│   └── security.md
├── performance/
│   └── performance.md
└── structure/
    └── project-structure.md
```

## For Agent Authors

When updating agent system prompts:
1. Reference core modules (always loaded)
2. Specify which modules to load for that agent's specialty
3. Use the `@context` prompt to load additional modules dynamically

## Backwards Compatibility

The original CLAUDE.md remains available for full reference. This system supplements it with a more efficient loading mechanism.
