# SRS Review Agent — Use Case ROI & Prioritization

**Status:** Deprecated
**Owner:** Product Management
**Audience:** PM, AI Architect, regulatory/quality consultants, advisors

> **Note:** This is the full v2 ROI analysis. The canonical v3 documents are [`master-overview.md`](master-overview.md), [`assumptions.md`](assumptions.md), [`mvp-specification.md`](mvp-specification.md), and [`roadmap.md`](roadmap.md). This document is retained as a detailed reference — particularly the glossary, worked scoring examples, and dual-jurisdiction benefit notes. UC7 and the IMDRF classification framework are not reflected here.

---

## Glossary of key terms

| Term | Definition |
|------|-----------|
| **SaMD** | Software as a Medical Device. Software that performs a medical function without being part of a hardware medical device. Subject to regulatory oversight in all major markets. |
| **SRS** | Software Requirements Specification. The controlled document that defines what the software must do. Central artifact in the IEC 62304 software lifecycle. |
| **Regulatory reviewer** | The authority responsible for assessing a submission or change. In the EU this is a Notified Body (NB) — an accredited third-party organisation. In the US this is the FDA (Food and Drug Administration). In other markets, equivalent national authorities apply. |
| **Submission** | A formal application to a regulatory authority to place a device on the market, or to register a significant change to an approved device. Examples: 510(k) or De Novo request (FDA); CE marking application under MDR (EU). |
| **Significant change** | A change to a device that, under applicable regulations, requires a new or updated submission to the regulatory authority before the change can be implemented. Criteria differ by jurisdiction. |
| **Deficiency / deficiency round** | When a regulatory reviewer identifies gaps or inconsistencies in a submission, they issue a list of deficiencies (FDA: additional information request; EU: list of outstanding issues). Each round of deficiency resolution adds cost and delay. |
| **Technical File / DHF** | Technical File (EU MDR) or Design History File (US FDA): the complete record of evidence supporting a device's safety and performance claims. Must be kept current throughout the device lifecycle. |
| **IEC 62304** | International standard for the software lifecycle of medical device software. Defines requirements for planning, development, testing, maintenance, and change management. |
| **ISO 14971** | International standard for risk management for medical devices. Defines the process for identifying hazards, estimating and evaluating risks, and implementing risk controls. |
| **Risk control** | A measure taken to reduce the probability or severity of a harm caused by a hazard. Risk controls must be implemented in the SRS as verifiable requirements. |
| **MDR** | EU Medical Device Regulation 2017/745. The primary regulatory framework for medical devices in the European Union. |
| **FDA** | US Food and Drug Administration. The US federal agency responsible for regulating medical devices in the United States. |
| **PCCP** | Predetermined Change Control Plan. An FDA mechanism that allows manufacturers of AI/ML-enabled devices to pre-specify the types of changes they may make without requiring a new submission. The EU equivalent concept appears in Article 83 of the EU AI Act. |
| **OWASP / ASVS** | Open Web Application Security Project / Application Security Verification Standard. A freely available framework of security requirements used to assess the security of software applications. |
| **IEC 81001-5-1** | International standard for cybersecurity activities in the health software lifecycle. Defines security requirements from design through maintenance. |
| **QMS** | Quality Management System. The set of processes, procedures, and controls a manufacturer uses to ensure consistent product quality and regulatory compliance. Often aligned with ISO 13485. |
| **RAG** | Retrieval-Augmented Generation. An AI architecture in which a language model retrieves relevant context from a document index before generating a response. Used in this agent to provide citation-backed findings. |
| **RICE** | A product prioritisation framework: Reach × Impact × Confidence / Effort. Adapted in this document — see section 3. |
| **V-model** | A software development model in which each development phase has a corresponding verification or validation phase. Standard in regulated medical device development. |
| **PRRC** | Person Responsible for Regulatory Compliance. A mandatory role under EU MDR Article 15, responsible for ensuring regulatory obligations are met. |

---

## Table of contents

1. Purpose and how to use this document
2. Context and framing
3. Scoring methodology
4. Parameter reference
5. Use case analysis (UC1–UC6)
6. Comparative view
7. Roadmap recommendation
8. Assumptions and limitations
9. How to update this document

---

## 1. Purpose and how to use this document

This document answers one question clearly: **which use cases of the SRS Review Agent should be built first, and why?**

It is addressed to anyone who joins this project — whether as a technical contributor, a regulatory consultant, an advisor, or a new team member. No prior context is assumed. The document stands alone.

It serves three related purposes. First, it documents the reasoning behind the release roadmap so that decisions are traceable rather than implicit. Second, it provides a structured basis for challenging estimates — if you disagree with a score or a figure, the parameter reference in section 4 is the right place to start. Third, it gives the AI Architect a concrete input for scoping each release.

**How to read this document if you are:**

- A decision-maker reviewing the roadmap: read sections 1, 2, 6, and 7.
- An AI Architect scoping a release: read sections 3, 4, and the relevant use case in section 5.
- A regulatory or quality consultant validating the assumptions: read sections 2, 4, and 8.
- A new team member getting up to speed: read the full document in order.

**How to challenge this document:** The scores are estimates built on explicit assumptions. Every assumption is named in section 4. If a figure seems wrong, identify which parameter you would change, by how much, and why — then re-run the formula from section 3. The scores will shift, and the roadmap may shift with them. That is the intended behaviour.

---

## 2. Context and framing

### What the SRS Review Agent is

The SRS Review Agent is an AI decision-support tool that integrates into the document management and change control workflow of a Software as a Medical Device (SaMD) team. When a Software Requirements Specification (SRS) or related controlled document is modified, the agent analyses the change against applicable regulatory standards, generates proposed findings with citations, and routes them to the relevant document owner for review and disposition. It does not create, approve, or finalise requirements. All findings are non-binding. Human reviewers retain full accountability for all regulatory decisions. Full product scope is defined in the product requirements document.

