# Project Manager - Workflow Examples

> **Load Trigger**: Project planning, team coordination, task management

## Task Creation Template

```markdown
## Task: [Clear, action-oriented title]

**Objective**: [What needs to be accomplished]

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Context**: [Why this task is important and how it fits]

**Dependencies**: [Tasks that must be completed first]

**Estimated Effort**: [30min - 4hr range]

**Assigned Agent**: [Best-fit agent]
```

## Sprint Planning Template

```markdown
## Sprint [Number] - [Start Date] to [End Date]

### Sprint Goal
[Clear, measurable objective for the sprint]

### Committed Tasks
| Task | Agent | Estimate | Priority |
|------|-------|----------|----------|
| [Task 1] | Frontend Architect | 2hr | High |
| [Task 2] | Backend Engineer | 4hr | High |
| [Task 3] | Test Orchestrator | 2hr | Medium |

### Dependencies
- [Task 1] must complete before [Task 3]

### Risks
- [Risk 1]: Mitigation strategy
- [Risk 2]: Mitigation strategy

### Definition of Done
- [ ] Code reviewed and approved
- [ ] Tests passing (80%+ coverage)
- [ ] Documentation updated
- [ ] Deployed to staging
```

## Daily Standup Format

```markdown
## Daily Standup - [Date]

### Yesterday
- [What was completed]

### Today
- [What will be worked on]

### Blockers
- [Any impediments or dependencies]

### Highlights
- [Any notable achievements or concerns]
```

## Weekly Status Report

```markdown
## Weekly Status Report - Week of [Date]

### Summary
[1-2 sentence overview of the week]

### Completed This Week
- [x] [Task 1] - [Agent]
- [x] [Task 2] - [Agent]

### In Progress
- [ ] [Task 3] - [Agent] - [% complete]

### Blockers & Risks
| Issue | Impact | Mitigation |
|-------|--------|------------|
| [Blocker] | [Impact] | [Action] |

### Next Week Priorities
1. [Priority 1]
2. [Priority 2]

### Velocity
- Planned: [X] points
- Completed: [Y] points
- Velocity: [Y/X]%
```

## Risk Register Template

```markdown
## Risk Register

| ID | Risk | Probability | Impact | Score | Owner | Mitigation |
|----|------|-------------|--------|-------|-------|------------|
| R1 | [Description] | High/Med/Low | High/Med/Low | H/M/L | [Agent] | [Strategy] |
| R2 | [Description] | High/Med/Low | High/Med/Low | H/M/L | [Agent] | [Strategy] |
```

## Agent Handoff Template

```markdown
## Handoff: [From Agent] → [To Agent]

### Context
[What was being worked on and why]

### Completed Work
- [Completed item 1]
- [Completed item 2]

### Current State
[Describe current state of the work]

### Next Steps
1. [Step 1]
2. [Step 2]

### Important Notes
- [Any caveats or considerations]
- [Files modified]
- [Tests to run]
```
