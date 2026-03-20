# Development Process Integration Guide

## Overview

Your development process now includes automated devlog updates at two key points:

1. **Feature Completion** - When code is reviewed and committed
2. **End of Day** - Daily summary of all work completed

This guide shows you how to integrate these into your existing workflow.

---

## Quick Start (5 Minutes)

### End of Day Update
```bash
# At the end of your programming day:
cd .kiro/devlog
./devlog-update.sh          # Unix/Mac/Linux
# OR
devlog-update.bat           # Windows
```

### Feature Completion
```bash
# When you finish a feature and are ready to commit:
cd .kiro/devlog
./feature-completion-hook.sh "Feature Name" "branch-name"
# OR
feature-completion-hook.bat "Feature Name"
```

---

## Integration into Your Development Workflow

### Your Complete Workflow

```
1. PLAN FEATURE
   └─ @plan-feature "Feature Name"
   └─ Creates systematic implementation plan

2. DEVELOP & COMMIT
   └─ Write code following the plan
   └─ Commit regularly with meaningful messages
   └─ Use @execute framework for systematic implementation

3. CODE REVIEW
   └─ @code-review to validate quality
   └─ Ensure tests are comprehensive
   └─ Fix any issues identified

4. FEATURE COMPLETION [NEW]
   └─ ./feature-completion-hook.sh "Feature Name"
   └─ Automatically captures feature metrics
   └─ Records statistics in devlog

5. CONTINUE DEVELOPMENT
   └─ Move to next feature or task
   └─ Repeat steps 1-4

6. END OF DAY [NEW]
   └─ ./devlog-update.sh
   └─ Interactive prompts capture day's work
   └─ Summarizes all activities and learnings
   └─ Updates development statistics
   └─ Creates comprehensive daily entry

7. SYSTEM REVIEW (Optional)
   └─ @system-review periodically
   └─ Analyze devlog for process improvements
   └─ Optimize workflows based on metrics
```

---

## When to Use Each Tool

### Use `devlog-update.sh` / `devlog-update.bat`:
- **At the end of each programming day** - captures complete daily summary
- **Before switching major projects** - consolidates work completed
- **When you want to reflect** - asks structured questions about the day
- **For metrics tracking** - automatically gathers git statistics

**Run Time**: 5-10 minutes (mostly for answering questions)

### Use `feature-completion-hook.sh` / `feature-completion-hook.bat`:
- **When you finish implementing a feature** - captures feature metrics
- **After code review passes** - before merging to main
- **Multiple times per day** - you can complete multiple features
- **As a quick milestone marker** - minimal time impact

**Run Time**: < 1 minute per feature

---

## The Questions Asked (End of Day)

When you run the daily update, you'll be asked:

1. **What did you work on today?** - High-level summary of focus
2. **How much time did you spend?** - Total hours worked
3. **What were your main accomplishments?** - Key achievements
4. **Any challenges or blockers?** - Problems encountered and solutions
5. **Key technical decisions made?** - Architecture or design choices
6. **What's planned for next session?** - Next priorities
7. **Any new learnings or insights?** - Skills gained or patterns discovered
8. **Which Kiro prompts were most helpful?** - Tool/workflow effectiveness

---

## Example Daily Workflow

### 9:00 AM - Start of Day
```bash
# Load project context
@prime
```

### 9:15 AM - First Feature
```bash
# Plan first feature
@plan-feature "User Authentication"

# Implement following the plan
@execute

# Review code quality
@code-review

# Feature complete - record milestone
cd .kiro/devlog
./feature-completion-hook.sh "User Authentication"
```

### 12:00 PM - Lunch Break

### 1:00 PM - Second Feature
```bash
# Plan second feature
@plan-feature "Email Notifications"

# Implement
@execute

# Review
@code-review

# Record completion
cd .kiro/devlog
./feature-completion-hook.sh "Email Notifications"
```

### 5:30 PM - End of Day
```bash
# Comprehensive daily update
cd .kiro/devlog
./devlog-update.sh

# Answer the 8 questions:
# 1. User authentication, email notifications
# 2. 8
# 3. Completed two major features
# 4. Had to refactor auth module for performance
# 5. Chose JWT for stateless auth
# 6. Complete payment system
# 7. Learned about token expiration patterns
# 8. @plan-feature and @code-review were very helpful
```

### 6:00 PM - Optional System Review
```bash
# Periodically analyze process improvements
@system-review

# Review devlog trends
# Identify optimization opportunities
# Plan process improvements
```

---

## Integration with Git Workflow

### Option 1: Manual Integration

At each milestone in your git workflow:
```bash
# After feature branch is created
git checkout -b feature/user-auth

# After implementation complete, before PR
cd .kiro/devlog
./feature-completion-hook.sh "User Authentication"

# After code review passes, before merge
git commit -m "Implement user authentication"
git push origin feature/user-auth

# Create PR and merge to main
# At end of day, run full daily update
./devlog-update.sh
```

### Option 2: Automated Integration (Advanced)

Create a git hook to automatically capture feature metrics:

**File**: `.git/hooks/post-commit`
```bash
#!/bin/bash
# Auto-capture feature metrics on commit
BRANCH=$(git branch --show-current)
if [[ $BRANCH == feature/* ]]; then
    FEATURE_NAME=$(echo $BRANCH | sed 's/feature\///')
    ./.kiro/devlog/feature-completion-hook.sh "$FEATURE_NAME" "$BRANCH"
fi
```

