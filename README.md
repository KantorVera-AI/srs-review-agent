# SRS Review Agent

**Status:** Stable
**Owner:** Product Management
**Audience:** All stakeholders

---

AI decision-support agent that analyses Software Requirements Specifications (SRS) and related controlled documents against regulatory standards, generates citation-backed findings, and routes them to the appropriate document owners for human review and disposition.

**Decision-support only.** The agent proposes findings. Humans decide. No autonomous regulatory actions.

---

## What it does

- Detects changes to controlled documents and classifies their regulatory impact
- Checks SRS requirements against risk controls, cybersecurity obligations, usability engineering obligations, and applicable standards
- Generates structured findings with citations to specific standard clauses
- Routes findings to the correct document owner based on change type and classification
- Calibrates output depth based on the device's IMDRF significance category and the IEC 62304 safety class of the affected software item
- Logs all findings and dispositions for audit trail purposes

**What it does not do:** create or approve requirements, make risk acceptability decisions, generate regulatory submissions, replace formal design reviews or sign-offs, or act as the system of record for any controlled document.

---

## Applicable regulatory frameworks

This agent supports both **EU MDR** (EU Medical Device Regulation 2017/745, harmonised standards IEC 62304 and ISO 14971) and **US FDA** (21 CFR Part 820 / QMSR, FDA software and AI/ML guidance) workflows. Where requirements differ between jurisdictions, both are addressed explicitly. Where they are equivalent, jurisdiction-neutral language is used.

The agent is **product-agnostic** — it works across device types and classification tiers. Its outputs are **classification-dependent** — what it flags, how deeply it analyses, who it notifies, and what evidence it requires all vary based on the product's IMDRF significance category (I through IV) and the IEC 62304 safety class of each software item being reviewed.

---

## Who reads what

| If you are                            | Start here                                                                                                                                                                 |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| New to the project — any role        | This file, then [`docs/README.md`](docs/README.md)                                                                                                                           |
| Deciding what to build and when       | [`docs/02-roi/master-overview.md`](docs/02-roi/master-overview.md)                                                                                                          |
| Building the system (AI Architect)    | [`docs/01-system/prd.md`](docs/01-system/prd.md) → [`docs/03-integration/metadata-spec.md`](docs/03-integration/metadata-spec.md)                                           |
| Reviewing regulatory scope (RA/QA)    | [`docs/00-overview/compliance-landscape.md`](docs/00-overview/compliance-landscape.md) → [`docs/01-system/stakeholders.md`](docs/01-system/stakeholders.md)                 |
| Integrating with existing systems     | [`docs/03-integration/operating-model.md`](docs/03-integration/operating-model.md) → [`docs/03-integration/system-categories.md`](docs/03-integration/system-categories.md) |
| Deploying and configuring the agent   | [`docs/03-integration/ui-scope.md`](docs/03-integration/ui-scope.md)                                                                                                        |
| Challenging a prioritisation decision | [`docs/02-roi/assumptions.md`](docs/02-roi/assumptions.md)                                                                                                                  |

---

## Repository structure

```
srs-review-agent/
│
├── README.md                          ← You are here
│
├── docs/
│   ├── README.md                      ← Documentation navigation guide
│   ├── git-workflow.md                ← Team working process
│   ├── 00-overview/                   ← Compliance context (reference)
│   ├── 01-system/                     ← Agent system definition (specification)
│   ├── 02-roi/                        ← ROI and prioritisation (decision support)
│   ├── 03-integration/                ← Integration and UI (operational)
│   └── 04-diagrams/                   ← PlantUML source diagrams
│
├── data/
│   ├── README.md                      ← Data policy
│   ├── raw/
│   │   ├── srs/                       ← Synthetic SRS documents (v1, v2)
│   │   └── risk/                      ← Synthetic risk management files
│   └── reference/                     ← Standard clause summaries and checklists
│
├── src/
│   ├── analysis/                      ← Core agent logic
│   └── integrations/                  ← Integration tier implementations
│       ├── tier0-manual/              ← File upload and export handlers
│       ├── tier1-sync/                ← Scheduled pull connectors
│       ├── tier2-events/              ← Event receiver and webhook handlers
│       └── tier3-handoff/             ← Task creation and disposition sync
│
└── experiments/                       ← Evaluation runs and results
```

---

## Core principles

1. **Non-binding** — all findings are proposals. Humans accept, reject, defer, or escalate.
2. **Traceable** — every finding cites the specific standard clause and source document version that produced it.
3. **Auditable** — every finding and every disposition is logged with a timestamp, a finding ID, and a rationale.
4. **Classification-calibrated** — output depth, severity thresholds, and routing rules vary by IMDRF category a