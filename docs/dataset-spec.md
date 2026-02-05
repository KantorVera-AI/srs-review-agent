# Dataset Specification

## Corpus types
| Type | Source | Location | Versions |
|------|--------|----------|----------|
| SRS | Synthetic | `data/raw/srs/` | v1, v2 (delta test) |
| Risk file | Synthetic | `data/raw/risk/` | v1 |
| IEC62304 Mapping | openregulatory/templates | `data/reference/iec62304-mapping.md` | v1.0 |
| IEC62304 SRS Checklist | Synthetic | `data/reference/iec62304-srs-requirements.md` | v1.0 |

## ID conventions
- SRS: `SRS-001`, `SRS-045`
- Risk: `H-001`, `RC-001` (risk control)
- Standards: `IEC62304-4.3.2`

## Evaluation set (20 events)
1. SRS v1 → v2 (add SRS-011, modify SRS-005)
2. Risk control RC-001 → verify SRS coverage  
3. IEC62304-4.3.2 → SRS completeness (iec62304-mapping.md)
4. IEC62304-5.2.1 → risk traceability gaps

## Data policy
See `data/README.md`
