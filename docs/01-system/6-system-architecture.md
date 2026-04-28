**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect, integration partners, RA/QA consultants

---

# System Architecture

This document is the consolidated technical architecture for the SRS Review Agent. It binds the operating model (`../03-integration/1-operating-model.md`), the system categories (`../03-integration/2-system-categories.md`), the metadata specification (`../03-integration/3-metadata-spec.md`), the output calibration (`4-output-calibration.md`), and the finding lifecycle (`5-finding-lifecycle.md`) into one technology recommendation and one phased buildout sequence.

The labels used in this document are technology-neutral. Concrete product recommendations live in section 12 ("Component selection — concrete recommendations"). They are recommendations, not constraints — any component that satisfies the data contract for its layer is acceptable.

---

## 1. Architectural principles

The architecture follows eight principles. They are not negotiable — every component decision must trace to one or more of them.

1. **One validation target wherever possible.** Each additional engine in the data layer multiplies GAMP 5 validation effort. Prefer one database that covers relational, graph, and vector needs over three specialised engines.
2. **The agent is never the system of record.** All authoritative records live in the team's QMS, DMS, and risk management system. The agent's analysis store is a working cache (see operating-model section "Working analysis store"). The agent's audit log is a compliance intelligence record, not a QMS audit trail replacement.
3. **The agent does not hold version history of source documents.** Each analysis ingests one input pair: the current document version and the diff against the previous version. Older versions live in the DMS and are not replicated into the agent. Per-run snapshots retained inside the agent are reproducibility artefacts, not a document archive (see section 3.4).
4. **Tier 0 must work standalone.** The architecture must support full UC1 + UC3 functionality with manual file upload only — no external integrations required. Higher tiers add convenience and event-driven operation, never new capabilities.
5. **Calibration is data, not code.** The IMDRF × safety class matrix in `4-output-calibration.md` is implemented as a configuration file (versioned in source control), not hardcoded logic. The same applies to severity floors, routing rules, and reclassification triggers.
6. **Every output is reproducible.** Each finding can be regenerated bit-for-bit from its source binding (analysed-version content hash + diff hash + model version + prompt version + reference corpus version + calibration config version). See section 10.
7. **Append-only audit log, separately protected.** The audit log lives in its own logical store with restricted permissions, no UPDATE or DELETE grants, and independent backup. Its integrity is the most important non-functional property of the system.
8. **Findings never auto-write to the system of record.** Findings flow to the agent UI and (at Tier 3) to the workflow system. Disposition sync-back to the QMS (Tier 4) is an explicit, controlled write — not a silent one.

---

## 2. The layer model

The agent decomposes into seven layers. Each layer has a defined input contract, a defined output contract, and a single responsibility.

| Layer | Responsibility | Reads | Writes |
|---|---|---|---|
| 1. Trigger receiver | Detect events, queue analysis runs | External webhooks, scheduler, UI submissions | Analysis run queue |
| 2. Ingestion | Sync source content into the analysis store, normalise to canonical schema | Source systems (Tier 1+) or UI uploads (Tier 0) | Analysis store |
| 3. Analysis store | Hold the current document snapshot, traceability links, classification metadata, and per-run reproducibility snapshots | Ingestion layer | Read-only to analysis engines |
| 4. Reference corpus | Hold standards content for citation retrieval | Manual ingestion + scheduled refresh | Read-only to analysis engines |
| 5. Analysis engines | Run UC1–UC7 logic, generate findings | Analysis store + reference corpus + LLM | Finding store |
| 6. Finding store | Hold findings, dispositions, audit log | Analysis engines + UI dispositions | UI + export |
| 7. Delivery | Route findings to inboxes, workflow system, exports | Finding store | UI, Tier 3+ workflow systems |

This layering is the basis for the C4 container diagram referenced in `../04-diagrams/architecture/2-c4-container.puml`.

---

## 3. The data layer — analysis store

The analysis store is the working cache the agent uses for cross-document reasoning. It is **not authoritative**: every record is a snapshot bound to a source version with a sync timestamp.

### 3.1 What it holds

The analysis store contains six distinct logical models. They are presented separately for clarity but should live in one engine for validation simplicity (principle 1).

