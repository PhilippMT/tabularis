# Core Workflows

## 🎯 **The 4 Fundamental Development Patterns**

These are the essential workflows that form the foundation of systematic development with our agent team. Master these patterns and you'll handle 90% of development scenarios effectively.

## 🚀 **Workflow 1: New Project Setup**

### **When to Use**
- Starting a new project or major feature area
- Onboarding new team members
- Establishing development baseline

### **Step-by-Step Process**

#### **Phase 1: Context Establishment**
```bash
@prime
```
**What Happens:**
- Project Manager analyzes codebase structure
- Identifies existing patterns and architecture
- Establishes shared context for all agents
- Documents current state and capabilities

**Expected Output:**
```
🎯 Project Context Loaded
- Technology Stack: Node.js/React/PostgreSQL
- Architecture: RESTful API + SPA frontend
- Current Features: [list of existing functionality]
- Development Patterns: [identified patterns]
- Next Steps: Ready for feature planning
```

#### **Phase 2: Project Structure**
```bash
# Project Manager creates project in Archon
"Create new project [ProjectName] with initial structure"
```
**What Happens:**
- Project created in Archon knowledge base
- Initial task framework established
- Agent coordination protocols set up
- Documentation templates prepared

#### **Phase 3: First Feature Planning**
```bash
@plan-feature "Core Application Setup"
```
**What Happens:**
- Comprehensive feature breakdown
- Task assignment to appropriate agents
- Timeline and dependency mapping
- Quality standards establishment

### **Success Criteria**
- ✅ All agents have shared project understanding
- ✅ Project structure exists in Archon
- ✅ First feature plan is comprehensive and actionable
- ✅ Team coordination protocols are established

---

## 🔧 **Workflow 2: Feature Development Cycle (PIV Loop)**

### **When to Use**
- Implementing any new feature or enhancement
- Making significant changes to existing functionality
- Adding new capabilities to the application

### **Step-by-Step Process**

#### **Phase 1: Planning Focus**

1. **Vibe & Brainstorm** (`@plan-vibe`)
   - **Agent**: Project Manager (Lead) + Team
   - **Action**: Collaborative open-ended discussion to discover goals, "vibe", and technical direction.
   - **Outcome**: A shared vision and clear intent.

2. **Define Requirements** (`@create-prd`)
   - **Agent**: Project Manager
   - **Action**: Formalize the vision into a Product Requirements Document (PRD).
   - **Outcome**: `PRD.md` with explicit scope and user stories.

3. **Plan Implementation** (`@plan-feature`)
   - **Agent**: Project Manager
   - **Action**: Create a detailed technical implementation plan based on the PRD.
   - **Outcome**: `.kiro/features/[feature].md` with step-by-step tasks.

4. **User Review (GATE)**
   - **Agent**: User (Reviewer)
   - **Action**: User reviews the plan. **STOP** here until approved.
   - **Outcome**: Approval to proceed.

#### **Phase 2: Execution Focus**

5. **Execute Plan** (`@execute`)
   - **Agent**: Specialist Agent (e.g., Backend Engineer, Frontend Architect)
   - **Action**: Implement the code following the confirmed plan.
   - **Outcome**: Implemented feature.

#### **Phase 3: Verification & Improvement Focus**

6. **Code Review** (`@code-review`)
   - **Agent**: Test Orchestrator
   - **Action**: Objective review of code quality, security, and standards.
   - **Outcome**: Pass/Fail + Issues list.

7. **Fix Issues** (`@implement-fix`)
   - **Agent**: Specialist Agent (Active Agent)
   - **Action**: Resolve issues found in code review.
   - **Outcome**: Clean code ready for re-review.

8. **Execution Report** (`@execution-report`)
   - **Agent**: Specialist Agent (Active Agent)
   - **Action**: Reflect on the implementation process, challenges, and divergences.
   - **Outcome**: `execution-report.md`.

9. **System Review** (`@system-review`)
   - **Agent**: Development Logger
   - **Action**: Analyze the process (Plan vs Execution) to find systemic improvements.
   - **Outcome**: `system-review.md` with "System Improvement Actions".

10. **Implement System Changes** (`@implement-system-changes`)
    - **Agent**: Project Manager
    - **Action**: Apply the improvements to `.kiro/` docs, prompts, or rules.
    - **Outcome**: Evolved agent system.

11. **Commit & Log** (`@commit`)
    - **Agent**: Development Logger (Log) / Project Manager (Commit)
    - **Action**: Commit changes and update the DevLog.
    - **Outcome**: Secured progress.

### **Success Criteria**
- ✅ Feature implemented according to plan
- ✅ All quality gates passed
- ✅ System improved based on learning
- ✅ Process fully documented

---

## 🐛 **Workflow 3: Bug Investigation and Resolution**

### **When to Use**
- Critical production issues
- Security vulnerabilities
- Performance problems
- Any systematic problem requiring analysis

### **Step-by-Step Process**

#### **Phase 1: Root Cause Analysis**
```bash
@rca [github-issue-id]
```
**What Happens:**
- Security Specialist (or appropriate agent) investigates issue
- Systematic analysis of problem scope and impact
- Identification of root cause and contributing factors
- Documentation of findings and proposed solution

**Expected Output:**
```
🚨 RCA: SQL Injection Vulnerability #247
- Root Cause: Unsanitized input in user search
- Impact: Potential full database access
- Affected Systems: User search API, admin functions
- Proposed Fix: Parameterized queries + input validation
- Timeline: 6 hours for complete resolution
```

#### **Phase 2: Systematic Fix Implementation**
```bash
@implement-fix [github-issue-id]
```
**What Happens:**
- Appropriate specialist implements fix based on RCA
- Follows systematic implementation approach
- Includes comprehensive testing and validation
- Documents fix details and verification steps

