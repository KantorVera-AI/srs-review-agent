# V-Model & Stakeholder Guide for SRS Review Copilot

## Understanding the V-Model in Medical Device Software Development

The V-Model is a software development lifecycle framework widely adopted in regulated industries like medical devices. It emphasizes a structured approach where each development phase has a corresponding verification/validation phase.

### V-Model Structure

```
User Needs ────────────────────────► User Acceptance Testing
    │                                        ▲
    ▼                                        │
System Requirements ───────────► System Testing/Validation
    │                                        ▲
    ▼                                        │
Software Requirements (SRS) ───► Software Integration Testing
    │                                        ▲
    ▼                                        │
Detailed Design ────────────────► Unit Testing
    │                                        ▲
    └──────────► Implementation ────────────┘
```

### Where SRS Review Copilot Fits

The **SRS Review Copilot** operates at the **Software Requirements Specification (SRS)** level of the V-Model. This is a critical phase because:

1. **Requirements Quality**: The SRS translates system requirements into detailed software specifications
2. **Traceability Foundation**: SRS establishes the basis for design, implementation, and testing
3. **Regulatory Compliance**: SRS must comply with standards (IEC 62304, FDA guidance, EU MDR Annex I)
4. **Risk Management**: SRS directly impacts software risk analysis and mitigation strategies

### Impact on the V-Model

By automating SRS review, the copilot:
- **Prevents defects early**: Catching issues at the requirements phase prevents costly downstream fixes
- **Maintains traceability**: Ensures each requirement is properly structured for V&V phases
- **Enforces standards**: Validates compliance with regulatory and organizational standards
- **Accelerates cycles**: Reduces manual review time, enabling faster iteration

---

## Stakeholder Roles & Responsibilities

### 1. Requirements Engineer / Business Analyst

**Primary Interaction**: Direct user of the SRS Review Copilot

**Responsibilities**:
- Create and update SRS documents in the version control system
- Review copilot findings before finalizing requirements
- Address identified issues (ambiguity, incompleteness, non-compliance)
- Ensure requirements are testable and traceable
- Update SRS based on copilot recommendations

**What to Do with Findings**:
- **Review each finding**: Evaluate whether the identified issue is valid
- **Prioritize fixes**: Address critical compliance issues first, then quality improvements
- **Refine requirements**: Rewrite ambiguous or unclear requirements
- **Add missing elements**: Include safety classifications, traceability IDs, acceptance criteria
- **Document decisions**: If rejecting a finding, document the rationale
- **Re-run validation**: After updates, trigger copilot review again to verify fixes

---

### 2. Software Architect / Lead Developer

**Primary Interaction**: Receives validated SRS as input for design phase

**Responsibilities**:
- Review SRS findings related to feasibility and architectural constraints
- Provide feedback on technical requirements clarity
- Ensure requirements are implementable and appropriately detailed
- Participate in SRS reviews when architectural decisions are impacted

**What to Do with Findings**:
- **Assess technical feasibility**: Flag requirements that are technically infeasible
- **Clarify interfaces**: Work with requirements engineers to specify system interfaces
- **Review security findings**: Ensure OWASP and security requirements are architecturally sound
- **Validate risk classifications**: Confirm software safety classes align with design approach

---

### 3. Quality Assurance / Validation Engineer

**Primary Interaction**: Uses copilot-validated SRS as basis for test planning

**Responsibilities**:
- Verify that SRS requirements are testable
- Ensure traceability from SRS to test cases
- Validate that acceptance criteria are measurable
- Review copilot findings related to testability and verification

**What to Do with Findings**:
- **Check testability**: Identify requirements that lack clear acceptance criteria
- **Plan test coverage**: Use validated SRS to design comprehensive test cases
- **Flag verification gaps**: Escalate requirements that cannot be adequately tested
- **Maintain traceability**: Ensure each requirement has corresponding test coverage

---

### 4. Regulatory Affairs / Compliance Specialist

**Primary Interaction**: Reviews copilot findings for regulatory compliance