Make executable:
```bash
chmod +x .git/hooks/post-commit
```

---

## Metrics Automatically Captured

### Daily Update Captures:
- ✅ Time spent (user-provided)
- ✅ Total commits for the day
- ✅ Lines added/removed
- ✅ Files modified
- ✅ Accomplishments (user-provided)
- ✅ Challenges and solutions (user-provided)
- ✅ Key decisions (user-provided)
- ✅ Learnings (user-provided)
- ✅ Next session priorities (user-provided)

### Feature Completion Captures:
- ✅ Feature name
- ✅ Branch name
- ✅ Commit count for feature
- ✅ Files modified
- ✅ Lines added/removed
- ✅ Completion timestamp

### Overall Statistics (Updated Daily):
- ✅ Total development days
- ✅ Total hours logged
- ✅ Total commits
- ✅ Total lines added/removed
- ✅ Files modified count

---

## File Structure

```
.kiro/devlog/
├── DEVLOG.md                          # Main development log (auto-updated)
├── devlog-update.sh                   # End-of-day update (Unix/Mac/Linux)
├── devlog-update.bat                  # End-of-day update (Windows)
├── feature-completion-hook.sh         # Feature milestone (Unix/Mac/Linux)
├── feature-completion-hook.bat        # Feature milestone (Windows)
├── DEVLOG-INTEGRATION.md              # This file - integration guide
└── .feature-milestones/               # Temporary feature data (auto-created)
    └── 2026-01-10.txt                 # Daily feature list
```

---

## Tips for Best Results

### 1. **Consistency is Key**
- Run daily update at the **same time each day** - builds habit
- Always capture feature completion - even small features
- Review devlog weekly - identify patterns

### 2. **Be Honest and Specific**
- Actual time spent (include debugging, research)
- Real challenges - helps identify patterns
- Specific decisions - useful for future reference
- Honest learnings - tracks skill development

### 3. **Use with Kiro Prompts**
- Before daily update, use @system-review
- Before feature planning, use @prime for context
- After code review, use @execution-report
- Periodically use @code-review-hackathon for assessment

### 4. **Review Regularly**
- Weekly: Review daily entries for patterns
- Monthly: Analyze metrics for trends
- Quarterly: Use @system-review for deep analysis
- Project end: Use @code-review-hackathon for comprehensive assessment

### 5. **Keep Entries Concise**
- Focus on what matters
- Skip optional questions if nothing significant
- Let git metrics speak for changes
- Link to commits if helpful

---

## Troubleshooting

### "command not found: ./devlog-update.sh"
**Solution**: Make script executable
```bash
chmod +x .kiro/devlog/devlog-update.sh
chmod +x .kiro/devlog/feature-completion-hook.sh
```

### "DEVLOG.md is locked"
**Solution**: Another process is reading the file. Wait a moment and retry.

### Git metrics not showing
**Solution**: Ensure you're in the git repository root or subdirectory
```bash
git rev-parse --git-dir  # Should show .git
```

### "No commits today" message
**Solution**: Normal if you haven't committed. The devlog still captures your work time and accomplishments.

### On Windows, batch files don't run
**Solution**: Run with `cmd /c` prefix:
```bash
cmd /c devlog-update.bat
cmd /c feature-completion-hook.bat
```

---

## Advanced Customization

### Custom Devlog Questions

Edit `devlog-update.sh` or `devlog-update.bat` to add your own questions:

```bash
echo "Your custom question?"
read -p "Answer: " CUSTOM_VAR
```

### Integration with Project Management Tools

Add commands to export devlog to:
- JIRA (issue tracking)
- Linear (modern issue tracking)
- Notion (team wiki)
- GitHub Projects (development tracking)

### Automated Reports

Schedule daily report generation:
```bash
# Create cron job (Unix/Mac/Linux)
0 17 * * * cd /path/to/kiro-agent-team/.kiro/devlog && ./devlog-update.sh
```

---

## Success Metrics

After implementing this system, you should see:

- **30 days**: Clear daily patterns in your development habits
- **60 days**: Accurate historical record of all work completed
- **90 days**: Data-driven insights on productivity, challenges, and improvements
- **180 days**: Complete project history for reference and analysis

---

## Next Steps

1. **Today**: Run your first daily update
   ```bash
   cd .kiro/devlog && ./devlog-update.sh
   ```

2. **This Week**: Integrate feature completion into your workflow
   ```bash
   # Complete a feature and run
   ./feature-completion-hook.sh "Feature Name"
   ```

3. **This Month**: Review your devlog and identify patterns
   ```bash
   # Read DEVLOG.md
   # Use @system-review for analysis
   ```

4. **Ongoing**: Use insights to optimize your development process

---

## Questions?

If you encounter issues or have questions:
- Review the main [README.md](./../README.md)
- Check [INTEGRATION_COMPLETE.md](./../INTEGRATION_COMPLETE.md)
- Run `@system-review` prompt for process analysis
- Refer to workflow guides in [./guides/](./../guides/)

---

**Last Updated**: January 10, 2026  
**System**: Kiro CLI Development Process Integration  
**Status**: Ready for production use
