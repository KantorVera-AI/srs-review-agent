# Evaluation Plan

## AI Architect Metrics (technical)
| Metric | How | Target |
|--------|-----|--------|
| Citation validity | Manual check 50 findings | ≥90% |
| Hallucination rate | Output vs source docs | <5% |
| Change detection | v1→v2 SRS deltas | Precision ≥85% |
| Constraint compliance | No risk acceptance claims | 100% |
| Classification calibration | Output depth matches expected tier for each IMDRF category | 100% match on test corpus |
| Reclassification detection | Agent flags SRS changes that remove software item isolation | ≥90% detection rate |

## PM Metrics (product)
| Metric | How | Target |
|--------|-----|--------|
| Findings acceptance | Simulated review | ≥80% |
| Time saved | Manual vs Agent review | Measure review cycle time per change event |
| Stakeholder coverage | Findings by role | All roles hit |
| Phase 1 gap coverage | % of first-submission gaps caught before filing (simulated) | ≥80% |
| Routing accuracy | % of findings routed to the correct owner role | ≥90% |

## Test scenarios (20 total)
1. SRS v1 complete check
2. SRS v1→v2 delta (SRS-005 modified)
3. Risk RC-001 → SRS coverage
4. IEC 62304 template → SRS gaps
5. IMDRF Category IV product — verify Critical finding depth and mandatory escalation routing
6. SRS change removing module isolation — verify reclassification flag is generated

## Run eval
1. python src/analysis/eval.py --corpus data/raw/
2. Review outputs in experiments/eval01/
