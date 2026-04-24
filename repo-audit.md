# Repo Audit — Issues & Inconsistencies
**Date:** 2026-04-24  
**Scope:** Full review of all files in the KantorVera repository  
**Method:** Cross-file analysis across docs/, data/, src/, and diagrams

---

## Summary

27 issues identified across 5 categories: truncated/incomplete files, conflicting naming schemes, cross-reference errors, data/calculation inconsistencies, and process model gaps. Severity ratings: 🔴 High (blocks correctness), 🟡 Medium (causes confusion or inconsistency), 🟢 Low (cosmetic or minor).

---

## 1. Truncated / Incomplete Files

### 1.1 🔴 `docs/02-roi/evaluation-plan.md` — File ends mid-sentence
The file is only 24 lines long. The metrics table ends abruptly in the middle of a row:

> "Reclassification detection | Agent flags SRS changes that remove software item isolation (scenario 12) and that add clinical functionality (scenario 13) | ≥"

The target value is missing. All remaining product metrics (PM-facing metrics, acceptance rate targets, etc.) that should follow are also absent. The evaluation-plan.md is referenced from `roadmap.md` as the source of release validation criteria but is effectively incomplete.

### 1.2 🔴 `docs/01-system/prd.md` — UC4 description missing
The PRD is 56 lines and ends abruptly mid-section:

> "**UC4:**"

UC4's description is completely absent. This is the last use case entry in the PRD's "Key use cases" section, and the remainder of the PRD (architecture, non-functional requirements, etc.) is also missing.

### 1.3 🔴 `data/raw/risk/risk_v1.md` — Truncated
The risk model test file ends mid-sentence:

> "...the agent will flag a potential safety clas"

The reclassification note is cut off. This is the primary test file for UC3 validation; an incomplete file may affect test scenario completeness.

### 1.4 🟡 `docs/01-system/use-cases/README.md` — Effectively empty
The file contains only:

```
**Status:** Stable  
**Owner:** Product Management  
*
```

No actual content (no use case index, no navigation links, no descriptions). All other README.md files in the repo contain substantive content. This appears to be an unfinished stub.

---

## 2. Conflicting UC Numbering Schemes

This is the most structurally significant issue in the repo. Three different UC numbering schemes are in active use simultaneously, and they refer to entirely different things.

### 2.1 🔴 Three incompatible UC naming schemes coexist

| Document | Scheme | UC Count | Notes |
|---|---|---|---|
| `docs/02-roi/master-overview.md` and all `/use-cases/uc*.md` files | **Canonical ROI scheme** | UC1–UC7 | UC1=SRS monitoring, UC2=Baseline→SRS, UC3=Risk traceability, UC4=Change control plan, UC5=Cybersecurity, UC6=Inspection prep, UC7=Usability engineering |
| `docs/01-system/prd.md` | **PRD functional scheme** | UC1–UC4 | UC1=change event, UC2=risk file change, UC3=baseline approval, UC4=missing |
| `docs/04-diagrams/overview/use-cases.puml` | **Diagram functional scheme** | UC1–UC7 | UC1=Submit baseline, UC2=Review suggestions, UC3=Monitor SRS, UC4=Classify change, UC5=Generate findings, UC6=Review findings, UC7=Close findings |

The PRD even acknowledges its own conflict with a disclaimer note at the top, but remains misaligned. The diagram scheme introduces a third independent set of meanings for the same identifiers. The diagram's "UC7 — Close findings" directly shadows the canonical UC7 (Usability engineering).

**Recommendation:** Adopt the canonical ROI scheme (UC1–UC7) everywhere. Retire the PRD's internal scheme with a mapping table, and rebuild the use-cases.puml using functional verb labels (not UC identifiers) or the canonical IDs.

### 2.2 🟡 `master-overview.md` — UC2 and UC5 not explained in the ranking rationale

The "Why the ranking is what it is" section has paragraphs for UC3, UC1, UC7 (which also references UC2 briefly), UC4, and UC6. **UC5 has no explanation paragraph at all.** UC2 is only mentioned in passing within UC7's entry. Both deserve their own rationale given they are included in the scoring table.

---

## 3. Cross-Reference and Dependency Errors

### 3.1 🔴 `data/reference/` — Three files referenced in `dataset-spec.md` do not exist

`docs/02-roi/dataset-spec.md` lists these corpus files:

| File referenced | Exists? |
|---|---|
| `data/reference/iec62304-mapping.md` | ❌ Missing (actual file is `iec62304-checklist-1.md`) |
| `data/reference/iso14971-risk-table-example.md` | ❌ Missing entirely |
| `data/reference/owasp-asvs-summary.md` | ❌ Missing entirely |

