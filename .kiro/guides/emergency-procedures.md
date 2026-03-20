# Emergency Procedures

## 🚨 **Rapid Response with Systematic Quality**

When critical issues arise, our agent team provides structured emergency response that maintains quality standards even under pressure. This guide covers procedures for handling urgent situations while preserving the systematic approach that ensures reliable outcomes.

## ⚡ **Emergency Response Philosophy**

### **Systematic Under Pressure**
Even in emergencies, we maintain systematic approaches because:
- **Prevents Mistakes**: Pressure leads to errors; systematic approaches prevent them
- **Ensures Completeness**: Critical steps aren't skipped in the rush
- **Maintains Quality**: Emergency fixes that create new problems aren't solutions
- **Enables Learning**: Systematic response provides data for prevention

### **Speed Through Structure**
Our emergency procedures are designed for speed through:
- **Pre-defined Workflows**: No time wasted deciding what to do
- **Clear Responsibilities**: Each agent knows their emergency role
- **Parallel Processing**: Multiple agents work simultaneously when possible
- **Quality Shortcuts**: Streamlined but not eliminated quality checks

## 🎯 **Emergency Classification**

### **Critical (Immediate Response - 0-1 Hour)**
**Characteristics:**
- Production system down or severely impaired
- Security breach or active attack
- Data corruption or loss risk
- Compliance violation with legal implications

**Examples:**
- Database server failure
- Active SQL injection attack
- Payment system outage
- GDPR data breach

**Response Team:** All relevant agents mobilized immediately

### **High (Urgent Response - 1-4 Hours)**
**Characteristics:**
- Significant functionality impaired
- Performance severely degraded
- Security vulnerability discovered
- Major feature completely broken

**Examples:**
- Authentication system failure
- API response times >5 seconds
- Critical security vulnerability
- Core feature not working

**Response Team:** Primary agents with specialist support

### **Medium (Priority Response - 4-24 Hours)**
**Characteristics:**
- Minor functionality issues
- Performance degradation
- Non-critical security concerns
- Quality standard violations

**Examples:**
- Secondary feature bugs
- Slow page load times
- Code quality issues
- Documentation gaps

**Response Team:** Assigned specialist agents

## 🚨 **Critical Emergency Response**

### **Phase 1: Immediate Assessment (0-15 minutes)**

#### **Step 1: Situation Assessment**
```bash
# Project Manager immediately assesses situation
"EMERGENCY: [Brief description of issue]
- Impact: [User/system impact]
- Severity: [Critical/High/Medium]
- Affected Systems: [List of affected components]
- Immediate Actions Needed: [Containment steps]"
```

#### **Step 2: Team Mobilization**
```bash
# Mobilize appropriate agents based on issue type
Security Issue → Security Specialist leads
Performance Issue → Backend Engineer + DevOps Engineer
Data Issue → Database Specialist leads
Frontend Issue → Frontend Architect leads
```

#### **Step 3: Immediate Containment**
```bash
# Take immediate steps to prevent further damage
- Isolate affected systems if necessary
- Implement temporary workarounds
- Notify stakeholders of issue and response
- Begin logging all actions for post-incident review
```

### **Phase 2: Root Cause Analysis (15-45 minutes)**

#### **Rapid RCA Process**
```bash
@rca [emergency-issue-id]
```

**Emergency RCA Focus:**
- **What happened?** Clear description of the issue
- **When did it start?** Timeline of issue emergence
- **What's the impact?** Scope of affected users/systems
- **What's the root cause?** Primary cause identification
- **What's the fix?** Immediate solution approach

**Expected Output (15-30 minutes):**
```
🚨 EMERGENCY RCA: [Issue Description]
- Timeline: Issue started at [time], detected at [time]
- Root Cause: [Primary cause - keep it simple and actionable]
- Impact: [Affected users/systems/functionality]
- Immediate Fix: [Specific actions to resolve]
- Risk Assessment: [Risks of proposed fix]
- Estimated Resolution Time: [Realistic timeline]
```

### **Phase 3: Emergency Fix Implementation (30-60 minutes)**

#### **Systematic Emergency Fix**
```bash
@implement-fix [emergency-issue-id]
```

**Emergency Implementation Priorities:**
1. **Restore Service**: Get systems operational
2. **Minimize Risk**: Don't introduce new problems
3. **Document Actions**: Track all changes made
4. **Prepare Rollback**: Have backup plan ready