**Responsibilities**:
- Ensure SRS complies with applicable regulations (FDA, EU MDR, IEC 62304)
- Review safety and risk-related requirements
- Validate that regulatory guidance is properly interpreted
- Support audits and regulatory submissions with validated SRS documentation

**What to Do with Findings**:
- **Prioritize compliance issues**: Address all regulatory non-conformances immediately
- **Verify standard adherence**: Ensure IEC 62304, ISO 14971, and other standards are followed
- **Review safety requirements**: Validate that all safety requirements are properly documented
- **Audit trail**: Ensure all SRS changes are tracked and justified for regulatory inspection

---

### 5. Project Manager / Product Owner

**Primary Interaction**: Monitors copilot metrics to track requirements quality

**Responsibilities**:
- Track SRS review cycle times and defect rates
- Prioritize requirements backlog based on copilot findings
- Ensure team addresses critical findings within project timelines
- Report requirements quality metrics to stakeholders

**What to Do with Findings**:
- **Monitor trends**: Track recurring issues (e.g., frequent ambiguity in certain requirement types)
- **Allocate resources**: Ensure team has time to address findings before moving to design
- **Manage risk**: Escalate high-severity findings that could impact project timeline or compliance
- **Communicate status**: Report requirements maturity to leadership using copilot metrics

---

### 6. Risk Manager

**Primary Interaction**: Reviews SRS findings related to safety and risk controls

**Responsibilities**:
- Ensure SRS requirements address identified software risks
- Validate risk control measures are properly specified
- Verify traceability between risk analysis and SRS
- Review copilot findings on OWASP security requirements

**What to Do with Findings**:
- **Validate risk controls**: Ensure all identified risks have corresponding mitigations in SRS
- **Review safety classifications**: Confirm software safety class assignments are correct
- **Address security gaps**: Work with requirements engineers to add missing security controls
- **Update risk files**: Ensure risk management file reflects SRS updates

---

## Workflow Integration

### Standard Review Process

1. **Requirements Engineer** creates/updates SRS in Git
2. **Pipeline triggers** SRS Review Copilot automatically
3. **Copilot generates** findings report (compliance, quality, security)
4. **Requirements Engineer** reviews findings and updates SRS
5. **Stakeholders** review updated SRS (Architect, QA, Regulatory, Risk Manager)
6. **SRS approved** after all critical findings are resolved
7. **Next V-Model phase** begins (detailed design)

### Finding Severity Levels

- **Critical**: Regulatory non-compliance, missing safety requirements, major security gaps
  - **Action**: Must be resolved before SRS approval
  - **Owner**: Requirements Engineer + Regulatory Affairs

- **High**: Poor traceability, untestable requirements, ambiguous specifications
  - **Action**: Should be resolved before design phase
  - **Owner**: Requirements Engineer + QA

- **Medium**: Style inconsistencies, minor clarity issues, optimization suggestions
  - **Action**: Address in current cycle or backlog
  - **Owner**: Requirements Engineer

- **Low**: Informational, best practice recommendations
  - **Action**: Consider for future improvements
  - **Owner**: Team discretion

---

## Key Principles

1. **Human-in-the-Loop**: Copilot proposes, humans decide. All findings require human review.
2. **Non-Binding**: Findings are recommendations, not mandates. Stakeholders can accept, reject, or modify.
3. **Traceability**: All decisions (acceptance/rejection of findings) should be documented.
4. **Continuous Improvement**: Track copilot effectiveness and refine rules based on team feedback.
5. **Early Detection**: Address findings at SRS level to prevent costly downstream changes.

---

## Success Metrics by Stakeholder

- **Requirements Engineer**: Reduced review cycles, fewer downstream change requests
- **QA Engineer**: Higher first-time test pass rate, better requirements coverage
- **Regulatory Affairs**: Faster audit prep, zero compliance findings in inspections
- **Project Manager**: Predictable requirements phase duration, reduced rework costs
- **Risk Manager**: Complete risk-to-requirement traceability, no post-release safety issues

---

*This guide ensures all stakeholders understand how the SRS Review Copilot integrates into the V-Model and their specific responsibilities in acting on copilot findings.*
