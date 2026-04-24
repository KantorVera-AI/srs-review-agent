**Status:** Working draft
**Owner:** Product Management
**Audience:** PM, AI Architect, advisors

---

# Roadmap

Defines the release structure, the rationale for sequencing, the dependency chain, and what must be validated before each release begins.

---

## Release structure

| Release | Use cases | Core rationale |
|---|---|---|
| **Initial release** | UC1 + UC3 | Foundation — monitoring loop and traceability. Validates the core hypothesis. Applicable to all classification tiers from day one. |
| **Release 2** | UC2 + UC5 + UC7 | Extensions — baseline intake, cybersecurity, usability engineering. All reuse initial release infrastructure. Can be built in parallel. |
| **Release 3** | UC4 | AI/ML change control plan boundary check. Requires stable pipeline, validated classifier precision, and regulatory guidance maturity. AI-enabled products only. |
| **Later** | UC6 | Inspection and submission preparation. Requires 6+ months of production findings history. |

---

## Dependency chain

```
UC1 — SRS monitoring and change classification
  │
  └── UC3 — Risk traceability check
        │    (built together with UC1, same infrastructure)
        │
        ├── UC2 — Baseline to SRS suggestions
        │         (Release 2 — extends ingestion pipeline)
        │
        ├── UC5 — Cybersecurity change impact
        │         (Release 2 — extends classifier routing)
        │
        ├── UC7 — Usability engineering lifecycle integration
        │         (Release 2 — reuses UC2 baseline intake + UC3 risk cross-check)
        │
        └── UC4 — Change control plan boundary check
                  (Release 3 — requires stable pipeline + guidance maturity)

UC1, UC2, UC3, UC4, UC5, UC7 → UC6 — Inspection and submission preparation
                  (Later — aggregates data from all previous use cases)
```

UC1 is a prerequisite for every other use case. No other use case can function without it.

---

## Sequencing rationale

### Why UC1 and UC3 together in the initial release

UC1 and UC3 share the same core infrastructure — the document ingestion layer, the SRS parser, the RAG retrieval engine, the findings generator, and the notification router. Building them in the same release is more efficient than building them sequentially, and together they deliver the complete monitoring → classification → traceability → finding workflow that constitutes the minimum viable product.

UC3 has the highest RICE score of any use case (85) because broken risk control traceability is the most common cause of regulatory deficiency rounds in both EU MDR and FDA submissions. Placing it in the initial release alongside UC1 means the first deployment already demonstrates the agent's core regulatory value.

### Why UC7 moves to Release 2 (not later)

UC7 was originally proposed for Release 2 and this placement is confirmed. The rationale: usability engineering obligations exist at all classification tiers and for all product types. UC7 reuses UC2's baseline intake mechanism (for summative study baseline) and UC3's risk cross-check infrastructure (for use error to hazard mapping) — so the incremental build effort is low once those are in place. The post-summative SRS change monitoring is a quality gate that teams need active from the point their first summative study is completed, which for many products happens during initial development before Release 3 would be available.

### Why UC4 waits for Release 3

UC4 (AI/ML change control plan boundary check) has the highest potential regulatory cost avoidance of any use case but the lowest confidence score (0.60). Two factors justify the wait:

First, the regulatory guidance for AI/ML change control plans was still maturing as of early 2026 — FDA PCCP guidance in draft, EU AI Act Article 83 implementing acts in development. Building a boundary checker before the guidance stabilises produces a tool that needs significant rework.

Second, UC4 requires a purpose-built change control plan document parser in addition to the standard classifier. This parser cannot be validated without real or realistic change control plan documents to test against. The empirical data from UC1–UC5 will calibrate the classifier precision needed to make UC4 reliable.

### Why UC6 is last

UC6 (inspection and submission preparation) is a reporting layer that aggregates data from all previous use cases. Its output quality is directly proportional to the completeness and consistency of the findings history it draws from. Building UC6 before 6 months of production history exists produces a tool with little to report — and potentially a false sense of audit readiness that is worse than no tool at all.

---

