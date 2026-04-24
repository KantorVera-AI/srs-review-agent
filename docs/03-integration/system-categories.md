**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect, integration partners

---

# System Categories

Defines the data contracts between the agent and each category of system a regulated SaMD team operates. Organised by system category, not by vendor or product name — the specific tools a team uses vary; the data the agent needs from each category does not.

For each category: what the agent needs from it, what events trigger analysis, what the agent sends back, and the recommended integration tier.

---

## Cross-cutting metadata fields

Two metadata fields must be present across all categories before the agent can produce classification-calibrated outputs. They are highlighted wherever they appear in the category descriptions below.

**Field 1 — IMDRF significance category (product level)**
- Format: integer 1–4
- Source: intended use document or regulatory classification rationale
- Lives in: document management system or directly in the agent's product registry
- Required by: every use case

**Field 2 — IEC 62304 software item safety class (item level)**
- Format: string A, B, or C — one value per software item
- Source: Software Architecture Document (SAD), maintained by the Software Architect
- Lives in: requirements and traceability management system (linked to item records) or directly in the agent's software item registry
- Required by: UC1, UC3, UC7 — and all use cases that generate classification-calibrated findings

If either field is absent or unstructured, see `metadata-spec.md` for fallback behaviour and the tagging specification.

---

## Category 1 — Document and quality management systems

**What these systems hold:** Authoritative versions of controlled documents, approval states, revision histories, document type classifications, and relationships between documents (for example, the link between a risk management file and the SRS it covers).

**What the agent needs:**
- Document identifier (stable, unique per document)
- Document type classification (SRS, risk management file, usability engineering file, etc.)
- Version number or revision label
- Approval / status timestamp
- Links to related documents (parent and child relationships)
- **IMDRF significance category** — from the intended use document or classification rationale record

**What triggers analysis:**
- Document status transition (draft → review, review → approved, approved → obsolete)
- New version submitted for review
- Document marked as superseded

**What the agent sends back:**
- Finding notifications (Tier 2+)
- Audit log export for incorporation into the QMS audit trail (manual at Tier 0–3; automatic at Tier 4)
- Change assessment report (Tier 3+)

**Recommended integration tier:** Tier 1 for document sync; Tier 2 for event-driven triggers. This is the highest-priority integration category — without it, the agent cannot detect document change events automatically.

---

## Category 2 — Requirements and traceability management systems

**What these systems hold:** Software requirements with stable identifiers, their linkage to software items in the architecture, and traceability to test cases, risk controls, and design outputs. This is where the SRS lives in its most structured form.

**What the agent needs:**
- Requirement identifier (stable, unique — e.g. SRS-045)
- Requirement text (current version)
- Requirement status (draft, approved, deprecated)
- Linked software item identifier (e.g. SI-003)
- **IEC 62304 software item safety class** — attached to the software item record
- Baseline version of the requirements set (for UC2 baseline intake)
- Traceability links: requirement → test case, requirement → risk control

**What triggers analysis:**
- Requirement status change
- New requirement added
- Requirement modified (text or linked item changed)
- Baseline approved or released

**What the agent sends back:**
- SRS suggestions (UC2 — delivered as a suggestion set, not directly written to the system)
- Finding notifications for requirements with gaps (Tier 2+)

**Recommended integration tier:** Tier 1 for requirements sync; Tier 2 for change event triggers. Second-highest priority integration category after document management — UC3 cannot function without access to the traceability links this category holds.

**Note on software item safety class:** The safety class must be attached to the software item record in this system, not just described in the SAD narrative document. If the requirements system does not support item-level metadata fields, the software item registry in the agent's UI is the fallback.

---

## Category 3 — Risk management systems

**What these systems hold:** The full ISO 14971 chain — hazards, hazardous situations, harms, probability and severity estimates, risk controls, residual risk assessment, and the traceability from risk controls to SRS requirements.