> **Key term — SaMD:** Software as a Medical Device. Software that performs a medical function without being part of a hardware medical device. Subject to regulatory oversight in all major markets — including EU MDR, US FDA, Health Canada, TGA (Australia), and others.

### Regulatory applicability

This document and the use cases it describes are applicable to both the **EU regulatory framework** (Medical Device Regulation 2017/745, harmonised standards IEC 62304 and ISO 14971) and the **US regulatory framework** (FDA Quality Management System Regulation, 21 CFR Part 820, FDA guidance on software functions and AI/ML-enabled devices). Where requirements differ between jurisdictions, both are named explicitly. Where they are substantively equivalent, jurisdiction-neutral language is used.

The underlying problem — manual, error-prone change impact assessment across controlled documents — is identical in both frameworks. The cost of getting it wrong (deficiency rounds, delayed submissions, regulatory enforcement) is comparable in magnitude in both markets.

### Two phases of ROI

The value delivered by this agent differs materially depending on whether a team is in **initial development** (building and submitting a device for the first time) or **ongoing maintenance** (managing changes and updates to an approved device). Both phases are analysed in this document.

---

#### Phase 1 — Initial development and first submission

During initial development, the primary risk is submitting a technical file or design history file that contains gaps — requirements that do not trace to risk controls, risk controls that are not implemented in the SRS, security requirements that are missing, or clinical performance claims that exceed what the SRS supports. These gaps are typically discovered either internally during design review, or externally during the regulatory reviewer's assessment.

**Cost of a gap discovered internally** (before submission): rework of the affected documents, re-review by the responsible engineer and quality/regulatory staff, and potential knock-on effects on the verification and validation plan. Typical cost: 5–20k€ per significant gap, depending on how far the gap propagates through the technical file.

**Cost of a gap discovered by the regulatory reviewer** (during submission review): one deficiency round adds 4–12 weeks of delay and 10–40k€ of additional effort. Multiple rounds multiply this. For a first-market submission in the EU or US, a single deficiency round can delay revenue by one to two quarters and add 50–100k€ in total cost when internal and external resources are included.

The agent's value in Phase 1 is catching gaps before they reach the regulatory reviewer. The earlier a gap is detected, the cheaper it is to fix.

---

#### Phase 2 — Ongoing maintenance and change management

After first approval, every change to the device — including software updates, new integrations, algorithm modifications, and security patches — must be assessed for its regulatory impact. This is a recurring cost for the lifetime of the device.

**Cost of a change that is under-assessed:** If a change that should have triggered a new submission is not identified as significant, the manufacturer faces regulatory enforcement risk. If a change is over-assessed (treated as significant when it is not), the team spends unnecessary effort on a submission that was not required.

**Cost of routine change documentation:** Even for non-significant changes, the impact assessment across the technical file (SRS, risk file, clinical evaluation, usability file, cybersecurity documentation) requires 8–43 hours of expert time per moderate change, based on the OpenRegulatory SOP template workflow analysis.

The agent's value in Phase 2 is reducing the manual effort per change and improving the consistency and traceability of impact assessments.

---

### Why regulatory documentation creates measurable cost

In regulated SaMD development, every change to an SRS or risk file must be assessed for its impact on other controlled documents. This assessment is mandated by:

- **IEC 62304** section 5.7–5.8 (software change assessment and regression testing)
- **ISO 14971** sections 6–7 (risk control implementation and verification)
- **EU MDR** Article 83 and Annex IX (post-market change documentation)
- **FDA 21 CFR Part 820** (design change control, Quality Management System Regulation)

When this assessment is done manually, it is slow, inconsistent, and error-prone. The specific failure modes are:

- A missed link between a risk control and its implementing SRS requirement causes a deficiency from the regulatory reviewer.
- An AI/ML model update that exceeds the boundaries of an approved change control plan triggers an unplanned new submission.
- Poorly documented traceability discovered during an inspection delays market access.

These are not theoretical risks. They are the documented failure modes in regulatory submissions for SaMD, across both EU and US markets.

### Why LLM operating cost is not the constraint

The cost of running a language model to analyse an SRS change is in the order of cents per query. At the scale of a typical SaMD portfolio — several hundred queries per product per year — annual LLM operating cost remains well below 1,000€. Expert staff time for the equivalent manual analysis is 100–200€ per hour. The ROI of automation is therefore dominated by staff time and regulatory risk avoidance, not by infrastructure cost. This asymmetry is why the scoring model weights risk savings and human impact heavily and treats LLM cost as negligible overhead.

---

## 3. Scoring methodology

### Why standard RICE does not fit

The standard RICE framework scores use cases on four dimensions: Reach (how many users are affected), Impact (the effect on each user), Confidence (certainty of the estimate), and Effort (cost to build). RICE was designed for consumer product features where the primary value driver is user volume. For this product, the user base is small and fixed — a SaMD team has a defined set of regulatory stakeholders. The value driver is not how many people use a feature but **how much regulatory cost the feature prevents**.

Using Reach as a scoring dimension would artificially deflate the score of high-value regulatory use cases and misrepresent the economics of the product.

### The adapted formula

Reach is replaced by **Risk Savings**, a parameter that captures the regulatory cost avoidance potential of each use case:

```
RICE Score = (Risk Savings × Impact × Confidence) / Effort
```

Each parameter is defined on a consistent scale. The resulting score is a relative priority index — a higher score means higher priority relative to other use cases in this product. Scores are multiplied by 10 for display readability.

### Parameter definitions