## Multi-dimensional sequencing factors

The roadmap is not determined by RICE scores alone. Five dimensions affect the correct sequencing:

**Use case readiness** — RICE score and dependency chain (primary driver of the order above).

**Product type** — UC4 has zero value for non-AI SaMD. UC7 has reduced value for products with no summative usability study requirement. Teams deploying the agent for a non-AI product can skip UC4 entirely and configure UC7 at a lower sensitivity.

**Classification tier** — Higher classification tiers gain more value from the agent sooner. A Category IV product team has stronger incentive to deploy UC1 and UC3 immediately than a Category I team. Release 2 is similarly more urgent for teams with complex interfaces (UC7) and connected architectures (UC5).

**Market scope** — Dual-market EU/US teams have the strongest ROI case for every use case because the avoided cost is additive across markets. Multi-market teams should prioritise earlier deployment and more complete release coverage.

**Documentation maturity** — Teams with well-structured, already-tagged SRS documentation can deploy the initial release immediately. Teams with unstructured documentation need to invest in metadata preparation (IMDRF category, software item safety class tagging) before classification-calibrated output is available. See `docs/03-integration/metadata-spec.md`.

---

## What the AI Architect must validate before each release

### Before initial release

- [ ] Change detection and SRS diff parser correctly handle the synthetic corpus
- [ ] All six change type classifiers (clinical, risk/safety, UI/workflow, security, AI/ML, non-functional) achieve ≥85% precision on the evaluation test scenarios
- [ ] IMDRF Category I and Category IV produce visibly different output depth for the same change type
- [ ] Reclassification trigger fires correctly on evaluation scenarios 12 and 13
- [ ] Missing metadata fallback behaviour matches specification in `output-calibration.md`
- [ ] Finding routing delivers to the correct owner role in all test scenarios
- [ ] Audit log is append-only and exports correctly to a structured file format

### Before Release 2

- [ ] Baseline intake parser handles risk management plan and usability engineering plan document types
- [ ] Threat model format for UC5 is confirmed — structured table or narrative? Parser needed?
- [ ] UC7 post-summative monitoring correctly identifies use scenarios from the summative baseline
- [ ] Integration configuration UI is functional for Tier 1 and Tier 2 connections
- [ ] Classifier precision data from initial release is reviewed — any change type with <85% precision must be addressed before Release 2 extends the routing

### Before Release 3

- [ ] Change control plan guidance landscape re-assessed — FDA PCCP guidance finalised? EU AI Act Article 83 implementing acts published?
- [ ] Structured change control plan document format agreed with RA/PRRC
- [ ] Change control plan parser scoped and validated against at least one real or realistic PCCP document
- [ ] Release 2 classifier precision data confirms the AI/ML behaviour classification is reliable enough to be the UC4 trigger

---

## Roadmap update triggers

This roadmap should be reviewed when:

- A use case's Confidence score changes materially (see `assumptions.md`)
- A major regulatory guidance document is published that affects UC4 or UC7
- Empirical data from a production release shows a use case is delivering significantly more or less value than estimated
- A new use case candidate is identified (PMS-triggered changes, SOUP monitoring, localisation cascade — all currently in the backlog)

---

## Backlog — future use case candidates

These are not in the current roadmap but have been identified as candidates for post-Release 3 consideration based on the analysis to date.

| Candidate | Description | Why not now |
|---|---|---|
| PMS-triggered change assessment | When a complaint or adverse event maps to a specific SRS requirement, trigger a change impact assessment | Requires post-market surveillance system integration and CAPA linkage — complex dependencies |
| SOUP monitoring | When a SOUP component receives a vulnerability disclosure or version update, flag SRS requirements that may be affected | Requires SBOM integration and vulnerability feed — separate infrastructure |
| Localisation cascade | When a SRS change affects user-facing text, flag all translated documentation that requires updating | Lower regulatory priority; high organisational variability |
| Design review support | Generate a pre-review summary of open findings and traceability gaps ahead of a formal design review milestone | Close to UC6 but different audience and trigger — worth distinguishing once UC6 is built |