**What the agent needs:**
- Hazard identifier (e.g. H-001)
- Risk control identifier (e.g. RC-001)
- SRS requirement identifier(s) implementing each risk control
- Risk control status (open, implemented, verified)
- Risk management file version and approval status

**What triggers analysis:**
- Risk control status change
- New hazard or risk control added
- Risk management file version updated

**What the agent sends back:**
- Risk traceability findings (UC3) — routed to the Risk Engineer
- Reclassification flag when a SRS change affects the safety class of an item linked to a risk control

**Recommended integration tier:** Tier 1 for risk data sync. Risk management systems often have limited API capability — if structured export is not available, the risk-to-SRS traceability table can be maintained manually through the agent's traceability table entry UI (Tier 0).

**Critical dependency:** The risk-to-SRS traceability table (RC-NNN → SRS-NNN mapping) must be current for UC3 to produce accurate findings. A stale traceability table produces false negatives — the agent does not flag gaps that actually exist.

---

## Category 4 — Software architecture and design documentation

**What these systems hold:** The decomposition of the software system into items, the interfaces between items, the IEC 62304 safety class assigned to each item, and the isolation argument that justifies any class lower than the overall device's implied class.

**What the agent needs:**
- Software item identifier (e.g. SI-003)
- Software item name and description
- **IEC 62304 safety class** (A, B, or C) per item
- Isolation argument — what architectural mechanism justifies the assigned class
- Interfaces between items (which items communicate with which)

**What triggers analysis:**
- Architecture document updated (new item added, interface modified, safety class changed)

**What the agent sends back:**
- Reclassification flag when a SRS change may affect the isolation argument of a software item

**Recommended integration tier:** Tier 0 or Tier 1. Architecture changes are infrequent — scheduled sync is sufficient. This category often exists as a structured document rather than a database, which limits API capability. The software item registry in the agent's UI is the primary fallback.

**Note:** This is the category from which the IEC 62304 software item safety class metadata originates. If this category is not integrated, the Software Architect must maintain the software item registry manually through the agent's UI before classification-calibrated findings are available.

---

## Category 5 — Software development lifecycle systems

**What these systems hold:** Source code repositories, issue tracking, and CI/CD pipelines. These provide the highest-frequency change events in the development environment.

**What the agent needs:**
- Change event identifier (commit, review request, or equivalent)
- Associated document or requirement identifier (where the change is linked to an SRS requirement)
- Change state (open, under review, merged, released)

**What triggers analysis:**
- New change event linked to an SRS requirement or controlled document
- Release candidate marked for deployment

**What the agent sends back:**
- Finding notifications for changes affecting controlled documents (Tier 2+)

**Recommended integration tier:** Tier 2 for event-driven triggers. This category provides the most granular change event stream — use it to trigger UC1 analysis when SRS requirements are managed alongside source code. For teams where SRS lives only in the document management system, this category is lower priority.

---

## Category 6 — Usability and human factors documentation

**What these systems hold:** Formative and summative usability study plans and results, use error logs, and user interface specifications. This category is almost always document-based rather than database-based.

**What the agent needs:**
- Study type (formative or summative)
- Study completion status and approval date
- Use error log (structured list of use errors with identifiers where possible)
- Affected SRS requirement or user interface element per use error
- Summative study baseline version (for post-summative monitoring)

**What triggers analysis:**
- Formative study result submitted (manual submission through UI)
- Summative study approved and baselined (via UC2 baseline intake)
- Any SRS change after a summative baseline (detected by UC1 — triggers UC7 check)

**What the agent sends back:**
- Formative use error findings (UC7 Trigger 1) — routed to Requirements Engineer and Risk Engineer
- Post-summative change flags (UC7 Trigger 3) — routed to Usability/HF Specialist and RA/PRRC

**Recommended integration tier:** Tier 0 for study submissions (manual upload). The structured data the agent needs is typically not available in a queryable format — study results are submitted as documents. Extraction quality depends on document structure.

---

## Category 7 — Cybersecurity and threat management systems

