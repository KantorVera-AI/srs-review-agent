**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect, PM

---

# UC6 — Regulatory inspection and submission preparation

**Release tier:** Later (requires 6+ months of production findings history)
**Depends on:** UC1, UC2, UC3, UC4, UC5, UC7 — all previous use cases as data sources
**Required by:** Nothing downstream

---

## One-line description

Aggregate the findings history, disposition rationales, traceability links, and document change log across a defined period to produce a structured audit readiness summary package applicable to both EU MDR notified body audits and FDA inspections or pre-market submissions.

---

## What triggers it

A manual request from the Regulatory Affairs specialist or Quality Manager, typically 4–8 weeks before a planned inspection, audit, or submission deadline. UC6 is not triggered automatically — it is an on-demand reporting function.

---

## What the agent does

1. Receives the audit readiness request with a defined scope — product, time period, and target regulatory framework (EU MDR, FDA, or both)
2. Aggregates from the audit log:
   - All findings generated in the period, with their current state
   - All dispositions recorded, with rationale and reviewer identity
   - All reclassification findings and their outcomes
   - All economic trade-off assessments and the decisions made
3. Identifies open findings (not yet resolved or closed) with their age and assigned owner
4. Generates a traceability gap summary — requirements that have open findings or unresolved gaps in the risk control chain
5. Produces a checklist of outstanding items mapped to the applicable regulatory framework:
   - EU MDR: mapped to Annex II / Annex III technical documentation requirements
   - FDA: mapped to 21 CFR 820.30 design control requirements
6. Assembles the package and delivers it to the Regulatory Affairs specialist as an exportable structured file

The package is a summary for preparation purposes — it is not the technical file or design history file itself, and it does not replace any authoritative QMS record. It is evidence that the agent's systematic monitoring was operating during the period and that findings were reviewed and dispositioned.

---

## Who receives the output

| Output | Recipient | Condition |
|---|---|---|
| Audit readiness package | Regulatory Affairs specialist | On request |
| Open findings summary | Regulatory Affairs specialist + finding owners | Included in package |
| Traceability gap summary | Risk Engineer + Regulatory Affairs | Included in package |
| Outstanding items checklist | Regulatory Affairs specialist | Included in package, mapped to framework |

---

## RICE score

| Risk savings | Impact | Confidence | Effort | Score |
|---|---|---|---|---|
| 3 | 3 | 0.55 | 5 | 10 |

*Risk savings of 3: improved audit readiness reduces the probability of inspection findings, but the cost avoidance per event is lower than the traceability and classification use cases. Impact of 3: significant time saving but the use case is infrequent. Confidence of 0.55: the lowest confidence of any use case — output value depends entirely on the completeness of the findings history, and output format requirements vary by notified body and FDA review division. Effort of 5: the highest build effort — requires aggregation across all previous use cases, format customisation by regulatory framework, and validation against real inspection expectations.*

---

## Benefit breakdown

### Phase 1 — Initial development

| Dimension | Estimate |
|---|---|
| Typical events | 1–2 pre-submission readiness checks before first filing |
| Time saved per event | 15–40 hours of manual traceability consolidation |
| Total time saving | 15–80 hours = 2,000–10,400€ |
| Regulatory cost avoided | 10–30k€ — pre-submission gap analysis reduces deficiencies at first review |

### Phase 2 — Ongoing maintenance

| Dimension | Estimate |
|---|---|
| Annual events per product | 0.5–1 major audit or submission per year |
| Time saved per event | 10–30 hours of manual audit preparation |
| Annual time saving | 5–30 hours = 650–3,900€ |
| Regulatory cost avoided | 10–20k€ per year |

---

## Key assumptions

- UC6 is a reporting layer on top of all previous use cases. If the agent has not been operating consistently — if findings were not generated, or not dispositioned, or the audit log has gaps — the output package will be incomplete and may be worse than no package (false confidence in coverage).
- A minimum of 6 months of consistent production operation across UC1–UC5 is needed before the first UC6 output is meaningful. This is the primary reason for the "Later" release placement.
- Output format requirements vary by notified body and FDA review division. Significant customisation may be required for each specific inspection or submission target. The initial implementation should produce a neutral structured format that can be adapted rather than hard-coding any single format.
- The package does not replace the technical file or design history file — it supplements them with evidence of systematic change control monitoring.

---

## Dependencies and risks

**Dependencies:** All previous use cases as data sources. Minimum 6 months of production findings history. Regulatory Affairs specialist input on the target framework and expected format.

**Technical risks:**
- Incomplete findings history is the primary quality risk. If teams have been inconsistent in dispositiong findings, the aggregation will surface that inconsistency and may create remediation work at the worst possible time — weeks before an inspection.
- Format variability by notified body and FDA division means the initial implementation will not satisfy every possible inspection format. The RA specialist must review and potentially reformat the package output before using it for a specific inspection.

**Process risks:**
- Teams that have been using the agent casually — not dispositioning all findings, not maintaining the audit log — will find UC6 surfaces their process gaps. This is valuable signal but it creates short-term risk if discovered during inspection preparation.

---

## Regulatory basis

| Requirement | Standard | Reference |
|---|---|---|
| Technical documentation | EU MDR | Annex II and Annex III |
| Design history file | FDA 21 CFR 820 | 820.30 and 820.181 |
| Post-market surveillance records | EU MDR | Article 83–86 |
| Quality records retention | FDA 21 CFR 820 | 820.1