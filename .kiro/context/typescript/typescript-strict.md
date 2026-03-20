# TypeScript Strict Configuration

> **Load Trigger**: TypeScript work, type errors, type safety concerns

## MUST Follow These Compiler Options

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "allowJs": false
  }
}
```

## MANDATORY Type Requirements

- **NEVER use `any` type** - use `unknown` if type is truly unknown
- **MUST have explicit return types** for all functions and components
- **MUST use proper generic constraints** for reusable components
- **MUST use type inference from Zod schemas** using `z.infer<typeof schema>`
- **NEVER use `@ts-ignore`** or `@ts-expect-error` - fix the type issue properly

## Type Safety Hierarchy (STRICT ORDER)

1. **Specific Types**: Always prefer specific types when possible
2. **Generic Constraints**: Use generic constraints for reusable code
3. **Unknown**: Use `unknown` for truly unknown data that will be validated
4. **Never `any`**: The only exception is library declaration merging (must be commented)

## TypeScript Project Structure (MANDATORY)

- **App Code**: `tsconfig.app.json` - covers src/ directory
- **Node Config**: `tsconfig.node.json` - MUST include vite.config.ts, vitest.config.ts
- **ESLint Integration**: MUST reference both in parserOptions.project

## Branded Type Safety (MANDATORY)

```typescript
// ✅ CORRECT: Convert plain types to branded types
const cvId = CVIdSchema.parse(numericId);

// ❌ FORBIDDEN: Assuming type without validation
const cvId: CVId = numericId; // Type assertion without validation
```

## ExactOptionalPropertyTypes Compliance (MANDATORY)

- **MUST handle `undefined` vs `null` properly** in API interfaces
- **MUST use conditional spreads** instead of passing `undefined` to optional props
- **MUST convert `undefined` to `null`** for API body types

```typescript
// ✅ CORRECT: Handle exactOptionalPropertyTypes properly
const apiCall = async (data?: string) => {
  return fetch('/api', {
    method: 'POST',
    body: data ? JSON.stringify({ data }) : null,  // null, not undefined
  });
};

// Conditional prop spreading for optional properties
<Input
  label="Email"
  error={errors.email?.message}
  {...(showHelper ? { helperText: "Enter valid email" } : {})}
/>

// ❌ FORBIDDEN: Passing undefined to optional properties
<Input
  label="Email"
  error={errors.email?.message}
  helperText={showHelper ? "Enter valid email" : undefined}
/>
```

## Cross-Platform Compatibility

- **MUST use `globalThis` instead of `global`** for cross-platform compatibility
- **NEVER omit config files from TypeScript projects** - include ALL .ts files
