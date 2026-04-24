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

These fields are attached to the product record (IMDRF category) and to each software item record (safety class) in the traceability table. If absent, the agent falls back to conservative defaults and cannot be tested for classification-calibrated output.

The synthetic corpus must include at least two products at different IMDRF categories to enable calibration testing.

---

## Evaluation set

Twenty test scenarios covering the primary use cases and calibration requirements.

| # | Scenario | Use case | Tests |
|---|---|---|---|
| 1 | SRS v1 complete check | UC1, UC3 | Baseline finding generation |
| 2 | SRS v1 → v2 delta (SRS-005 modified) | UC1 | Change detection and classification |
| 3 | SRS v1 → v2 delta (SRS-011 added) | UC1 | New requirement classification |
| 4 | Risk control RC-001 → SRS-005 link check | UC3 | Traceability verification |
| 5 | RC-001 link broken (SRS-005 removed in v2) | UC3 | Missing link detection |
| 6 | IEC 62304 mapping → SRS completeness | UC1, UC3 | Standards compliance check |
| 7 | IEC 62304-5.2.1 → risk traceability gaps | UC3 | Risk control gap detection |
| 8 | IMDRF Category I product — same change as scenario 2 | UC1 | Classification calibration — advisory output only |
| 9 | IMDRF Category IV product — same change as scenario 2 | UC1 | Classification calibration — mandatory escalation |
| 10 | Class A software item — security requirement change | UC1, UC5 | Item-level calibration — reduced citation depth |
| 11 | Class C software item — security requirement change | UC1, UC5 | Item-level calibration — full citation depth |
| 12 | SRS change removing architectural isolation from SI-002 | UC1 | Reclassification trigger — safety class |
| 13 | SRS change adding diagnostic function to inform-only product | UC1 | Reclassification trigger — IMDRF category |
| 14 | Missing IMDRF category metadata | UC1 | Fallback behaviour — Category III defaults |
| 15 | Missing software item safety class metadata | UC1 | Fallback behaviour — Class C defaults |
| 16 | Baseline risk management plan approval | UC2 | Suggestion generation from baseline |
| 17 | Security requirement gap — new interface without authentication | UC5 | OWASP ASVS gap detection |
| 18 | Post-summative SRS change — UI requirement modified | UC7 | Post-summative change flag |
| 19 | Formative use error not in SRS or risk file | UC7 | Use error feedback loop |
| 20 | Dual-market product — same gap in EU MDR and FDA context | UC1, UC3 | Dual-market citation output |

---

## Data policy

See `data/README.md`. Key rules:

- No PHI or PII in any file
- No client-confidential SRS or risk documents
- No proprietary standards text — use clause summaries and open mapping tables only
- All synthetic data must be clearly labelled as illustrative
