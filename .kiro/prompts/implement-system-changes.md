---
description: Implement process improvements defined in System Review
argument-hint: [system-review-file]
---

# Implement System Changes

## Objective
Apply the process improvements identified in the `@system-review`. This ensures the agent system evolves and strictly follows the PIV Loop. This is the **Project Manager's** responsibility.

## Process

### 1. Read the Review
Read the System Review file provided in the arguments: `$ARGUMENTS`.
Extract the "System Improvement Actions".

### 2. Implement Changes
For each recommended action:
- **Update Steering Documents**: Edit `.kiro/guides/` or `.kiro/steering/` to add new patterns or warnings.
- **Update Prompts**: Edit `.kiro/prompts/` to clarify instructions or add validation.
- **Update Rules**: If a rule was ignored, make it more prominent in `CLAUDE.md` or the relevant context.

### 3. Verify
Ensure the changes are saved and syntactically correct (no broken markdown).

## Next Step Instruction
> [!IMPORTANT]
> **System improved?**
> The cycle is complete. You must now commit existing changes and log the progress.
>
> Run the following command:
> ```bash
> @commit "System improvements from $ARGUMENTS"
> ```
