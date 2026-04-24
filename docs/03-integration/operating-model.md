**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect, PM, integration partners

---

# Operating Model

Defines how the SRS Review Agent fits into regulated workflows without becoming a QMS replacement. Covers the product boundary, the working analysis store, the trigger model, the output delivery model, and the system of record.

---

## Product boundary

The agent is a compliance intelligence layer. It analyses controlled documents, generates structured findings, and feeds them into existing workflows. It does not own any authoritative record.

| Layer | Agent responsibility | Outside agent scope |
|---|---|---|
| Ingestion | Sync document snapshots, metadata, and traceability links into the analysis store | Authoritative document storage, approval workflows, signatures |
| Analysis | Detect changes, classify impact, cite standards, calibrate by classification | Final regulatory interpretation, risk acceptability decisions |
| Delivery | Route findings to document owners for review and disposition | Task assignment, CAPA creation, escalation enforcement |
| Evidence | Log analysis rationale, bind findings to source snapshots | Audit trail retention, legal record management |

The agent never becomes the system of record. All dispositions and actions flow back to the authoritative QMS, DMS, and risk management system.

---

## Working analysis store

The agent maintains a dedicated, non-authoritative analysis store — a working replica of the data it needs for analysis. It does not live-query the source systems during analysis runs.

**Why a separate store:** Source systems (eQMS, ALM, DMS) are not optimised for cross-document reasoning. They have inconsistent APIs, variable response times, and access controls that make live querying unreliable for time-sensitive analysis. A dedicated store decouples analysis performance from source system availability.

**What it holds:**
- Document snapshots bound to a specific version and timestamp
- Document metadata: identifier, type, version, status, approval date
- Traceability links: SRS requirement → software item → safety class, risk control → SRS requirement
- Owner directory: document type → responsible role → contact routing
- Classification metadata: IMDRF category per product, software item safety class per item
- Standards reference corpus: clause summaries, checklists, OWASP ASVS

**Sync rules:**
- Every document snapshot is bound to the exact source version at time of sync — the finding always cites which version was analysed
- Sync status is logged: last successful sync time, document count, any failures
- Staleness threshold: 24-hour warning, 7-day hard block (agent halts analysis and flags the issue)
- Manual override available for urgent analysis when sync is stale
- The analysis store is not a backup of the source systems — it is a working cache for analysis only

**What it does not hold:** Approved documents as authoritative records, signatures, CAPA records, training records, or any record that must remain in the QMS for legal or regulatory purposes.

---

## Trigger model

Six trigger types initiate agent analysis. The first two are the most important for Phase 2 value — they enable the agent to operate continuously without manual intervention.

| Trigger type | Source | Frequency | Agent action |
|---|---|---|---|
| Document state change | Document management system | Per event | Full UC1 analysis + UC3 if safety-relevant |
| Baseline approval | Document / requirements system | Per event | UC2 baseline intake + UC3 cross-check |
| Change event (SDLC) | Software development lifecycle system | Per event | UC1 change classification |
| Release candidate | CI/CD or release management system | Per release | Full compliance check across all active use cases |
| Scheduled re-check | Agent scheduler | Weekly or monthly | UC3 traceability validation — detects drift without a new change event |
| Manual submission | Agent UI | Ad hoc | Targeted analysis on demand |

**Trigger priority:** When multiple triggers fire simultaneously for the same product, the agent queues them in the order received and processes sequentially. It does not merge or deduplicate triggers — each event generates its own analysis run and its own finding set.

**Trigger failure handling:** If a trigger cannot be processed (source system unavailable, document not yet synced), the agent logs the failure, retries three times with exponential backoff, and escalates to the system administrator if all retries fail. The finding owner is not notified of trigger failures — only the administrator is.

---

## Output delivery model

Five output types. Each has a defined format, target, and owner.

| Output type | Format | Delivery target | Primary owner |
|---|---|---|---|
| Structured finding | Structured data + rendered summary | Agent UI inbox + notification | Assigned document owner |
| Reclassification flag | Structured finding with mandatory acknowledgement | Agent UI + RA/PRRC notification | RA/PRRC + Software Architect |
| Economic trade-off assessment | Section within a finding | Agent UI | PM + RA/PRRC |
| Change assessment report | Structured export (PDF or JSON) | Agent UI export + QMS change record (Tier 3+) | RA/QA |
| Audit log export | Structured file (JSON or CSV) | Agent UI export + QMS audit trail (Tier 4) | Quality Manager / RA |

