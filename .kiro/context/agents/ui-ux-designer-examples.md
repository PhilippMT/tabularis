# UI/UX Designer - Design Examples

> **Load Trigger**: Design systems, user research, accessibility

## User Persona Template

```markdown
## Persona: [Name]

### Demographics
- **Age**: [Range]
- **Occupation**: [Role]
- **Tech Savvy**: [Low/Medium/High]

### Goals
- [Primary goal]
- [Secondary goal]

### Pain Points
- [Frustration 1]
- [Frustration 2]

### Behaviors
- [How they typically interact]
- [Preferred devices/platforms]

### Quote
> "[Memorable quote that captures their perspective]"
```

## User Journey Map Template

```markdown
## Journey: [Task Name]

### Stages
| Stage | User Actions | Thoughts | Emotions | Opportunities |
|-------|--------------|----------|----------|---------------|
| Awareness | [Actions] | [Thoughts] | 😊/😐/😟 | [Improvements] |
| Consideration | [Actions] | [Thoughts] | 😊/😐/😟 | [Improvements] |
| Decision | [Actions] | [Thoughts] | 😊/😐/😟 | [Improvements] |
| Retention | [Actions] | [Thoughts] | 😊/😐/😟 | [Improvements] |

### Key Moments
- **Peak**: [Best experience point]
- **Pain Point**: [Worst experience point]

### Recommendations
1. [Improvement 1]
2. [Improvement 2]
```

## Design System Color Tokens

```css
:root {
  /* Primary colors */
  --color-primary-50: #eff6ff;
  --color-primary-100: #dbeafe;
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;
  --color-primary-700: #1d4ed8;

  /* Semantic colors */
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;

  /* Neutral colors */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-500: #6b7280;
  --color-gray-900: #111827;

  /* Typography scale */
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;

  /* Spacing scale */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-4: 1rem;
  --spacing-6: 1.5rem;
  --spacing-8: 2rem;
}
```

## Accessibility Checklist

```markdown
## WCAG 2.1 AA Compliance Checklist

### Perceivable
- [ ] Color contrast ratio ≥ 4.5:1 for normal text
- [ ] Color contrast ratio ≥ 3:1 for large text
- [ ] Images have alt text
- [ ] Videos have captions
- [ ] Content readable at 200% zoom

### Operable
- [ ] All interactive elements keyboard accessible
- [ ] Focus indicator visible
- [ ] No keyboard traps
- [ ] Skip navigation link provided
- [ ] Touch targets ≥ 44x44 pixels

### Understandable
- [ ] Language declared in HTML
- [ ] Labels associated with form inputs
- [ ] Error messages descriptive
- [ ] Consistent navigation

### Robust
- [ ] Valid HTML
- [ ] ARIA used correctly
- [ ] Works with screen readers
```

## Component Specification Template

```markdown
## Component: [Name]

### Purpose
[What this component is for]

### Anatomy
- [Element 1]: [Description]
- [Element 2]: [Description]

### States
| State | Appearance | Behavior |
|-------|------------|----------|
| Default | [Styles] | [Interactions] |
| Hover | [Styles] | [Interactions] |
| Focus | [Styles] | [Interactions] |
| Active | [Styles] | [Interactions] |
| Disabled | [Styles] | [Interactions] |
| Error | [Styles] | [Interactions] |

### Accessibility
- Role: `[ARIA role]`
- Required attributes: `[aria-*]`
- Keyboard: [Tab, Enter, Escape behaviors]

### Responsive Behavior
- Mobile: [Behavior]
- Tablet: [Behavior]
- Desktop: [Behavior]
```

## Usability Test Script

```markdown
## Usability Test: [Feature Name]

### Introduction (2 min)
"Thank you for participating. We're testing [feature], not you.
Please think aloud as you work through the tasks."

### Tasks

**Task 1: [Name]** (Est. 3 min)
"Imagine you want to [scenario]. Please show me how you would do that."

Success criteria:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Task 2: [Name]** (Est. 3 min)
"Now, please [scenario]."

### Post-Task Questions
1. On a scale of 1-5, how easy was that task?
2. What was confusing, if anything?
3. What would you improve?

### Wrap-Up
"Any other feedback about the overall experience?"
```
