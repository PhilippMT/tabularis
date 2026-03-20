# Kiro-CLI Agent Team Workflow Guide

## Overview

This guide demonstrates how to leverage our 9-agent team with integrated prompt workflows for systematic, quality-driven development. Each agent now has enhanced capabilities through prompt integration, creating a comprehensive development ecosystem.

## Quick Reference: Agent + Prompt Integration

| Agent | Primary Prompts | Use Cases |
|-------|----------------|-----------|
| **Project Manager** | `@prime`, `@plan-feature`, `@create-prd` | Project setup, feature planning, requirements |
| **Test Orchestrator** | `@code-review`, `@execution-report`, `@code-review-hackathon` | Quality assurance, project evaluation |
| **Development Logger** | `@system-review` | Process improvement, workflow analysis |
| **Security Specialist** | `@rca`, `@implement-fix` | Security incident analysis and resolution |
| **All Agents** | `@execute`, `@commit` | Systematic task implementation, committing changes |

## Core Development Workflows

### 🚀 Workflow 1: New Project Setup

**Scenario**: Starting a new fullstack application project

**Steps**:
1. **Initialize Project Context**
   ```
   @prime
   ```
   - Project Manager loads comprehensive project understanding
   - Analyzes codebase structure, documentation, and requirements
   - Establishes baseline context for all agents

2. **Create Project in Archon**
   ```
   Project Manager: Create new project "TaskFlow App" with initial task breakdown
   ```
   - Sets up project structure in Archon knowledge base
   - Creates initial milestone and task framework
   - Establishes agent coordination protocols

3. **Plan First Feature**
   ```
   @plan-feature "User Authentication System"
   ```
   - Project Manager creates comprehensive implementation plan
   - Breaks down feature into granular tasks (30min-4hr each)
   - Assigns tasks to appropriate specialist agents
   - Establishes dependencies and timeline

**Expected Outcome**: Fully planned project with clear task assignments and systematic approach to implementation.

---

### 🔧 Workflow 2: Feature Development Cycle

**Scenario**: Implementing a new feature from planning to deployment

**Steps**:
1. **Feature Planning** (Project Manager)
   ```
   @plan-feature "Task Management Dashboard"
   ```
   - Comprehensive feature analysis and architecture decisions
   - Task breakdown with clear acceptance criteria
   - Agent assignment based on expertise and availability

2. **Systematic Implementation** (Assigned Agents)
   ```
   @execute
   ```
   - Backend Engineer: API endpoints and business logic
   - Frontend Architect: UI components and state management
   - Database Specialist: Schema updates and data layer
   - Each agent follows systematic execution framework

3. **Quality Assurance** (Test Orchestrator)
   ```
   @code-review
   ```
   - Comprehensive code quality assessment
   - Security, performance, and maintainability review
   - Test coverage and quality gate validation

4. **Implementation Reporting** (Test Orchestrator)
   ```
   @execution-report
   ```
   - Detailed analysis of what was implemented vs planned
   - Quality metrics and validation results
   - Recommendations for process improvement

5. **Process Analysis** (Development Logger)
   ```
   @system-review [plan-file] [execution-report]
   ```
   - Meta-analysis of implementation vs plan adherence
   - Identification of process improvements
   - Updates to workflow and agent coordination

**Expected Outcome**: High-quality feature implementation with comprehensive documentation and continuous process improvement.

---

### 🐛 Workflow 3: Bug Investigation and Resolution

**Scenario**: Critical security vulnerability discovered in production

**Steps**:
1. **Root Cause Analysis** (Security Specialist)
   ```
   @rca [github-issue-id]
   ```
   - Systematic investigation of security vulnerability
   - Analysis of affected components and impact scope
   - Documentation of root cause and proposed fix strategy

2. **Fix Implementation** (Security Specialist)
   ```
   @implement-fix [github-issue-id]
   ```
   - Implementation based on RCA document findings
   - Security-focused testing and validation
   - Documentation of fix and prevention measures

3. **Quality Validation** (Test Orchestrator)
   ```
   @code-review
   ```
   - Security-focused code review of implemented fix
   - Regression testing and security validation
   - Deployment readiness assessment

4. **Process Learning** (Development Logger)
   ```
   @system-review [rca-document] [fix-implementation-report]
   ```
   - Analysis of incident response effectiveness
   - Identification of prevention measures
   - Updates to security processes and monitoring

**Expected Outcome**: Systematic security issue resolution with comprehensive documentation and process improvements to prevent recurrence.

---

### 🏆 Workflow 4: Project Evaluation and Quality Assessment

**Scenario**: Comprehensive project evaluation for hackathon submission or major release