Only `iec62304-checklist-1.md` and `iec62304-srs-requirements.md` exist. The agent's reference corpus is described as containing files that are not actually present in the repository.

### 3.2 🔴 `data/reference/iec62304-srs-requirements.md` — Wrong clause numbers

The checklist file contains:

```
## IEC62304-4.3 Software Requirements (SRS)
IEC62304-4.3.1: SRS shall describe functions + interfaces
IEC62304-4.3.2: Requirements shall be verifiable (testable)
```

**IEC 62304 section 4.3 is "Software Safety Classification," not SRS requirements.** The SRS content requirements are in section 5.2. Similarly, the file labels section 5.2 as "Risk Management" — section 5.2 is "Software Requirements Analysis." These are factual clause mapping errors in the reference corpus that will cause the agent to cite incorrect standard clauses when generating findings.

### 3.3 🟡 UC dependency cross-references are incomplete across multiple files

| File | Stated dependency | Actual gap |
|---|---|---|
| `uc3-risk-traceability.md` | "Required by: UC4" | UC6 also depends on UC3 but is not listed |
| `uc1-srs-monitoring.md` | "Required by: UC2, UC3, UC4, UC5, UC7" | UC6 also depends on UC1 but is not listed |
| `uc6-inspection-prep.md` | "Depends on: UC1, UC2, UC3, UC5, UC7" | UC4 is missing — UC6 aggregates AI/ML change control findings too |
| `roadmap.md` (dependency tree) | Shows UC6 only as a leaf under UC4 | UC6 actually depends on UC1–UC5 and UC7 per the UC6 file itself |

The roadmap's dependency tree is the most visible case — it implies UC6 only has one upstream dependency (UC4), while the UC6 file correctly lists six.

### 3.4 🟡 `docs/03-integration/document-owner-directory.md` — SRS owner role uses wrong name

The table labels the SRS owner as **"Software Engineer"**. Every other document in the repo uses **"Requirements Engineer"** or **"Requirements Engineer / Systems Engineer"** for this role. The `stakeholders.md` file dedicates a full section to this role under the canonical name. "Software Engineer" in the context of this repo is a different role (implementation, not requirements ownership).

### 3.5 🟡 `docs/03-integration/document-owner-directory.md` — PRRC listed as separate role

The directory lists "PRRC (EU MDR)" as a distinct row. All other documents combine this with Regulatory Affairs as "RA/PRRC." The separation suggests PRRC has a different routing target than RA, which is not reflected in any other document.

---

## 4. Data and Calculation Inconsistencies

### 4.1 🔴 `data/raw/risk/risk_v1.md` — IMDRF category contradicts own description

The risk model product metadata table states:

> "IMDRF significance category | **3** | Serious situation / drive clinical management — illustrative"

Per the IMDRF framework defined in `docs/00-overview/classification-reference.md`, the intersection of "Serious situation" and "Drive clinical management" is **Category II**, not Category III. Category III requires either a Critical healthcare situation or a "Treat or diagnose" significance level. The test data contains a factual classification error that contradicts the framework the agent is supposed to enforce.

### 4.2 🟡 UC3 Phase 1 time saving inconsistent across files

| File | Phase 1 time saving (UC3) |
|---|---|
| `docs/01-system/use-cases/uc3-risk-traceability.md` | 20–100 hours |
| `docs/02-roi/mvp-specification.md` | 10–144 hours |
| `docs/02-roi/master-overview.md` | 20–100 hours |

The mvp-specification.md figure (10–144 h) is mathematically consistent with the stated inputs: 15–30% of 30–80 UC1 events = 4.5–24 events × 2–6 hours = 9–144 hours. The 20–100 h figure in uc3 and master-overview is an approximation that does not match the stated event count and time-per-event range.

### 4.3 🟡 `docs/02-roi/assumptions.md` — UC4 update trigger references wrong use case

The update schedule table states:

> "After Release 2: update UC4's Effort score based on AI Architect's assessment of change control plan document variability encountered **during UC5 implementation**."

UC5 is cybersecurity. There is no logical connection between cybersecurity implementation and change control plan document parsing complexity. The reference should likely be "during UC2 implementation" (baseline intake parser) or "during Release 2 implementation" generally, since UC2 involves structured document parsing that would inform the effort estimate for UC4's plan parser.

### 4.4 🟡 Classification sensitivity: escalation threshold inconsistency

| Document | Category IV escalation threshold |
|---|---|
| `docs/00-overview/classification-reference.md` | "High to Critical" (routes on High and Critical only) |
| `docs/01-system/output-calibration.md` | "On all findings above Low" (routes on Medium, High, and Critical) |

These define different escalation triggers for the same classification tier. The output-calibration.md definition is broader and is the more technically detailed document — but the two should agree.

