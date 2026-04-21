# Dataset Specification

## Corpus types
| Type | Source | Location | Versions |
|------|--------|----------|----------|
| SRS | Synthetic | `data/raw/srs/` | v1, v2 (delta test) |
| Risk file | Synthetic | `data/raw/risk/` | v1 |
| IEC62304 Mapping | openregulatory/templates | `data/reference/iec62304-mapping.md` | v1.0 |
| IEC62304 SRS Checklist | Synthetic | `data/reference/iec62304-srs-requirements.md` | v1.0 |
| ISO 14971 risk table | Synthetic | `data/reference/iso14971-risk-table-example.md` | v1.0 |
| OWASP ASVS checklist | Public (open licence) | `data/reference/owasp-asvs-summary.md` | v4.0 |

## ID conventions
- SRS: `SRS-001`, `SRS-045`
- Risk: `H-001`, `RC-001` (risk control)
- Standards: `IEC62304-4.3.2`

## Required metadata fields

Two metadata fields must be present in the corpus for the agent to produce classification-calibrated outputs:

| Field | Format | Source | Example |
|---|---|---|---|
| IMDRF significance category | Integer 1–4 | Intended use document / regulatory strategy | `3` |
| Software item safety class | String A, B, or C | Software Architecture Document (SAD) | `C` |

These fields are attached to the product record (IMDRF category) and to each software item record (safety class). If absent, the agent falls back to conservative defaults and cannot distinguish finding depth by classification tier.

## Evaluation set (20 events)
1. SRS v1 → v2 (add SRS-011, modify SRS-005)
2. Risk control RC-001 → verify SRS coverage  
3. IEC62304-4.3.2 → SRS completeness (iec62304-mapping.md)
4. IEC62304-5.2.1 → risk traceability gaps
5. IMDRF Category I product — verify agent produces advisory-level findings only
6. SRS change that removes architectural isolation from a software item — verify agent flags potential safety class reclassification

## Data policy
See `data/README.md`