| Logical model | Contents | Volume profile |
|---|---|---|
| Current document snapshot | The latest analysed version of each in-scope document, with metadata and source-version reference | Bounded — one record per active document; old versions are NOT retained |
| Incoming change input | The current version plus the diff against the previous version, supplied at trigger time | Transient — discarded after the run, reduced to a content-hash retained in the run record |
| Canonical entity model | Requirement, Hazard, RiskControl, IntendedUseStatement, SoftwareItem, ClassificationClaim, TestCase, ThreatModelEntry, UseError | Bounded — reflects the current state, replaced on each successful ingest |
| Traceability links | Typed edges between current canonical entities | Bounded — reflects current state |
| Classification metadata | Product registry (IMDRF category) + software item registry (safety class + isolation argument) | Low volume, infrequent changes |
| Run snapshots (reproducibility artefacts) | Per-run minimal snapshot — content hashes of analysed input, the canonical entities derived from it, and the configuration used at run time | Append-only, retention-bounded (see section 3.4) |
| Run records | One per analysis run: input hashes, model version, prompt version, output finding IDs | Append-only |

The agent therefore stores **the current state plus per-run reproducibility snapshots** — not a continuous archive of every previous document version. Version history is the DMS's responsibility (principle 3).

### 3.2 Why one engine

Three options were considered: (a) a polyglot stack with a relational store, a graph database, and a vector store; (b) a single multi-model engine; (c) a relational store extended with graph and vector capabilities.

Option (c) is recommended. It satisfies principle 1 (one validation target), provides mature backup and HA tooling, has the longest qualification track record in regulated environments, and supports both the recursive traceability queries that UC3, UC6, and UC7 require and the semantic search that UC1, UC2, and UC5 need. Pure graph databases were rejected because they require a separate vector engine and add a second validation target. Document/key-value stores were rejected because the canonical model is highly relational.

### 3.3 Canonical entity model

The canonical schema is defined as YAML in source control (`/schemas/canonical/v{N}.yaml`) and is the contract that all ingestion adapters target. Every record cites the schema version it was validated against.

Core node types and required fields. Each entity carries a `source_run_id` and `source_version_label` — pointing to the run that ingested it and the DMS-supplied version label of the document it came from. The agent does not store prior versions of these entities; on each successful ingest the canonical state is replaced.

```
Document               id, type, current_version_label, source_system_ref
Requirement            id, text, status, source_run_id, source_version_label, software_item_id
Hazard                 id, description, severity, probability, source_run_id
RiskControl            id, description, control_type, status, source_run_id
IntendedUseStatement   id, text, scope, source_run_id
ClassificationClaim    id, dimension, value, source_run_id
SoftwareItem           id, name, safety_class, isolation_argument, sad_reference
TestCase               id, description, requirement_id, status
ThreatModelEntry       id, threat_description, affected_interface, mitigating_requirement_id
UseError               id, description, study_id, study_type, requirement_id
StandardClause         id, standard, clause, summary_text, source_url_or_doc
Finding                see section 7
```

Core edge types:

```
(Requirement)-[:INGESTED_BY]->(RunRecord)
(Requirement)-[:IMPLEMENTS]->(RiskControl)
(Requirement)-[:DERIVES_FROM]->(IntendedUseStatement)
(Requirement)-[:VERIFIED_BY]->(TestCase)
(Requirement)-[:GOVERNS]->(SoftwareItem)
(Requirement)-[:AFFECTS_CLASSIFICATION]->(ClassificationClaim)
(RiskControl)-[:MITIGATES]->(Hazard)
(SoftwareItem)-[:INTERFACES_WITH]->(SoftwareItem)
(ThreatModelEntry)-[:MITIGATED_BY]->(Requirement)
(UseError)-[:MAPS_TO_HAZARD]->(Hazard)
(UseError)-[:OBSERVED_IN]->(SummativeStudy)
(any)-[:CITES]->(StandardClause)
```

Schema evolution is a controlled change. New fields require a schema version bump, a migration script, and review by RA/QA before production rollout.

### 3.4 Run snapshots and reproducibility (replaces "baseline storage")

The agent does not maintain a long-term baseline archive. It receives one input pair per analysis run — the current document version plus the diff against the previous version — and produces one **run snapshot**: a minimal, immutable record of exactly what was analysed and how, sufficient to regenerate the resulting findings bit-for-bit.

A run snapshot contains:

- Content hash of the analysed document (current version as supplied)
- Content hash of the diff input (the diff against the previous version, as supplied)
- Hashes of the derived canonical entities (Requirement, Hazard, RiskControl, etc) at run time
- The configuration set used: schema version, calibration config version, prompt template version, reference corpus version, LLM model and revision, embedding model and revision
- Timestamps and run-id

A run snapshot is **not** a copy of the document. It is the minimal evidence package that proves "given this input and this configuration, these findings were produced." The original document text, where retained, is held only as long as needed for review of the resulting findings. Retention period is configurable per product and aligned to the team's QMS retention policy.

When a finding needs to be regenerated for audit purposes, the agent can:

