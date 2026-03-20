# Reflective Meta-Prompting (GEPA Protocol)

> **Context**: This module provides the cognitive framework for **Recursive Self-Correction** and **Reflective Prompt Evolution**.

## Core Principle: "Thinking about Thinking"
Instead of just executing, you must analyze *how* you executed and whether the *instructions* (prompts) could be better.

## Reflection Protocol

### 1. Trajectory Analysis
Review the interaction history (User Request -> Chain of Thought -> Tool Calls -> Output).
Ask:
- **Did I misunderstand the intent?** (Ambiguity in prompt?)
- **Did I misuse a tool?** (Unclear tool doc?)
- **Did I get stuck in a loop?** (Missing "stop" condition?)
- **Did I hallucinate context?** (Missing `@context`?)

### 2. Root Cause Diagnosis
Identify the upstream cause of the failure/inefficiency:
- **Missing Context**: "I didn't know X was forbidden."
- **Ambiguous Instruction**: "The prompt said 'optimize' but not 'how'."
- **Outdated Rule**: "The rule says use X, but X is deprecated."

### 3. Prompt Evolution (The "GEPA Step")
Propose a specific change to the system prompts (`CLAUDE.md`, Agent Definitions) to prevent this future error.

**Format for Proposal:**
```markdown
### Proposed Prompt Update
**Target File**: `.kiro/agents/backend-engineer.md`
**Reason**: Agent kept using `var` instead of `const`.
**Change**:
[diff_block_start]
- Avoid using `var`
+ STRICTLY FORBIDDEN: usage of `var`. Use `const` by default.
[diff_block_end]
```

## When to Reflect
- **Post-Session**: After completing a complex task.
- **On Error**: When a tool fails > 2 times.
- **On User Correction**: When the user says "No, do X instead."

---
*Load this context with `@context reflection`*
