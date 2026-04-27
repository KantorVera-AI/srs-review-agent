**Status:** Stable
**Owner:** Product Management
**Audience:** All stakeholders

---

# ROI and Prioritisation

Decision-support documentation covering use case scoring, roadmap rationale, financial analysis, and the assumptions that underpin every score.

| Document | Status | Description |
|---|---|---|
| [`1-master-overview.md`](1-master-overview.md) | Working draft | Complete ROI picture at summary depth — all seven use cases, scoring, classification sensitivity, roadmap summary, value proposition |
| [`2-roadmap.md`](2-roadmap.md) | Working draft | Release structure, dependency chain, multi-dimensional sequencing rationale, AI Architect validation criteria per release |
| [`3-mvp-specification.md`](3-mvp-specification.md) | Working draft | UC1 and UC3 in full detail — metadata prerequisite, Phase 1 and Phase 2 ROI, break-even analysis, validation criteria |
| [`4-assumptions.md`](4-assumptions.md) | Working draft | Parameter reference (Risk Savings, Impact, Confidence, Effort), per-use-case score breakdown, economic trade-off framework, update schedule |
| [`roi-analysis-full.md`](roi-analysis-full.md) | Deprecated | Full v2 ROI analysis — detailed UC1–UC6 analysis with glossary and worked examples. Superseded by v3 suite. UC7 and IMDRF framework not reflected. |
| [`5-dataset-spec.md`](5-dataset-spec.md) | Working draft | Synthetic test corpus specification — corpus types, ID conventions, 20 evaluation scenarios |
| [`6-evaluation-plan.md`](6-evaluation-plan.md) | Working draft | Technical and product metrics, test scenario index, update schedule |
| [`7-risk-model.md`](7-risk-model.md) | Working draft | Synthetic risk management file used as UC3 test data |

> The document master list, SRS change impact matrix, and owner directory have been moved to `docs/03-integration/` — they are integration configuration references, not ROI analysis.

**Reading order:** `1-master-overview.md` → `2-roadmap.md` → `3-mvp-specification.md` → `4-assumptions.md` (if challenging a number).

**How to challenge a score:** Go to `4-assumptions.md`. Identify the parameter and assumption. Propose a revised value. Re-run the formula. Update the relevant use case file in `01-system/use-cases/` and `2-roadmap.md` if release sequencing is affected.
