# Development Logger - Templates

> **Load Trigger**: Session logging, development metrics, process documentation

## DEVLOG Entry Template

```markdown
## DEVLOG Entry - [Date] [Time]

### Session Metadata
- **Duration**: [X hours Y minutes]
- **Agents Involved**: [List of agents]
- **Feature/Task**: [What was worked on]

### Complexity Assessment
**Rating**: [1-5] / 5
- 1 = Simple, straightforward task
- 3 = Moderate complexity, some challenges
- 5 = Highly complex, significant obstacles

### What Went Well
- [Success 1]
- [Success 2]

### Challenges Encountered
| Challenge | Impact | Resolution | Time Lost |
|-----------|--------|------------|-----------|
| [Issue] | [High/Med/Low] | [How resolved] | [Minutes] |

### Technical Decisions Made
| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| [Choice] | [Why] | [Other options] |

### Performance Metrics
- Build time: [X seconds]
- Test pass rate: [X%]
- Test coverage: [X%]
- Lint warnings: [X]

### Lessons Learned
1. [Insight 1]
2. [Insight 2]

### Recommendations for Future
- [Recommendation 1]
- [Recommendation 2]

### Satisfaction Rating
**Overall**: [1-5] / 5
```

## Weekly Insights Report Template

```markdown
## Weekly Development Insights
**Week of**: [Start Date] - [End Date]

### Executive Summary
[2-3 sentence overview of the week]

### Velocity Metrics
| Metric | This Week | Last Week | Trend |
|--------|-----------|-----------|-------|
| Tasks Completed | X | Y | ↑/↓/→ |
| Story Points | X | Y | ↑/↓/→ |
| Average Task Time | Xhr | Yhr | ↑/↓/→ |

### Quality Indicators
- **Test Coverage**: X% (target: 80%)
- **Bug Rate**: X bugs/feature
- **Build Success Rate**: X%
- **Code Review Turnaround**: Xhr average

### Top Challenges This Week
1. **[Challenge 1]**
   - Frequency: X occurrences
   - Total time impact: X hours
   - Recommended action: [Action]

2. **[Challenge 2]**
   - Frequency: X occurrences
   - Total time impact: X hours
   - Recommended action: [Action]

### Agent Collaboration Effectiveness
| Handoff | Count | Avg. Context Clarity |
|---------|-------|---------------------|
| PM → Backend | X | [1-5]/5 |
| Backend → Frontend | X | [1-5]/5 |
| Frontend → Test | X | [1-5]/5 |

### Patterns Identified
- **Successful Pattern**: [What worked well and should be repeated]
- **Anti-Pattern**: [What should be avoided]

### Recommendations for Next Week
1. [Priority recommendation]
2. [Secondary recommendation]
3. [Process improvement suggestion]
```

## Problem Resolution Log

```markdown
## Problem Resolution Log

### Problem ID: [PRB-XXX]
**Date Identified**: [Date]
**Date Resolved**: [Date]
**Resolution Time**: [Duration]

### Problem Description
[Clear description of the issue]

### Root Cause Analysis
**Category**: [Bug/Configuration/Design/External]
**Root Cause**: [What actually caused the problem]
**Contributing Factors**:
- [Factor 1]
- [Factor 2]

### Timeline
| Time | Event | Action Taken |
|------|-------|--------------|
| T+0 | Problem identified | [Initial response] |
| T+X | [Milestone] | [Action] |
| T+Y | Resolution | [Final fix] |

### Solution Applied
[Detailed description of the fix]

### Prevention Measures
- [ ] [Preventive action 1]
- [ ] [Preventive action 2]

### Knowledge Base Entry
**Tags**: [tag1, tag2, tag3]
**Searchable Summary**: [One-line description for future reference]
```

## Monthly Performance Review

```markdown
## Monthly Development Performance Review
**Month**: [Month Year]

### Overview
[Executive summary of the month's development activity]

### Key Metrics Summary
| Metric | Actual | Target | Status |
|--------|--------|--------|--------|
| Features Delivered | X | Y | ✅/⚠️/❌ |
| Test Coverage | X% | 80% | ✅/⚠️/❌ |
| Bug Rate | X | <Y | ✅/⚠️/❌ |
| Deployment Frequency | X/week | Y/week | ✅/⚠️/❌ |

### Trend Analysis
[Chart or description of trends over the month]

### Top Accomplishments
1. [Major achievement 1]
2. [Major achievement 2]
3. [Major achievement 3]

### Areas for Improvement
1. [Improvement area 1] - [Proposed action]
2. [Improvement area 2] - [Proposed action]

### Team Dynamics
- Agent collaboration score: [1-5]/5
- Knowledge sharing effectiveness: [1-5]/5
- Process adherence: [1-5]/5

### Strategic Recommendations
1. **Short-term (Next Month)**: [Recommendation]
2. **Medium-term (Next Quarter)**: [Recommendation]
3. **Long-term (6+ Months)**: [Recommendation]
```

## Session Metrics Collection Script

```typescript
interface SessionMetrics {
  sessionId: string;
  startTime: Date;
  endTime: Date;
  duration: number; // minutes
  agentsInvolved: string[];
  tasksCompleted: number;
  buildTimes: number[];
  testResults: {
    passed: number;
    failed: number;
    skipped: number;
  };
  filesChanged: number;
  linesAdded: number;
  linesRemoved: number;
}

function calculateSessionMetrics(session: SessionMetrics) {
  return {
    ...session,
    averageBuildTime: session.buildTimes.reduce((a, b) => a + b, 0) / session.buildTimes.length,
    testPassRate: session.testResults.passed / (session.testResults.passed + session.testResults.failed),
    codeChurn: session.linesAdded + session.linesRemoved,
    velocity: session.tasksCompleted / (session.duration / 60), // tasks per hour
  };
}
```