1. Re-run with the same inputs (if the original document is still available, either in the agent's short-term store or fetched from the DMS) and verify the output hashes match the recorded run.
2. Or, if the document is no longer available, present the run snapshot as the evidence — showing exactly which configuration produced the finding even though the input cannot be re-supplied.

This separation ensures the agent does not duplicate the DMS's role as long-term version archive while preserving full traceability and reproducibility for every finding it generates.

---

## 4. The reference corpus

The reference corpus is the agent's standards knowledge. It is **product-agnostic** and **separately versioned** from the analysis store.

### 4.1 What it holds

| Standard / framework | Content |
|---|---|
| IEC 62304:2006 + A1:2015 | Clause summaries for sections 5, 6, 7, 8, 9 |
| ISO 14971:2019 | Clause summaries for sections 4 through 10 |
| IEC 81001-5-1:2021 | Lifecycle activity clause summaries (paid standard — summaries only) |
| IEC 62366-1:2015 + A1:2020 | Usability engineering clause summaries |
| OWASP ASVS v4.0 | Full structured checklist (open licence) |
| EU MDR | GSPR text (Annex I), Article 83, Annex II–III references |
| EU AI Act | Article 14 (human oversight), Article 15 (accuracy/robustness), Article 83, Annex IV |
| FDA guidance | 21 CFR 820.30, cybersecurity guidance, PCCP guidance |
| IMDRF guidance | SaMD significance categorisation framework |

For each standard, the corpus stores: the clause identifier, a structured summary, embedding vector, source URL or document reference, and the corpus version that ingested it. Where the standard is a paid normative text (IEC 62304, IEC 81001-5-1, IEC 62366-1) only summaries derived from publicly available mapping tables and the team's internal copies are stored — the agent does not reproduce the normative text.

### 4.2 Refresh cadence

Standards update infrequently but not never. The corpus is versioned (`corpus-v{N}`) and a refresh is a controlled change with an explicit changelog entry. Every finding cites the corpus version it used.

### 4.3 Why a separate corpus

The reference corpus has different characteristics from project data: low volume, slow change, product-agnostic, mostly read-only, and used in the retrieval phase of every finding. Keeping it logically separate prevents accidental cross-contamination (a project document accidentally being cited as a standard), allows independent backup and refresh schedules, and makes corpus version pinning trivially auditable.

---

## 5. The classification & calibration engine

This engine is the agent's most precision-critical component. Its job is twofold.

### 5.1 Change classification (UC1)

Given a document delta, classify each change into one or more of the six change types (clinical, risk/safety, UI/workflow, security/data flows, AI/ML behaviour, non-functional) and detect reclassification triggers.

Recommended hybrid implementation:

| Stage | Mechanism | Purpose |
|---|---|---|
| 1. Rule-based pre-filter | Keyword + structural heuristics over the diff | Catch clear, deterministic signals (e.g. any change touching a requirement linked to an interface → security/data flows candidate) |
| 2. LLM classification | Structured-output LLM call with the change text + relevant context | Disambiguate, classify multi-type changes, provide rationale |
| 3. Confidence scoring | Aggregate rule-based and LLM signals | Flag low-confidence classifications for human review |
| 4. Reclassification check | Pattern match against the device-level and item-level criteria in `4-output-calibration.md` | Generate reclassification flag with mandatory acknowledgement when triggered |

The PRD target is ≥85% precision on change type detection. Pre-deployment, a labelled gold set of at least 200 change events covering all six types must achieve this threshold.

### 5.2 Output calibration

Once changes are classified and findings generated, the calibration engine applies the IMDRF × safety class matrix from `4-output-calibration.md` to determine: finding depth, severity floor, citation depth, routing, escalation, evidence requirement, and audit trail depth.

The calibration matrix is implemented as a configuration file:

```
/config/calibration/matrix-v{N}.yaml
/config/calibration/severity-floors.yaml
/config/calibration/routing-rules.yaml
/config/calibration/reclassification-triggers.yaml
```

Every finding records the calibration config version it was generated under.

---

## 6. The analysis engines

Each use case has its own engine. They share infrastructure (the analysis store, the reference corpus, the LLM client, the calibration engine, the finding writer) but encapsulate use-case-specific logic.

| Engine | Use case | Primary mechanism | Inputs | External dependencies |
|---|---|---|---|---|
| Change Classifier | UC1 | Hybrid rules + LLM | Document delta, classification metadata | None beyond LLM |
| Risk Traceability Resolver | UC3 | Graph traversal + LLM gap explanation | Risk-to-SRS link table, current SRS, current risk file | None |
| Baseline Intake Mapper | UC2 | Document-type-specific extractor + LLM mapping | Approved baseline document | Per-document-type parsers |
| AI/ML Boundary Checker | UC4 | PCCP / Article 83 parser + boundary comparison | Approved change control plan, AI/ML SRS delta | PCCP parser (Release 3) |
| Cybersecurity Sub-Check | UC5 | Cross-check against OWASP ASVS + IEC 81001-5-1 + threat model | SRS delta touching security, threat model | Threat model extractor |
| Usability Engineering Module | UC7 | Use error mapper + post-summative monitor | Formative study log, summative baseline, SRS delta | Study report extractor |
| Audit Readiness Aggregator | UC6 | Findings history aggregation + framework mapping | Finding store, audit log | None |

### 6.1 Why separate engines

Each engine has different inputs, different precision requirements, and a different release tier. Keeping them separate allows independent development, independent validation, and selective configuration per product (e.g. a non-AI product runs without UC4; a Category I product runs without UC7).

### 6.2 Document-type-specific extractors

UC2, UC4, UC5, UC7 all require parsers for specific document types: risk management plans, usability study reports, threat models, change control plans. These extractors are pluggable: each implements a common interface (`Document → CanonicalEntities`) and is selected by document type at ingest time. Extractor quality varies with input document structure — see the assumptions section of each use case file for the format dependency.

---

## 7. The finding store

The finding store holds findings, dispositions, and the audit log. It uses the same database engine as the analysis store but lives in a separate schema with stricter permissions.

### 7.1 Finding record

```
Finding
  id                       F-{YYYYMMDD}-{SEQUENCE} per 5-finding-lifecycle.md
  state                    Draft | Sent | InReview | Clarify | Route | Defer | Accept | Reject | Escalate | OutOfScope | Resolved | Closed
  use_case                 UC1 | UC2 | UC3 | UC4 | UC5 | UC6 | UC7
  generated_by_run_id      Link to the run record (which holds analysed_version_hash + diff_input_hash + config set)
  source_document_id       DMS identifier of the document the finding is about
  source_version_label     Version label as supplied by the DMS at analysis time
  affected_entity_ids      List of Requirement, Hazard, RiskControl IDs cited
  cited_clauses            List of StandardClause IDs
  finding_text             Rendered finding for human review (LLM-generated)
  finding_data             Structured machine-readable representation
  imdrf_category_used      Category at analysis time (frozen with finding)
  safety_class_used        Class at analysis time (frozen with finding)
  severity                 Calibrated per output-calibration matrix
  primary_owner_role       Routing target
  notification_targets     Full list of routed roles
  reclassification_flag    bool — mandatory acknowledgement required if true
  trade_off_assessment     Optional structured economic assessment
  generated_at             UTC timestamp
  superseded_by            Optional finding ID — when a re-generation supersedes this one
```

A finding is immutable after generation. The state machine in `5-finding-lifecycle.md` operates on finding state transitions, not on finding content.

### 7.2 Audit log

The audit log is a separate append-only table. Every state transition writes one row. The schema is fixed by `5-finding-lifecycle.md`.

Database-level guarantees:
- No UPDATE or DELETE grants on the audit log table for any application role
- Daily independent backup with offsite copy
- Hash chaining (each row stores the hash of the previous row plus its own content hash) so tampering is detectable
- Quarterly export to the QMS audit trail (manual at Tier 0–3, automatic at Tier 4)

### 7.3 Finding identifier

Format: `F-{YYYYMMDD}-{SEQUENCE}` per `5-finding-lifecycle.md`. The sequence is monotonically increasing per day. Identifiers are never reused.

---

## 8. The integration layer

The integration tier model from the operating model (Tier 0 manual → Tier 4 bidirectional) is implemented as adapter modules behind a single internal API.

### 8.1 Adapter pattern

Every external system integration implements two interfaces:

```
interface Ingester:
  pull_documents(since_timestamp) -> List<DocumentSnapshot>
  pull_metadata() -> ProductRegistry, SoftwareItemRegistry, OwnerDirectory
  pull_traceability_links() -> List<TraceabilityLink>

interface Notifier (Tier 3+):
  deliver_finding(finding, target_role) -> ExternalTaskID
  
interface Synchroniser (Tier 4):
  sync_disposition(finding_id, disposition, rationale) -> Confirmation
```

Adapters live under `/adapters/{system_category}/{vendor_or_format}/`. ReqIF is the recommended canonical interchange format for requirements and traceability — most ALMs export to it. Other formats (CSV, XLSX, ReqIFZ, JSON) are supported through dedicated adapters.

### 8.2 Tier capabilities

| Tier | Inbound | Outbound | Required adapter capability |
|---|---|---|---|
| 0 — Manual | UI upload | UI inbox + file export | None |
| 1 — Read sync | Scheduled pull | Same as Tier 0 | `Ingester` only |
| 2 — Event trigger | Webhook + pull | Same as Tier 0 | `Ingester` + event endpoint |
| 3 — Handoff | Same as Tier 2 | + workflow task creation | `Notifier` |
| 4 — Bidirectional | Same as Tier 2 | + disposition sync-back | `Notifier` + `Synchroniser` |

### 8.3 Tier 0 UI

Even at Tier 0, the agent must be fully functional. The UI provides:

- Document upload (single document, archive of multiple documents, or ReqIF export)
- Manual product registry entry (IMDRF category)
- Manual software item registry entry (safety class + isolation argument)
- Manual traceability table entry (RC → SRS, Requirement → SoftwareItem)
- Finding inbox with disposition workflow
- Audit log viewer with export
- Findings export (JSON, CSV, PDF)

See `../03-integration/4-ui-scope.md` for the full UI specification.

---

## 9. Trigger model and analysis run flow

The trigger receiver is the entry point for every analysis. It implements the six trigger types from the operating model.

### 9.1 Run flow

```
1. Trigger received with input pair: (current document version, diff against previous version)
2. Trigger validated and queued
3. Sync verification — is the source data current? (24h warning, 7d hard block)
4. Input hashing — compute content hashes for the analysed version and the diff
5. Canonical entities derived from the input pair, replacing prior current state
6. Run snapshot assembled — input hashes + entity hashes + configuration set
7. Use case engines invoked (UC1 first; UC3 if change is safety-relevant; UC2/4/5/7 per trigger type)
8. Findings generated, calibrated, written to finding store
9. Reclassification check — if any reclassification flag, suppress other findings for that owner until acknowledged
10. Findings delivered (UI inbox; Tier 3+ workflow system)
11. Run record written to audit trail
12. Latency target: under 5 minutes from trigger to delivery (per operating model)
```

### 9.2 Run record

Every analysis run writes one record:

```
RunRecord
  run_id                       ULID
  trigger_type                 One of six trigger types
  trigger_payload_hash         Hash of the inbound trigger
  analysed_version_hash        Hash of the current document version supplied as input
  diff_input_hash              Hash of the diff against the previous version
  canonical_entities_hash      Hash of the canonical entity state derived for the run
  source_document_id           DMS identifier of the analysed document
  source_version_label         Version label as supplied by the DMS (string, not stored content)
  product_id                   Product under analysis
  use_cases_invoked            List of use case IDs
  llm_model                    e.g. claude-sonnet-4-6
  llm_model_revision           Revision ID
  embedding_model              Model + version
  prompt_template_version      Git tag of the prompt set
  calibration_config_version   Git tag of the config set
  reference_corpus_version     Corpus version used
  schema_version               Canonical schema version used
  generated_findings           List of finding IDs
  started_at                   UTC
  completed_at                 UTC
  status                       success | partial_failure | failure
  errors                       List of error records (if any)
```

Run records are immutable. They are the primary artefact for reproducibility (principle 6). They contain hashes and references — not document content — and so do not duplicate the DMS's role as long-term version archive.

---

## 10. Reproducibility and validation

This section is what makes the agent auditable as a SaMD development tool. It is non-negotiable.

### 10.1 Reproducibility contract

Every finding can be regenerated by re-running the agent with the same inputs:
- Same analysed document version (verified by `analysed_version_hash` in the run record) — supplied externally; the agent does not retain prior versions
- Same diff input (verified by `diff_input_hash`)
- Same LLM model + revision (pinned, not auto-upgraded)
- Same embedding model + version
- Same prompt template version (Git tag)
- Same calibration config version (Git tag)
- Same reference corpus version
- LLM temperature = 0; deterministic decoding settings recorded
- Same retrieval strategy (top-k, similarity threshold)

When any of these inputs change, the agent generates a new run with new findings. Old findings remain in the finding store as historical evidence.

Where the original document content is no longer available in the agent (for example, after the configured retention period has expired), the run record itself stands as evidence that the named configuration produced the recorded findings against an input matching the recorded hashes. The original document, when needed, is retrieved from the DMS — the authoritative source.

### 10.2 GAMP 5 categorisation

The agent is treated as **GAMP 5 Category 5 (custom application)**. The validation package includes:

| Document | Owner | Cadence |
|---|---|---|
| Intended use of the agent | PM + RA | At first deployment + on major revision |
| User Requirements Specification (the agent's URS) | PM | At first deployment + per release |
| Functional Specification | AI Architect | Per release |
| Risk analysis of the agent itself | RA + AI Architect | At first deployment + on major revision |
| Configuration specification | AI Architect | Per release |
| Test protocols (IQ, OQ, PQ) | QA | Per release |
| Validation report | QA | Per release |

This is in addition to the device's own design controls — the agent is a development support tool subject to ISO 13485 design control of supporting tools.

### 10.3 LLM-specific validation

LLM behaviour is non-deterministic by default. The validation strategy:

| Concern | Mitigation |
|---|---|
| Stochastic outputs | Temperature = 0; same input → same output verified per release |
| Model drift | LLM model version pinned; upgrade is a controlled change with full regression suite |
| Prompt injection | Inputs sanitised; LLM responses validated against expected output schema; hallucination checks before finding emission |
| Hallucinated citations | Every cited clause must resolve to a real entry in the reference corpus; findings with unresolvable citations are blocked at generation time |

The PRD targets ≥90% citation validity, ≥80% findings acceptance, <5% hallucination rate, 100% classification calibration accuracy on the test corpus, and ≥90% reclassification detection. These are validated per release on the labelled test corpus.

### 10.4 Regression suite

A labelled gold corpus is maintained with at least:
- 200 SRS change events covering all six change types and the AI overlay (for UC1)
- 50 risk traceability scenarios covering missing, broken, and ambiguous links (for UC3)
- 25 baseline intake scenarios per supported document type (for UC2)
- 20 PCCP boundary scenarios (for UC4)
- 30 cybersecurity scenarios (for UC5)
- 15 post-summative change scenarios (for UC7)
- 10 reclassification scenarios (device-level and item-level)

The regression suite runs on every model upgrade, every prompt change, every calibration config change, and every release. Pass thresholds per use case match the validation criteria in each `use-cases/*.md` file.

---

## 11. Output delivery

Five output types per the operating model. The architecture for each:

| Output | Generated by | Delivery channel | Format |
|---|---|---|---|
| Structured finding | Analysis engines | UI inbox + Tier 3 workflow task | Structured + rendered text |
| Reclassification flag | Calibration engine | UI + RA/PRRC notification | Same as finding + flag field |
| Trade-off assessment | UC4 engine + cross-engine aggregator | UI section within finding | Embedded in finding |
| Change assessment report | UC1 + UC3 + UC5 aggregator | UI export + Tier 3+ task | PDF or JSON |
| Audit log export | Audit log writer | UI export + Tier 4 sync | JSON or CSV |

Delivery guarantees: every finding carries a finding ID, source document binding, standard clause citations, and an action link. Three retries with exponential backoff on delivery failure; escalation to administrator after the third failure.

---

## 12. Component selection — concrete recommendations

This section names specific products. They are recommendations based on the principles in section 1. Any component that meets the data contract is acceptable.

### 12.1 Analysis store and finding store

**Recommended:** PostgreSQL 16 LTS, with `pgvector` for embeddings, with `Apache AGE` for graph queries (optional — see below), and with standard JSONB for semi-structured fields.

Rationale: Postgres has the longest qualification track record in regulated environments. pgvector is mature and Apache 2.0. AGE is Apache 2.0 but pre-1.0 (use only if recursive CTEs prove insufficient for UC3 / UC6 traceability queries — start without AGE and add it only if required).

**Rejected alternatives:**
- Neo4j Community Edition: GPLv3 exposure, no clustering, separate vector store needed (two validation targets).
- ArcadeDB: Apache 2.0 multi-model is attractive but qualification track record is shorter than Postgres.
- Pure document store: canonical model is too relational to fit naturally.

### 12.2 LLM provider

**Recommended:** A frontier hosted LLM with deterministic-mode support (temperature=0 honoured), structured-output capability, and SOC 2 Type II + ISO 27001 attestation. Specific revision pinned and upgrade-controlled. Both inputs and outputs logged in full to the run record.

**Constraint:** No regulated personal data (PHI/PII) leaves the agent's environment without explicit data processing addendum coverage. For products that ingest patient data, a self-hosted or VPC-deployed LLM is preferred.

### 12.3 Embedding model

**Recommended:** A version-pinned embedding model with at least 768-dimensional output, multilingual capability (for EU regulatory text), and a stable revision policy. Re-embedding the corpus on model change is a controlled action.

### 12.4 Trigger receiver / queue

**Recommended:** A simple message queue (e.g. Postgres-backed job queue, or Redis Streams) — not a heavyweight orchestrator. The latency target (<5 minutes) does not require Kafka-class infrastructure.

### 12.5 UI and API

**Recommended:** A web UI for reviewers (document owners, RA/QA, Software Architect, Risk Engineer, etc) and a REST or RPC API for adapters. Authentication via the team's SSO provider. Role-based access control aligned with the stakeholder roles in `3-stakeholders.md`.

### 12.6 Source control for configuration

**Recommended:** Git for: canonical schema YAML, calibration config YAML, prompt templates, reference corpus content (the structured summaries, not the LLM weights), adapter code. Tagged releases per release tier. Schema and config changes flow through standard PR review.

**Not recommended for:** controlled documents themselves (those live in the DMS), audit log content (that lives in the database), or generated findings (those live in the finding store).

### 12.7 Object storage

**Recommended:** A standard object store (S3-compatible) for: ingested document originals (retained for the configured retention period only — version history lives in the DMS, not here), generated PDF reports, exported audit logs. Lifecycle policies configured to expire ingested originals after the retention period. Encryption at rest mandatory.

---

## 13. Phased buildout

The buildout sequence aligns with the roadmap in `../02-roi/2-roadmap.md`. The numerical prefix on each use case file in `use-cases/` is the canonical roadmap order — file `1-uc1-srs-monitoring.md` is built first, then `2-uc3-risk-traceability.md`, and so on through `7-uc6-inspection-prep.md`. The phases below follow that order:

| File | Use case | Phase |
|---|---|---|
| `1-uc1-srs-monitoring.md` | UC1 | Phase 1 |
| `2-uc3-risk-traceability.md` | UC3 | Phase 1 |
| `3-uc2-baseline-to-srs.md` | UC2 | Phase 2 |
| `4-uc5-cybersecurity.md` | UC5 | Phase 2 |
| `5-uc7-usability-engineering.md` | UC7 | Phase 2 |
| `6-uc4-change-control-plan.md` | UC4 | Phase 3 |
| `7-uc6-inspection-prep.md` | UC6 | Phase 4 |

Each phase has a defined exit criterion that gates the next phase.

### 13.1 Phase 0 — Foundations (weeks 1–4)

Build the layers that everything else depends on. No use case capability yet.

| Week | Deliverable |
|---|---|
| 1 | Canonical schema v1 — defined, reviewed by RA/QA, committed to source control |
| 1–2 | Postgres + pgvector stand-up, schema migrations under version control, backup/restore tested |
| 2–3 | Reference corpus v1 — IEC 62304 + ISO 14971 + OWASP ASVS clause summaries ingested |
| 3 | Calibration config v1 — IMDRF × safety class matrix encoded as YAML |
| 3–4 | Run record + audit log infrastructure with append-only enforcement and hash chaining |
| 4 | LLM client wrapper with deterministic settings, prompt template versioning, full input/output logging |

**Exit criterion:** an end-to-end pipeline can accept a synthetic (current version, diff) input pair, generate one trivial finding via the LLM, write a run record with all hashes captured, and the finding can be regenerated bit-for-bit by re-supplying the same input pair against the same configuration.

### 13.2 Phase 1 — Initial release (weeks 5–14)

Build UC1 + UC3 to MVP completeness. This is the build scope from `../02-roi/3-mvp-specification.md`.

| Weeks | Deliverable |
|---|---|
| 5–6 | Tier 0 UI for document upload, product registry, software item registry, traceability table — supports the input pair (current version + diff against previous version) |
| 6–7 | Document ingestion + canonical schema mapping for SRS (CSV/XLSX/ReqIF), replacing prior canonical state on each successful run |
| 7–9 | UC1 change classifier — hybrid rules + LLM, six change types, all supported, operating on the supplied diff |
| 9–10 | UC1 reclassification trigger — device-level and item-level criteria from `4-output-calibration.md` |
| 10–11 | UC3 risk traceability resolver — graph queries (recursive CTEs initially; AGE if needed) |
| 11–12 | Output calibration applied per IMDRF × safety class matrix |
| 12–13 | Finding lifecycle — full state machine, audit log, disposition workflow per `5-finding-lifecycle.md` |
| 13–14 | Validation against the regression suite — meet all acceptance criteria from `mvp-specification.md` |

**Exit criterion:** all initial release validation criteria from `mvp-specification.md` met.

### 13.3 Phase 2 — Release 2 (months 4–7)

Add UC2, UC5, UC7. Add Tier 1 sync for at least one document management system and one requirements management system. Phase 2 ROI begins accruing here.

| Weeks | Deliverable |
|---|---|
| 1–3 | Document-type-specific parsers — risk management plan, usability study report, threat model |
| 3–5 | UC2 baseline intake mapper |
| 5–7 | UC5 cybersecurity sub-check — OWASP ASVS + IEC 81001-5-1 cross-check |
| 7–9 | UC7 usability engineering — formative trigger + post-summative monitor |
| 9–11 | Tier 1 sync adapters for one DMS + one ALM |
| 11–12 | Tier 2 webhook trigger receiver |
| 12 | Validation against expanded regression suite |

**Exit criterion:** UC2, UC5, UC7 validation criteria met; at least one product running in Tier 2 mode in pilot deployment.

### 13.4 Phase 3 — Release 3 (months 8–10)

Add UC4. Re-evaluate confidence score before starting (PCCP guidance maturity check).

| Weeks | Deliverable |
|---|---|
| 1–2 | Confidence re-evaluation: PCCP guidance status review, EU AI Act Article 83 implementing acts review |
| 2–6 | PCCP / Article 83 boundary parser — purpose-built per the team's actual document format |
| 6–8 | UC4 boundary checker engine |
| 8–10 | Validation against UC4 regression suite |

**Exit criterion:** UC4 validation criteria met for AI-enabled products.

### 13.5 Phase 4 — Later (months 12+)

Add UC6 inspection preparation. Requires 6+ months of production findings history per the use case definition.

| Weeks | Deliverable |
|---|---|
| 1–4 | UC6 audit readiness aggregator |
| 4–6 | Framework-specific output formatters (EU MDR Annex II/III, FDA 21 CFR 820.30) |
| 6–8 | Tier 3+ workflow handoff for at least one task management system |
| 8–10 | Tier 4 disposition sync-back design and pilot — high-risk integration, careful staging |

**Exit criterion:** first audit readiness package generated for a real pre-submission readiness check.

---

## 14. Validation criteria for the agent itself

Independent of any use case, the agent as a whole must meet these criteria before any production use:

- [ ] GAMP 5 Category 5 validation package complete (intended use, URS, FS, risk analysis of the agent, IQ/OQ/PQ protocols, validation report)
- [ ] Reproducibility test: regenerate 10 historic findings bit-for-bit from their run records
- [ ] Audit log integrity test: simulated tamper attempt detected by hash chain verification
- [ ] Backup/restore test: full round-trip with no data loss and integrity verified
- [ ] Latency test: 95th percentile trigger-to-delivery under 5 minutes for standard documents
- [ ] Calibration test: 100% match against the gold corpus for all 16 IMDRF × safety class combinations
- [ ] Citation validity ≥90% on the regression suite
- [ ] Hallucination rate <5% on the regression suite
- [ ] All adapters validated against their respective system contract documents
- [ ] Runbook documented for: model upgrade, prompt upgrade, schema migration, corpus refresh, calibration config change

---

## 15. What this architecture deliberately does not specify

These decisions are deferred to implementation:

- **Specific LLM vendor.** Pick at implementation time based on data residency, language support, and cost.
- **Hosting topology.** Single-tenant vs multi-tenant, on-premise vs cloud — depends on the team's regulatory posture and existing IT.
- **UI framework.** Any modern web framework that supports the role-based access requirements is acceptable.
- **Specific embedding model revision.** Pin at implementation time and document.
- **Backup retention period.** Should match the team's QMS retention policy (typically 10 years for EU MDR, 2 years beyond device life for FDA).
- **Whether to use AGE or stick with recursive CTEs.** Decide after Phase 1 by measuring real query patterns and response times.

---

## 16. Open questions and watch items

Items that will require revisiting:

1. **AI Act Article 83 implementing acts.** When the EU publishes the implementing acts, UC4's scope and the AI overlay calibration may need updating.
2. **FDA PCCP guidance finalisation.** Same — UC4 was scoped against the 2023 draft; the final guidance may require parser changes.
3. **IEC 81001-5-1 update cycle.** A revision in scope may require corpus refresh and UC5 re-validation.
4. **EU MDR / IVDR convergence.** If IVDR-specific adaptations are needed, the calibration matrix may need an IVDR overlay.
5. **Self-hosted LLM viability.** As open-weight models improve, the hosted-LLM dependency may be replaced. Re-evaluate per release.

---

See: [vision](1-vision.md) · [PRD](2-prd.md) · [stakeholders](3-stakeholders.md) · [output calibration](4-output-calibration.md) · [finding lifecycle](5-finding-lifecycle.md) · [operating model](../03-integration/1-operating-model.md) · [system categories](../03-integration/2-system-categories.md) · [metadata spec](../03-integration/3-metadata-spec.md) · [MVP specification](../02-roi/3-mvp-specification.md) · [roadmap](../02-roi/2-roadmap.md)