**Delivery guarantee:** Every output carries a finding ID, source document binding (document ID, version, sync timestamp), standard clause citation, and an action link. A finding that cannot be delivered is retried and escalated to the administrator if delivery fails after three attempts.

**Reclassification flag special handling:** When the agent detects a potential device-level IMDRF category change or software item safety class change, the reclassification flag is the first finding delivered. No other findings from the same analysis run are surfaced to the document owner until the reclassification flag has received a mandatory acknowledgement. See `docs/01-system/finding-lifecycle.md`.

---

## System of record

The agent is never the system of record. The following table defines which authoritative system owns each type of record.

| Record type | Authoritative system |
|---|---|
| Controlled document | DMS / eQMS document control module |
| Document approval and signature | eQMS |
| Change control decision | QMS change management module |
| Risk management records | Risk management system or eQMS risk module |
| CAPA record | QMS CAPA module |
| Training record | LMS or QMS training module |
| Audit evidence | eQMS audit trail |
| Regulatory submission | Regulatory submission management system |

The agent's audit log (finding history + dispositions) is not the QMS audit trail — it is a compliance intelligence record that must be exported and incorporated into the QMS audit trail at appropriate intervals. Until a Tier 4 integration is in place, this export is a manual step performed by the Quality Manager or Regulatory Affairs specialist.

---

## Integration tiers

Five tiers of integration depth. The agent is designed to operate at any tier — teams start where their infrastructure allows and move to higher tiers as integration work is completed.

| Tier | Description | What it enables | Build effort |
|---|---|---|---|
| 0 — Manual | File upload and download through the UI | Full analysis capability; manual trigger submission | None |
| 1 — Read sync | Scheduled pull from source systems into the analysis store | Automatic document refresh; no manual uploads for synced systems | Low–Medium |
| 2 — Event trigger | Webhook or event push from source systems | Automatic trigger on document state change; near-real-time analysis | Medium |
| 3 — Handoff | Agent creates tasks or references in workflow system | Findings delivered directly into the team's existing task workflow | High |
| 4 — Bidirectional | Full sync including disposition sync-back to QMS | Dispositions recorded in both the agent and the QMS simultaneously | Very high |

**Recommended deployment path:** Tier 0/1 for the initial release → Tier 2 for core event-driven operation → Tier 3 for selected high-value workflows. Tier 4 should be evaluated after Tier 3 is stable — the complexity of disposition sync-back is significant and requires careful data model alignment with the target QMS.

**Tier 0 is a permanent valid option** for low-frequency analysis needs (for example, pre-submission gap checks) even for teams that use higher tiers for ongoing monitoring.

---

## Decision workflow — illustrative example

This example shows the end-to-end flow for a document state change event. It is illustrative — the specific systems involved depend on the team's tooling and integration tier.

1. **Trigger:** SRS document transitions to "In Review" state in the document management system
2. **Ingestion:** The event receiver detects the state change and initiates a sync of the SRS and its linked documents into the analysis store
3. **Analysis:** The agent runs UC1 (change classification) and UC3 (risk traceability check) against the updated snapshot
4. **Delivery:** Findings are delivered to the document owner's inbox in the agent UI; if Tier 3 is configured, a task is also created in the workflow system
5. **Disposition:** The document owner reviews each finding and records a disposition with rationale
6. **Evidence:** The finding + disposition is logged in the agent's audit log; if Tier 4 is configured, the disposition is synced back to the QMS change record
7. **Resolution:** The finding moves to Resolved or Closed state and the audit log entry is complete

**Target cycle time:** Trigger to finding delivery in under 5 minutes for a standard SRS document. Larger documents or complex traceability queries may take longer — the UI shows analysis-in-progress status to the document owner.

---

## Operational health metrics

| Metric | Target |
|---|---|
| Sync success rate | ≥99% of scheduled syncs complete without error |
| Trigger-to-delivery latency | <5 minutes for standard documents |
| Finding delivery success rate | 100% — all generated findings reach their assigned owner |
| Staleness incidents | Zero documents in hard-block state without administrator notification |
| Audit log completeness | 100% of findings and dispositions logged with all required fields |