| Parameter | Scale | What it measures |
|-----------|-------|-----------------|
| Risk Savings | 1–5 | Potential to reduce regulatory cost: deficiency rounds, unplanned submissions, inspection findings |
| Impact | 1–5 | Combined value of time saved for the team and quality of findings delivered to document owners |
| Confidence | 0.5–1.0 | How certain we are that the estimates for this use case are accurate given current knowledge |
| Effort | 1–5 | Build complexity from the AI Architect's perspective (1 = simple, 5 = highly complex) |

Effort appears in the denominator — higher effort reduces the score, all else equal. This reflects the opportunity cost of building a complex feature when a simpler one delivers comparable value.

### Worked example

UC1 (continuous SRS monitoring) has scores: Risk Savings = 4, Impact = 4, Confidence = 0.9, Effort = 2.

```
Score = (4 × 4 × 0.9) / 2 = 14.4 / 2 = 7.2 → displayed as 72
```

UC4 (AI/ML change control plan analysis) has scores: Risk Savings = 5, Impact = 3, Confidence = 0.6, Effort = 4.

```
Score = (5 × 3 × 0.6) / 4 = 9 / 4 = 2.25 → displayed as 23
```

UC4 has a higher Risk Savings score than UC1, but its lower confidence and higher effort reduce its priority significantly. This is intentional: building complex features with uncertain requirements before simpler, higher-confidence ones is a common source of wasted effort in early-stage products.

### What the formula does not capture

The formula does not capture strategic dependencies between use cases. UC1 is a prerequisite for UC3, UC2, and UC5 — if UC1 is not built first, none of the others can function correctly. This dependency structure is captured in the roadmap (section 7) rather than in the scores. A reader who sees UC1 and UC3 with similar scores should not conclude they can be built in any order.

---

## 4. Parameter reference

This section defines exactly how each parameter was estimated. It is the primary place to challenge the scores. If a number seems wrong, identify the parameter, the assumption behind it, and propose an alternative — then re-run the formula.

### Risk Savings (1–5)

**What it represents:** The expected reduction in regulatory cost if this use case is implemented. A score of 5 means the use case directly prevents high-cost regulatory events (unplanned submissions, major deficiency rounds). A score of 1 means the use case improves quality but does not directly reduce external regulatory cost.

**How it was estimated:** Based on the probability that a missed finding in this domain triggers a deficiency from a regulatory reviewer, multiplied by the typical cost of one additional review round. This applies equally to EU MDR deficiency procedures and FDA additional information requests — the cost structures are comparable. Sources: industry benchmarks for SaMD compliance cost, EU MDR and FDA change control guidance, OpenRegulatory technical file template complexity analysis, FDA software submission guidance.

**Key assumption:** A 20–40% baseline probability of regulatory reviewer questions on a moderate change falls to 5–15% with systematic AI-assisted traceability review. If your team's historical deficiency rate is lower than 20%, Risk Savings scores should be reduced proportionally.

| Score | Meaning |
|-------|---------|
| 5 | Directly prevents unplanned submissions or major deficiency rounds (15–80k€ per event) |
| 4 | Reduces deficiency probability significantly; prevents 5–15k€ rework per event |
| 3 | Reduces minor reviewer questions; prevents 1–5k€ rework per event |
| 2 | Improves traceability quality but with indirect regulatory benefit |
| 1 | Operational efficiency only; no direct regulatory cost avoidance |

### Impact (1–5)

**What it represents:** The combined value of time saved for the team per event and the quality of the output for the document owner receiving findings. A score of 5 means the use case saves significant expert time (8+ hours per event) and produces actionable, well-cited findings. A score of 1 means minimal time saving or low output quality.

**How it was estimated:** Based on time-and-motion analysis of typical SaMD change control workflows using the OpenRegulatory SOP template as a baseline (8–43 hours per moderate change across 4–6 roles). Blended hourly rate assumed at 130€, representing the loaded cost for senior regulatory, risk, and quality staff in Western European or comparable markets.

**Key assumption:** The agent achieves 30–60% automation of the manual triage and document-update identification steps. If your team is significantly faster than average at manual review, Impact scores should be reduced accordingly.

### Confidence (0.5–1.0)

**What it represents:** How certain we are that the benefit estimates for this use case will materialise as described. A score of 1.0 means the use case is well-understood, the reference data exists, and the technical approach is proven. A score of 0.5 means significant unknowns remain — in the regulatory requirements, the technical approach, or both.

**How it was estimated:** Based on three factors: (a) maturity of the reference standards for this domain, (b) availability of structured test data in the current document corpus, and (c) degree to which the technical approach has been validated through prior work or published research.

**Key assumption:** Confidence scores should be updated after the initial release, using actual finding acceptance rates and time savings as calibration data.

### Effort (1–5)

**What it represents:** Build complexity from the AI Architect's perspective, accounting for integration effort, reference corpus preparation, and validation requirements. A score of 1 means the use case reuses existing infrastructure and can be implemented quickly. A score of 5 means significant new architecture is required and validation is complex.

**How it was estimated:** Based on the AI Architect's assessment of the technical dependencies, the availability of structured reference data, and the complexity of the output format required.

**Key assumption:** Effort scores assume a single AI Architect working part-time on implementation. A dedicated full-time Architect would reduce effective effort scores by approximately one point across all use cases.

---

## 5. Use case analysis

> **Note on phases:** Each use case includes separate ROI estimates for Phase 1 (initial development and first submission) and Phase 2 (ongoing maintenance and change management). Phase 1 ROI reflects the value of catching gaps before they reach a regulatory reviewer. Phase 2 ROI reflects the recurring value of efficient change impact assessment. These phases are not mutually exclusive — a team using the agent from the start benefits from both.