**Parallel Activities:**
- **Primary Agent**: Implements the fix
- **Secondary Agent**: Prepares rollback procedure
- **Test Orchestrator**: Prepares rapid validation tests
- **Project Manager**: Coordinates and communicates status

### **Phase 4: Emergency Validation (15-30 minutes)**

#### **Rapid Quality Check**
```bash
@code-review
```

**Emergency Review Focus:**
- **Fix Effectiveness**: Does it resolve the issue?
- **No New Issues**: Doesn't introduce new problems
- **Rollback Ready**: Can be quickly reversed if needed
- **Monitoring**: Appropriate monitoring in place

**Streamlined Validation:**
```
⚡ Emergency Validation Checklist:
- [ ] Issue resolved (verified in affected environment)
- [ ] No new critical issues introduced
- [ ] Rollback procedure tested and ready
- [ ] Monitoring alerts configured
- [ ] Stakeholders notified of resolution
```

### **Phase 5: Deployment and Monitoring (15-30 minutes)**

#### **Controlled Emergency Deployment**
```bash
# Deploy with enhanced monitoring
- Deploy to staging first (if possible)
- Deploy to production with careful monitoring
- Verify fix effectiveness immediately
- Monitor for any new issues
- Communicate resolution to stakeholders
```

#### **Post-Deployment Monitoring**
- **Immediate (0-2 hours)**: Intensive monitoring for new issues
- **Short-term (2-24 hours)**: Regular monitoring for stability
- **Medium-term (1-7 days)**: Ongoing monitoring for side effects

## 🔧 **High Priority Response**

### **Structured High-Priority Process**

#### **Assessment and Planning (30 minutes)**
```bash
@prime                    # Load current context
@rca [high-priority-issue] # Systematic analysis
```

#### **Implementation (1-2 hours)**
```bash
@implement-fix [issue-id] # Systematic fix
```

#### **Validation (30 minutes)**
```bash
@code-review             # Quality validation
```

#### **Documentation (30 minutes)**
```bash
@execution-report        # Document resolution
```

### **High-Priority Response Team**
- **Lead Agent**: Specialist most relevant to issue type
- **Support Agent**: Secondary expertise as needed
- **Quality Agent**: Test Orchestrator for validation
- **Coordinator**: Project Manager for oversight

## 🛡️ **Security Emergency Response**

### **Security Incident Classification**

#### **Critical Security (0-1 Hour Response)**
- Active attacks or breaches
- Data exfiltration in progress
- System compromise detected
- Compliance violation with legal implications

#### **High Security (1-4 Hour Response)**
- Vulnerability with active exploits
- Unauthorized access detected
- Data integrity concerns
- Security control failures

### **Security Emergency Workflow**

#### **Phase 1: Containment (0-15 minutes)**
```bash
# Security Specialist leads immediate containment
- Isolate affected systems
- Preserve evidence
- Assess scope of compromise
- Implement temporary security measures
```

#### **Phase 2: Analysis (15-45 minutes)**
```bash
@rca [security-incident-id]
```

**Security RCA Focus:**
- **Attack Vector**: How was the system compromised?
- **Scope**: What systems/data are affected?
- **Timeline**: When did the incident start?
- **Evidence**: What forensic evidence is available?
- **Immediate Actions**: What must be done now?

#### **Phase 3: Response (30-90 minutes)**
```bash
@implement-fix [security-incident-id]
```

**Security Response Actions:**
- **Eliminate Threat**: Remove attack vector
- **Secure Systems**: Implement additional security measures
- **Preserve Evidence**: Maintain forensic integrity
- **Restore Service**: Return to secure operational state

#### **Phase 4: Validation (15-30 minutes)**
```bash
@code-review
```

**Security Validation:**
- **Threat Eliminated**: Attack vector closed
- **Systems Secure**: Additional security measures effective
- **No New Vulnerabilities**: Fix doesn't introduce new risks
- **Monitoring Enhanced**: Improved detection capabilities

## 📊 **Performance Emergency Response**

### **Performance Crisis Classification**

#### **Critical Performance (0-1 Hour)**
- System completely unresponsive
- Database deadlocks causing outages
- Memory leaks causing crashes
- Complete service unavailability

