**Status:** Working draft
**Owner:** Product Management
**Audience:** PM, AI Architect, anyone challenging a score

---

# Assumptions and Parameter Reference

This is the primary place to challenge the ROI model. Every score in `master-overview.md` is built from four parameters defined here. If a number seems wrong, identify the parameter, identify the assumption behind it, propose a revised value, and re-run the formula.

```
Score = (Risk Savings × Impact × Confidence) / Effort × 10
```

---

## Risk Savings (1–5)

**What it represents:** Expected reduction in regulatory cost if this use case is implemented. A score of 5 means the use case directly prevents high-cost regulatory events — unplanned submissions, major deficiency rounds. A score of 1 means operational improvement only, with no direct regulatory cost avoidance.

**How it was estimated:** Based on the probability that a missed finding in this domain triggers a regulatory reviewer deficiency, multiplied by the typical cost of one additional review round. Cost structures are comparable in EU MDR and FDA processes.

Sources: SaMD compliance cost industry benchmarks, EU MDR and FDA change control guidance, OpenRegulatory technical file template complexity analysis, FDA software submission guidance.

**Key assumption:** A 20–40% baseline probability of regulatory reviewer questions on a moderate change falls to 5–15% with systematic AI-assisted traceability review. If your team's historical deficiency rate is below 20%, all Risk Savings scores should be reduced proportionally.

| Score | Meaning |
|---|---|
| 5 | Directly prevents unplanned submissions or major deficiency rounds (15–80k€ per event) |
| 4 | Reduces deficiency probability significantly; prevents 5–15k€ rework per event |
| 3 | Reduces minor reviewer questions; prevents 1–5k€ rework per event |
| 2 | Improves traceability quality; indirect regulatory benefit |
| 1 | Operational efficiency only; no direct regulatory cost avoidance |

---

## Impact (1–5)

**What it represents:** Combined value of time saved for the team per event and quality of the output for the document owner receiving findings. A score of 5 means the use case saves 8+ hours per event with actionable, well-cited findings. A score of 1 means minimal time saving or low output quality.

**How it was estimated:** Based on time-and-motion analysis of SaMD change control workflows using the OpenRegulatory SOP template as a baseline (8–43 hours per moderate change across 4–6 roles). Blended hourly rate assumed at 130€ — loaded cost for senior regulatory, risk, and quality staff in Western European or comparable markets.

**Key assumption:** The agent achieves 30–60% automation of manual triage and document-update identification. If your team is significantly faster at manual review, reduce Impact scores accordingly.

---

## Confidence (0.5–1.0)

**What it represents:** Certainty that the benefit estimates for this use case will materialise as described. A score of 1.0 means the use case is well-understood, reference data exists, and the technical approach is proven. A score of 0.5 means significant unknowns remain.

**How it was estimated:** Based on three factors: maturity of the reference standards for this domain, availability of structured test data in the current corpus, and degree to which the technical approach has been validated.

**Key assumption:** Confidence scores should be updated after each release using actual finding acceptance rates as calibration data. If the acceptance rate from the initial release is below 70%, reduce all subsequent Confidence scores by 0.1. If above 85%, increase by 0.1.

---

## Effort (1–5)

**What it represents:** Build complexity from the AI Architect's perspective — integration effort, reference corpus preparation, and validation requirements. A score of 1 means the use case reuses existing infrastructure and can be implemented quickly. A score of 5 means significant new architecture is required.

**How it was estimated:** Based on the AI Architect's assessment of technical dependencies, reference corpus availability, and output format complexity.

**Key assumption:** Effort scores assume a single AI Architect working part-time. A dedicated full-time Architect reduces effective effort by approximately one point across all use cases.

---

## Per-use-case score breakdown

### UC1 — SRS monitoring and change classification

| Parameter | Value | Key assumption |
|---|---|---|
| Risk Savings | 4 | 20–40% baseline deficiency probability falls to 5–15% with systematic classification |
| Impact | 4 | 1–3 hours saved per change event across the team |
| Confidence | 0.9 | Test data and technical approach fully defined |
| Effort | 2 | Lowest build effort — document ingestion already scoped in PRD |
| **Score** | **72** | |

### UC3 — Risk traceability check

| Parameter | Value | Key assumption |
|---|---|---|
| Risk Savings | 5 | Broken traceability is the most common deficiency cause — 15–40k€ per avoided major round |
| Impact | 4 | 3–8 hours saved per safety-relevant change event |
| Confidence | 0.85 | Reference data and traceability table format defined; slight uncertainty on risk file format variability |
| Effort | 2 | Shares infrastructure with UC1 |
| **Score** | **85** | |

### UC2 — Baseline document to SRS suggestions

| Parameter | Value | Key assumption |
|---|---|---|
| Risk Savings | 3 | Prevents 10–25k€ in requirement gaps at first submission — indirect rather than direct deficiency prevention |
| Impact | 4 | 8–20 hours saved per baseline event during Phase 1 |
| Confidence | 0.75 | Suggestion quality depends on baseline document structure — narrative documents produce lower-quality suggestions |
| Effort | 3 | Requires baseline intake parser for multiple document types |
| **Score** | **30** | |

### UC7 — Usability engineering lifecycle integration

| Parameter | Value | Key assumption |
|---|---|---|
| Risk Savings | 4 | Post-summative study invalidation is a high-cost event (10–30k€ per occurrence) — comparable to a major deficiency round for UI-intensive products |
| Impact | 3 | High value for complex UI products; low value for products with no summative study requirement |
| Confidence | 0.75 | Post-summative monitoring logic is well-defined; formative study extraction quality depends on document structure |
| Effort | 3 | Reuses UC2 baseline intake and UC3 risk cross-check |
| **Score** | **30** | |

