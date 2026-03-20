# Kiro-CLI Agent Team Quick Reference

## Essential Commands

### 🚀 Core Development Flow
```bash
@prime                    # Load project context (Project Manager)
@plan-feature [name]      # Create implementation plan (Project Manager)  
@execute                  # Systematic task execution (All Agents)
@code-review             # Quality assurance review (Test Orchestrator)
@execution-report        # Implementation documentation (Test Orchestrator)
```

### 🔧 Specialized Workflows
```bash
@create-prd [feature]     # Product requirements doc (Project Manager)
@commit                  # Generate commit message and commit changes (All Agents)
@rca [issue-id]          # Root cause analysis (Security Specialist)
@implement-fix [issue-id] # Fix implementation (Security Specialist)
@system-review [plan] [report] # Process improvement (Development Logger)
@code-review-hackathon   # Project evaluation (Test Orchestrator)
```

## Agent Responsibilities

| Agent | Primary Role | Key Prompts | Best For |
|-------|-------------|-------------|----------|
| **Project Manager** | Coordination & Planning | `@prime`, `@plan-feature`, `@create-prd` | Project setup, feature planning, team coordination |
| **Backend Engineer** | Server-side Development | `@execute` | APIs, business logic, database integration |
| **Frontend Architect** | Client-side Development | `@execute` | UI components, state management, user experience |
| **Database Specialist** | Data Layer Management | `@execute` | Schema design, migrations, query optimization |
| **DevOps Engineer** | Infrastructure & Deployment | `@execute` | CI/CD, containerization, cloud deployment |
| **Security Specialist** | Application Security | `@rca`, `@implement-fix` | Vulnerability assessment, security fixes |
| **Test Orchestrator** | Quality Assurance | `@code-review`, `@execution-report`, `@code-review-hackathon` | Testing strategy, quality gates, project evaluation |
| **UI/UX Designer** | User Experience Design | `@execute` | Interface design, usability, accessibility |
| **Development Logger** | Process Documentation | `@system-review` | Workflow analysis, process improvement |

## Common Workflow Patterns

### 🎯 New Feature Development
```
1. @prime (load context)
2. @plan-feature [name] (create plan)
3. @execute (implement by assigned agents)
4. @code-review (quality check)
5. @execution-report (document results)
```

### 🐛 Bug Fix Process
```
1. @rca [issue-id] (analyze problem)
2. @implement-fix [issue-id] (fix implementation)
3. @code-review (validate fix)
4. @system-review (improve process)
```

### 🏆 Project Evaluation
```
1. @code-review-hackathon (comprehensive evaluation)
2. @create-prd [project] (complete documentation)
3. @system-review (process analysis)
```

## Quality Gates Checklist

### ✅ Before Implementation
- [ ] Project context loaded with `@prime`
- [ ] Feature planned with `@plan-feature`
- [ ] Tasks assigned to appropriate agents
- [ ] Dependencies identified and resolved

### ✅ During Implementation
- [ ] All agents following `@execute` framework
- [ ] Regular progress updates and coordination
- [ ] Issues documented and addressed promptly
- [ ] Quality standards maintained throughout

### ✅ Before Deployment
- [ ] Code review completed with `@code-review`
- [ ] All tests passing and coverage adequate
- [ ] Security validation completed
- [ ] Performance benchmarks met
- [ ] Documentation updated and complete

### ✅ After Deployment
- [ ] Implementation report generated with `@execution-report`
- [ ] Process review conducted with `@system-review`
- [ ] Lessons learned documented and shared
- [ ] Process improvements identified and planned

## Emergency Procedures

### 🚨 Critical Security Issue
```bash
1. @rca [issue-id]           # Immediate analysis
2. @implement-fix [issue-id] # Emergency fix
3. @code-review             # Rapid validation
4. Deploy with monitoring
```

### ⚡ Production Incident
```bash
1. Assess impact and contain issue
2. @rca [incident-id] for systematic analysis
3. @implement-fix [incident-id] for resolution
4. @system-review for prevention measures
```

### 🔄 Process Breakdown
```bash
1. Identify specific workflow issues
2. @system-review [current-process] [issues]
3. Update agent configurations and workflows
4. Test improved process with small feature
```

## Best Practices

### 🎯 Do's
- ✅ Always start with `@prime` for context
- ✅ Use `@plan-feature` before major development
- ✅ Follow `@execute` framework consistently
- ✅ Run `@code-review` before deployment
- ✅ Generate `@execution-report` for documentation
- ✅ Conduct `@system-review` for improvement

### ❌ Don'ts
- ❌ Skip planning phase - leads to scope creep
- ❌ Ignore quality gates - creates technical debt
- ❌ Work without coordination - causes conflicts
- ❌ Skip documentation - loses valuable insights
- ❌ Avoid process review - misses improvement opportunities

## Troubleshooting

### Issue: Agent Coordination Problems
**Solution**: Use Project Manager as central coordinator
```bash
@prime  # Establish shared context
@plan-feature [name]  # Clear task assignments
```

### Issue: Quality Issues
**Solution**: Implement systematic quality gates
```bash
@code-review  # Before any deployment
@execution-report  # Document quality metrics
```

### Issue: Process Inefficiency
**Solution**: Regular process analysis and improvement
```bash
@system-review [plan] [report]  # Identify bottlenecks
Update agent configurations based on findings
```

### Issue: Knowledge Loss
**Solution**: Comprehensive documentation workflow
```bash
@execution-report  # After major implementations
@system-review  # For process insights
Regular DEVLOG updates
```

## Success Metrics

### 📊 Development Velocity
- Time from feature request to deployment
- Number of features delivered per sprint
- Reduction in rework and bug fixes

### 🎯 Quality Metrics  
- Code review pass rate
- Test coverage percentage
- Production incident frequency
- Security vulnerability count

### 🔄 Process Effectiveness
- Agent coordination efficiency
- Knowledge retention and reuse
- Process improvement implementation rate
- Team satisfaction with workflows

## Getting Help

### 📚 Documentation
- `AGENT_WORKFLOW_GUIDE.md` - Comprehensive workflow documentation
- `IMPLEMENTATION_EXAMPLES.md` - Real-world usage examples
- Individual agent specifications in `agents/` directory

### 🔧 Configuration
- Agent hooks in `agents/hooks/` directory
- System prompts in `agents/prompts/` directory
- Project steering documents in `.kiro/steering/`

### 🎯 Support
- Use agent consultation triggers for guidance
- Review implementation examples for patterns
- Analyze system reviews for process improvements

---

*Keep this reference handy for quick access to essential commands and workflows!*