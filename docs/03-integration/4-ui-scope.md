# UI Scope — SRS Review Agent

**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect, PM, integration partners, deployment teams

---

## Purpose of this document

This document defines exactly what the agent's own user interface does, what it does not do, and where the boundary lies between the UI and the systems it integrates with. It is a constraint document as much as a specification document — the boundaries are as important as the features.

The UI exists to handle what integrated systems do not yet handle, and to make the agent usable for teams at any integration tier — from a team with no system integration (Tier 0, manual file upload) to a team with full bidirectional integration (Tier 4, disposition sync-back to the QMS). The UI must scale gracefully across all tiers without duplicating what the integrated systems already do.

---

## The three jobs of the UI

The UI has exactly three responsibilities. Everything else belongs to an integrated system or to a human workflow outside the agent.

### Job 1 — Manual input fallback (Tier 0 and Tier 1 gaps)

When a team does not have an automated integration to a source system, the UI provides the manual path to get data into the agent.

**Document upload.** A user uploads a document file directly through the UI. The UI assigns an internal document identifier, a version label, a document type classification, and a timestamp. The uploaded document is ingested into the analysis store and treated identically to a document that arrived via an automated sync.

**Change event submission.** A user manually submits a change event by selecting a document, specifying the type of change, and optionally providing a change description. The agent uses this as its analysis trigger.

**Metadata entry.** Two metadata fields are required for classification-calibrated output: the **IMDRF significance category** of the device (I, II, III, or IV) and the **IEC 62304 safety class** of each software item referenced in the SRS (A, B, or C). The UI provides a structured form for a qualified user to enter these when they are not available from an integrated source system. The form includes inline definitions and requires a confirmation that the entry represents a documented classification decision.

**Traceability table entry.** For teams without an integrated requirements or risk management system, the UI provides a structured interface to enter the core traceability links the agent needs: SRS requirement ID → software item ID → software item safety class, and risk control ID → SRS requirement ID. This is not a full requirements management interface — only the linking tables the agent reads.

**What the UI does not provide for input:** a full document editor, a requirements management interface, a risk table editor, or any capability that duplicates what the integrated source systems already do.

---

### Job 2 — Finding review and disposition

**Finding inbox.** A user sees all findings assigned to their role, sorted by severity and date. Each finding shows: finding ID, use case, source document and version, change or gap detected, standard clause cited, severity level, and recommended action.

**Classification context.** Each finding shows the IMDRF category and software item safety class that produced it, so the reviewer understands why the finding has the severity it does.

**Disposition.** For each finding, the reviewer selects:

| Disposition | Meaning | Required input |
|---|---|---|
| Accept | Finding is valid, action will be taken | Rationale (one sentence minimum) |
| Reject | Finding is not applicable | Rationale (mandatory) |
| Defer | Valid but addressed later | Target date or milestone |
| Clarify | Needs more information | Question or clarification request |
| Route | Belongs to a different owner | Target role or person |
| Escalate | Requires attention above normal review level | Escalation reason |
| Out of scope | Outside the current review boundary | Brief explanation |

All dispositions are logged with: finding ID, disposition state, reviewer identity, timestamp, and rationale. This log is immutable once written.

**Reclassification findings — special handling.** When a finding includes a reclassification flag (the analysis has detected that a SRS change may affect the software item safety class or device IMDRF category), the UI presents a mandatory acknowledgement step before any other disposition is available. The reviewer confirms the reclassification as valid (generating a mandatory escalation to Regulatory Affairs / PRRC) or rejects it with a documented rationale.

**Economic trade-off assessments.** When a finding includes a trade-off assessment (the full regulatory cost of a proposed change), the UI presents this as a distinct section within the finding. It informs the disposition but does not change the disposition options.

**What the UI does not provide for dispositions:** the ability to edit a finding's content (findings are immutable), the ability to create a CAPA or change control record, or the ability to mark a document as approved.

---

### Job 3 — Configuration and monitoring

**Product registry.** List of products under analysis, each with: product name, internal ID, IMDRF significance category, applicable regulatory markets, and active use cases.

**Software item registry.** For each product, the list of software items with: item identifier, name, IEC 62304 safety class, and isolation argument. Maintained in the UI when not available from an integrated system; read-only when imported.

**Document owner directory.** Mapping of document types to responsible roles and individuals. Used by the agent to route findings.

**Analysis store status.** Dashboard showing sync health: last sync time, document count, staleness warnings (24h warning, 7d hard block), sync errors.

**Integration configuration.** Connection parameters for each integration tier. Accessible to system administrators only. Does not store credentials — these are managed by the deployment environment.

**Audit log access.** Searchable, read-only view of all findings and dispositions. Filterable by product, use case, document, date, reviewer, and disposition state. Exportable as a structured file for QMS import or regulatory inspection preparation.

