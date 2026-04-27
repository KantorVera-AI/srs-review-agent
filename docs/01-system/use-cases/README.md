**Status:** Stable
**Owner:** Product Management
**Audience:** AI Architect, PM

---

# Use Cases

One file per use case. Each file contains: one-line description, trigger, output routing, RICE score, Phase 1 and Phase 2 benefit breakdown, assumptions, dependencies, risks, and regulatory basis.

The UC1–UC7 numbering is the canonical ROI-based taxonomy used across all documentation. See `prd.md` for the functional workflow trigger descriptions.

| File | Use case | Release | RICE score |
|---|---|---|---|
| [`1-uc1-srs-monitoring.md`](1-uc1-srs-monitoring.md) | SRS monitoring and change classification | Initial release | 72 |
| [`2-uc3-risk-traceability.md`](2-uc3-risk-traceability.md) | Risk traceability check | Initial release | 85 |
| [`3-uc2-baseline-to-srs.md`](3-uc2-baseline-to-srs.md) | Baseline document to SRS suggestions | Release 2 | 30 |
| [`4-uc5-cybersecurity.md`](4-uc5-cybersecurity.md) | Cybersecurity change impact | Release 2 | 21 |
| [`5-uc7-usability-engineering.md`](5-uc7-usability-engineering.md) | Usability engineering lifecycle integration | Release 2 | 30 |
| [`6-uc4-change-control-plan.md`](6-uc4-change-control-plan.md) | Change control plan boundary check | Release 3 | 23 |
| [`7-uc6-inspection-prep.md`](7-uc6-inspection-prep.md) | Regulatory inspection and submission preparation | Later | 10 |

**Dependency chain:** UC1 → UC3 (initial release) → UC2, UC5, UC7 (Release 2) → UC4 (Release 3) → UC6 (Later).

UC1 is a prerequisite for all other use cases. UC3 shares infrastructure with UC1 and is built in the same release.