**Status:** Working draft
**Owner:** Product Management
**Audience:** All stakeholders

---

# Compliance Landscape

This document describes the regulatory environment that the SRS Review Agent is designed to operate in. It covers the V-model lifecycle framework, the controlled document ecosystem that surrounds the SRS, the standards the agent references, and the design control activities the agent supports.

Read this document if you are new to regulated SaMD development or need to understand why the agent exists and what regulatory obligations it addresses.

---

## The V-model in regulated SaMD development

The V-model is the software development lifecycle framework used in regulated medical device software. It structures development as two arms of a V: the left arm descends from user needs through system requirements, software requirements, and detailed design down to implementation. The right arm ascends through unit testing, integration testing, system testing, and user acceptance testing back up to validated user needs. Each level on the left has a corresponding verification or validation activity on the right.

```
User Needs ─────────────────────────────► User Acceptance Testing
    │                                               ▲
    ▼                                               │
System Requirements ────────────────► System Testing / Validation
    │                                               ▲
    ▼                                               │
Software Requirements (SRS) ───────► Software Integration Testing
    │                                               ▲
    ▼                                               │
Detailed Design ─────────────────────► Unit Testing
    │                                               ▲
    └───────────────► Implementation ───────────────┘
```

The SRS sits at the midpoint of the left arm. It is the document that translates system-level requirements into specific, verifiable software requirements. Everything above it constrains what it must contain. Everything below it derives from what it says.

This position makes the SRS the most consequential single document in the software technical file. Gaps or inconsistencies in the SRS propagate in both directions — upward to unmet regulatory obligations, downward to untestable design and incomplete verification evidence.

### Where the agent operates

The SRS Review Agent operates at the SRS level of the V-model. It monitors changes to the SRS and related controlled documents, checks alignment against regulatory standards, and surfaces gaps before they propagate. It supports but does not replace the human review activities at each V-model phase.

The agent specifically supports two types of V-model activity:

**Design input verification** — checking that the SRS correctly captures all regulatory, risk, usability, cybersecurity, and clinical requirements that should be present, with proper traceability identifiers and verifiable acceptance criteria. This maps to IEC 62304 section 5.2.6 and 21 CFR 820.30(e).

**Change impact assessment** — when the SRS is modified, checking that the change has been assessed against all related controlled documents and that the downstream verification activities are still valid. This maps to IEC 62304 section 5.7–5.8 and 21 CFR 820.30(i).

---

## The controlled document ecosystem

A regulated SaMD team maintains a set of controlled documents that together constitute the technical file (EU MDR) or design history file (US FDA). These documents are interdependent — changes to one often require changes to others. The SRS sits at the centre of this network.

### Documents that constrain the SRS

These documents are created first or in parallel with the SRS. Their content drives what the SRS must contain.

**Intended use and indications for use** defines the clinical purpose, target population, use environment, and intended user of the device. It determines which hazards, usability scenarios, cybersecurity threats, and clinical performance claims must be reflected in the SRS. Update frequency: very infrequent — only when expanding indications or changing clinical role. Both EU MDR (Annex I, Annex II) and FDA (21 CFR 801, 21 CFR 820) require this document.

**Device classification and regulatory strategy** establishes the device risk class and the regulatory pathway. Higher classification drives stricter requirements on safety features, logging, cybersecurity, clinical evidence, and traceability depth in the SRS. Update frequency: very infrequent — only on major scope changes. Governed by EU MDR Rule 11 and MDCG 2019-11 for SaMD in the EU; FDA device classification regulations and IMDRF SaMD framework in the US.

**Risk management file** contains the full ISO 14971 chain: hazards, hazardous situations, harms, risk controls, and verification evidence. Risk controls must be implemented as verifiable SRS requirements and traced explicitly. The risk management file is a living document, updated continuously as design changes occur and post-market data arrives. Governed by ISO 14971:2019, applicable in both EU MDR and FDA contexts.

**Usability engineering file** documents the formative and summative usability studies, use error analysis, and user interface specifications. Use errors identified in formative studies must be assessed against the risk file and may generate new SRS requirements. The summative study validates the complete user interface — SRS changes after the summative study is completed must be carefully controlled and may require study reassessment. Governed by IEC 62366-1:2015.

**Cybersecurity documentation** includes the threat model, SBOM (software bill of materials), vulnerability tracking records, and security risk assessments. Threat modelling generates non-functional and functional security requirements that must appear in the SRS. New interfaces or data flows in the SRS require the threat model to be updated. Governed by IEC 81001-5-1:2021, referenced in both FDA cybersecurity guidance and EU MDR Annex I.

**AI/ML documentation** (for AI-enabled products) defines performance targets, supported cohorts, input data constraints, failure modes, drift monitoring requirements, and the change control plan (PCCP in the US under FDA guidance; Article 83 of the EU AI Act in the EU). These must be expressed as SRS requirements, including update rules if models change post-market.

**Clinical evaluation** (CEP and CER in the EU; clinical evidence for FDA submissions) defines clinical performance endpoints and evidence thresholds that must appear as SRS requirements. Governed by EU MDR Annex XIV and MEDDEV 2.7/1 rev.4 in the EU; FDA clinical evidence expectations vary by submission pathway.

### Documents that the SRS drives

These documents derive their content from the SRS. Changes to the SRS must be assessed against each of them.

**Software Architecture Document (SAD)** decomposes the software system into items, defines interfaces, and assigns an IEC 62304 safety class (A, B, or C) to each item. The SRS is the primary driver of the architecture. Importantly, each SRS requirement is linked to the software item it belongs to, and that item's safety class determines the verification depth required for that requirement.

