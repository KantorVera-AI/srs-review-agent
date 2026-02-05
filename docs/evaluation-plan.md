# Evaluation Plan

## AI Architect Metrics (technical)
| Metric | How | Target |
|--------|-----|--------|
| Citation validity | Manual check 50 findings | ≥90% |
| Hallucination rate | Output vs source docs | <5% |
| Change detection | v1→v2 SRS deltas | Precision ≥85% |
| Constraint compliance | No risk acceptance claims | 100% |

## PM Metrics (product)
| Metric | How | Target |
|--------|-----|--------|
| Findings acceptance | Simulated review | ≥80% |
| Time saved | Manual vs Agent review | Measure PR cycles |
| Stakeholder coverage | Findings by role | All roles hit |

## Test scenarios (20 total)
1. SRS v1 complete check
2. SRS v1→v2 delta (SRS-005 modified)
3. Risk RC-001 → SRS coverage
4. IEC 62304 template → SRS gaps

## Run eval
1. python src/analysis/eval.py --corpus data/raw/
2. Review outputs in experiments/eval01/
