# Quick Start Guide

## 🚀 **Get Up and Running in 15 Minutes**

This guide will get you productive with the agent team system immediately. Follow these steps to start leveraging systematic, quality-driven development.

## ⚡ **5-Minute Setup**

### **Step 1: Understand Your Team**
You have **9 specialist agents** ready to help:
- **Project Manager**: Coordinates everything
- **Backend/Frontend/Database/DevOps/Security/Test/UX/Logger**: Specialists for each domain

### **Step 2: Learn the Core Commands**
```bash
@prime                    # Load project context (always start here)
@plan-feature [name]      # Plan before you build
@execute                  # Implement systematically
@code-review             # Validate quality
```

### **Step 3: First Workflow Test**
Try this right now:
```bash
@prime
# Wait for Project Manager to load context
# Then try planning a simple feature
@plan-feature "Add user profile page"
```

## 🎯 **Your First 3 Workflows**

### **Workflow 1: New Feature Development (10 minutes)**
```bash
# 1. Load context
@prime

# 2. Plan the feature
@plan-feature "User authentication"

# 3. Let assigned agents implement
@execute

# 4. Review quality
@code-review

# 5. Document results
@execution-report
```

**Expected Result**: Complete feature plan with task assignments and quality validation.

### **Workflow 2: Code Quality Check (5 minutes)**
```bash
# Review any code changes
@code-review

# Get comprehensive quality assessment
# - Security analysis
# - Performance review
# - Code quality metrics
# - Deployment readiness
```

**Expected Result**: Detailed quality report with specific recommendations.

### **Workflow 3: Emergency Bug Fix (15 minutes)**
```bash
# 1. Analyze the problem
@rca [github-issue-id]

# 2. Implement systematic fix
@implement-fix [github-issue-id]

# 3. Validate the solution
@code-review
```

**Expected Result**: Systematic problem analysis, fix implementation, and quality validation.

## 🎭 **Agent Quick Reference**

### **When to Use Each Agent**

**🎯 Project Manager** - Use for:
- Starting any new work (`@prime`)
- Planning features (`@plan-feature`)
- Creating requirements (`@create-prd`)

**🔧 Backend Engineer** - Use for:
- API development and business logic
- Database integration
- Server-side functionality

**🎨 Frontend Architect** - Use for:
- User interface development
- State management
- User experience implementation

**🛡️ Security Specialist** - Use for:
- Security vulnerabilities (`@rca`, `@implement-fix`)
- Security reviews and audits
- Compliance requirements

**✅ Test Orchestrator** - Use for:
- Quality assurance (`@code-review`)
- Implementation documentation (`@execution-report`)
- Project evaluation (`@code-review-hackathon`)

## 🔄 **Essential Patterns**

### **Pattern 1: Always Start with Context**
```bash
# ALWAYS do this first for any new work
@prime
```
**Why**: Ensures all agents work from shared understanding.

### **Pattern 2: Plan Before Implementation**
```bash
# Before building anything significant
@plan-feature [feature-name]
```
**Why**: Prevents scope creep and coordination issues.

### **Pattern 3: Quality Gates**
```bash
# Before any deployment
@code-review
```
**Why**: Catches issues before they reach production.

### **Pattern 4: Document and Learn**
```bash
# After major implementations
@execution-report
@system-review [plan] [report]
```
**Why**: Captures insights and improves processes.

## ⚠️ **Common Mistakes to Avoid**

### **❌ Don't Skip Planning**
```bash
# Wrong: Jump straight to implementation
@execute

# Right: Plan first
@prime
@plan-feature [name]
@execute
```

### **❌ Don't Ignore Quality Gates**
```bash
# Wrong: Deploy without review
git push origin main

# Right: Review first
@code-review
# Then deploy after approval
```

### **❌ Don't Work in Isolation**
```bash
# Wrong: Individual agent work
Backend Engineer: Build API alone

# Right: Coordinated approach
Project Manager: @plan-feature
Backend Engineer: @execute
Test Orchestrator: @code-review
```

## 🎯 **Success Indicators**

### **You're Doing It Right When:**
- ✅ Every feature starts with `@prime` and `@plan-feature`
- ✅ All implementations use `@execute` framework
- ✅ Nothing deploys without `@code-review` approval
- ✅ You regularly generate `@execution-report` for learning
- ✅ Agents coordinate smoothly with clear handoffs

### **Red Flags to Watch For:**
- ❌ Skipping planning phase
- ❌ Working without agent coordination
- ❌ Deploying without quality review
- ❌ Not documenting implementations
- ❌ Repeating the same mistakes

## 🚀 **Next Steps**

### **After This Quick Start:**

**Immediate (Today):**
1. Try all 3 workflows above with your current project
2. Read [Core Workflows](core-workflows.md) for comprehensive patterns
3. Bookmark [Troubleshooting](troubleshooting.md) for when you need help

**This Week:**
1. Master [Agent Coordination](agent-coordination.md) patterns
2. Implement [Quality Assurance](quality-assurance.md) processes
3. Set up [Emergency Procedures](emergency-procedures.md) for your team

**Next Week:**
1. Explore [Advanced Patterns](advanced-patterns.md)
2. Try [Project Evaluation](project-evaluation.md) methods
3. Customize workflows for your specific needs

## 🆘 **Need Help?**

### **Quick Solutions:**
- **Command not working?** → [Troubleshooting](troubleshooting.md)
- **Agent coordination issues?** → [Agent Coordination](agent-coordination.md)
- **Quality problems?** → [Quality Assurance](quality-assurance.md)
- **Emergency situation?** → [Emergency Procedures](emergency-procedures.md)

### **Learning Resources:**
- **Comprehensive workflows**: [Core Workflows](core-workflows.md)
- **Real examples**: `IMPLEMENTATION_EXAMPLES.md` in root directory
- **Command reference**: `QUICK_REFERENCE.md` in root directory

## 🎉 **You're Ready!**

With these basics, you can immediately start benefiting from:
- **Systematic development** with predictable outcomes
- **Built-in quality assurance** preventing issues
- **Agent coordination** eliminating conflicts
- **Continuous improvement** through process learning

**Start with `@prime` and begin your systematic development journey!**

---

*Quick Start complete! Ready for [Core Workflows](core-workflows.md)?*