> **Note on technology:** The trigger mechanisms and integration patterns described below are intentionally technology-agnostic. The terms "change event," "workflow trigger," and "documentation platform" refer to whatever version control, document management, or workflow system the team uses. An example in a Git-based environment is provided where helpful, but no specific technology is required or assumed.

---

### UC1 — Continuous SRS monitoring and change classification

**One-line description:** Detect every SRS change event, classify the change type (clinical, risk/safety, UI/workflow, security, AI/ML, non-functional), and route findings to the appropriate document owner.

**What triggers it:** A change event on any SRS document — for example, a new version submitted for review, a modification to a previously approved requirement, or a status transition (draft to review, review to approved). The agent monitors the document management system for these events and initiates analysis automatically.

> **Example (illustrative only):** In a Git-based workflow, a trigger might be a pull request that modifies an SRS file. In a document management system, the trigger might be a workflow state change. The specific mechanism depends on the team's tooling.

**Who receives the output:** The SRS owner receives a summary of classified changes. Document owners (risk engineer, UX/human factors specialist, cybersecurity engineer, clinical affairs) receive targeted findings based on which change types are detected.

**RICE scores:**

| Risk Savings | Impact | Confidence | Effort | Score |
|-------------|--------|------------|--------|-------|
| 4 | 4 | 0.9 | 2 | 72 |

**Benefit breakdown — Phase 1 (initial development):**

| Dimension | Estimate |
|-----------|---------|
| Typical events | 30–80 SRS creation/update events during initial development |
| Time saved per event | 0.5–2 hours of manual classification and routing |
| Total time saving (Phase 1) | 15–160 hours = 2,000–20,800€ |
| Regulatory cost avoided | 5–15k€ (systematic classification reduces gaps reaching first submission) |

**Benefit breakdown — Phase 2 (ongoing maintenance):**

| Dimension | Estimate |
|-----------|---------|
| Annual events per product | 20–40 SRS change events per year |
| Time saved per event | 1–3 hours of manual change triage across the team |
| Annual time saving | 20–120 hours = 2,600–15,600€ |
| Regulatory cost avoided | 5–10k€ per year (reduced probability of reviewer deficiency from missed change classification) |
| LLM operating cost | ~0.01–0.05€ per query — negligible in both phases |

**Key assumptions:**

- 20–40 annual change events is calibrated against an actively developed SaMD product with multiple integrations and algorithm features. A less active product may see 8–15 events per year.
- Change classifier achieves 85%+ precision using the structured requirements mapping and established document ID conventions.
- Phase 1 event count assumes a new product being built from scratch. For a product being migrated to this agent mid-development, events will be lower.

**Dependencies and risks:**

This is the foundation use case. UC2, UC3, UC5, and UC4 all depend on UC1's classifier output. The primary technical risk is false-positive classification — flagging non-safety-relevant changes for risk manager review creates noise and will reduce adoption if not controlled. A precision threshold should be agreed with the team before deployment.

**Rationale for initial release placement:**

UC1 has the lowest build effort (2/5) because the change detection and classification mechanism reuses the document ingestion infrastructure already scoped in the product requirements. Building UC1 first creates a working loop — detect, classify, notify — from which all subsequent releases extend without architectural rework. This is the correct starting point regardless of the team's tooling choices.

---

### UC3 — Risk traceability check (risk control to SRS requirement gap detection)

**One-line description:** For every SRS change classified as safety-relevant, verify that every risk control measure in the risk management file still has a corresponding SRS requirement, and flag gaps or broken links.

> **Key term — Risk control:** A measure taken to reduce the probability or severity of a harm. Under ISO 14971, risk controls must be implemented as verifiable requirements in the SRS, and this traceability must be maintained throughout the product lifecycle. Both EU MDR and FDA regulations require documented evidence of this traceability.

**What triggers it:** UC1 classifies a change as "risk/safety" or "clinical." The traceability resolver queries the risk-to-SRS traceability table against the current SRS to identify risk control links that are missing, broken, or newly unverifiable.

**Who receives the output:** The Risk/Safety Engineer receives a structured finding: hazard identifier, risk control identifier, expected SRS requirement identifier, finding type (missing / modified / ambiguous), and citation to the applicable standard clause (ISO 14971 section 7.3.3 — traceability requirement, applicable in both EU and US regulatory contexts).

**RICE scores:**

| Risk Savings | Impact | Confidence | Effort | Score |
|-------------|--------|------------|--------|-------|
| 5 | 4 | 0.85 | 2 | 85 |

**Benefit breakdown — Phase 1 (initial development):**

| Dimension | Estimate |
|-----------|---------|
| Typical events | All safety-relevant SRS changes during development (typically 15–30% of all SRS events) |
| Time saved per event | 2–6 hours of manual risk file cross-check |
| Total time saving (Phase 1) | 20–100 hours = 2,600–13,000€ |
| Regulatory cost avoided | 15–40k€ (broken traceability at first submission is among the most common causes of a deficiency round in both EU and US markets) |

**Benefit breakdown — Phase 2 (ongoing maintenance):**

| Dimension | Estimate |
|-----------|---------|
| Annual events per product | 8–20 safety-relevant SRS changes per year |
| Time saved per event | 3–8 hours of manual risk file cross-check |
| Annual time saving | 24–160 hours = 3,100–20,800€ |
| Regulatory cost avoided | 15–40k€ per avoided major deficiency round |
| LLM operating cost | Negligible |

**Key assumptions:**

- The risk-to-SRS traceability table must be maintained by the Risk Engineer as a controlled document. Stale reference data generates false negatives.
- 15–40k€ regulatory cost avoidance assumes a moderately complex SaMD where a major deficiency round costs 50–100k€ in total (internal + external resources + delay cost), and where poor traceability increases the probability of a deficiency by 15–25%. This cost range applies comparably to EU MDR and FDA submission processes.
- For dual EU/US submissions, catching a traceability gap before filing saves it from appearing as a deficiency in both markets simultaneously — multiplying the avoided cost.