**Expected Output:**
```
🔧 Fix Implemented: Issue #247
- Changes: Parameterized queries, input validation
- Testing: All security tests passing
- Performance: 15% improvement in query time
- Validation: Zero vulnerabilities detected
- Status: READY FOR DEPLOYMENT
```

#### **Phase 3: Quality Validation**
```bash
@code-review
```
**What Happens:**
- Test Orchestrator validates fix quality
- Ensures no new issues introduced
- Confirms original problem resolved
- Approves for deployment

#### **Phase 4: Process Learning**
```bash
@system-review [rca-document] [fix-implementation]
```
**What Happens:**
- Development Logger analyzes incident response
- Identifies prevention measures
- Updates processes to avoid similar issues
- Documents lessons learned

### **Success Criteria**
- ✅ Root cause identified and documented
- ✅ Fix implemented and validated
- ✅ No new issues introduced
- ✅ Prevention measures established

---

## 🏆 **Workflow 4: Project Evaluation and Quality Assessment**

### **When to Use**
- Before major releases or deployments
- Hackathon submissions or project evaluations
- Comprehensive quality audits
- Milestone assessments

### **Step-by-Step Process**

#### **Phase 1: Comprehensive Evaluation**
```bash
@code-review-hackathon
```
**What Happens:**
- Test Orchestrator evaluates against multiple criteria
- Application quality, documentation, innovation assessment
- Scoring against established standards
- Detailed feedback and improvement recommendations

**Expected Output:**
```
🏆 Project Evaluation: 87/100 Points
- Application Quality: 35/40 (Excellent functionality)
- Documentation: 17/20 (Comprehensive guides)
- Innovation: 12/15 (Creative workflow integration)
- Kiro CLI Usage: 18/20 (Exceptional agent coordination)
- Presentation: 5/5 (Clear demonstration)
- Status: READY FOR SUBMISSION
```

#### **Phase 2: Requirements Documentation**
```bash
@create-prd "Complete Project Specification"
```
**What Happens:**
- Project Manager creates comprehensive documentation
- Feature specifications and acceptance criteria
- Technical architecture and implementation details
- Success metrics and evaluation criteria

#### **Phase 3: Process Effectiveness Analysis**
```bash
@system-review [project-plan] [evaluation-results]
```
**What Happens:**
- Development Logger analyzes overall development process
- Identifies successful patterns and improvement opportunities
- Documents best practices for future projects
- Creates recommendations for process optimization

### **Success Criteria**
- ✅ Comprehensive project evaluation completed
- ✅ Complete documentation generated
- ✅ Process insights captured and documented
- ✅ Improvement recommendations established

---

## 🔄 **Workflow Integration Patterns**

### **Sequential Pattern**
```
Project Manager → Specialist Agent → Test Orchestrator → Development Logger
```
**Best For:** Complex features requiring careful coordination

### **Parallel Pattern**
```
Project Manager → Multiple Agents (simultaneous) → Test Orchestrator
```
**Best For:** Independent components that can be developed simultaneously

### **Iterative Pattern**
```
Plan → Implement → Review → Fix → Improve → Repeat
```
**Best For:** Experimental features or complex problem-solving

### **Emergency Pattern**
```
RCA → Fix → Review → Deploy → Learn
```
**Best For:** Critical issues requiring rapid but systematic response

## 🎯 **Quality Gates Integration**

### **Mandatory Gates for All Workflows**

1. **Planning Gate**: No implementation without `@prime` + `@plan-feature`
2. **Implementation Gate**: All agents must use `@execute` framework
3. **Quality Gate**: No deployment without `@code-review` approval
4. **Documentation Gate**: Major features require `@execution-report`
5. **Improvement Gate**: Regular `@system-review` for optimization

### **Gate Enforcement**
- **Automated**: Hooks trigger appropriate prompts at workflow stages
- **Manual**: Team discipline in following established patterns
- **Validation**: Regular process reviews ensure gate compliance

## 🚀 **Advanced Workflow Combinations**

### **Full Development Cycle**
```bash
# Setup and Planning
@prime
@plan-feature "Complete Feature"

# Implementation Phase
@execute (by assigned agents)

# Quality Assurance
@code-review
@execution-report

# Process Improvement
@system-review [plan] [report]

# Project Evaluation
@code-review-hackathon
@create-prd "Final Documentation"
```

### **Emergency Response with Learning**
```bash
# Crisis Response
@rca [issue-id]
@implement-fix [issue-id]
@code-review

# Process Improvement
@system-review [rca] [fix-report]
# Update procedures based on learnings
```

## 📊 **Workflow Success Metrics**

### **Velocity Metrics**
- Time from feature request to deployment
- Number of workflow cycles completed per sprint
- Reduction in rework and bug fixes

### **Quality Metrics**
- Percentage of workflows passing quality gates on first attempt
- Test coverage and security compliance rates
- Production incident reduction

### **Process Metrics**
- Agent coordination efficiency
- Knowledge retention and reuse
- Process improvement implementation rate

## 🎓 **Mastery Checklist**

### **Beginner Level**
- [ ] Can execute all 4 core workflows
- [ ] Understands when to use each pattern
- [ ] Follows quality gates consistently

### **Intermediate Level**
- [ ] Can combine workflows effectively
- [ ] Adapts patterns to specific project needs
- [ ] Contributes to process improvements

### **Advanced Level**
- [ ] Creates custom workflow variations
- [ ] Mentors others in workflow adoption
- [ ] Drives systematic process optimization

---

**Ready for more advanced patterns? Check out [Agent Coordination](agent-coordination.md) for multi-agent collaboration techniques!**