**What these systems hold:** Threat model, SBOM (software bill of materials), vulnerability tracking records, and security risk assessments.

**What the agent needs:**
- Threat identifier and description
- Affected interface or data flow per threat
- Mitigating SRS requirement identifier per threat
- SBOM component list with versions
- Vulnerability records for SOUP components (CVE identifiers and affected versions)

**What triggers analysis:**
- Threat model updated (new interface or data flow added)
- SBOM component version change
- New vulnerability disclosure affecting an SOUP component in the SBOM

**What the agent sends back:**
- Security findings (UC5) — routed to Cybersecurity Engineer
- Reclassification flag if a new interface affects a previously isolated software item

**Recommended integration tier:** Tier 0 or Tier 1. Threat model format varies widely — structured tables enable automated correlation; narrative threat models require manual extraction. SBOM can typically be exported as a structured file (SPDX or CycloneDX format).

---

## Category 8 — Post-market surveillance and complaint management systems

**What these systems hold:** Field safety data, complaints, incident reports, PSUR data, and CAPA records.

**What the agent needs:**
- Complaint or incident identifier
- Associated device function or SRS requirement (where established)
- CAPA status and link to corrective action

**What triggers analysis:**
- Complaint or incident linked to a specific SRS requirement (triggers a change impact assessment for that requirement)

**What the agent sends back:**
- Change impact findings routed to Risk Engineer and RA/PRRC (future — backlog candidate, not in current release scope)

**Recommended integration tier:** Tier 0 or Tier 1. This category is a backlog integration candidate — not required for the initial release or Release 2. The data contracts are defined here for planning purposes.

---

## Category 9 — Workflow and task management systems

**What these systems hold:** Tasks, tickets, queues, and work items. This category is the primary delivery target for agent findings — it is where document owners manage their work.

**What the agent needs from it:** Nothing for analysis. This category is an output target, not an input source.

**What the agent sends to it:**
- Finding notifications as tasks or tickets (Tier 3)
- Disposition sync-back (Tier 4 — the workflow system records dispositions that are synced back to the agent's audit log)

**What triggers analysis:** Nothing — this category does not trigger agent analysis.

**Recommended integration tier:** Tier 3 for finding delivery. This is the integration that delivers the most visible workflow improvement for teams — findings appear directly in the tool the team already uses for daily work. Prioritise after Tier 1/2 integrations for document management and requirements systems are stable.

---

## Category 10 — Regulatory submission management systems

**What these systems hold:** Submission history, deficiency letters, regulatory correspondence, and submission status records.

**What the agent needs:**
- Submission identifier and status
- Deficiency letter content (for UC6 inspection preparation)
- Submission date and regulatory decision date

**What triggers analysis:** Nothing ongoing. This category is used on demand for UC6 (inspection and submission preparation) — the agent queries it when generating a pre-submission readiness package.

**What the agent sends back:** Nothing — this category is read-only for the agent.

**Recommended integration tier:** Tier 0 or Tier 1. Low integration priority — relevant primarily for UC6 which is in the Later release tier.

---

## Integration priority summary

| Priority | Category | Use cases enabled | Recommended tier |
|---|---|---|---|
| 1 | Document and quality management | UC1, UC2, UC3, UC6 | Tier 1 sync → Tier 2 events |
| 2 | Requirements and traceability | UC1, UC2, UC3 | Tier 1 sync → Tier 2 events |
| 3 | Risk management | UC3 | Tier 1 sync |
| 4 | Workflow and task management | All (finding delivery) | Tier 3 handoff |
| 5 | Software architecture and design | UC1, UC3 (reclassification) | Tier 0/1 |
| 6 | Software development lifecycle | UC1 | Tier 2 events |
| 7 | Usability and human factors | UC7 | Tier 0 (manual submission) |
| 8 | Cybersecurity and threat management | UC5 | Tier 0/1 |
| 9 | Post-market surveillance | Future | Tier 0/1 (backlog) |
| 10 | Regulatory submission management | UC6 | Tier 0/1 |