**Dependencies and risks:**

Depends on UC1. Also depends on the risk management file existing in a structured, machine-readable format that the traceability resolver can query. If the risk management file is maintained in a proprietary quality management system tool rather than a structured document format, an integration layer will be required — this is an additional effort item that should be clarified with the AI Architect before the initial release.

**Rationale for initial release placement:**

UC3 delivers the highest regulatory value of any use case (Risk Savings: 5/5) and shares the same infrastructure as UC1. It directly addresses the core product insight: comparing the SRS against a risk control model and verifying traceability. Placing it in the initial release alongside UC1 means the first deployment already demonstrates the full monitoring → classification → traceability → finding workflow, which is the value proposition that matters most to regulatory and quality reviewers.

---

### UC2 — Baseline document to SRS suggestions

**One-line description:** When a regulatory document (risk management file, clinical evaluation, usability engineering file) is baselined or approved, automatically generate suggested SRS requirements that should exist to support the document's scope.

> **Key term — Baseline:** A formally approved version of a controlled document, establishing a reference point for subsequent changes. Under IEC 62304 and both EU MDR and FDA quality system regulations, baselines must be maintained and changes tracked.

**What triggers it:** A document owner marks a document as approved or baselined in the document management system. The baseline intake module parses the document, extracts requirements and controls, and maps them against the SRS traceability model to generate suggestions for the SRS owner.

**Who receives the output:** The SRS owner receives a list of proposed SRS additions or updates, with citations to the source document and relevant standard clauses.

**RICE scores:**

| Risk Savings | Impact | Confidence | Effort | Score |
|-------------|--------|------------|--------|-------|
| 3 | 4 | 0.75 | 3 | 30 |

**Benefit breakdown — Phase 1 (initial development):**

| Dimension | Estimate |
|-----------|---------|
| Typical events | 3–6 initial baselines during product development (risk management plan, preliminary hazard analysis, usability plan, clinical evaluation plan, etc.) |
| Time saved per event | 8–20 hours of initial SRS mapping against each baseline |
| Total time saving (Phase 1) | 24–120 hours = 3,100–15,600€ |
| Regulatory cost avoided | 10–25k€ (preventing requirement gaps introduced during initial baseline alignment, caught before first submission) |

**Benefit breakdown — Phase 2 (ongoing maintenance):**

| Dimension | Estimate |
|-----------|---------|
| Annual events per product | 1–3 document baselines updated per year |
| Time saved per event | 2–8 hours (incremental update, smaller than initial alignment) |
| Annual time saving | 2–24 hours = 260–3,100€ |
| Regulatory cost avoided | 5–15k€ per year (early gap prevention reduces deficiencies at next submission) |
| LLM operating cost | Negligible |

**Key assumptions:**

- The primary benefit of UC2 occurs during Phase 1 (initial development), when all regulatory documents are being baselined for the first time. For a mature product in Phase 2, the per-event benefit is lower.
- Quality of suggestions depends on the structure of the incoming baseline document. Structured documents with explicit control identifiers generate precise, traceable suggestions. Narrative-style documents generate less specific suggestions requiring more human interpretation.
- Phase 2 event count assumes a stable, approved product with periodic document updates. A product undergoing major changes or a new indication would see higher event counts.

**Dependencies and risks:**

Depends on UC1's ingestion infrastructure. Also requires a notification routing module to deliver suggestion sets to the SRS owner with context about which baseline triggered them. Primary risk: over-suggestion (too many low-confidence suggestions) reduces adoption among SRS owners who will begin to ignore agent output.

**Rationale for Release 2 placement:**

UC2 is placed in Release 2 because it requires additional infrastructure beyond the core UC1/UC3 monitoring loop: a baseline intake parser that handles multiple document types, and an owner notification routing system. Deferring it to Release 2 allows the team to validate the core monitoring approach first, then extend to the reverse flow (baseline → SRS suggestions) with a higher-confidence implementation.

---

### UC5 — Cybersecurity change impact (IEC 81001-5-1 / OWASP ASVS)

**One-line description:** When an SRS change introduces or modifies interfaces, data flows, authentication, or encryption requirements, verify coverage against IEC 81001-5-1 cybersecurity controls and OWASP Application Security Verification Standard requirements, and route findings to the Cybersecurity Engineer.

> **Key term — IEC 81001-5-1:** International standard for cybersecurity activities throughout the health software lifecycle. Applicable in both EU and US regulatory contexts; referenced in FDA pre-market cybersecurity guidance (2023/2026) and required under EU MDR Annex I General Safety and Performance Requirements for networked and connected devices.

**What triggers it:** UC1 classifies a change as "security/data flows." The cybersecurity sub-check queries the OWASP ASVS structured checklist and IEC 81001-5-1 clause summaries and cross-checks against the threat model document.

**Who receives the output:** The Cybersecurity Engineer receives a finding identifying which new interfaces or data flows lack corresponding security requirements, with citations to OWASP ASVS sections and IEC 81001-5-1 clauses.

**RICE scores:**

| Risk Savings | Impact | Confidence | Effort | Score |
|-------------|--------|------------|--------|-------|
| 3 | 3 | 0.70 | 3 | 21 |

**Benefit breakdown — Phase 1 (initial development):**

| Dimension | Estimate |
|-----------|---------|
| Typical events | 5–15 SRS changes touching interfaces or security requirements during development |
| Time saved per event | 2–5 hours of manual security requirement cross-check |
| Total time saving (Phase 1) | 10–75 hours = 1,300–9,750€ |
| Regulatory cost avoided | 8–20k€ (cybersecurity gaps at first submission are a growing source of deficiencies under both FDA cybersecurity guidance and EU MDR Annex I) |

