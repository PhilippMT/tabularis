# Code Style & Quality

> **Load Trigger**: Linting, formatting, code review, ESLint issues

## Linting Stack (MANDATORY)

- **ESLint 9.x** with TypeScript plugin
- **Prettier 3.x** for formatting
- **eslint-plugin-sonarjs** for code quality
- **Pre-commit validation** must pass before any commit

## ESLint TypeScript Integration (MANDATORY)

- **Project References**: MUST include ALL .ts/.tsx files in parserOptions.project
- **Config Files**: Node.js config files (vite.config.ts, vitest.config.ts) belong in tsconfig.node.json
- **Zero Warnings**: `--max-warnings 0` is MANDATORY - no exceptions
- **Complete Coverage**: Every TypeScript file MUST be parseable by ESLint

## MUST Follow These Rules

```javascript
{
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "error",
    "no-console": ["error", { "allow": ["warn", "error"] }],
    "react/function-component-definition": ["error", {
      "namedComponents": "arrow-function"
    }],
    "sonarjs/cognitive-complexity": ["error", 15],
    "sonarjs/no-duplicate-string": ["error", 3]
  }
}
```

## npm Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "test": "vitest",
    "test:coverage": "vitest --coverage",
    "lint": "eslint . --ext ts,tsx --max-warnings 0",
    "format": "prettier --write \"src/**/*.{ts,tsx}\"",
    "type-check": "tsc --noEmit",
    "validate": "npm run type-check && npm run lint && npm run test:coverage"
  }
}
```

## Semantic Commits

- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **refactor:** Code refactoring
- **test:** Test additions/changes
