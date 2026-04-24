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

**Baseline intake:** Document approved or baselined → agent generates pre-approval compliance summary and SRS suggestions

**Obsolescence check:** Document marked obsolete → agent verifies successor documentation exists

For the full ROI-based use case taxonomy (UC1–UC7), see `02-roi/master-overview.md` and `use-cases/`.

---

# 5. Stakeholders and workflow

| Role | What they do with findings |
|---|---|
| Requirements Engineer | Disposition findings + update SRS |
| Software Architect | Assess reclassification flags + maintain software item registry |
| Risk / Safety Engineer | Verify hazard control traceability |
| Regulatory Affairs / PRRC | Review Critical findings + assess submission impact |
| QA / Validation Engineer | Verify testability and test coverage |
| Cybersecurity Engineer | Review security requirement gaps |
| Usability / HF Specialist | Review usability and use error findings |
| Clinical Affairs | Review clinical performance claim changes |

All stakeholders follow the disposition workflow defined in `01-system/stakeholders.md`.

---

# 6. Functional requirements

**FR1:** Detect document change events from configured sources (state transitions, version updates, manual submissions) and trigger analysis

**FR2:** Ingest SRS and risk files with stable document identifiers, version labels, and requirement IDs

**FR3:** Retrieve relevant standard clauses via RAG and generate citation-backed findings

**FR4:** Deliver findings to the review interface and log all dispositions with rationale

**FR5:** Read IMDRF significance category and IEC 62304 software item safety class metadata and apply output calibration per `01-system/output-calibration.md`

**FR6:** Flag potential device-level and software item-level reclassification triggers per `01-system/output-calibration.md`

---

# 7. Success criteria

| Metric | Target |
|---|---|
| Citation validity | ≥90% |
| Findings acceptance rate | ≥80% |
| Hallucination rate | <5% |
| Classification calibration accuracy | 100% match on test corpus |
| Reclassification detection rate | ≥90% |

---

# 8. Principles

1. Non-binding proposals only — humans decide
2. Every finding cites a specific standard clause and source document version
3. Human approval gates at every disposition point
4. Full audit trail — finding ID, disposition, rationale, timestamp, reviewer identity
5. Classification-calibrated — output depth varies by IMDRF category and software item safety class
6. Bounded — the agent never acts as the system of record

---

See [risk model](../02-roi/risk-model.md) · [stakeholders](stakeholders.md) · [output calibration](output-calibration.md)