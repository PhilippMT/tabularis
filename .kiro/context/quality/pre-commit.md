# Pre-commit Checklist

> **Load Trigger**: Before commit, PR review, final validation

## MUST COMPLETE ALL

- [ ] TypeScript compiles with ZERO errors
- [ ] Zod schemas validate ALL external data
- [ ] Tests written and passing (MINIMUM 80% coverage)
- [ ] ESLint passes with ZERO warnings
- [ ] SonarQube quality gate PASSED
- [ ] ALL states handled (loading, error, empty, success)
- [ ] Accessibility requirements met (ARIA labels, keyboard nav)
- [ ] ZERO console.log statements
- [ ] ALL functions have complete JSDoc documentation
- [ ] Component props are fully documented
- [ ] Complex logic has explanatory comments
- [ ] File-level @fileoverview is present
- [ ] TODOs include issue numbers
- [ ] Component files under 200 lines
- [ ] Cognitive complexity under 15 for all functions

## FORBIDDEN Practices

- **NEVER use `any` type** (except library declaration merging with comments)
- **NEVER skip tests**
- **NEVER ignore TypeScript errors**
- **NEVER trust external data without validation**
- **NEVER exceed complexity limits**
- **NEVER skip documentation**
- **NEVER use undocumented code**
- **NEVER use `JSX.Element`** - use `ReactElement` instead
- **NEVER pass `undefined` to optional props** - use conditional spreads
- **NEVER assume component prop names** - verify interfaces first
- **NEVER use `global`** - use `globalThis` for cross-platform compatibility
- **NEVER omit config files from TypeScript projects** - include ALL .ts files

## Quick Validation Command

```bash
npm run validate
# Runs: type-check && lint && test:coverage
```