**Verification and validation plans and test specifications** derive directly from the SRS. Every verifiable requirement must have a corresponding test case. Changes to the SRS require test plans to be updated.

**Instructions for use (IFU) and labelling** reflect the user-visible behaviour and warnings that the SRS defines. Changes to SRS requirements affecting user interaction require IFU updates.

**Technical documentation / Design History File** is the container that holds all of the above, plus release records, incident reports, and post-market surveillance plans. It must remain current and traceable throughout the device lifecycle.

### The SRS as the monitoring point

Because the SRS sits at the intersection of upstream constraints and downstream derivations, it is the most efficient point to monitor for compliance gaps. A change to the SRS that is not assessed against the risk file, the usability engineering file, the cybersecurity documentation, and the test plans can introduce gaps that will only be discovered late — during design review, during verification, or during a regulatory submission review.

This is the core justification for the agent: systematic, citation-backed SRS monitoring catches gaps at the point of lowest remediation cost.

---

## Standards corpus

The agent's reference corpus covers the following standards and regulatory frameworks. These are the sources it cites when generating findings.

| Standard / Framework | Scope | Applicable markets |
|---|---|---|
| IEC 62304:2006 + A1:2015 | Software lifecycle for medical device software | EU MDR (harmonised), FDA (recognised) |
| ISO 14971:2019 | Risk management for medical devices | EU MDR (harmonised), FDA (recognised) |
| IEC 62366-1:2015 | Usability engineering for medical devices | EU MDR (harmonised), FDA (recognised) |
| IEC 81001-5-1:2021 | Cybersecurity for health software lifecycle | EU MDR Annex I, FDA cybersecurity guidance |
| EU MDR 2017/745 | Medical device regulation — EU market | EU |
| FDA 21 CFR Part 820 (QMSR) | Quality management system regulation — US market | US FDA |
| FDA software guidance (2023) | Premarket submissions for device software functions | US FDA |
| IMDRF SaMD framework | SaMD classification and clinical evaluation | Jurisdiction-neutral reference |
| OWASP ASVS | Application security verification standard | Cross-jurisdictional |
| EU AI Act (2024) | AI system regulation — EU market (AI-enabled products) | EU |
| FDA AI/ML guidance | AI/ML-enabled device submissions (AI-enabled products) | US FDA |
| ISO/IEC 42001:2023 | AI management system (AI-enabled products) | Cross-jurisdictional |

The agent does not require the full normative text of paid standards to be present in the reference corpus. It uses structured clause summaries, publicly available mapping tables, and open reference documents (such as OWASP ASVS) to generate citation-backed findings. For the highest-confidence findings against specific normative clauses, teams should provide their own licensed copies of the relevant standards.

---

## Design control as the regulatory framework

Both EU MDR and FDA structure their software documentation requirements around design control — the formal process by which user needs are systematically translated into a verified and validated device design, with documented evidence at every step.

In the EU, design control obligations flow from EU MDR Annex IX and IEC 62304 sections 5–6. In the US, they are codified in 21 CFR 820.30. The two frameworks use different terminology but require substantially the same activities: design inputs, design outputs, design reviews, design verification, design validation, and design transfer, all with documented traceability.

The SRS Review Agent supports the following design control activities:

**Design input management** — verifying that SRS requirements correctly reflect the intended use, risk controls, usability requirements, cybersecurity requirements, and clinical performance targets that constitute the design inputs. Supported by UC1 (SRS monitoring) and UC3 (risk traceability check).

**Design change control** — assessing the impact of proposed SRS changes on related controlled documents, existing verification evidence, and regulatory submission status. Supported by UC1 and UC4 (change control plan boundary check).

**Design review support** — generating a pre-review summary of open findings and traceability gaps to support formal design review milestones. Supported by UC6 (inspection and submission preparation).

**Traceability maintenance** — verifying that the chain from hazard to risk control to SRS requirement to test case remains intact as changes are made. Supported by UC3.

The agent does not conduct design reviews, approve design outputs, or make design acceptability decisions. These remain the responsibility of the qualified individuals in the team.

---

## Software item safety classification

A concept specific to IEC 62304 that has significant implications for how the agent calibrates its outputs.

IEC 62304 section 4.3 allows a software system to be decomposed into individual software items, each assigned its own safety class (A, B, or C) based on the potential harm if that specific item fails — independently of the overall device classification. A Class A item cannot contribute to a hazardous situation. A Class B item can contribute to non-serious injury. A Class C item can contribute to serious injury or death.

This decomposition means that a single product can contain software items at different safety classes. A user authentication module in a Class IIb device might be justified as Class B if it is architecturally isolated from the clinical algorithm. The clinical algorithm module would be Class C.

The safety class of a software item determines the verification rigor required for any SRS requirement that belongs to that item. It also determines how the agent calibrates its findings — a finding about a Class C requirement is flagged differently from a finding about a Class A requirement in the same product.

**Two-way reclassification:** SRS changes can affect software item safety class in both directions. A change that adds a new interface between a previously isolated Class B item and a Class C item may remove the isolation argument, requiring the Class B item to be reassessed as Class C. A change that introduces a new safety mechanism may justify downgrading an item's class. The agent flags both types of potential reclassification for human assessment.

**IEC 62366-1 exception:** Software item decomposition does not reduce usability engineering obligations. IEC 62366-1 applies at the system level — the scope of the summative usability study is determined by the device's user interface as a whole, not by the safety class of individual software items. A team cannot reduce their summative study scope by arguing that the user interface module is a Class B item.

See `docs/00-overview/classification-reference.md` for the full classification framework including IMDRF significance categories and national market mappings.