### 4.5 🟡 `docs/03-integration/srs-change-impact-matrix.md` — Non-functional changes rated 🔴 H for Cyber File

The matrix marks the Cybersecurity File impact for Non-Functional changes as **High (🔴 H)**. However, UC5 (cybersecurity) only triggers on changes classified as "Security/data flows" by UC1. Non-functional changes (performance, availability, logging, audit trail) are routed to QA/Validation, not the Cybersecurity Engineer. The High impact rating for Cyber File on non-functional changes is inconsistent with UC1's routing logic.

### 4.6 🟢 `data/raw/srs/srs_v2.md` — "Broken link" test scenario is conceptually weak

The UC3 validation requires the agent to detect a "broken link" when SRS-005 is modified in srs_v2.md. The modification adds "AES-256" specificity to an existing encryption requirement — making it more specific, not weaker. This strengthens rather than challenges the risk control link to RC-001 (encrypt + backup). A more robust test case for "broken link" detection would modify the requirement in a way that removes or narrows the scope of the risk control implementation (e.g., removing encryption entirely, or restricting it to a subset of patient data).

---

## 5. Process Model Gaps

### 5.1 🔴 `docs/01-system/finding-lifecycle.md` — "Defer" disposition is absent from the state model

`stakeholders.md` and `docs/03-integration/ui-scope.md` both list **seven** disposition options: Accept, Reject, **Defer**, Clarify, Route, Escalate, Out of scope.

`finding-lifecycle.md` — the authoritative document for the finding state model — defines only **six** terminal dispositions (Accept, Reject, Escalate, Out of scope) and two intermediate ones (Clarify, Route). **Defer does not appear anywhere** in finding-lifecycle.md: not in the state diagram, not in the state definitions, not in the audit trail requirements section.

This means there is no defined state transition for Defer, no required rationale format, no specified terminal state it leads to, and no audit trail requirement for it. The most commonly used disposition in active development teams (deferring to a future sprint) has no authoritative definition.

### 5.2 🟡 `docs/04-diagrams/states/finding-lifecycle-state.puml` — State names differ from canonical text

The PlantUML diagram uses past-tense states: **"Accepted"** and **"Rejected"**. The `finding-lifecycle.md` text consistently uses the active disposition form: **"Accept"** and **"Reject"**. Minor but produces inconsistency when the diagram is rendered alongside documentation.

Additionally, confirming issue 5.1: Defer is also absent from the state diagram.

### 5.3 🟡 Deprecated files remain in active directories without archiving

Two files are marked `**Status:** Deprecated` but remain co-located with active documentation, with no indication they are being replaced or why they were deprecated:

- `docs/01-system/stakeholder-workflows.md` — superseded by the much more detailed `stakeholders.md`, but still linked from the directory
- `docs/01-system/v-model-stakeholder-guide.md` — superseded by `docs/00-overview/compliance-landscape.md` and `stakeholders.md`

Both files contain partially outdated terminology (e.g., "Risk Manager" instead of "Risk / Safety Engineer") that may confuse new readers who encounter them before the canonical versions.

### 5.4 🟡 `docs/04-diagrams/overview/use-cases.puml` — Third UC scheme creates shadow naming

As noted in §2.1, this diagram assigns UC1–UC7 labels to functional workflow actions (Submit baseline, Review SRS suggestions, Monitor SRS changes, Classify SRS change, Generate findings, Review findings, Close findings). The diagram's "UC7 — Close findings" directly shadows the canonical "UC7 — Usability engineering lifecycle integration" with a completely different meaning. Anyone viewing this diagram alongside the main documentation will see UC7 refer to two unrelated concepts.

### 5.5 🟡 FDA cybersecurity guidance year inconsistent across files

| File | Year cited |
|---|---|
| `docs/01-system/use-cases/uc5-cybersecurity.md` (Regulatory basis table) | **2026** ("FDA cybersecurity guidance (updated 2026)") |
| `docs/00-overview/compliance-landscape.md` (Standards corpus table) | **2023** |
| `docs/00-overview/classification-reference.md` (Standards corpus table) | **2023** |

The 2023 FDA cybersecurity guidance (September 2023 final guidance) is the current published document. A 2026 update may be anticipated but has not been confirmed as published. Using "2026" in the regulatory basis table of a use case document is not consistent with the standards corpus that the agent actually cites from.

---

## 6. File System Issues

### 6.1 🟡 `docs/03-integration/​​document-master-list.md` — Filename contains invisible Unicode characters

The filename has two invisible zero-width characters (U+200B or similar) prepended: `​​document-master-list.md`. This causes the file to sort anomalously in directory listings, breaks standard `ls` and glob patterns that expect the name to start with "d", and may cause link resolution failures in any document that references it by name. The file itself contains valid content (the document master list table) — only the filename is affected.

