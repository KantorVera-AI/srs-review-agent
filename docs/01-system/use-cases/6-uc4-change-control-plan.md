**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect, PM

---

# UC4 — Change control plan boundary check

**Release tier:** Release 3
**Depends on:** UC1 (AI/ML change classification), UC3 (traceability infrastructure), stable pipeline from Release 2
**Required by:** Nothing downstream

---

## One-line description

When a SRS change modifies algorithm behaviour, model inputs or outputs, or clinical performance claims, verify whether the change remains within the boundaries of the approved change control plan or triggers a new regulatory submission.

---

## Context — change control plans for AI/ML devices

An AI/ML-enabled SaMD can make changes to its algorithm post-approval without requiring a new submission, provided those changes stay within the boundaries of an approved change control plan. In the US, FDA calls this a Predetermined Change Control Plan (PCCP). In the EU, the equivalent mechanism appears in Article 83 of the EU AI Act, which applies alongside EU MDR for AI-enabled medical devices.

Both frameworks require the manufacturer to pre-specify: the types of algorithm changes anticipated, the performance specifications that bound those changes, and the methodology for implementing and validating changes. Any change outside these specifications triggers a new regulatory assessment — a new 510(k) or PMA supplement in the US, or a significant change assessment under EU MDR Article 83.

UC4 checks whether a proposed SRS change stays within the approved boundaries. Without this check, a team may unknowingly implement a change that should have triggered a new submission — a regulatory compliance failure that is both costly and difficult to remediate after the fact.

---

## What triggers it

UC1 classifies a change as **AI/ML behaviour**. The change control checker then retrieves the approved change control plan document and compares the SRS delta against its boundaries.

---

## What the agent does

1. Receives the AI/ML behaviour classification from UC1
2. Retrieves the approved change control plan from the analysis store
3. Identifies the specific change: algorithm logic modification, model input/output change, performance specification change, training data scope change, or population scope change
4. Compares the change against the change control plan boundary definitions
5. Classifies the result:
   - **Within bounds** — the change is within the pre-specified boundaries, no new submission required
   - **Exceeds bounds** — the change clearly exceeds the pre-specified boundaries, new submission required
   - **Ambiguous** — the change may or may not exceed the boundaries, human assessment required before proceeding
6. For **exceeds bounds**: generates a mandatory escalation finding to the RA/PRRC role with a hold recommendation — the SRS change should not be approved until the submission question is resolved
7. For **ambiguous**: generates a mandatory clarification finding to the RA/PRRC and AI Engineer — the boundary assessment must be documented before the change proceeds

---

## Who receives the output

| Output | Recipient | Condition |
|---|---|---|
| Within bounds confirmation | Requirements Engineer + AI Engineer | Change confirmed within PCCP/Article 83 scope |
| Exceeds bounds — mandatory escalation | RA/PRRC (mandatory) + AI Engineer | Change clearly exceeds boundaries |
| Ambiguous — mandatory clarification | RA/PRRC + AI Engineer | Boundary status unclear |
| Economic trade-off assessment | RA/PRRC + PM | When submission is required — full cost estimate of proceeding vs scoping differently |

---

## RICE score

| Risk savings | Impact | Confidence | Effort | Score |
|---|---|---|---|---|
| 5 | 3 | 0.60 | 4 | 23 |

*Risk savings of 5: an undetected out-of-bounds change implemented without a new submission is a regulatory compliance failure — cost equivalent to an unplanned 510(k) or PMA supplement (50–200k€) plus potential enforcement risk. Impact of 3: high value for AI-enabled products but zero value for non-AI products. Confidence of 0.60: the lowest confidence of any use case — PCCP guidance was in draft as of early 2026 and change control plan document structure varies significantly by product. Effort of 4: requires a purpose-built change control plan document parser in addition to the classifier.*

---

## Benefit breakdown

### Phase 1 — Initial development (AI-enabled products only)

| Dimension | Estimate |
|---|---|
| Typical events | 3–8 AI/ML algorithm definition events during initial SRS development |
| Time saved per event | 3–10 hours of manual change control plan boundary review |
| Total time saving | 9–80 hours = 1,200–10,400€ |
| Regulatory cost avoided | 10–30k€ — correctly scoping the initial change control plan prevents out-of-bounds implementation in early post-market releases |

### Phase 2 — Ongoing maintenance (AI-enabled products only)

| Dimension | Estimate |
|---|---|
| Annual events per product | 2–10 AI/ML model updates per year |
| Time saved per event | 5–15 hours of manual boundary analysis |
| Annual time saving | 10–150 hours = 1,300–19,500€ |
| Regulatory cost avoided | ~43k€ average per avoided unplanned submission |

> **AI-only note:** UC4 has zero value for non-AI SaMD. It should only be configured for products with an approved change control plan.

---

## Key assumptions

- Change control plan document structure varies significantly by product and regulatory jurisdiction. A boundary checker that works for one product's PCCP may require significant reconfiguration for another. This is the primary driver of the low confidence score.
- 43k€ cost avoidance = estimated cost of an unplanned submission discounted by 60–70% detection probability for systematic versus informal review.
- FDA PCCP guidance was in draft form as of early 2026. EU AI Act Article 83 implementing framework was also developing. Both are expected to mature before Release 3 is built — the Confidence score should be re-evaluated at that point.
- The change control plan document must be available in a structured or semi-structured format for the boundary checker to function reliably. Narrative-only change control plans require a purpose-built parser — this is additional effort not reflected in the Effort score of 4.

---

## Dependencies and risks

**Dependencies:** UC1 for AI/ML change classification. UC3 traceability infrastructure. Approved change control plan in a parseable format. Stable pipeline validated through Release 2.

**Technical risks:**
- Change control plan parsing is the highest technical risk in the entire use case set. Plans are often written as narrative prose with no structured boundary definitions. The parser must be scoped and validated with the AI Architect before Release 3 begins.
- Regulatory guidance maturity: if PCCP guidance or EU AI Act Article 83 implementing acts introduce significant changes to how boundaries must be documented, the parser and boundary logic may need revision.

**Process risks:**
- The RA/PRRC must be closely involved in Release 3 scoping to ensure the boundary definitions in the agent's logic match the team's actual PCCP or Article 83 documentation.

---

## Regulatory basis

| Requirement | Standard / Guidance | Reference |
|---|---|---|
| Predetermined Change Control Plan | FDA PCCP guidance (2023 draft) | Full guidance |
| Post-market AI/ML system modifications | EU AI Act | Article 83 |
| Significant change assessment | EU MDR | Article 83 + Annex IX |
| Design change control | FDA 21 CFR 820.30(i) | Design changes |
