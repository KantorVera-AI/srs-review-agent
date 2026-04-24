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
| Reclassification detection | Agent flags SRS changes that remove software item isolation (scenario 12) and that add clinical functionality (scenario 13) | ≥