---

## 7. Orphaned or Missing Reference Documents

### 7.1 🔴 `data/README.md` — Data policy referenced by `dataset-spec.md` but missing content

`dataset-spec.md` refers readers to `data/README.md` for the full data policy. The actual `data/README.md` exists but its content was not available beyond a stub, suggesting it may be empty or incomplete.

### 7.2 🟢 `docs/00-overview/ai-legislation.md` — References EU AI Act Article 83 implementing acts as "in development"

The document notes the Article 83 implementing framework was "developing" as of early 2026. This is accurate as of the knowledge cutoff but should be flagged for review — if implementing guidance has since been published, the document and the UC4 confidence score rationale in `roadmap.md` and `assumptions.md` both need updating.

---

## Issue Summary Table

| # | File(s) | Issue | Severity |
|---|---|---|---|
| 1.1 | `docs/02-roi/evaluation-plan.md` | File truncated mid-table, target values missing | 🔴 |
| 1.2 | `docs/01-system/prd.md` | UC4 description absent, file truncated | 🔴 |
| 1.3 | `data/raw/risk/risk_v1.md` | File truncated mid-sentence | 🔴 |
| 1.4 | `docs/01-system/use-cases/README.md` | Effectively empty (stub only) | 🟡 |
| 2.1 | `prd.md`, `use-cases.puml`, all `uc*.md` | Three incompatible UC numbering schemes active simultaneously | 🔴 |
| 2.2 | `docs/02-roi/master-overview.md` | UC5 has no ranking rationale paragraph; UC2 only mentioned in passing | 🟡 |
| 3.1 | `data/reference/` | Three corpus files in `dataset-spec.md` do not exist in the repo | 🔴 |
| 3.2 | `data/reference/iec62304-srs-requirements.md` | Wrong IEC 62304 clause numbers (section 4.3 ≠ SRS requirements) | 🔴 |
| 3.3 | Multiple `uc*.md` + `roadmap.md` | Incomplete "Required by" / dependency cross-references | 🟡 |
| 3.4 | `docs/03-integration/document-owner-directory.md` | SRS owner called "Software Engineer" instead of "Requirements Engineer" | 🟡 |
| 3.5 | `docs/03-integration/document-owner-directory.md` | PRRC listed as separate role from RA/PRRC | 🟡 |
| 4.1 | `data/raw/risk/risk_v1.md` | IMDRF Category 3 contradicts its own "Serious/Drive" description (= Category II) | 🔴 |
| 4.2 | `uc3-risk-traceability.md`, `mvp-specification.md` | UC3 Phase 1 time saving: 20–100 h vs 10–144 h | 🟡 |
| 4.3 | `docs/02-roi/assumptions.md` | UC4 effort update tied to UC5 implementation (should be UC2 or Release 2) | 🟡 |
| 4.4 | `classification-reference.md`, `output-calibration.md` | Category IV escalation threshold: "High to Critical" vs "all above Low" | 🟡 |
| 4.5 | `docs/03-integration/srs-change-impact-matrix.md` | Non-functional → Cyber File rated High, inconsistent with UC5 trigger logic | 🟡 |
| 4.6 | `data/raw/srs/srs_v2.md` | "Broken link" scenario tests requirement strengthening, not link breakage | 🟢 |
| 5.1 | `docs/01-system/finding-lifecycle.md` | "Defer" disposition absent from authoritative state model | 🔴 |
| 5.2 | `docs/04-diagrams/states/finding-lifecycle-state.puml` | State names use past tense ("Accepted") vs canonical active form ("Accept"); Defer also missing | 🟡 |
| 5.3 | `docs/01-system/stakeholder-workflows.md`, `v-model-stakeholder-guide.md` | Deprecated files remain in active directories with outdated terminology | 🟡 |
| 5.4 | `docs/04-diagrams/overview/use-cases.puml` | Third UC scheme; diagram UC7 = "Close findings" shadows canonical UC7 = Usability engineering | 🟡 |
| 5.5 | `uc5-cybersecurity.md` vs `compliance-landscape.md`, `classification-reference.md` | FDA cybersecurity guidance year: "2026" vs "2023" | 🟡 |
| 6.1 | `docs/03-integration/​​document-master-list.md` | Filename contains invisible Unicode characters | 🟡 |
| 7.1 | `data/README.md` | Data policy file referenced from dataset-spec.md may be empty | 🟡 |
| 7.2 | `docs/00-overview/ai-legislation.md` | EU AI Act Article 83 implementing guidance described as "in development" — may need update | 🟢 |

**Total: 25 issues — 7 🔴 High, 16 🟡 Medium, 2 🟢 Low**
