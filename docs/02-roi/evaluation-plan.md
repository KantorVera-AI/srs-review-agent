**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect, PM

---

# Evaluation Plan

Defines the metrics and test scenarios used to evaluate the agent before each release. Metrics are split by audience — technical metrics for the AI Architect and product metrics for the PM.

All percentages are targets for the initial release. Targets for subsequent releases will be revised based on empirical data.

---

## AI Architect metrics (technical)

| Metric | How measured | Target |
|---|---|---|
| Citation validity | Manual check of 50 findings — does each citation resolve to the correct clause in the reference corpus? | ≥90% |
| Hallucination rate | Output compared against source documents — does the finding assert something not present in the source? | <5% |
| Change detection precision | SRS v1 → v2 delta — what proportion of detected changes are real changes (not false positives)? | ≥85% |
| Change detection recall | SRS v1 → v2 delta — what proportion of real changes are detected? | ≥90% |
| Constraint compliance | Agent never generates risk acceptability decisions or autonomous regulatory conclusions | 100% |
| Classification calibration | Output depth matches expected tier for each IMDRF category test scenario in the evaluation set | 100% match |
| Reclassification detection | Agent flags SRS changes that remove software item isolation (scenario 12) and that add clinical functionality (scenario 13) | ≥90% detection rate |
| Routing accuracy | Finding delivered to the correct owner role in each test scenario | ≥95% |
| Fallback behaviour | Agent applies correct defaults when IMDRF category or safety class metadata is absent (scenarios 14, 15) | 100% correct |

---

## PM metrics (product)

| Metric | How measured | Target |
|---|---|---|
| Findings acceptance rate | Proportion of findings accepted in simulated review across all test scenarios | ≥80% |
| Phase 1 gap coverage | Proportion of pre-seeded gaps in the synthetic first-submission corpus detected before filing | ≥80% |
| Review cycle time | Time from finding generation to disposition in simulated workflow | Measure baseline — no target for initial release |
| Stakeholder coverage | All defined owner roles receive at least one correctly routed finding across the test scenarios | 100% |
| Dual-market citation | For scenario 20, findings cite both EU MDR and FDA applicable clauses | 100% |

---

## Test scenarios

Run against the evaluation set defined in `dataset-spec.md`. Scenarios are numbered to match the dataset spec.

| Scenario | Primary metric tested |
|---|---|
| 1 — SRS v1 complete check | Citation validity, constraint compliance |
| 2 — SRS v1→v2 delta (modified) | Change detection precision and recall |
| 3 — SRS v1→v2 delta (new requirement) | Change detection, routing accuracy |
| 4 — RC-001 link check | Citation validity, classification calibration |
| 5 — RC-001 link broken | Reclassification detection, findings acceptance |
| 6 — IEC 62304 completeness | Hallucination rate, citation validity |
| 7 — Risk traceability gaps | Routing accuracy, citation validity |
| 8 — Category I calibration | Classification calibration (advisory only) |
| 9 — Category IV calibration | Classification calibration (mandatory escalation) |
| 10 — Class A item calibration | Item-level calibration (reduced depth) |
| 11 — Class C item calibration | Item-level calibration (full depth) |
| 12 — Isolation removal | Reclassification detection (safety class) |
| 13 — Diagnostic function added | Reclassification detection (IMDRF category) |
| 14 — Missing IMDRF metadata | Fallback behaviour |
| 15 — Missing safety class metadata | Fallback behaviour |
| 16 — Baseline suggestion generation | Phase 1 gap coverage |
| 17 — Security gap detection | Routing accuracy, citation validity |
| 18 — Post-summative change flag | Stakeholder coverage, routing accuracy |
| 19 — Formative use error feedback | Phase 1 gap coverage |
| 20 — Dual-market citation | Dual-market citation metric |

---

## How to run the evaluation

```bash
# Index the synthetic corpus
python src/analysis/ingest.py --corpus data/raw/

# Run the full evaluation suite
python src/analysis/eval.py --corpus data/raw/ --output experiments/eval01/

# Review outputs
ls experiments/eval01/
```

Results are stored in `experiments/eval01/`. Each scenario produces a structured output file with the finding content, the expected output (for calibration scenarios), and a pass/fail indicator.

---

## Updating targets after each release

After the initial release, update the following targets based on empirical data from production use:

| Metric | Update trigger |
|---|---|
| Findings acceptance rate | After 3 months of production — use actual disposition data |
| Classification calibration | After first deployment to a product with confirmed IMDRF category |
| Reclassification detection | After first confirmed reclassification event in production |
| Review cycle time | After 3 months — set a target based on the measured baseline |

See `assumptions.md` in this folder for the parameter update schedule tied to the ROI model.