### UC5 — Cybersecurity change impact

| Parameter | Value | Key assumption |
|---|---|---|
| Risk Savings | 3 | Cybersecurity gaps are a growing deficiency source but per-finding cost is lower than risk traceability gaps |
| Impact | 3 | 3–8 hours saved per security-relevant SRS change |
| Confidence | 0.70 | Finding quality depends on threat model availability and structure — varies significantly by organisation |
| Effort | 3 | Requires cybersecurity sub-check module and OWASP/IEC corpus |
| **Score** | **21** | |

### UC4 — Change control plan boundary check

| Parameter | Value | Key assumption |
|---|---|---|
| Risk Savings | 5 | Undetected out-of-bounds change = unplanned submission — 43k€ average cost avoidance per event |
| Impact | 3 | High value for AI-enabled products only; zero value for non-AI |
| Confidence | 0.60 | PCCP guidance in draft; document structure varies widely; lowest confidence of any use case |
| Effort | 4 | Requires purpose-built change control plan parser in addition to classifier |
| **Score** | **23** | |

### UC6 — Inspection and submission preparation

| Parameter | Value | Key assumption |
|---|---|---|
| Risk Savings | 3 | Improved audit readiness reduces inspection findings but event frequency is low |
| Impact | 3 | 10–30 hours saved per audit preparation event |
| Confidence | 0.55 | Value depends entirely on completeness of findings history; output format varies by authority |
| Effort | 5 | Highest build effort — aggregation across all use cases plus format customisation |
| **Score** | **10** | |

---

## Economic trade-off framework

Beyond the priority scoring, the agent's findings enable a second type of economic analysis: whether a specific proposed SRS change should be made at all.

When the agent's outputs from UC1, UC3, and UC4 are combined, the team can estimate the full regulatory cost of implementing a proposed change — which documents must be updated, which submissions may be required, what verification work is triggered. Comparing this cost against the expected value of the change enables a documented build-versus-defer decision.

This is most impactful for UC4 (AI/ML changes that may exceed PCCP boundaries) but applies to any change that triggers multiple high-severity findings across different document areas simultaneously.

The economic trade-off output is described in `finding-lifecycle.md` as a special finding section. It does not change the disposition options but provides the information needed to make a rational scope decision.

---

## What this model does not capture

The scoring model does not capture:
- Strategic dependencies between use cases (UC1 is a prerequisite for everything — this is handled in the roadmap, not the scores)
- Compounding multi-market effect (dual-market submissions multiply avoided cost — the model uses single-market estimates)
- Time-to-market acceleration value
- Knowledge retention value

All of these would increase the ROI figures if quantified.

---

## Data quality caveat

The cost and time benchmarks are calibrated against the OpenRegulatory MAGIC DICOM Viewer template (Class B SaMD, 18 software requirements, 20 risk table entries) and analysis of a complex multi-integration SaMD product active in both FDA and EU markets. These are representative baselines, not universal. Teams on simpler products should use the lower end of all ranges. Teams on Class III / PMA-level products should consider the upper end or beyond.

These are order-of-magnitude estimates calibrated against industry benchmarks, not your specific product's historical data. Replace estimates with actuals as soon as measurement data is available.

---

## Update schedule

| Parameter | Owner | Update trigger |
|---|---|---|
| Risk Savings | Regulatory Affairs / PM | Major guidance change or new product risk class in either jurisdiction |
| Impact | PM (with regulatory input) | After each release, based on document owner feedback |
| Confidence | PM + AI Architect jointly | After each release, based on empirical acceptance rate data |
| Effort | AI Architect | Before each release scoping session |

After the initial release: update Confidence scores for UC2, UC4, UC5, and UC7 based on actual UC1/UC3 finding acceptance rates.

After Release 2: update UC4's Effort score based on AI Architect's assessment of structured document parsing complexity encountered during UC2 implementation (baseline intake parser).

After a major regulatory guidance update (FDA AI/ML guidance finalisation; EU AI Act Article 83 implementing acts): review Risk Savings scores for UC4 and UC7.

After 6 months of production data: replace Phase 2 time-saving estimates with actuals from real finding events.

---

## Worked scoring examples

These examples show the full arithmetic behind two scores at opposite ends of the priority ranking. Use them to sanity-check any proposed parameter change.

### UC1 — SRS monitoring and change classification

Parameters: Risk Savings = 4, Impact = 4, Confidence = 0.9, Effort = 2

```
Score = (4 × 4 × 0.9) / 2 × 10
      = (14.4) / 2 × 10
      = 7.2 × 10
      = 72
```

UC1 benefits from high confidence (test data and technical approach fully defined) and low effort (document ingestion already scoped). If a challenger proposes reducing Impact from 4 to 3 (team is faster at manual review than assumed), the score drops to 54 — still second place, but the gap with UC3 narrows.

### UC4 — Change control plan boundary check

Parameters: Risk Savings = 5, Impact = 3, Confidence = 0.6, Effort = 4

```
Score = (5 × 3 × 0.6) / 4 × 10
      = (9) / 4 × 10
      = 2.25 × 10
      = 23
```

UC4 has Risk Savings = 5 (matching UC3) but scores 23 versus UC3's 85. The difference is entirely in Confidence (0.6 vs 0.85) and Effort (4 vs 2). If the FDA PCCP guidance finalises and confidence rises to 0.8, and if the parser effort is lower than feared (Effort = 3), the score becomes 40 — still behind UC2/UC7 but meaningfully higher. This is the correct trigger to re-evaluate UC4's release placement.
