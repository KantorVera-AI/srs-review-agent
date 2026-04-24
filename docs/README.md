# Documentation Navigation Guide

**Status:** Stable
**Owner:** Product Management
**Audience:** All stakeholders

---

This guide explains how the documentation is structured, why it is organised this way, and where to find what you need. Read this before diving into any specific document.

---

## Why four domains

The documentation covers four distinct types of content, each serving different audiences with different questions to answer. Keeping them separate means each document can be read, updated, and challenged independently without touching unrelated material.

| Domain | Folder | Question it answers | Changes when |
|---|---|---|---|
| Compliance context | `00-overview/` | Why does this problem exist? What is the regulatory landscape? | Regulatory guidance changes |
| System definition | `01-system/` | What does the agent do? How does it behave? | Product decisions change |
| ROI and prioritisation | `02-roi/` | Why this order? What is the expected value? | Empirical data arrives or assumptions are challenged |
| Integration and UI | `03-integration/` | How do inputs arrive and outputs leave? What does the UI do? | Integration partners change or new system categories are added |

Diagrams live in `04-diagrams/` and are referenced by documents across all four domains.

---

## Domain 0 — Compliance context (`00-overview/`)

**Who reads this:** Anyone who needs to understand the regulatory environment before evaluating the agent. Regulatory consultants, advisors, new team members, investors doing technical due diligence.

**What it contains:**

`compliance-landscape.md` — The V-model, the SaMD document ecosystem, the standards corpus the agent references, and the design control framework the agent supports.

`classification-reference.md` — The IMDRF SaMD significance framework (Categories I–IV) as the jurisdiction-neutral classification spine, with mappings to EU MDR device classes, FDA device classes, and IEC 62304 software item safety classes (A, B, C). Also covers Health Canada, TGA, and PMDA.

`ai-legislation.md` — EU AI Act obligations for AI-enabled SaMD, FDA AI/ML framework, ISO/IEC 42001, and the anticipated ISO 14971 amendment on AI-specific hazards.

**Reading order:** `compliance-landscape.md` → `classification-reference.md` → `ai-legislation.md` (if AI-enabled product).

---

## Domain 1 — System definition (`01-system/`)

**Who reads this:** AI Architect (to build), RA/QA consultants (to validate scope), PM (to define requirements).

**What it contains:**

`vision.md` — One-page product vision.

`prd.md` — Product requirements. Technology-neutral. Use case taxonomy UC1–UC7 defined here — canonical naming across all documentation.

`use-cases/` — One file per use case (UC1–UC7). Each contains: description, trigger, output owners, RICE score, Phase 1 and Phase 2 benefit, assumptions, dependencies, release tier.

`stakeholders.md` — All stakeholder roles, finding disposition workflow, severity level definitions.

`finding-lifecycle.md` — Finding states, valid transitions, audit trail requirements, reclassification special handling.

`output-calibration.md` — How agent output changes by IMDRF category and IEC 62304 software item safety class. Defines the two-way reclassification trigger logic and the IEC 62366-1 decomposition exception.

**Reading order:** `vision.md` → `prd.md` → relevant use case files → `stakeholders.md` → `output-calibration.md`.

---

## Domain 2 — ROI and prioritisation (`02-roi/`)

**Who reads this:** PM and AI Architect (roadmap decisions), advisors, investors, anyone challenging a prioritisation decision.

**What it contains:**

`master-overview.md` — Complete ROI picture at summary depth. All seven use cases with RICE scores, roadmap rationale, classification sensitivity, overall value proposition.

`mvp-specification.md` — UC1 and UC3 in full detail with Phase 1 and Phase 2 ROI, assumptions, sensitivities, metadata tagging prerequisite.

`roadmap.md` — Release structure, dependency chain, multi-dimensional sequencing logic, what the AI Architect must validate before each release.

`assumptions.md` — Parameter reference (Risk Savings, Impact, Confidence, Effort), limitations, economic trade-off framework, update trigger table.

**Reading order:** `master-overview.md` → `roadmap.md` → `mvp-specification.md` → `assumptions.md` (if challenging a number).

**How to challenge:** Go to `assumptions.md`. Identify the parameter and assumption. Propose a revised value. Re-run the formula. Update the relevant use case file and roadmap if release sequencing is affected.

---

## Domain 3 — Integration and UI (`03-integration/`)

**Who reads this:** AI Architect (integration layer design), integration partners (data contracts), deployment teams (configuration and operation).

**What it contains:**

`operating-model.md` — System boundaries, working analysis store, trigger model, output delivery model, system of record table.

`system-categories.md` — Data contracts by system category (not vendor names). Covers all system types a regulated SaMD team operates. Defines the two cross-cutting metadata fields: IMDRF category and IEC 62304 software item safety class.

`metadata-spec.md` — Tagging specification that teams must implement before the agent can produce classification-calibrated outputs. Prerequisite for the AI Architect before starting the ingestion layer.

`ui-scope.md` — What the agent's own UI does and does not do. Three jobs: manual input fallback, finding review and disposition, configuration and monitoring. Explicit list of what the UI must never do.

**Reading order:** `operating-model.md` → `system-categories.md` → `metadata-spec.md` → `ui-scope.md`.

---

## Domain 4 — Diagrams (`04-diagrams/`)

All diagrams use technology-neutral labels. Render using any PlantUML renderer or the PlantUML VS Code extension.

```
04-diagrams/
├── overview/       system-context, doc-relationships, use-cases
├── workflows/      baseline-to-srs-activity, srs-monitoring-activity
├── architecture/   functional-components, c4-context, c4-container
├── sequences/      baseline-approved-sequence, srs-change-detected-sequence
└── states/         finding-lifecycle-state
```

---

## Terminology conventions

| Use | Not |
|---|---|
| SRS Review Agent | SRS Review Copilot |
| UC1–UC7 (ROI taxonomy) | UC1–UC4 (PRD taxonomy from earlier versions) |
| IMDRF Category I–IV | EU class or FDA class as primary reference |
| Regulatory reviewer | Notified Body or FDA (unless jurisdiction-specific) |
| Version control / document repository | GitHub (unless specifically referring to the team's own tooling) |
| Requirements and traceability management system | Jama, Polarion (unless giving an example) |
| Workflow and task management system | Jira (unless giving an example) |

---

## Document status conventions

| Status | Meaning |
|---|---|
| `Stable` | Agreed — change requires tracked decision |
| `Working draft` | Active development — challenge it |
| `Placeholder` | Structure defined, content not yet written |
| `Deprecated` | Superseded — do not use |

---

## Contributing

Changes to `Stable` documents require a documented rationale. Changes to use case files in `01-system/use-cases/` should reference the issue or decision that drove the change. The document most likely to need updating as the project matures is `02-ro