**Steps**:
1. **Comprehensive Project Review** (Test Orchestrator)
   ```
   @code-review-hackathon
   ```
   - Evaluation against multiple quality criteria
   - Assessment of application quality, documentation, innovation
   - Scoring and detailed feedback on all aspects

2. **Requirements Documentation** (Project Manager)
   ```
   @create-prd "Complete Application Specification"
   ```
   - Comprehensive product requirements documentation
   - Feature specifications and acceptance criteria
   - Stakeholder alignment and project scope definition

3. **Process Effectiveness Analysis** (Development Logger)
   ```
   @system-review [project-plan] [implementation-history]
   ```
   - Analysis of overall development process effectiveness
   - Identification of successful patterns and improvement areas
   - Recommendations for future project workflows

**Expected Outcome**: Comprehensive project evaluation with detailed feedback, complete documentation, and process insights for future improvements.

---

## Advanced Use Cases

### 🔄 Multi-Agent Collaboration Patterns

#### Pattern 1: Sequential Handoff
```
Project Manager (@plan-feature) → 
Backend Engineer (@execute) → 
Frontend Architect (@execute) → 
Test Orchestrator (@code-review) →
Development Logger (@system-review)
```

#### Pattern 2: Parallel Development
```
Project Manager (@plan-feature) →
├── Backend Engineer (@execute)
├── Frontend Architect (@execute)  
└── Database Specialist (@execute)
→ Test Orchestrator (@code-review)
```

#### Pattern 3: Iterative Improvement
```
Implementation → @code-review → Fix Issues → @execution-report → @system-review → Process Updates
```

### 🎯 Specialized Workflows

#### Security-First Development
1. Security Specialist consultation during planning
2. Security code review at each implementation stage
3. Vulnerability assessment before deployment
4. Incident response procedures with @rca and @implement-fix

#### Performance-Optimized Development
1. Performance requirements in @plan-feature
2. Performance testing integration in @execute
3. Performance validation in @code-review
4. Performance metrics in @execution-report

#### Compliance-Driven Development
1. Compliance requirements in project planning
2. Compliance validation at each development stage
3. Audit trail documentation throughout process
4. Compliance reporting and certification support

## Best Practices

### 🎯 Effective Prompt Usage

**Do:**
- Always start with `@prime` for new projects or major context changes
- Use `@plan-feature` before beginning any significant development work
- Execute `@code-review` before deployment or major releases
- Generate `@execution-report` after completing major implementations
- Run `@system-review` periodically to improve processes

**Don't:**
- Skip the planning phase - always use systematic approach
- Ignore quality gates - maintain high standards throughout
- Forget to document - use reporting prompts consistently
- Work in isolation - leverage agent collaboration patterns

### 📊 Quality Gates Integration

**Mandatory Quality Gates:**
1. **Planning Gate**: `@plan-feature` must be completed before implementation
2. **Implementation Gate**: `@execute` framework must be followed by all agents
3. **Quality Gate**: `@code-review` must pass before deployment
4. **Documentation Gate**: `@execution-report` must be generated for major features
5. **Improvement Gate**: `@system-review` must be conducted for process optimization

### 🔄 Continuous Improvement Cycle

1. **Plan** → Use `@prime` and `@plan-feature` for systematic planning
2. **Execute** → Follow `@execute` framework for consistent implementation
3. **Review** → Apply `@code-review` for quality assurance
4. **Report** → Generate `@execution-report` for documentation
5. **Improve** → Conduct `@system-review` for process enhancement
6. **Repeat** → Apply learnings to next development cycle

## Troubleshooting Common Issues

### Issue: Agent Coordination Problems
**Solution**: Use Project Manager as central coordinator with clear task assignments and handoff protocols

### Issue: Quality Inconsistency
**Solution**: Implement mandatory quality gates with Test Orchestrator `@code-review` before any deployment

### Issue: Process Inefficiency
**Solution**: Regular `@system-review` analysis to identify and address workflow bottlenecks

### Issue: Knowledge Loss
**Solution**: Consistent use of Development Logger and `@execution-report` for comprehensive documentation

## Success Metrics

### Development Velocity
- Time from feature planning to deployment
- Number of features delivered per sprint/milestone
- Reduction in rework and bug fixes

### Quality Metrics
- Code review pass rate
- Test coverage and quality gate compliance
- Production incident reduction
- Security vulnerability prevention

### Process Effectiveness
- Agent collaboration efficiency
- Knowledge retention and reuse
- Process improvement implementation rate
- Team satisfaction and workflow adoption

---

*This workflow guide represents a systematic approach to leveraging our 9-agent team with integrated prompt capabilities for maximum development effectiveness and quality.*