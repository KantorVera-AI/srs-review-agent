**Status:** Working draft
**Owner:** Product Management
**Audience:** All stakeholders

---

# Classification Reference

This document defines the classification frameworks the agent uses to calibrate its outputs. It is the single reference for understanding how device classification, software item safety class, and multi-market scope interact to determine what the agent produces for any given finding.

---

## Why classification determines output depth

The agent is product-agnostic — it applies the same use cases and the same analysis logic to any SaMD product. But what it produces is not the same for every product. A finding about a missing risk control link in a Category IV AI-enabled diagnostic device carries fundamentally different regulatory consequences than the same finding in a Category I wellness application.

The agent uses two classification inputs to calibrate every finding it generates:

**The IMDRF significance category of the device** — determines the overall regulatory burden, the depth of documentation required, and the cost of getting it wrong. This is the primary classification input.

**The IEC 62304 safety class of the affected software item** — determines the verification rigor required for the specific requirement being analysed, independently of the overall device classification.

Both inputs must be present as structured metadata in the agent's analysis store before it can produce calibrated outputs. If either is absent, the agent falls back to conservative defaults and flags the missing metadata as an issue requiring resolution. See `docs/03-integration/metadata-spec.md` for the tagging specification.

---

## The IMDRF SaMD significance framework

The IMDRF (International Medical Device Regulators Forum) SaMD framework provides a jurisdiction-neutral classification system based on the clinical significance of what the software does, not on the technical properties of how it does it. It is the classification spine used throughout this agent's documentation.

Classification is determined by two dimensions:

**State of the healthcare situation** — how serious is the condition the software addresses?
- Critical: conditions that are life-threatening or require major therapeutic interventions
- Serious: conditions that require professional consultation or treatment
- Non-serious: conditions that do not require professional consultation

**Significance of the information provided** — how directly does the software drive clinical action?
- Treat or diagnose: the software output directly determines a clinical decision
- Drive clinical management: the software output influences a clinical decision
- Inform clinical management: the software output is one input among many

The intersection of these two dimensions produces four significance categories:

| | Treat or diagnose | Drive clinical management | Inform clinical management |
|---|---|---|---|
| **Critical situation** | Category IV | Category III | Category II |
| **Serious situation** | Category III | Category II | Category I |
| **Non-serious situation** | Category II | Category I | Category I |

Category I represents the lowest regulatory significance. Category IV represents the highest.

---

## Mapping IMDRF categories to national classification systems

The IMDRF framework does not replace national classification systems — it provides a common reference point that maps onto them. The following table shows approximate mappings. These are indicative, not definitive — actual classification always requires a product-specific assessment by a qualified regulatory professional.

| IMDRF Category | EU MDR (SaMD — Rule 11) | FDA (typical pathway) | IEC 62304 item class (typical) |
|---|---|---|---|
| I | Class I or Class IIa | Class I (exempt or 510k) | A or B |
| II | Class IIa or Class IIb | Class II (510k) | B |
| III | Class IIb | Class II (510k or De Novo) | B or C |
| IV | Class IIb or Class III | Class III (PMA) or De Novo | C |

### EU MDR — Rule 11 for SaMD

Under EU MDR, SaMD is classified primarily under Rule 11, which uses the IMDRF-aligned logic of healthcare situation severity and information significance. Key reference document: MDCG 2019-11 guidance on qualifying and classifying software under MDR.

Key thresholds for Rule 11:
- Software that provides information used to make decisions with diagnosis or therapeutic purposes in serious situations: Class IIa minimum
- Software intended to monitor physiological processes, where incorrect information could cause immediate danger: Class IIb
- Software intended to control or influence the use of Class III medical devices: Class III

### US FDA — SaMD classification

FDA classifies SaMD under the Federal Food, Drug, and Cosmetic Act with the same three-class system (Class I, II, III) and uses the IMDRF SaMD framework as a reference for risk-based assessment. Key documents: FDA's 2023 guidance on content of premarket submissions for device software functions, and the IMDRF SaMD clinical evaluation guidance.

De Novo is the pathway for novel Class II devices without a predicate. PMA is required for Class III devices. 510(k) is the most common pathway for Class II SaMD with a predicate.

### Other major markets

| Market | Regulatory body | Framework | Notes |
|---|---|---|---|
| Canada | Health Canada | Class I–IV, IMDRF-aligned | SaMD guidance aligns closely with IMDRF categories |
| Australia | TGA | Class I–III (AIMD separate) | Broadly GHTF/IMDRF-aligned |
| Japan | PMDA | Class I–IV | Own SaMD-specific guidance; generally more stringent for AI-enabled devices |

### Multi-market products

A product submitted to multiple markets carries the obligations of the most stringent applicable classification. A product that is IMDRF Category III in the EU but Category II under FDA must be documented to Category III standards throughout — the agent's output calibration follows the highest applicable tier.

For dual-market EU/US submissions, this has a direct cost implication: the same traceability gap found by the agent prevents a deficiency in both markets simultaneously. The regulatory cost avoided is additive.

