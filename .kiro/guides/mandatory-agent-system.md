# Mandatory Agent System Guide

## Overview

This project uses a **mandatory agent system** that ensures all development work is performed by specialized agents with clear visibility into who is working on what.

## Why Mandatory Agents?

- **Consistency**: Specialized expertise for each task type
- **Traceability**: Clear audit trail of who did what
- **Quality**: Agents follow best practices and guidelines
- **Coordination**: Clear handoffs prevent work duplication
- **Visibility**: Team always knows which agent is active
- **IDE/CLI Compatibility**: Works identically in both environments

## How It Works

### 1. Agent Selection

When a task is requested:
1. Determine which agent is appropriate
2. The agent announces itself
3. Work proceeds under that agent's expertise

### 2. Activation Announcements

Every agent MUST announce when becoming active:
- Clear role identification
- Mission statement
- What will be accomplished

### 3. Handoff Announcements

When work is passed between agents:
- Current agent announces completion
- Next agent is clearly identified
- Context is provided for continuity

## Usage in Kiro IDE

### Starting with an Agent
1. Open agent picker (Cmd/Ctrl + K, type "agent")
2. Select appropriate agent
3. Agent automatically announces activation
4. Proceed with task

### Switching Agents
1. Current agent announces handoff
2. Use agent picker to select next agent
3. New agent announces activation
4. Continue work

### Agent Picker
- Access via command palette
- Shows all 9 available agents
- Displays agent roles and capabilities
- Tracks active agent in conversation

## Usage in Kiro CLI

### Starting with an Agent
```bash
# Start with specific agent
kiro chat --agent project-manager

# Or start and switch
kiro chat
> /agent swap
# Select agent from list
```

### Switching Agents
```bash
# Within chat session
> /agent swap
# Select new agent from list
```

### Agent Commands
```bash
# List available agents
kiro-cli agent list

# View agent details
kiro-cli agent show backend-engineer

# Set default agent
kiro-cli agent set-default project-manager
```

## Enforcement

The mandatory agent system is enforced via:

### 1. Steering File (`.kiro/steering/mandatory-agents.md`)
- Loaded automatically in every session
- Enforces agent usage requirement
- Provides agent selection rules
- Works in both IDE and CLI

### 2. Agent System Prompts
- Each agent includes announcement requirements
- Built-in activation and handoff formats
- Consistent behavior across all agents

### 3. System Configuration
- Agent configurations in `.kiro/agents/`
- JSON files define agent capabilities
- Markdown files define agent behaviors
- Hooks define agent automation

## Agent Roles and Selection

### Project Manager
**Use for:**
- Project planning and setup
- Feature breakdown and task management
- Multi-agent coordination
- Progress tracking and reporting

**Example:**
```
🎭 **PROJECT MANAGER ACTIVE**

[Role]: Development Team Orchestrator
[Mission]: Planning user authentication feature

I'll break down this feature into tasks...
```

### Backend Engineer
**Use for:**
- API development
- Server-side logic
- Database integration
- Authentication and security implementation

**Example:**
```
🎭 **BACKEND ENGINEER ACTIVE**

[Role]: API Developer & Business Logic Architect
[Mission]: Implementing login API endpoint

I'll create the authentication endpoint...
```

### Frontend Architect
**Use for:**
- UI component development
- Client-side logic
- State management
- User experience implementation

**Example:**
```
🎭 **FRONTEND ARCHITECT ACTIVE**

[Role]: Client-side Developer & UX Specialist
[Mission]: Building login form component

I'll create the React component...
```

### Database Specialist
**Use for:**
- Schema design and migrations
- Query optimization
- Database performance tuning
- Data modeling

**Example:**
```
🎭 **DATABASE SPECIALIST ACTIVE**

[Role]: Data Layer Management Expert
[Mission]: Creating user authentication schema

I'll design the users table...
```

### DevOps Engineer
**Use for:**
- Infrastructure setup
- CI/CD pipeline configuration
- Deployment automation
- Monitoring and logging

**Example:**
```
🎭 **DEVOPS ENGINEER ACTIVE**

[Role]: Infrastructure & Deployment Specialist
[Mission]: Setting up production deployment pipeline

I'll configure the CI/CD workflow...
```

### Security Specialist
**Use for:**
- Security audits and reviews
- Vulnerability analysis and fixes
- Security implementation
- Compliance validation

**Example:**
```
🎭 **SECURITY SPECIALIST ACTIVE**

[Role]: Application Security Expert
[Mission]: Reviewing authentication security

I'll analyze the authentication flow...
```

### UI/UX Designer
**Use for:**
- Design system creation
- User experience design
- Accessibility implementation
- Visual design decisions

**Example:**
```
🎭 **UI/UX DESIGNER ACTIVE**

[Role]: User Experience Design Specialist
[Mission]: Designing authentication flow UX

I'll create the user journey...
```

### Test Orchestrator
**Use for:**
- Testing strategy
- Test implementation
- Quality assurance reviews
- Code review coordination

**Example:**
```
🎭 **TEST ORCHESTRATOR ACTIVE**

[Role]: Quality Assurance Lead
[Mission]: Creating test suite for authentication

I'll design the testing strategy...
```

