**Status:** Working draft
**Owner:** Product Management
**Audience:** All stakeholders

---

# AI Legislation and Standards

This document covers the regulatory and standards landscape specifically applicable to AI-enabled SaMD products. It is relevant only for products that incorporate machine learning, AI-driven decision support, or adaptive algorithms. Teams developing non-AI SaMD can skip this document.

The agent itself is not subject to these obligations — it is decision-support software, not a medical device. But the SaMD products it monitors may be subject to all of these frameworks, and the agent's reference corpus and finding logic must reflect them.

---

## The dual-framework challenge for AI-enabled SaMD

An AI-enabled SaMD operating in the EU faces two parallel regulatory frameworks simultaneously: EU MDR (governing it as a medical device) and the EU AI Act (governing it as a high-risk AI system). These frameworks have overlapping but not identical requirements. A team that satisfies EU MDR documentation requirements is not automatically compliant with EU AI Act obligations, and vice versa.

In the US, the challenge is simpler in structure — FDA governs AI-enabled SaMD through a combination of device classification regulations and AI-specific guidance — but the guidance landscape was still evolving as of early 2026.

---

## EU AI Act

**Regulation (EU) 2024/1689, in force August 2024. High-risk AI system obligations phasing in through August 2026.**

### Applicability to AI-enabled SaMD

The EU AI Act classifies AI systems into risk categories. AI-enabled SaMD is presumptively high-risk under Annex III, point 5(b) — AI systems intended to be used for making decisions, or decisively influencing decisions, related to the health and safety of persons. This applies regardless of the device's MDR classification.

A product that is Class IIa under EU MDR may still be high-risk AI under the AI Act if its AI component makes or significantly influences clinical decisions.

### Key obligations relevant to SRS content

**Article 14 — Human oversight.** High-risk AI systems must be designed and developed with human oversight measures built into the system itself, not just documented as a policy. This means the SRS must contain specific requirements for:
- Mechanisms allowing human operators to understand the system's outputs
- Mechanisms allowing human operators to override or interrupt the system
- Safeguards preventing over-reliance on the system's outputs

These are a new class of SRS requirements that EU MDR does not explicitly require. The agent's UC1 classifier should flag changes to these requirements as high-priority, and the agent's reference corpus must include Article 14 as a citation source.

**Article 15 — Accuracy, robustness, and cybersecurity.** High-risk AI systems must achieve appropriate levels of accuracy and be robust against errors, faults, and inconsistencies. They must also be resilient against attempts by third parties to alter their use or performance through adversarial inputs. These obligations generate SRS requirements for:
- Performance specifications with defined accuracy thresholds
- Input validation requirements
- Adversarial robustness requirements (relevant for UC5, cybersecurity)
- Drift monitoring requirements for deployed models

**Article 11 and Annex IV — Technical documentation for the AI system.** In addition to the MDR technical file, an AI Act technical documentation package is required. This includes:
- A general description of the AI system and its intended purpose
- A description of the development process including training data and data governance
- Information about the monitoring, functioning, and control of the system
- A description of the changes made to the system and its performance
- Assessment of the human oversight measures

This is a separate documentation obligation from the MDR technical file. Some elements overlap (intended use, performance specifications) but others are unique to the AI Act (training data governance, model architecture description).

**Article 83 — Post-market modifications (change control).** Changes to a high-risk AI system that affect its conformity with the AI Act requirements must be assessed before implementation. Article 83 is the EU equivalent of FDA's PCCP concept — it allows manufacturers to pre-specify the types of AI system modifications that remain within the original conformity assessment. Changes outside this scope require a new conformity assessment.

The interaction between Article 83 (AI Act change control) and EU MDR Article 83 (post-market modifications) is not yet fully resolved in implementing guidance as of early 2026. The agent's UC4 must handle both frameworks and flag when a SRS change may trigger obligations under either or both.

### Relationship to EU MDR

Where the AI Act and EU MDR impose overlapping requirements, compliance with one does not automatically imply compliance with the other. However, the European Commission has provided guidance (MDCG and AI Office joint guidance, expected 2025-2026) on how to align the two technical documentation packages to reduce duplication.

The agent's reference corpus should include both frameworks and flag findings with the applicable citation — MDR, AI Act, or both — depending on which obligation the finding relates to.

---

## US FDA — AI/ML framework

**No single AI-specific regulation as of early 2026. Governed by a combination of existing device regulations and AI-specific guidance documents.**

### Key FDA documents

**Guidance on predetermined change control plans for machine learning-enabled medical devices (2023 draft, anticipated finalisation 2026).** The PCCP mechanism allows manufacturers to pre-specify the types of algorithm changes they may make post-approval without requiring a new submission. The PCCP must describe: the types of modifications anticipated, the performance specifications that bound those modifications, and the methodology used to implement and validate changes.

The PCCP is the US equivalent of EU AI Act Article 83. Both frameworks require that changes outside the approved scope trigger a new regulatory assessment. The agent's UC4 checks whether a SRS change stays within PCCP boundaries or triggers a new submission requirement.

**Guidance on content of premarket submissions for device software functions (2023).** Defines the documentation required for AI/ML-enabled devices in premarket submissions, including algorithm description, training data governance, performance testing methodology, and change management approach.