---

## What the UI must never do

| Prohibited capability | Why |
|---|---|
| Approve or reject a controlled document | Document approval belongs to the DMS / eQMS |
| Create a change control record | Change control belongs to the QMS change module |
| Update a risk table entry | Risk records belong to the risk management system |
| Create a CAPA | CAPA belongs to the QMS CAPA module |
| Generate a regulatory submission package | Submissions require regulatory affairs oversight |
| Assign a training requirement | Training belongs to the LMS / QMS training module |
| Override a finding's citation | Findings are immutable — disagreement is recorded in the disposition rationale |
| Store a document as the authoritative version | The analysis store is non-authoritative by design |
| Send a regulatory notification to an authority | Any regulatory communication is entirely outside the agent's scope |

---

## Input handling by integration tier

| Input type | Tier 0 (manual) | Tier 1 (sync) | Tier 2 (events) | Tier 3–4 (full) |
|---|---|---|---|---|
| Document content | UI upload | Auto-synced | Auto-synced | Auto-synced |
| Document metadata | UI form | Auto-synced | Auto-synced | Auto-synced |
| IMDRF category | UI form (mandatory) | Auto-synced if available | Auto-synced if available | Auto-synced |
| Software item safety class | UI form (mandatory) | Auto-synced from SAD | Auto-synced from SAD | Auto-synced |
| Traceability links (SRS → item) | UI form | Auto-synced from ALM | Auto-synced | Auto-synced |
| Risk control links (RC → SRS) | UI form | Auto-synced from risk system | Auto-synced | Auto-synced |
| Change event trigger | UI manual submit | Scheduled check | Webhook / event push | Webhook / event push |
| Baseline approval event | UI manual submit | Polling check | Event push | Event push |

---

## Output handling by integration tier

| Output type | Tier 0 (manual) | Tier 1 (sync) | Tier 2 (events) | Tier 3–4 (full) |
|---|---|---|---|---|
| Structured finding | UI inbox | UI inbox | UI inbox + email | UI inbox + task in workflow system |
| Reclassification flag | UI inbox (mandatory acknowledgement) | Same | Same + escalation notification | Same + task with mandatory routing |
| Trade-off assessment | Within finding in UI | Same | Same | Same |
| Change assessment report | UI export (PDF / structured file) | UI export | UI export | Auto-pushed to QMS change record |
| Pre-submission readiness report | UI export | UI export | UI export | Auto-pushed to submission system |
| Audit log export | UI export (manual) | UI export | UI export | Auto-synced to QMS audit trail |
| Disposition sync-back | Not available | Not available | Not available | Auto-synced to QMS / workflow system |

---

## UI screens — summary

**Initial release (UC1 + UC3):**

| Screen | Primary user | Purpose |
|---|---|---|
| Finding inbox | All document owners | Review and disposition of findings |
| Finding detail | All document owners | Full finding, citation, classification context, disposition form |
| Document upload | PM / QA / RA | Manual Tier 0 document ingestion |
| Change event submission | PM / QA / RA | Manual Tier 0 trigger |
| Metadata entry — IMDRF category | RA / PRRC | Set or confirm device classification per product |
| Metadata entry — software item registry | Software Architect / QA | Set or confirm software item safety classes |
| Traceability table entry | Risk Engineer / QA | Enter SRS → item and RC → SRS links manually |
| Product registry | PM / Admin | Manage products under analysis |
| Analysis store status | Admin | Monitor sync health and staleness |
| Audit log | RA / QA / Admin | Search and export finding and disposition history |

**Release 2 additions (UC2 + UC5 + UC7):**

| Screen | Primary user | Purpose |
|---|---|---|
| Baseline submission | Document owners | Submit approved baseline for UC2 processing |
| Usability study submission | Usability / HF specialist | Submit formative or summative study result for UC7 |
| Post-summative change flag | RA / PRRC | Review and acknowledge SRS changes after a summative study |
| Integration configuration | Admin | Configure Tier 1–3 connection parameters |
| Document owner directory | Admin / PM | Maintain routing rules for finding delivery |

**Release 3 and later (not in initial scope):**

| Screen | Notes |
|---|---|
| Change control plan boundary review | UC4 — PCCP / Article 83 boundary analysis for AI/ML changes |
| Trade-off assessment dashboard | Aggregated change cost estimates across multiple use cases |
| Pre-submission readiness report | UC6 — requires 6+ months of findings history |

---

## Success criteria for the UI

- 100% of findings accessible through the UI within five minutes of generation.
- 80% of findings receive a disposition within the agreed review cycle time.
- Zero instances of the UI being used to perform an action in the "must never do" list.
- All Tier 0 teams can complete a full analysis cycle without requiring AI Architect support.
- Audit log exports are accepted by the QMS without manual reformatting.