**Benefit breakdown — Phase 2 (ongoing maintenance):**

| Dimension | Estimate |
|-----------|---------|
| Annual events per product | 2–8 security-relevant SRS changes per year |
| Time saved per event | 3–8 hours of manual security requirement cross-check |
| Annual time saving | 6–64 hours = 780–8,300€ |
| Regulatory cost avoided | 5–10k€ per year |
| LLM operating cost | Negligible |

**Key assumptions:**

- The OWASP ASVS is freely available and can be incorporated into the reference corpus without licensing restrictions. The IEC 81001-5-1 reference corpus will be built from clause summaries and publicly available mapping tables rather than the full normative text (which is a paid standard). Finding quality will be somewhat lower than UC3 as a result.
- A structured threat model document must exist in a machine-readable format for this use case to produce high-quality findings. If the threat model exists only as a narrative document, a parsing step is required — this additional effort should be clarified with the AI Architect before Release 2 scoping.
- Confidence is lower (0.70) than UC1/UC3 because the security reference corpus quality depends on the availability and structure of the threat model, which varies by organisation.

**Dependencies and risks:**

Depends on UC1 and UC2. Primary technical risk: security sub-checks trigger on every interface-related SRS change unless the classifier is sufficiently precise. A precision threshold should be agreed with the Cybersecurity Engineer before deployment to avoid notification fatigue.

**Rationale for Release 2 placement:**

Cybersecurity is an increasing regulatory priority in both EU (MDR Annex I, GSPR 17) and US (FDA cybersecurity guidance, updated 2026) markets, but the reference corpus quality and threat model format dependency make it more complex to implement than UC1/UC3. Release 2 placement allows the team to validate classifier precision on the simpler traceability cases first, then extend the sub-check architecture to the security domain.

---

### UC4 — AI/ML behaviour and change control plan boundary check

**One-line description:** When an SRS change modifies algorithm behaviour, model inputs or outputs, or clinical performance claims, verify whether the change remains within the boundaries of the approved change control plan, or whether it triggers a new regulatory submission.

> **Key term — Change control plan (PCCP/Article 83):** A mechanism that allows manufacturers of AI/ML-enabled devices to pre-specify the types of changes they may make to the algorithm without requiring a new submission. In the US, the FDA uses the term Predetermined Change Control Plan (PCCP); the EU equivalent appears in Article 83 of the EU AI Act, which applies alongside EU MDR for AI-enabled medical devices. Both frameworks require that changes outside the approved plan trigger a new regulatory assessment.

**What triggers it:** UC1 classifies a change as "AI/ML behaviour." The change control checker compares the SRS delta against the approved change control plan document to determine whether the change is within defined bounds (no new submission required), exceeds them (new submission required), or is ambiguous (human review required).

**Who receives the output:** The AI/ML Engineer and the Regulatory Affairs specialist jointly receive a structured finding: change description, change control plan section reference, boundary status (within / exceeds / ambiguous), and recommended action.

**RICE scores:**

| Risk Savings | Impact | Confidence | Effort | Score |
|-------------|--------|------------|--------|-------|
| 5 | 3 | 0.60 | 4 | 23 |

**Benefit breakdown — Phase 1 (initial development):**

| Dimension | Estimate |
|-----------|---------|
| Typical events | 3–8 AI/ML algorithm definition events during initial SRS development |
| Time saved per event | 3–10 hours of manual change control plan boundary definition review |
| Total time saving (Phase 1) | 9–80 hours = 1,200–10,400€ |
| Regulatory cost avoided | 10–30k€ (correctly scoping the initial change control plan prevents implementation that exceeds its bounds in early post-market releases) |

**Benefit breakdown — Phase 2 (ongoing maintenance):**

| Dimension | Estimate |
|-----------|---------|
| Annual events per product | 2–10 AI/ML model updates per year |
| Time saved per event | 5–15 hours of manual change control plan boundary analysis |
| Annual time saving | 10–150 hours = 1,300–19,500€ |
| Regulatory cost avoided | ~43k€ average per avoided unplanned submission (applicable in both EU and US — an out-of-bounds change triggers a new 510(k) or PMA supplement in the US, or a significant change assessment under EU MDR Article 83) |
| LLM operating cost | Negligible |

**Key assumptions:**

- The change control plan document structure varies significantly by product and regulatory jurisdiction. This variability is the primary reason for the low confidence score (0.60). A checker that works well for one product's change control plan may require significant reconfiguration for another.
- 43k€ regulatory cost avoidance = estimated cost of an unplanned submission (50–200k€ total including regulatory authority fees, consultant time, and submission preparation) discounted by an estimated 60–70% detection probability for systematic monitoring versus informal review.
- The FDA PCCP guidance was in draft form as of early 2026. The EU AI Act Article 83 implementing framework was also developing. Both are expected to mature by the time this use case reaches Release 3 — the Confidence score should be re-evaluated at that point.

**Dependencies and risks:**

Depends on UC1, UC3, and a stable document analysis pipeline. Primary technical risk: change control plan documents are typically written in narrative prose, making automated boundary checking unreliable without a purpose-built document parser. This parser is an additional build item that is not reflected in the current Effort score of 4 and must be scoped with the AI Architect before Release 3.

**Rationale for Release 3 placement:**

Despite having the highest potential regulatory cost avoidance (Risk Savings: 5/5), UC4 is placed in Release 3 because of low confidence and high effort. The regulatory guidance for AI/ML change control plans in both EU and US markets was still maturing as of early 2026. Building this use case before the guidance stabilises would produce a checker that needs significant rework. The empirical data from UC1/UC3/UC2/UC5 will also calibrate the classifier precision needed to make UC4 reliable.