**FDA AI Action Plan (2025).** Describes FDA's approach to AI governance including algorithmic transparency expectations — the requirement that the basis for AI-generated outputs be explainable to clinical users. This generates SRS requirements for explainability that are distinct from performance specifications.

**Good machine learning practice (GMLP) guiding principles (2021, joint with Health Canada and UK MHRA).** Defines best practices for AI/ML medical device development including data management, model training, clinical evaluation, and post-market monitoring. While not a regulation, these principles are expected in submissions.

### Algorithmic transparency as an SRS requirement category

FDA's increasing focus on algorithmic transparency means that for AI-enabled SaMD, the SRS must contain requirements specifically addressing how the system communicates the basis for its outputs to clinical users. A requirement that says "the system shall display a confidence score" has a specific regulatory origin (FDA AI guidance) and a specific verification obligation that differs from a functional requirement.

The agent's reference corpus should include this as a distinct requirement category, separate from functional requirements and performance specifications.

---

## ISO/IEC 42001:2023 — AI Management System

ISO/IEC 42001 defines requirements for establishing, implementing, maintaining, and continually improving an AI management system within an organisation. It is to AI governance what ISO 13485 is to medical device quality management.

As of early 2026, ISO/IEC 42001 is not a harmonised standard under EU MDR and is not a recognised standard under FDA. However, it is increasingly cited by regulatory bodies as a framework for demonstrating AI governance maturity, and conformity with it is expected to become a marker of good practice in regulated AI system development.

For teams developing AI-enabled SaMD, ISO/IEC 42001 adds the following relevant concepts that may generate SRS requirements:

- Data governance and data quality management for training and validation datasets
- AI risk management as a process integrated with (but separate from) ISO 14971 product risk management
- Transparency and explainability as system design requirements
- Ongoing monitoring and performance tracking as operational requirements

---

## ISO 14971 Amendment 1 — AI-specific hazards (anticipated 2025–2026)

ISO 14971:2019 Amendment 1 is expected to add specific guidance on AI-related hazard categories. The anticipated additions address failure modes specific to machine learning that are not well-covered by the 2019 version:

- **Distributional shift** — the AI system encounters input data in deployment that differs from the training distribution, causing degraded performance
- **Adversarial inputs** — deliberately crafted inputs that cause the AI system to produce incorrect outputs
- **Model degradation over time** — performance drift in deployed models due to changes in the patient population, clinical practice, or data collection methods

When published, this amendment will directly affect UC3 (risk traceability check) by adding new hazard categories that must be present in the risk management file and linked to SRS requirements. The agent's risk traceability reference corpus will need to be updated to include these categories.

---

## IEC TR 81001-5-2 — Cybersecurity guidance for AI health software (2024 draft)

IEC TR 81001-5-2 supplements IEC 81001-5-1 with specific guidance for AI-enabled health software. Key additions relevant to SRS requirements:

- Security requirements for training pipelines and model artefacts
- Protection against adversarial attacks on inference components
- Requirements for monitoring and detecting anomalous model behaviour in deployment

This is a technical report (TR) rather than a standard — it provides guidance rather than requirements. However, its content is expected to inform future normative requirements and is already referenced in cybersecurity assessments for AI-enabled SaMD submissions.

---

## Summary — additional SRS requirement categories for AI-enabled products

Teams developing AI-enabled SaMD should ensure their SRS contains requirements in the following categories, in addition to the standard IEC 62304 requirements. The agent's finding logic for AI-enabled products covers all of these.

| Requirement category | Regulatory origin | UC that checks it |
|---|---|---|
| Human oversight mechanisms | EU AI Act Article 14 | UC1 (change classification) |
| AI output explainability | FDA AI guidance | UC1 |
| Performance specifications with accuracy thresholds | EU AI Act Article 15, FDA AI guidance | UC1, UC4 |
| Input validation and adversarial robustness | EU AI Act Article 15, IEC TR 81001-5-2 | UC1, UC5 |
| Drift monitoring requirements | ISO 14971 (anticipated amendment), GMLP | UC3, UC4 |
| Change control plan boundaries | FDA PCCP guidance, EU AI Act Article 83 | UC4 |
| Training data governance | EU AI Act Annex IV, FDA AI guidance | UC4 |
| Post-market performance monitoring | EU AI Act Article 72, FDA GMLP | UC6 (future) |

---

## Monitoring this landscape

The AI legislation and standards landscape is moving faster than any other area of medical device regulation. The following items were in active development as of early 2026 and may have changed:

- EU AI Act implementing acts and delegated regulations (2025–2026)
- FDA PCCP guidance finalisation (anticipated 2026)
- ISO 14971 Amendment 1 publication
- MDCG / AI Office joint guidance on MDR and AI Act alignment
- ISO/IEC 42001 harmonisation status under EU MDR

The `docs/00-overview/classification-reference.md` classification sensitivity table and the UC4 confidence score in `docs/02-roi/assumptions.md` are the two places in this documentation suite most sensitive to changes in this landscape. They should be reviewed whenever a significant guidance document is published or updated.