---

## IEC 62304 software item safety classes

IEC 62304 section 4.3 defines three software safety classes assigned at the individual software item level, not the device level.

| Class | Definition | Verification requirements |
|---|---|---|
| A | No injury or damage to health is possible | Basic testing and documentation |
| B | Non-serious injury is possible | Additional unit testing and anomaly resolution |
| C | Death or serious injury is possible | Full unit testing, integration testing, complete traceability |

The safety class of a software item is determined by the potential harm if that item fails to function as specified. A team can assign a lower safety class to an item than the overall device's implied class if they can demonstrate — through architectural evidence — that the item is isolated from safety-critical functions.

This isolation argument must be:
- Documented in the Software Architecture Document (SAD)
- Supported by architectural mechanisms (defensive design, independent monitoring, redundancy)
- Maintained as a living document — any SRS change that affects the isolation must trigger reassessment

### How the agent uses software item safety class

The agent reads the safety class of each software item from the SAD via the traceability links in the requirements management system. Each SRS requirement is linked to its software item, and the agent uses the item's safety class to:

- Determine the depth of the finding generated (advisory, warning, or mandatory escalation)
- Determine which document owners are notified
- Determine what evidence is cited in the finding
- Flag potential reclassification when a SRS change affects isolation

---

## Output calibration by classification tier

The following matrix defines how the agent's output changes across IMDRF significance categories and IEC 62304 software item safety classes. This is the practical answer to "what does appropriate documentation depth mean."

### Finding depth by IMDRF category

| IMDRF Category | Finding type | Severity threshold | Routing | Escalation |
|---|---|---|---|---|
| I | Advisory | Informational or Low | SRS owner only | — |
| II | Standard finding | Low to High | SRS owner + relevant document owner | — |
| III | Standard finding with mandatory review | Medium to Critical | SRS owner + document owner + RA | On Critical findings |
| IV | Mandatory finding | High–Critical | SRS owner + document owner + RA/PRRC mandatory | On all findings above Low |

### Finding depth by software item safety class

| IEC 62304 class | Citation depth | Evidence requirement | Reclassification check |
|---|---|---|---|
| A | Clause reference only | None required | Not applicable |
| B | Clause reference + section | Document traceability | Triggered if isolation argument is affected |
| C | Clause reference + section + subsection | Full traceability to test case | Triggered if isolation argument is affected |

### Combined calibration

When an IMDRF category and a software item safety class are both present, the agent applies the more stringent of the two calibrations. A Class C item in a Category I device is treated as Class C because the software item class governs the verification requirement regardless of the device-level category.

### Reclassification triggers

The agent flags two types of reclassification risk:

**Device-level reclassification** — a SRS change that adds clinical functionality, expands the intended population, or changes the significance of the software's output may elevate the product's IMDRF category. Example: adding a "diagnose" function to a product that previously only "informed" moves the product from Category II to Category III or IV. The agent flags this for assessment by the Regulatory Affairs specialist and PRRC.

**Software item-level reclassification** — a SRS change that modifies the relationship between software items may remove or weaken the isolation argument that justified a lower safety class. Example: a new interface between a Class B authentication module and a Class C clinical algorithm module may require the authentication module to be reassessed as Class C. The agent flags this for joint assessment by the Software Architect and Risk Engineer.

Both directions apply in reverse: a SRS change that introduces new isolation mechanisms may justify downgrading a safety class. This is legitimate and the agent supports it, but the isolation argument must be documented and reviewed.

### IEC 62366-1 exception — usability engineering

Software item safety class decomposition does not apply to usability engineering obligations. IEC 62366-1 requires that the complete user interface of the device be evaluated in the summative usability study — the scope of this study is determined by the full user interface, not by the safety class of individual software items that implement parts of it.

A team cannot reduce their summative study scope by arguing that a particular UI module is a Class B item. The agent's UC7 (usability engineering lifecycle integration) applies this rule regardless of the software item safety class of the modified requirement.

---

## Classification sensitivity and the agent's ROI

Classification tier is the single largest driver of the agent's value. The cost of a missed finding scales with classification:

| IMDRF Category | Typical cost of one missed finding | Notes |
|---|---|---|
| I | Low — 1–5k€ in rework if caught internally | Minimal regulatory submission risk |
| II | Medium — 5–20k€ in rework or deficiency round | Pre-market submission likely; one deficiency round is significant |
| III | High — 15–50k€ in deficiency round or partial resubmission | Complex submissions; multiple rounds are not uncommon |
| IV | Very high — 50–200k€+ in resubmission or regulatory enforcement | PMA-level cost structure; delay cost is also significant |

For products targeting multiple markets, the cost of a missed finding at Category III or IV is effectively multiplied across the number of markets where the same gap would trigger a deficiency.

The agent's Risk Savings scoring in the ROI model (`docs/02-roi/assumptions.md`) uses these cost ranges as the basis for the Risk Savings parameter. Teams with a specific market profile and submission history should adjust these figures to reflect their actual cost experience.