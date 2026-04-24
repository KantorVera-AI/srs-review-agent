**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect, PM

---

# UC7 — Usability engineering lifecycle integration

**Release tier:** Release 2
**Depends on:** UC1 (change classification), UC2 (baseline intake — summative study baseline), UC3 (risk file cross-check for use errors)
**Required by:** Nothing downstream

---

## One-line description

Integrate formative and summative usability study outcomes into the agent's monitoring loop — feeding use errors back into the risk and SRS change workflow, and flagging any SRS change after a summative study baseline that may affect study validity.

---

## Background — why usability engineering needs its own use case

Usability engineering under IEC 62366-1 operates at the system level, not the software item level. This creates a specific situation that the other use cases do not handle:

**Formative studies** (iterative testing during development) identify use errors that must be assessed against the risk file and may generate new SRS requirements. Currently, this feedback loop is entirely manual — a use error finding from a formative study may never reach the SRS if the handoff between the usability specialist and the requirements engineer is informal.

**Summative studies** (the final validation of the complete user interface, required before submission) establish a validated baseline. After this baseline, any SRS change that affects a use scenario evaluated in the summative study is a high-risk event — it may invalidate the study and require either a supplemental evaluation or a new study.

**Critical exception — IEC 62366-1 decomposition rule:** Software item safety class decomposition does **not** reduce usability engineering obligations. A team cannot narrow the scope of the summative study by arguing that the user interface module is a Class B item. UC7 applies this rule regardless of the software item safety class of the changed requirement. A UC7 finding on a Class A UI component carries the same usability engineering obligation as a finding on a Class C component.

---

## What triggers it

**Trigger 1 — Formative study submission:**
A Usability/HF Specialist submits a completed formative study result through the UI's usability study submission screen. The agent analyses the use error log against the current SRS and risk file.

**Trigger 2 — Summative study baseline:**
A completed summative evaluation report is approved and baselined via UC2's baseline intake mechanism. The agent records the summative baseline and begins monitoring all subsequent SRS changes for study validity impact.

**Trigger 3 — Post-summative SRS change:**
UC1 classifies any SRS change after a summative baseline as a potential study validity event. Every SRS change after the summative baseline triggers a UC7 check — not just changes classified as UI/workflow.

---

## What the agent does

### For formative study submission (Trigger 1)

1. Parses the use error log from the submitted study
2. Maps each use error to the SRS requirement that governs the affected user interaction
3. Checks whether each use error has a corresponding entry in the risk management file (use error → hazardous situation mapping, per IEC 62366-1 section 4.1.4)
4. Generates findings for:
   - Use errors not yet reflected in any SRS requirement
   - Use errors that map to existing hazards not addressed in the risk management file
   - Use errors that suggest a new hazard not yet in the risk management file
5. Routes risk-related findings jointly to the Risk Engineer and the Usability/HF Specialist

### For post-summative SRS change (Trigger 3)

1. Receives the SRS change classification from UC1
2. Queries the summative study baseline to identify which use scenarios were evaluated
3. Checks whether the changed SRS requirement governs any part of a use scenario in the summative baseline
4. If yes: generates a post-summative change flag with mandatory acknowledgement
5. Routes to the Usability/HF Specialist and the RA/PRRC jointly

The post-summative change flag is a mandatory acknowledgement finding — it cannot be dismissed without a documented decision. The reviewer must confirm either:
- The change does not affect any evaluated use scenario (with rationale), or
- The change does affect an evaluated use scenario and a supplemental evaluation or new study is required

---

## Who receives the output

| Output | Recipient | Condition |
|---|---|---|
| Use error → SRS finding | Requirements Engineer | Use error not reflected in SRS |
| Use error → risk finding | Risk Engineer + Usability/HF Specialist | Use error maps to unaddressed hazard |
| Post-summative change flag | Usability/HF Specialist + RA/PRRC | Any SRS change after summative baseline |
| Mandatory escalation | RA/PRRC | Post-summative flag confirmed as affecting an evaluated use scenario |

---

## RICE score

| Risk savings | Impact | Confidence | Effort | Score |
|---|---|---|---|---|
| 4 | 3 | 0.75 | 3 | 30 |

*Risk savings of 4: post-summative SRS changes that invalidate the summative study without detection are a high-cost regulatory event — requiring a new study or a documented justification that is frequently challenged by regulatory reviewers. The formative feedback loop also prevents use error gaps from reaching submissions. Impact of 3: the use case is high-value for complex UI products but lower-value for products with simple interfaces or no summative study requirement. Confidence of 0.75: the post-summative monitoring logic is well-defined; the formative study extraction quality depends on the structure of the submitted study documents. Effort of 3: reuses UC2 baseline intake and UC3 risk cross-check infrastructure.*

---

## Benefit breakdown

### Phase 1 — Initial development

| Dimension | Estimate |
|---|---|
| Typical events | 2–4 formative study cycles + 1 summative study baseline |
| Time saved per event | 3–8 hours of manual use error to SRS/risk mapping |
| Total time saving | 6–32 hours = 780–4,160€ |
| Regulatory cost avoided | 10–30k€ — missed post-summative study invalidation is a critical submission risk for UI-intensive products |

### Phase 2 — Ongoing maintenance

| Dimension | Estimate |
|---|---|
| Annual events per product | 1–3 post-summative SRS changes requiring assessment per year |
| Time saved per event | 2–6 hours |
| Annual time saving | 2–18 hours = 260–2,340€ |
| Regulatory cost avoided | 10–30k€ per avoided study invalidation event |

> **Classification note:** UC7 value scales with UI complexity and with IMDRF category. For Category I products with simple interfaces and no summative study requirement, the benefit is minimal. For Category III–IV products with complex clinical interfaces, the post-summative monitoring is a critical quality gate.

---

## Key assumptions

- Formative study use error logs must be submitted in a structured format for automated extraction. A free-text study report requires more manual extraction and reduces the agent's value for Trigger 1.
- The summative study baseline must be formally submitted to the agent via UC2's baseline intake — it is not automatically detected.
- UC7 applies regardless of software item safety class. A Class A UI component is subject to the same post-summative monitoring as a Class C component.
- For products with no summative study requirement (typically Category I), UC7 provides minimal value and need not be configured.

---

## Dependencies and risks

**Dependencies:** UC1 for change classification (Trigger 3). UC2 for summative study baseline intake (Trigger 2). UC3 risk cross-check infrastructure (use error → hazard mapping).

**Technical risks:**
- Unstructured formative study documents are the primary extraction quality risk. The agent's extraction must be validated against the team's actual study report format.
- Post-summative monitoring creates a permanent check on all SRS changes after the first summative baseline. This generates ongoing findings for every UI change — the signal-to-noise ratio must be managed carefully to avoid fatigue.

**Process risks:**
- Teams must understand the IEC 62366-1 decomposition exception before deployment. If a team believes they can exempt Class A UI items from UC7, the post-summative monitoring will appear to generate unnecessary findings and adoption will suffer.

---

## Regulatory basis

| Requirement | Standard | Clause |
|---|---|---|
| Use error feedback into risk management | IEC 62366-1:2015 | Section 4.1.4 |
| Summative usability evaluation | IEC 62366-1:2015 | Section 5.9 |
| Usability as part of safety | EU MDR Annex I | GSPR 5 |
| Human factors in design validation | FDA 21 CFR 820.30(g) | Design validation |
| System-level usability obligation | IEC 62366-1:2015 | Section 1 (scope) — applies at system level, not item level |