### Development Logger
**Use for:**
- Process documentation
- Workflow analysis
- Improvement identification
- Experience capture

**Example:**
```
🎭 **DEVELOPMENT LOGGER ACTIVE**

[Role]: Process Documentation Specialist
[Mission]: Analyzing authentication implementation process

I'll review the development workflow...
```

## Workflow Examples

### Simple Feature Implementation
```
🎭 **PROJECT MANAGER ACTIVE**
[Mission]: Planning login feature

Task breakdown created...

🔄 **Handing off to Backend Engineer**

🎭 **BACKEND ENGINEER ACTIVE**
[Mission]: Creating login API

API implemented...

✅ **BACKEND ENGINEER Complete**
🔄 **Handing off to Frontend Architect**

🎭 **FRONTEND ARCHITECT ACTIVE**
[Mission]: Building login UI

Component created...

✅ **FRONTEND ARCHITECT Complete**
🔄 **Handing off to Test Orchestrator**

🎭 **TEST ORCHESTRATOR ACTIVE**
[Mission]: Testing login feature

Tests passed, feature complete!
```

### Complex Multi-Agent Feature
```
🎭 **PROJECT MANAGER ACTIVE**
[Mission]: Coordinating full authentication system

📋 **Task Assignments:**
- Database Specialist: Schema
- Backend Engineer: API
- Security Specialist: Security review
- Frontend Architect: UI
- DevOps Engineer: Deployment
- Test Orchestrator: Testing

🔄 **Assigning to Database Specialist**

🎭 **DATABASE SPECIALIST ACTIVE**
[Mission]: Creating authentication schema

[Work completed]

✅ **DATABASE SPECIALIST Complete**
🔄 **Handing off to Backend Engineer**

[Continue through all agents...]
```

## Best Practices

### DO ✅
- Always start with agent announcement
- Use appropriate agent for each task type
- Provide clear mission statements
- Include context in handoffs
- Complete work before handing off
- Hand back to Project Manager if uncertain

### DON'T ❌
- Skip agent announcements
- Use wrong agent for task type
- Hand off without completion
- Forget to provide context
- Work without active agent
- Switch agents mid-task unnecessarily

## Troubleshooting

### Issue: Not sure which agent to use
**Solution**: Default to Project Manager, who will coordinate and assign the appropriate agent.

### Issue: Need multiple agents for one task
**Solution**: Project Manager coordinates multi-agent tasks with clear assignments.

### Issue: Agent handoff seems inefficient
**Solution**: Complete related work under one agent before handing off. Group related tasks.

### Issue: Announcement format confusion
**Solution**: Refer to `.kiro/agents/ANNOUNCEMENTS.md` for detailed formats and examples.

### Issue: Works in CLI but not IDE (or vice versa)
**Solution**: The system works identically in both. Check that `.kiro` directory is properly set up.

## Configuration Files

### Agent Definitions
- Location: `.kiro/agents/[agent-name].json`
- Contains: Agent metadata, tools, prompts
- Used by: Both Kiro IDE and CLI

### Agent System Prompts
- Location: `.kiro/agents/prompts/[agent-name]-system.md`
- Contains: Agent behavior, guidelines, expertise
- Used by: Agent system for consistent behavior

### Agent Hooks
- Location: `.kiro/agents/hooks/[agent-name]-hooks.yaml`
- Contains: Automation triggers and actions
- Used by: System for automated agent activation

## Integration Points

### With Kiro IDE
- Native agent picker integration
- Visual agent indicators
- Conversation history with agents
- Agent switching UI

### With Kiro CLI
- `/agent swap` command
- `--agent` flag support
- Terminal-based agent selection
- Consistent announcement output

### With Steering System
- `.kiro/steering/mandatory-agents.md` enforces usage
- Loaded automatically in all sessions
- Works with other steering files
- Applies to both IDE and CLI

### With Prompt System
- Agents use prompts from `.kiro/prompts/`
- `@prime`, `@plan-feature`, `@execute` etc.
- Consistent prompt access across agents
- Same prompts in IDE and CLI

## Success Metrics

Track these indicators of effective agent system usage:

- **Agent Usage Rate**: 100% of development work uses agents
- **Announcement Compliance**: All agents announce activations and handoffs
- **Handoff Efficiency**: Clear context provided in all handoffs
- **Agent Selection Accuracy**: Appropriate agent chosen for task type
- **Multi-Agent Coordination**: Smooth coordination on complex tasks

## Reference

### Key Files
- `.kiro/steering/mandatory-agents.md` - Enforcement rules
- `.kiro/agents/ANNOUNCEMENTS.md` - Announcement guidelines
- `.kiro/agents/[agent].json` - Agent configurations
- `.kiro/agents/prompts/[agent]-system.md` - Agent prompts

### Related Guides
- `.kiro/guides/AGENT_WORKFLOW_GUIDE.md` - Agent workflows
- `.kiro/guides/agent-coordination.md` - Multi-agent patterns
- `.kiro/guides/QUICK_REFERENCE.md` - Quick reference

### Documentation
- `AGENTS.md` - Agent system overview
- `README.md` - Project documentation
- `.kiro/README.md` - Kiro system documentation

---

*This mandatory agent system ensures consistent, high-quality development with full traceability in both Kiro IDE and Kiro CLI.*
