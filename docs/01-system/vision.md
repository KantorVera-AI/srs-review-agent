**Status:** Working draft
**Owner:** Product Management
**Audience:** All stakeholders

---

# SRS Review Agent — Product Vision

## The challenge

Medical device software teams operating under EU MDR, FDA, and international standards (ISO 13485, IEC 62304, ISO 14971, IEC 81001-5-1) face a critical documentation challenge:

- SRS and risk files are configuration-controlled, version-managed artefacts that must continuously align with evolving standards, internal SOPs, and security best practices
- Manual reviews are slow, error-prone, and dependent on individual expertise
- Version-controlled workflows manage document changes, but regulatory impact assessments remain manual
- Missed gaps surface late — during design reviews, submissions, or inspections — when remediation cost is highest

---

## Our solution

An AI decision-support agent that integrates into the document management and change control workflow of a SaMD team:

### What it does

- **Monitors SRS and risk files** across the device lifecycle
- **Triggers on document lifecycle events** — state changes, approval events, version updates, manual submissions
- **Analyses against standards** — IEC 62304, ISO 14971, OWASP, IEC 81001-5-1, EU MDR, FDA 21 CFR 820
- **Generates findings with citations** — traceable references to specific standard clauses and source document versions
- **Calibrates output depth** — findings vary by the device's IMDRF significance category (I–IV) and the IEC 62304 safety class of each affected software item
- **Routes to the right owner** — RA, QA, Risk, Cybersecurity, Usability, Clinical teams, based on change type and document ownership
- **Logs every decision** — full audit trail of findings, dispositions, rationales, and timestamps for regulatory inspection

### What it does not do

- No autonomous regulatory decisions
- No clinical decision support
- No automated risk acceptability decisions
- No creation or approval of controlled documents
- No replacement of formal design reviews or sign-offs
- Always requires human review and disposition

---

## Value proposition

### For Requirements Owners and Systems Engineers
- Catch gaps before peer review — earlier detection means lower remediation cost
- Consistent, citation-backed feedback on completeness, traceability, and clarity
- Fewer downstream change requests and rework cycles

### For Regulatory Affairs and QA
- Systematic, repeatable SRS quality checks across every change event
- Documented evidence of compliance due diligence for audit and submission preparation
- Classification-calibrated findings — depth and routing reflect the actual regulatory burden of each product

### For Risk Management
- Continuous verification that risk controls are implemented in the SRS and traceable
- Immediate detection of broken hazard-to-requirement links
- Reclassification trigger detection — flagging when a SRS change may affect the device's IMDRF category or a software item's IEC 62304 safety class

### For Cybersecurity teams
- Proactive detection of missing security requirements when new interfaces or data flows are introduced
- OWASP ASVS and IEC 81001-5-1 aligned gap analysis
- SBOM-aware SOUP vulnerability monitoring (Release 2)

### For the organisation
- **Faster time to approval** — reduce manual review bottlenecks and catch deficiencies before they reach the regulator