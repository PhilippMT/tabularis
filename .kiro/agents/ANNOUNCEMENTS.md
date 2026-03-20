# Agent Announcement System

## Purpose

All agents MUST announce themselves when becoming active and when passing work to other agents. This ensures transparency, traceability, and proper agent coordination.

## Activation Announcements

When an agent becomes active, it MUST start its first message with:

### Format
```
🎭 **[AGENT NAME] ACTIVE**

[Role]: [Brief role description]
[State]: Read from .kiro/TEAM_STATE.md
[Mission]: What I'm about to do

[Proceed with work]
```

### Example
```
🎭 **BACKEND ENGINEER ACTIVE**

[Role]: API Developer & Business Logic Architect
[Mission]: Implementing user authentication API endpoints

I'll now create the authentication endpoints with JWT support...
```

## Handoff Announcements

When an agent completes work and passes it to another agent:

### Format
```
✅ **[CURRENT AGENT] Complete**

**Completed Work:**
- [What was accomplished]

🔄 **Handing off to [NEXT AGENT]**

**Next Steps:**
- [What needs to be done next]
- [Context for the next agent]

[State Update]: .kiro/TEAM_STATE.md updated

🎭 **[NEXT AGENT] ACTIVE** (announced by receiving agent)
```

### Example
```
✅ **BACKEND ENGINEER Complete**

**Completed Work:**
- Created `/api/auth/login` endpoint
- Implemented JWT token generation
- Added password hashing with bcrypt

🔄 **Handing off to FRONTEND ARCHITECT**

**Next Steps:**
- Create login form component
- Implement token storage
- Add authentication state management

🎭 **FRONTEND ARCHITECT ACTIVE**

[Role]: Client-side Developer & UX Specialist
[Mission]: Building the login UI and authentication flow

I'll now create the login component...
```

## Announcement Guidelines

1. **Always Announce**: Never proceed without an announcement
2. **Be Specific**: Clearly state what will be accomplished
3. **Provide Context**: Include relevant information for handoffs
4. **Use Emojis**: Use 🎭 for activation, 🔄 for handoffs, ✅ for completion
5. **Be Consistent**: Use the same format across all agents
6. **Brief but Complete**: Keep announcements concise but informative

## Multi-Agent Scenarios

When multiple agents work on related tasks:

```
🎭 **PROJECT MANAGER ACTIVE**

[Role]: Development Team Orchestrator
[Mission]: Coordinating multi-agent authentication feature implementation

📋 **Task Breakdown:**
- Backend Engineer: API endpoints
- Frontend Architect: UI components  
- Database Specialist: Schema updates

🔄 **Assigning work to Backend Engineer...**

🎭 **BACKEND ENGINEER ACTIVE**

[Role]: API Developer
[Mission]: Creating authentication API endpoints

[Work completed]

✅ **BACKEND ENGINEER Complete**

**Completed Work:**
- Login endpoint created
- Token generation implemented
- Password hashing added

🔄 **Handing off to Database Specialist...**

🎭 **DATABASE SPECIALIST ACTIVE**

[Role]: Data Layer Expert
[Mission]: Optimizing schema for authentication
```

## Parallel Work Announcements

When agents work simultaneously:

```
🎭 **PROJECT MANAGER ACTIVE**

[Role]: Development Team Orchestrator
[Mission]: Coordinating parallel development work

📋 **Parallel Task Assignment:**

🔄 **Assigning to Backend Engineer**: API development
🔄 **Assigning to Frontend Architect**: UI components

Both agents will work in parallel...

---

🎭 **BACKEND ENGINEER ACTIVE**
[Mission]: API endpoints

---

🎭 **FRONTEND ARCHITECT ACTIVE**
[Mission]: UI components

[Both agents proceed with their work]
```

## Announcement Best Practices

### DO ✅
- Always announce before starting work
- Use clear, specific mission statements
- Provide complete context for handoffs
- Use consistent emoji indicators
- Announce completion before handoff
- Specify which agent receives the handoff

### DON'T ❌
- Skip announcements for "quick fixes"
- Use vague mission statements
- Handoff without context
- Change announcement format
- Proceed without activation announcement
- Forget to specify receiving agent

## Integration with Kiro IDE & CLI

Both environments support agent announcements:

### Kiro IDE
- Announcements appear in the chat interface
- Visual indicators for active agents
- Agent picker shows available agents
- Handoffs tracked in conversation history

### Kiro CLI
- Announcements appear in terminal output
- `/agent swap` command for switching agents
- `--agent` flag for starting with specific agent
- Clear visual separation between agent responses

The announcement format works identically in both environments.

## Troubleshooting

**Q: Do I need to announce for every message?**
A: Only when becoming active or handing off. Once active, continue working until handoff.

**Q: Can I abbreviate announcements?**
A: No. Use the full format for clarity and traceability.

**Q: What if I'm already the active agent?**
A: If you're continuing work, no new announcement needed. Only announce when first becoming active.

**Q: How do I know which agent to hand off to?**
A: The Project Manager coordinates handoffs. If uncertain, hand back to Project Manager.

## Reference

See also:
- `.kiro/steering/mandatory-agents.md` - Enforcement rules
- `.kiro/guides/mandatory-agent-system.md` - Complete system guide
- `.kiro/agents/[agent-name].md` - Individual agent specifications
