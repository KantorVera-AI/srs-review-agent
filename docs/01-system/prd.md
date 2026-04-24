**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect, PM, RA/QA consultants

---

> **Note on use case numbering:** This PRD describes functional workflow triggers. The canonical ROI-based use case taxonomy (UC1–UC7) is defined in `02-roi/master-overview.md` and is the naming convention used across all other documentation.

# Tool scope

**Decision-support only.** Generates **non-binding findings** for human review. Does **not** create or approve SRS, replace formal sign-offs, or act as the system of record for any controlled document.

---

# 1. Purpose

AI agent that reviews **SRS and risk files** against regulatory standards on document change events, approvals, and obsolescence. Delivers citation-backed findings to document owners for review and disposition.

---

# 2. Problem Statement

SRS and risk files change throughout the device lifecycle, but regulatory impact assessments remain manual — error-prone, inconsistent, and dependent on individual expertise. Missed gaps surface late, during design reviews, submissions, or inspections, when remediation cost is highest.

---

# 3. MVP scope

## In scope

- **Workflow triggers:** document state transitions, version updates, baseline approvals, manual submissions
- Analyse SRS and risk files against IEC 62304, ISO 14971, MDR, FDA 21 CFR 820, OWASP
- Generate findings with SRS requirement ID and standard clause citation
- Calibrate output depth by IMDRF significance category and IEC 62304 software item safety class
- Deliver findings to document owners via review interface
- Track dispositions (Accept / Reject / Defer / Clarify / Route / Escalate / Out of scope) per finding
- Log all findings and dispositions for audit trail

## Out of scope

- SRS generation or rewriting
- Risk acceptability decisions
- Code or test analysis
- Regulatory submission generation
- Any action that belongs to the authoritative QMS, DMS, or risk management system

---

# 4. Key use cases

The agent handles the following functional workflow triggers:

**Change event monitoring:** Document change event detected → agent classifies change type → generates findings routed to relevant document owners

**Risk file monitoring:** Risk file change event detected → agent flags hazard and risk control gaps

**Baseline