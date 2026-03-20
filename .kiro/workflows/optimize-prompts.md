# Workflow: Optimize System Prompts (GEPA Cycle)

This workflow guides the **Development Logger** in analyzing recent activity to improve the agent team's system prompts.

## 1. Gather Trajectories
- Read recent `DEVLOG` entries.
- (If available) Read raw session logs or recall recent "Error" events.

## 2. Analyze Friction Points
Identify repeated issues:
- Frequent user corrections?
- Tool usage errors?
- Style violations (lint errors)?
- "I don't know how to..." statements?

## 3. Generate "Prompt Patches"
For each identified issue, draft a specific text update for the relevant `md` file.

**Targets**:
- `CLAUDE.md` (Core rules)
- `.kiro/agents/*.md` (Role definitions)
- `.kiro/context/**/*.md` (Context modules)

## 4. Present to User
**CRITICAL**: You cannot modify system prompts without user approval.
Present your findings:

> "I noticed the Backend Agent frequently forgets to add JSDocs.
> I propose updating `CLAUDE.md` to make this a 'Critical Rule'."

## 5. Apply Changes
If (and only if) the User approves:
- Use `replace_file_content` to apply the patch.
- Announce the upgrade: "System prompts upgraded. JSDocs are now mandatory."
