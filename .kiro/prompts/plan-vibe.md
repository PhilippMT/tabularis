---
description: Collaborative brainstorming session to explore ideas before PRD creation
argument-hint: [optional-topic-summary]
---

# Plan (Vibe): Collaborative Brainstorming

## Objective
Establish a shared understanding and creative direction for the project or feature through an open-ended "vibing" session. This is the **Project Manager's** responsibility, in consultation with the team.

## Process

### 1. Explore & Ideate
Engage the user in a free-form discussion.
- **Ask Clarifying Questions:** Don't just accept the initial prompt. Dig deeper.
- **Suggest Angles:** Propose technical or design approaches that might fit the "vibe".
- **Identify Goals:** What is the core "feeling" or "objective"?
- **Consult Team:** If technical questions arise, tag specific agents (e.g., `@Frontend Architect` for UI vibes, `@Backend Engineer` for capabilities).

### 2. Capture the Vision
Synthesize the discussion into a clear set of goals or a unified "vibe" summary.

### 3. Transition to PRD
Once the direction is clear and the user is satisfied with the "vibe", you must formalize it.

## Output
A clear summary of the agreed-upon direction.

## Next Step Instruction
> [!IMPORTANT]
> **Vibe established?**
> Now that you have a shared vision, you MUST formalize it.
>
> Run the following command:
> ```bash
> @create-prd "Context from Vibe Session"
> ```
