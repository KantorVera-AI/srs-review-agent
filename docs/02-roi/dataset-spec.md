**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect

---

# Dataset Specification

Defines the synthetic test corpus used to develop and evaluate the agent. All data in this corpus is synthetic or publicly licensed — no PHI, no client-confidential documents, no proprietary standards text. See `data/README.md` for the full data policy.

---

## Corpus types

| Type | Source | Location | Versions |
|---|---|---|---|
| SRS | Synthetic | `data/raw/srs/` | v1, v2 (delta test) |
| Risk management file | Synthetic | `data/raw/risk/` | v1 |
| IEC 62304 requirements mapping | openregulatory/templates (open licence) | `data/reference/iec62304-mapping.md` | v1.0 |
| IEC 62304 SRS checklist | Synthetic | `data/reference/iec62304-srs-requirements.md` | v1.0 |
| ISO 14971 risk table example | Synthetic | `data/reference/iso14971-risk-table-example.md` | v1.0 |
| OWASP ASVS summary | Public (Creative Commons) | `data/reference/owasp-asvs-summary.md` | v4.0 |

---

## ID conventions

| Identifier type | Format | Example |
|---|---|---|
| SRS requirement | `SRS-NNN` | `SRS-001`, `SRS-045` |
| Hazard | `H-NNN` | `H-001` |
| Risk control | `RC-NNN` | `RC-001` |
| Software item | `SI-NNN` | `SI-001`, `SI-003` |
| Standard clause | `STANDARD-SECTION.SUBSECTION` | `IEC62304-5.2.3`, `ISO14971-7.3.3` |

---

## Required metadata fields

Two metadata fields must be present for the agent to produce classification-calibrated outputs. The synthetic corpus must include both.

| Field | Format | Scope | Example |
|---|---|---|---|
| IMDRF significance category | Integer 1–4 | Product level | `3` |
| IEC 62304 software item safety class | String A, B, or C | Per software item | `C` |

These fields are attached to the product record (IMDRF category) and to each software item record (safety class) in the trac