---

### UC6 — Regulatory inspection and submission preparation

**One-line description:** Aggregate the findings history, disposition rationales, traceability links, and document change log across a defined period to produce a structured audit readiness summary package, applicable for both EU MDR notified body audits and FDA inspections or pre-market submissions.

> **Key term — Technical File / Design History File (DHF):** The Technical File (EU MDR) or Design History File (FDA 21 CFR 820) is the complete record of evidence demonstrating that a device meets applicable requirements. Both regulatory frameworks require this file to be current, traceable, and available for inspection at any time.

**What triggers it:** A manual request from the Regulatory Affairs specialist or Quality Manager, typically 4–8 weeks before a planned inspection, audit, or submission deadline.

**Who receives the output:** The Regulatory Affairs specialist receives a structured package: open findings with time elapsed since creation, disposition rationale summary by document area, traceability gap summary, and a checklist of outstanding items mapped to the applicable regulatory framework (EU MDR Annex II/III or FDA 21 CFR 820 design controls, as selected by the user).

**RICE scores:**

| Risk Savings | Impact | Confidence | Effort | Score |
|-------------|--------|------------|--------|-------|
| 3 | 3 | 0.55 | 5 | 10 |

**Benefit breakdown — Phase 1 (initial development):**

| Dimension | Estimate |
|-----------|---------|
| Typical events | 1–2 pre-submission readiness checks before first filing |
| Time saved per event | 15–40 hours of manual traceability consolidation |
| Total time saving (Phase 1) | 15–80 hours = 2,000–10,400€ |
| Regulatory cost avoided | 10–30k€ (pre-submission gap analysis reduces deficiencies at first review) |

**Benefit breakdown — Phase 2 (ongoing maintenance):**

| Dimension | Estimate |
|-----------|---------|
| Annual events per product | 0.5–1 major audit or submission per year |
| Time saved per event | 10–30 hours of manual audit preparation |
| Annual time saving | 5–30 hours = 650–3,900€ |
| Regulatory cost avoided | 10–20k€ per year |
| LLM operating cost | Negligible |

**Key assumptions:**

- UC6 is a reporting layer built on top of all previous use cases. Its value depends entirely on the quality and completeness of the findings history from UC1–UC5. A minimum of 6 months of production operation is needed to generate a meaningful dataset.
- Output format requirements vary by regulatory framework and specific authority. Different notified bodies and FDA review divisions have different expectations. Significant customisation may be required per submission.
- The confidence score of 0.55 reflects this dependency and the format variability, not uncertainty about whether the use case is valuable.

**Dependencies and risks:**

Depends on all previous use cases and at least 6 months of operational findings data. Primary risk: the audit package surfaces gaps in the findings history that were not visible during routine monitoring, creating remediation work at the worst possible time — weeks before an inspection. Secondary risk: the package format does not match the reviewer's expectations, requiring manual reformatting.

**Rationale for "Later" placement:**

UC6 cannot be built or validated until the product has been running in production long enough to generate a meaningful findings history. "Later" does not mean "never" — it means this use case requires the foundation to be solid and empirically validated before it is built. A team using UC1–UC5 consistently for 6–12 months will have exactly the data needed to make UC6 genuinely useful, at which point the build cost (Effort: 5/5) becomes justifiable.

---

## 6. Comparative view

### Summary table

| Use case | Risk savings | Impact | Confidence | Effort | RICE score | Phase 1 time saving | Phase 2 annual saving | Tier |
|----------|-------------|--------|------------|--------|-----------|--------------------|-----------------------|------|
| UC3 Risk traceability | 5 | 4 | 0.85 | 2 | 85 | 20–100 h | 24–160 h/yr | Initial release |
| UC1 SRS monitoring | 4 | 4 | 0.90 | 2 | 72 | 15–160 h | 20–120 h/yr | Initial release |
| UC2 Baseline → SRS | 3 | 4 | 0.75 | 3 | 30 | 24–120 h | 2–24 h/yr | Release 2 |
| UC4 Change control plan | 5 | 3 | 0.60 | 4 | 23 | 9–80 h | 10–150 h/yr | Release 3 |
| UC5 Cybersecurity | 3 | 3 | 0.70 | 3 | 21 | 10–75 h | 6–64 h/yr | Release 2 |
| UC6 Inspection prep | 3 | 3 | 0.55 | 5 | 10 | 15–80 h | 5–30 h/yr | Later |

### Why the ranking is what it is

UC3 scores highest despite not being the most visible use case. Broken traceability between risk controls and SRS requirements is the most common cause of deficiency rounds in SaMD submissions — consistently cited in both EU MDR notified body findings and FDA additional information requests. The fact that it is detectable automatically and cheaply (Effort: 2/5) makes it the highest-priority use case by a significant margin.

UC1 scores second because it is the prerequisite for everything else. Its high confidence score (0.90) reflects that the test data, reference corpus, and technical approach are all already defined and available.

UC4 has a Risk Savings score of 5 — matching UC3 — but its RICE score is much lower because of low confidence and high effort. The AI/ML change control plan guidance is still maturing in both EU and US markets, and the document parsing challenge is significant. Building UC4 before the foundation is proven would be premature in both financial and technical terms.

UC6 has the lowest score. This is not because inspection preparation is unimportant — it is critical in both regulatory frameworks — but because its value is entirely dependent on data that does not yet exist. Building it first would produce a tool with nothing to report.

### Dual-jurisdiction note

