# PIV Loop

The following is a guideline for the development process -> Plan ➡️Implement ➡️Verify / Validate (PIV Loop)

## Planning

### Phase 1

During phase 1 of Planning, the user "vibe codes" and establishes the vision.

```bash
@plan-vibe    # 1. Collaborative brainstorming
```

This is where the user is trying to understand:
- Tech stack decisions
- Architectural patterns
- Constraints and conventions

When the user has a clear idea of what the overall plan is, a Product Requirements Document (PRD) is created.

```bash
@create-prd    # 2. Formalize requirements
```

### Phase 2

This is where the PIV loop iteration begins. The user now begins planning out the features of the application:

```bash
@plan-feature [Feature Name]   # 3. Create technical plan
```

**CRITICAL**: The user MUST review the plan before proceeding (`4. User Review`).

## Implementation

Once the plan is approved, the Specialist Agent executes it.

```bash
@execute [plan relative path].md    # 5. Execute code
```

## Validation

Once the feature has been implemented, it is the time to validate the code.

```bash
# Review the code
@code-review    # 6. Test Orchestrator reviews
```

If issues are found:
```bash
@implement-fix  # 7. Specialist Agent fixes
```

Once quality is passed, we learn and improve:

```bash
@execution-report   # 8. Active Agent reflects
@system-review      # 9. Dev Logger analyzes process
@implement-system-changes # 10. PM evolves system
```

## Next Feature...

Now it is time for the user to move onto the next feature.  To know what that is:

```bash
# ask for the next feature
User: "What feature do you recommend on next.  Give me 5 tops features
and recommend which one you think I should do and why"
Agent: "Ok, here are the top 5 features you should work on..."
Agent: "I recommend you proceed with [XYZ] because..."
User: "Ok great, @create-plan [XYZ]"
```

The user keeps looping through the process until the MVP is completed.

![](C:\test\kiro-agent-team\PIV%20Loop.png)


