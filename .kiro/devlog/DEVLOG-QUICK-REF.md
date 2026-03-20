# Development Log Quick Reference

## One-Page Guide to Devlog Integration

### Daily Routine

#### Start of Day
```bash
@prime                    # Load project context
```

#### During Development (Per Feature)
```bash
@plan-feature "Name"      # Plan the feature
@execute                  # Implement systematically
@code-review              # Validate quality
./feature-completion-hook # Record completion
```

#### End of Day
```bash
./devlog-update          # Create daily entry
# Answer 8 questions, automatic metrics gathered
```

#### Weekly (Optional)
```bash
@system-review           # Analyze process improvements
```

---

## Quick Command Reference

### Windows
```bash
# Daily update (from .kiro/devlog directory)
devlog-update.bat

# Feature completion
feature-completion-hook.bat "Feature Name"
```

### Unix/Mac/Linux
```bash
# Daily update (from .kiro/devlog directory)
./devlog-update.sh

# Feature completion
./feature-completion-hook.sh "Feature Name"
```

---

## The 8 Questions (Daily Update)

1. **What did you work on?** - High-level focus
2. **How much time?** - Total hours
3. **Main accomplishments?** - Key achievements
4. **Challenges or blockers?** - Problems and solutions
5. **Key decisions?** - Technical choices
6. **Next session plan?** - Priorities
7. **Learnings or insights?** - Skills/patterns gained
8. **Kiro prompts used?** - Tool effectiveness

---

## What Gets Captured

### Automatic (From Git)
- ✅ Commits made
- ✅ Files modified
- ✅ Lines added/removed
- ✅ Code statistics

### Manual (From Your Answers)
- ✅ Time invested
- ✅ Accomplishments
- ✅ Challenges overcome
- ✅ Technical decisions
- ✅ Learnings and insights
- ✅ Next priorities

### Metrics Updated
- ✅ Total dev days
- ✅ Total hours logged
- ✅ Total commits
- ✅ Total lines added/removed
- ✅ Files modified count

---

## File Locations

```
.kiro/devlog/
├── DEVLOG.md                    # Your development log (auto-updated)
├── devlog-update.sh             # End-of-day script
├── devlog-update.bat            # Windows version
├── feature-completion-hook.sh   # Feature milestone script
├── feature-completion-hook.bat  # Windows version
├── DEVLOG-INTEGRATION.md        # Complete integration guide
├── COMPLETE-WORKFLOW.md         # Full workflow documentation
└── DEVLOG-QUICK-REF.md         # This file
```

---

## Integration Points

### With Your Git Workflow
```
Code → Commit → Code Review → feature-completion-hook → Deploy
```

### With Kiro Prompts
```
@prime → @plan-feature → @execute → @code-review → devlog-update
```

### Weekly Process
```
Mon-Fri: Daily updates → Fri: @system-review → Analysis → Next week improvements
```

---

## Time Investment

| Activity | Time | When |
|----------|------|------|
| Daily update | 5-10 min | End of day |
| Feature completion | < 1 min | Per feature |
| Weekly review | 15-20 min | Friday |
| Monthly analysis | 30-45 min | End of month |

---

## Common Scenarios

### Multiple Features in One Day
```bash
# Feature 1
@plan-feature "Auth"
@execute
@code-review
./feature-completion-hook.bat "Auth"

# Feature 2
@plan-feature "Notifications"
@execute
@code-review
./feature-completion-hook.bat "Notifications"

# End of day - single devlog entry captures both
./devlog-update.bat
```

### Working on One Complex Feature
```bash
# Day 1
@plan-feature "Payment System"
@execute (morning)
git commit -m "Payment API foundation"

# Day 2
@execute (continue)
git commit -m "Payment processing logic"

# Day 3
@execute (finish)
@code-review
./feature-completion-hook.bat "Payment System"

# End of day
./devlog-update.bat
```

### Bug Fix Day
```bash
# Multiple quick fixes throughout day
@execute (fix bug 1)
git commit -m "Fix: User profile loading"

@execute (fix bug 2)
git commit -m "Fix: Email validation"

# End of day - capture all fixes
./devlog-update.bat
# Answer: "Fixed 5 bugs related to user management"
```

---

## Success Indicators

### After 1 Week
- [ ] Daily update habit established
- [ ] DEVLOG.md has 5 daily entries
- [ ] Clear daily pattern visible

### After 1 Month
- [ ] DEVLOG.md has ~20 entries
- [ ] Metrics show productivity trends
- [ ] Can identify your patterns

### After 3 Months
- [ ] Complete historical record
- [ ] Clear growth patterns visible
- [ ] Process improvements implemented
- [ ] Can forecast delivery timelines

---

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Script won't run | Make executable: `chmod +x *.sh` |
| Git stats missing | Ensure in git repo root |
| DEVLOG.md locked | Wait/close other editors |
| Batch file fails | Use: `cmd /c devlog-update.bat` |
| Questions unclear | Skip with Enter, add in notes |

---

## Pro Tips

1. **Be Honest**: Actual time and real challenges help identify patterns
2. **Be Specific**: Use actual feature names and decision rationale
3. **Be Consistent**: Same time each day builds habit
4. **Review Weekly**: Spot trends you can't see in individual days
5. **Act on Insights**: Use @system-review findings to improve

---

## Next Prompt Commands

After establishing devlog:

```bash
@system-review              # Analyze your devlog patterns
@code-review-hackathon      # Comprehensive project assessment
@execution-report           # Detailed feature documentation
@prime                      # Project context with history
```

---

## Example Daily Entry

```
## Day 6 (January 10, 2026) - Auth & Notifications [8h]

### 📊 **Daily Metrics**
- Time: 8h | Commits: 23 | Files: 28 | +2,450/-175 lines

### 🎯 **Accomplishments**
- User auth system with JWT tokens
- Email notifications with queue
- 95% test coverage

### 💻 **Technical Progress**
- 23 commits across 28 files
- 2,450 lines added, 175 removed

### 🚧 **Challenges**
Auth performance issue (N+1 queries) - solved with caching

### 🧠 **Decisions**
- JWT for stateless auth
- Redis for token blacklist

### 📚 **Learnings**
Token expiration patterns, email queue optimization

### ⚡ **Kiro Usage**
@plan-feature excellent for breakdown,
@code-review caught security issue

### 📋 **Next**
- Payment system
- Webhook integration
```

---

## Resources

- **Full Integration Guide**: `DEVLOG-INTEGRATION.md`
- **Complete Workflow**: `COMPLETE-WORKFLOW.md`
- **Main README**: `../.kiro/README.md`
- **Your Development Log**: `DEVLOG.md`

---

**Quick Start**: Run `devlog-update` today at 5:30 PM. Spend 5 minutes answering questions. Done!

**Remember**: The devlog works best with consistent, honest entries. Quality over quantity!