#### **High Performance (1-4 Hours)**
- Response times >5 seconds
- High error rates (>5%)
- Resource exhaustion warnings
- Significant user impact

### **Performance Emergency Workflow**

#### **Immediate Actions**
```bash
# Backend Engineer + DevOps Engineer coordinate
- Check system resources (CPU, memory, disk)
- Identify performance bottlenecks
- Implement immediate scaling if possible
- Enable enhanced monitoring
```

#### **Analysis and Fix**
```bash
@rca [performance-issue-id]
@implement-fix [performance-issue-id]
```

**Performance Fix Priorities:**
1. **Resource Optimization**: Address immediate resource constraints
2. **Query Optimization**: Fix slow database queries
3. **Caching**: Implement emergency caching
4. **Load Balancing**: Distribute load more effectively

## 🔄 **Post-Emergency Procedures**

### **Immediate Post-Emergency (0-2 hours)**

#### **System Stabilization**
- Monitor for any side effects of emergency fixes
- Verify all systems are operating normally
- Confirm user experience is restored
- Update stakeholders on resolution

#### **Initial Documentation**
```bash
@execution-report
```

**Emergency Report Contents:**
- Timeline of events and actions taken
- Root cause and fix implemented
- Impact assessment and user communication
- Immediate lessons learned

### **Short-Term Post-Emergency (2-24 hours)**

#### **Comprehensive Analysis**
```bash
@system-review [emergency-rca] [emergency-fix-report]
```

**Post-Emergency Analysis:**
- **Response Effectiveness**: How well did emergency procedures work?
- **Process Improvements**: What can be improved for next time?
- **Prevention Measures**: How can similar issues be prevented?
- **Team Performance**: How did agent coordination work under pressure?

#### **Permanent Fix Planning**
- Assess if emergency fix is sufficient long-term
- Plan proper solution if temporary fix was implemented
- Schedule permanent fix implementation
- Update monitoring and alerting

### **Long-Term Post-Emergency (1-7 days)**

#### **Process Improvement**
- Update emergency procedures based on learnings
- Enhance monitoring and alerting systems
- Implement prevention measures
- Train team on lessons learned

#### **Documentation Updates**
- Update runbooks and procedures
- Enhance monitoring documentation
- Create prevention checklists
- Share learnings with broader team

## 🎯 **Emergency Response Best Practices**

### **Communication During Emergencies**
- **Clear Status Updates**: Regular, specific status communication
- **Stakeholder Notification**: Appropriate level of detail for each audience
- **Team Coordination**: Clear role assignments and progress updates
- **Documentation**: Real-time logging of actions and decisions

### **Quality Under Pressure**
- **Don't Skip Steps**: Follow systematic approach even when rushed
- **Parallel Processing**: Use multiple agents to maintain speed
- **Validation Focus**: Ensure fixes work and don't create new problems
- **Rollback Readiness**: Always have a way to undo changes

### **Learning from Emergencies**
- **Blameless Post-Mortems**: Focus on process improvement, not blame
- **Systematic Analysis**: Use structured approach to understand what happened
- **Prevention Focus**: Implement measures to prevent recurrence
- **Process Evolution**: Continuously improve emergency response procedures

## 📋 **Emergency Response Checklist**

### **Critical Emergency Checklist**
- [ ] Situation assessed and classified (0-5 minutes)
- [ ] Appropriate agents mobilized (5-10 minutes)
- [ ] Immediate containment actions taken (10-15 minutes)
- [ ] Root cause analysis initiated (@rca) (15-30 minutes)
- [ ] Emergency fix implemented (@implement-fix) (30-60 minutes)
- [ ] Fix validated (@code-review) (60-75 minutes)
- [ ] Solution deployed with monitoring (75-90 minutes)
- [ ] Stakeholders notified of resolution (90-120 minutes)
- [ ] Post-emergency analysis scheduled (within 24 hours)

### **Quality Maintenance Checklist**
- [ ] Systematic approach followed despite time pressure
- [ ] All actions documented for post-incident review
- [ ] Fix validated before deployment
- [ ] Rollback procedure prepared and tested
- [ ] Monitoring enhanced to detect similar issues
- [ ] Lessons learned captured and shared

---

**Ready to evaluate your projects comprehensively? Check out [Project Evaluation](project-evaluation.md) for assessment and optimization workflows!**