All six use cases apply to both EU MDR and FDA-regulated products. The specific standard clauses cited in findings differ by jurisdiction (e.g. ISO 14971:2019 section 7.3.3 vs. FDA 21 CFR 820.30 design input traceability), but the underlying gap being detected is identical. The agent's reference corpus should include jurisdiction-specific mappings so that findings are correctly cited for the target market. For teams submitting to both markets simultaneously, the agent's findings are applicable to both technical files, and the cost avoidance estimates can be doubled where the same gap would have caused deficiencies in both markets.

---

## 7. Roadmap recommendation

### Release structure

| Release | Use cases | Rationale |
|---------|-----------|-----------|
| Initial release | UC1 + UC3 (build together) | Shared infrastructure; delivers the full detection → classification → traceability → finding workflow. Applicable to both EU and US regulatory contexts from day one. |
| Release 2 | UC2 + UC5 | Both extend the initial release infrastructure without requiring new core architecture. Can be built in parallel or sequentially (UC2 first, as it reuses more of the existing pipeline). |
| Release 3 | UC4 | Requires stable pipeline, validated classifier precision data, and clearer regulatory guidance on AI/ML change control plans in both jurisdictions. |
| Later | UC6 | Requires 6+ months of production findings data and a specific submission or audit target to optimise for. |

### Dependency chain

```
UC1 (foundation)
  └── UC3 (same release, same infrastructure)
        └── UC2 (Release 2, extends document intake)
        └── UC5 (Release 2, extends classifier routing)
              └── UC4 (Release 3, requires stable pipeline + guidance maturity)
                    └── UC6 (Later, requires 6+ months of findings data)
```

### Phase interaction with the roadmap

The initial release (UC1 + UC3) delivers value in both Phase 1 and Phase 2, making it suitable as the starting point whether the team is building a new product or managing an existing one. Teams that deploy the agent during initial development will benefit from Phase 1 gap prevention through the full release roadmap. Teams deploying to an existing product will primarily benefit from Phase 2 change management efficiency.

### What the AI Architect needs to validate before each release

- **Before initial release:** Confirm that the change detection module, SRS parser, and document retrieval pipeline handle the structured test corpus correctly, and that the classifier achieves 85%+ precision on UC1/UC3 test scenarios.
- **Before Release 2:** Confirm the threat model document format for UC5 and whether a dedicated parser is needed. Confirm the baseline intake document format for UC2. Both assessments are jurisdictionally neutral.
- **Before Release 3:** Re-evaluate the AI/ML change control plan guidance landscape in both EU (AI Act Article 83 implementing acts) and US (FDA AI/ML SaMD lifecycle guidance) markets. Agree a structured change control plan document format for the agent to work with.

---

## 8. Assumptions and limitations

### What this model does not include

This ROI model does not quantify time-to-market acceleration (faster, more confident submissions create competitive advantage in both markets), knowledge retention value (institutional knowledge about which SRS changes affect which documents is currently held by individuals, not systems), or the cost of onboarding new regulatory/quality staff without documented traceability context. All of these are real benefits that would increase the ROI figures if quantified.

The model also does not account for the compounding effect of dual-market submissions. For products submitted simultaneously to EU and US, a single traceability gap caught by the agent prevents a deficiency in both markets — the avoided cost is additive, not duplicated.

### Data quality

The cost and time benchmarks are calibrated against two reference points: the OpenRegulatory technical file template for a Class B/Class II equivalent SaMD (18 software requirements, 20 risk table entries, full documentation set), and analysis of a complex multi-integration SaMD product (multi-device platform with algorithmic features, active in both FDA and EU markets). These are representative but not universal. Teams working on simpler products should use the lower end of all ranges; teams on Class III / PMA-level products should consider the upper end or beyond.

The figures should be treated as order-of-magnitude estimates calibrated against industry benchmarks, not as precise forecasts for any specific product.

### Regulatory environment

The regulatory references in this document are current as of early 2026. Key items to monitor:

- **EU AI Act:** Full enforcement obligations for high-risk AI systems in healthcare enter effect in August 2026. If the agent itself (not the SaMD it supports) is classified as high-risk AI under the AI Act, additional transparency, logging, and documentation obligations apply to the agent's own development.
- **FDA AI/ML SaMD lifecycle guidance:** In draft as of early 2026. Finalisation will affect the Confidence and Risk Savings scores for UC4.
- **FDA cybersecurity guidance:** Updated guidance issued in 2026 increases the specificity of security requirements for connected medical devices, strengthening the case for UC5.

---

## 9. How to update this document

This document should be treated as a living reference, updated at defined trigger points rather than continuously.

**Trigger-based updates:**

- After the initial release: update Confidence scores for UC2, UC4, and UC5 based on actual UC1/UC3 finding acceptance rates. If acceptance rate is below 70%, reduce all Confidence scores by 0.1. If above 85%, increase by 0.1.
- After Release 2: update UC4's Effort score based on the AI Architect's assessment of change control plan document variability encountered during UC5 implementation.
- After a major regulatory guidance update (FDA AI/ML guidance finalisation; EU AI Act implementing acts): review Risk Savings scores for UC4 and UC5, as these are most sensitive to evolving guidance.
- After accumulating 6 months of production data: replace the Phase 2 time-saving estimates with actuals measured from real finding events.

### Parameter ownership

| Parameter | Owner | Update trigger |
|-----------|-------|---------------|
| Risk Savings | Regulatory Affairs / PM | Major guidance change or new product risk class in either jurisdiction |
| Impact | PM (with regulatory input) | After each release, based on document owner feedback |
| Confidence | PM + AI Architect jointly | After each release, based on empirical acceptance rate data |
| Effort | AI Architect | Before each release scoping session |

---

*This document is version-controlled in the product repository under `docs/use-case-roi-prioritization.md`. Challenges to scores and parameters should be raised as tracked issues in the project backlog with the label `type:doc` and assigned to the PM for triage.*
