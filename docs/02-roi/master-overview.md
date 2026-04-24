**Status:** Working draft
**Owner:** Product Management
**Audience:** All stakeholders

---

# Master Overview — Use Case ROI & Prioritisation

This document provides the complete ROI picture at summary depth. It covers all seven use cases, the scoring methodology, the classification sensitivity framework, the roadmap, and the overall value proposition.

For the full scoring rationale and parameter definitions, see `assumptions.md`. For UC1 and UC3 in full detail, see `mvp-specification.md`. For the full release plan, see `roadmap.md`.

---

## One-line thesis

> The SRS Review Agent prioritises use cases using a regulatory-value-based scoring model that is product-agnostic, classification-dependent, and designed to support both EU MDR and FDA workflows.

---

## Why this agent exists

In regulated SaMD development, every change to an SRS or risk file must be assessed for its impact on related controlled documents. This assessment is mandated by IEC 62304 sections 5.7–5.8, ISO 14971 sections 6–7, EU MDR change control requirements, and FDA 21 CFR 820.30. When done manually it is slow, inconsistent, and error-prone.

The consequences are concrete. A missed risk control link causes a deficiency round — 10–40k€ of additional effort per round. An AI/ML model update that exceeds change control plan boundaries without being flagged triggers an unplanned regulatory submission. Poor traceability discovered during an inspection delays market access by months.

The agent catches these gaps systematically, with citations, before they reach the regulatory reviewer.

---

## Scoring methodology

The agent uses an adapted RICE framework. Standard RICE uses Reach (user count) as a value driver. For this product, the value driver is regulatory cost avoidance — not user count. Reach is replaced by **Risk Savings**.

```
Score = (Risk Savings × Impact × Confidence) / Effort × 10
```

| Parameter | Scale | What it measures |
|---|---|---|
| Risk Savings | 1–5 | Regulatory cost avoidance — deficiency rounds, unplanned submissions, inspection findings |
| Impact | 1–5 | Team time saved + quality of output delivered to document owners |
| Confidence | 0.5–1.0 | Certainty that benefit estimates will materialise given current knowledge |
| Effort | 1–5 | AI Architect build complexity (1 = simple, 5 = highly complex) |

Effort is in the denominator — higher effort reduces the score. The score is a **relative priority index**, not a financial ROI model. For financial ROI figures, see `mvp-specification.md` and `assumptions.md`.

---

## Use case summary

| Use case | Risk savings | Impact | Confidence | Effort | Score | Phase 1 saving | Phase 2 / yr | Tier |
|---|---|---|---|---|---|---|---|---|
| UC3 Risk traceability | 5 | 4 | 0.85 | 2 | **85** | 20–100 h | 24–160 h | Initial release |
| UC1 SRS monitoring | 4 | 4 | 0.90 | 2 | **72** | 15–160 h | 20–120 h | Initial release |
| UC2 Baseline → SRS | 3 | 4 | 0.75 | 3 | **30** | 24–120 h | 2–24 h | Release 2 |
| UC7 Usability engineering | 4 | 3 | 0.75 | 3 | **30** | 6–32 h | 2–18 h | Release 2 |
| UC4 Change control plan | 5 | 3 | 0.60 | 4 | **23** | 9–80 h | 10–150 h | Release 3 |
| UC5 Cybersecurity | 3 | 3 | 0.70 | 3 | **21** | 10–75 h | 6–64 h | Release 2 |
| UC6 Inspection prep | 3 | 3 | 0.55 | 5 | **10** | 15–80 h | 5–30 h | Later |

---

## Why the ranking is what it is

**UC3 scores highest** despite not being the most visible use case. Broken traceability between risk controls and SRS requirements is consistently the most common cause of deficiency rounds in SaMD submissions — cited in both EU MDR notified body findings and FDA additional information requests. It is also cheap to build (Effort: 2) because it shares infrastructure with UC1.

**UC1 scores second** because it is the prerequisite for everything else. Its confidence score is the highest (0.90) because the test data, reference corpus, and technical approach are all defined and available.

**UC7 scores equal to UC2** at 30 — both Release 2 use cases. UC7 was not in the original v2 analysis. Its Risk Savings score of 4 reflects the specific high cost of a post-summative study invalidation event, which is among the most disruptive regulatory events during initial development for UI-intensive products.

**UC4 has Risk Savings 5 — matching UC3** — but its RICE score is 23 because of low confidence (0.60) and high effort (4). The AI/ML change control plan guidance landscape was still maturing as of early 2026. Building it before the guidance stabilises produces a checker that needs rework.

**UC6 scores lowest** not because inspection preparation is unimportant — it is critical — but because its output quality depends entirely on data that does not yet exist when it is built.

---

## Classification sensitivity

The agent's outputs are classification-dependent. The same use case produces different findings for different products.

| IMDRF Category | Finding type | Routing | Escalation |
|---|---|---|---|
| I | Advisory | SRS owner only | Not automatic |
| II | Standard finding | SRS owner + document owner | On Critical only |
| III | Standard with mandatory review | + RA notification | On High and Critical |
| IV | Mandatory finding | + RA/PRRC mandatory | On all above Low |

Software item safety class adds a second dimension. A Class C requirement in a Category II product receives fuller citation depth and stricter evidence requirements than a Class A requirement in the same product.

When both inputs are present, the more stringent calibration applies per dimension independently. See `output-calibration.md` for the full matrix.

---

## Two phases of ROI

Every use case delivers value in two distinct phases:

**Phase 1 — Initial development and first submission:** The agent catches gaps before they reach the regulatory reviewer. A gap discovered internally costs 5–20k€ to fix. The same gap discovered by the regulatory reviewer costs 10–40k€ per deficiency round plus weeks of delay. The agent's value in Phase 1 is the cost difference between those two outcomes.

**Phase 2 — Ongoing maintenance and change management:** After first approval, every change must be assessed for regulatory impact. Without the agent, this takes 8–43 hours of expert time per moderate change. The agent automates 30–60% of this, with consistent quality.

Teams deploying the agent during initial development benefit from both phases. Teams deploying to an existing product primarily benefit from Phase 2 efficiency.

---

## Multi-market value

For products filing simultaneously to EU and US markets, a single traceability gap caught by the agent prevents a deficiency in both markets simultaneously. The avoided cost is additive — one finding can prevent two deficiency rounds.

For dual-market EU/US products at IMDRF Category III, the expected annual value of UC1 and UC3 combined is approximately 20–60k€ in avoided deficiency cost and 40–280 hours of saved expert time — before accounting for Phase 1 gap prevention.

---

## What this model does not include

This analysis does not quantify:
- Time-to-market acceleration value — faster, more confident submissions create competitive advantage
- Knowledge retention — institutional knowledge about which SRS changes affect which documents is currently held by individuals; the agent makes it systematic and durable
- Onboarding cost reduction — new regulatory or quality staff can operate to a consistent standard from day one
- Compounding multi-market effect — for products in three or more markets, avoided cost multiplies further

All of these would increase the ROI figures if quantified. The model is intentionally conservative.

---

## How to challenge these numbers

Go to `assumptions.md`. Identify the parameter (Risk Savings, Impact, Confidence, or Effort) and the assumption behind it. Propose a revised value. Re-run the formula. The score will shift and the roadmap may shift with it. That is the intended behaviour — this is a working document, not a fixed plan.
